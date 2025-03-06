from datetime import datetime, timedelta
from src.database.models import (
    Achievement, UserAchievement, UserLevel, 
    AchievementType, StudySession, Task
)
from src.database.database import get_session
from sqlalchemy import and_, func
import math
from src.services.pomodoro import PomodoroTimer
from src.services.task_manager import TaskManager
import logging

class AchievementManager:
    """Gerenciador de conquistas e sistema de gamificação."""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session = get_session()
        self.logger = logging.getLogger('achievement_manager')
        self._ensure_user_level()
        self.setup_default_achievements()
        
    def _ensure_user_level(self):
        """Garante que o usuário tenha um registro de nível."""
        user_level = self.session.query(UserLevel).filter_by(
            user_id=self.user_id
        ).first()
        
        if not user_level:
            user_level = UserLevel(user_id=self.user_id)
            self.session.add(user_level)
            self.session.commit()
            
    def setup_default_achievements(self):
        """Configura as conquistas padrão se ainda não existirem."""
        try:
            # Verificar se já existem conquistas
            if self.session.query(Achievement).count() == 0:
                default_achievements = [
                    # Conquistas de pomodoro
                    {
                        'name': 'Primeiro Pomodoro',
                        'description': 'Complete seu primeiro ciclo pomodoro.',
                        'type': 'pomodoro_count',
                        'requirement': 1,
                        'xp_reward': 50
                    },
                    {
                        'name': 'Focado',
                        'description': 'Complete 10 ciclos pomodoro.',
                        'type': 'pomodoro_count',
                        'requirement': 10,
                        'xp_reward': 100
                    },
                    {
                        'name': 'Mestre do Tempo',
                        'description': 'Complete 50 ciclos pomodoro.',
                        'type': 'pomodoro_count',
                        'requirement': 50,
                        'xp_reward': 250
                    },
                    
                    # Conquistas de tempo de estudo
                    {
                        'name': 'Estudante Dedicado',
                        'description': 'Acumule 10 horas de estudo.',
                        'type': 'study_time',
                        'requirement': 600,  # Em minutos
                        'xp_reward': 150
                    },
                    {
                        'name': 'Intelectual',
                        'description': 'Acumule 50 horas de estudo.',
                        'type': 'study_time',
                        'requirement': 3000,  # Em minutos
                        'xp_reward': 300
                    },
                    {
                        'name': 'Gênio em Formação',
                        'description': 'Acumule 100 horas de estudo.',
                        'type': 'study_time',
                        'requirement': 6000,  # Em minutos
                        'xp_reward': 500
                    },
                    
                    # Conquistas de tarefas
                    {
                        'name': 'Produtivo',
                        'description': 'Complete sua primeira tarefa.',
                        'type': 'task_complete',
                        'requirement': 1,
                        'xp_reward': 50
                    },
                    {
                        'name': 'Ágil',
                        'description': 'Complete 10 tarefas.',
                        'type': 'task_complete',
                        'requirement': 10,
                        'xp_reward': 150
                    },
                    {
                        'name': 'Realizador',
                        'description': 'Complete 50 tarefas.',
                        'type': 'task_complete',
                        'requirement': 50,
                        'xp_reward': 300
                    },
                    
                    # Conquistas de streak
                    {
                        'name': 'Consistente',
                        'description': 'Estude por 3 dias consecutivos.',
                        'type': 'streak_days',
                        'requirement': 3,
                        'xp_reward': 100
                    },
                    {
                        'name': 'Disciplinado',
                        'description': 'Estude por 7 dias consecutivos.',
                        'type': 'streak_days',
                        'requirement': 7,
                        'xp_reward': 200
                    },
                    {
                        'name': 'Inabalável',
                        'description': 'Estude por 30 dias consecutivos.',
                        'type': 'streak_days',
                        'requirement': 30,
                        'xp_reward': 500
                    }
                ]
                
                # Inserir conquistas no banco
                for ach_data in default_achievements:
                    achievement = Achievement(**ach_data)
                    self.session.add(achievement)
                
                self.session.commit()
                self.logger.info("Conquistas padrão criadas com sucesso.")
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Erro ao criar conquistas padrão: {e}")
    
    def check_achievements(self):
        """Verifica todas as conquistas pendentes para o usuário."""
        try:
            user = self.session.query(User).get(self.user_id)
            if not user:
                return []
            
            # Obter conquistas que o usuário ainda não tem
            earned_achievements_ids = [
                ua.achievement_id for ua in 
                self.session.query(UserAchievement).filter_by(user_id=self.user_id).all()
            ]
            
            pending_achievements = self.session.query(Achievement).filter(
                ~Achievement.id.in_(earned_achievements_ids) if earned_achievements_ids else True
            ).all()
            
            # Verificar cada conquista
            newly_earned = []
            
            for achievement in pending_achievements:
                if self.check_achievement_completion(achievement):
                    # Conceder a conquista
                    user_achievement = UserAchievement(
                        user_id=self.user_id,
                        achievement_id=achievement.id,
                        earned_at=datetime.now()
                    )
                    self.session.add(user_achievement)
                    
                    # Conceder XP
                    self.award_xp(achievement.xp_reward)
                    
                    newly_earned.append(achievement)
            
            self.session.commit()
            return newly_earned
            
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Erro ao verificar conquistas: {e}")
            return []
    
    def check_achievement_completion(self, achievement):
        """Verifica se uma conquista específica foi completada."""
        try:
            if achievement.type == 'pomodoro_count':
                # Verificar número de pomodoros completos
                count = self.session.query(PomodoroTimer.completed_sessions).filter_by(
                    user_id=self.user_id
                ).scalar() or 0
                
                return count >= achievement.requirement
                
            elif achievement.type == 'study_time':
                # Verificar tempo total de estudo (em minutos)
                total_time = self.session.query(PomodoroTimer.total_study_time).filter_by(
                    user_id=self.user_id
                ).scalar() or 0
                
                return total_time >= achievement.requirement
                
            elif achievement.type == 'task_complete':
                # Verificar número de tarefas completas
                count = self.session.query(TaskManager.completed_tasks).filter_by(
                    user_id=self.user_id, 
                    completed=True
                ).count()
                
                return count >= achievement.requirement
                
            elif achievement.type == 'streak_days':
                # Verificar dias consecutivos de estudo
                streak = self.session.query(PomodoroTimer.current_streak).filter_by(
                    user_id=self.user_id
                ).scalar() or 0
                
                return streak >= achievement.requirement
            
            return False
            
        except Exception as e:
            self.logger.error(f"Erro ao verificar conclusão de conquista: {e}")
            return False
    
    def award_xp(self, xp_amount):
        """Concede XP ao usuário e atualiza seu nível."""
        try:
            # Buscar o nível atual do usuário
            user_level = self.session.query(UserLevel).filter_by(
                user_id=self.user_id
            ).first()
            
            # Se não existir registro, criar um
            if not user_level:
                user_level = UserLevel(
                    user_id=self.user_id,
                    current_level=1,
                    current_xp=0,
                    total_xp=0
                )
                self.session.add(user_level)
                self.session.flush()
            
            # Atualizar XP
            previous_level = user_level.current_level
            user_level.current_xp += xp_amount
            user_level.total_xp += xp_amount
            
            # Verificar se subiu de nível
            # Fórmula: xp_para_proximo_nivel = nivel_atual * 100
            while user_level.current_xp >= user_level.current_level * 100:
                user_level.current_xp -= user_level.current_level * 100
                user_level.current_level += 1
            
            self.session.commit()
            
            # Retornar se houve level up
            return user_level.current_level > previous_level, user_level.current_level
            
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Erro ao conceder XP: {e}")
            return False, 0
    
    def get_user_level(self):
        """Retorna as informações de nível do usuário."""
        try:
            user_level = self.session.query(UserLevel).filter_by(
                user_id=self.user_id
            ).first()
            
            if not user_level:
                return {
                    'level': 1,
                    'current_xp': 0,
                    'total_xp': 0,
                    'next_level_xp': 100,
                    'progress': 0
                }
            
            # Calcular XP necessário para o próximo nível
            next_level_xp = user_level.current_level * 100
            progress = (user_level.current_xp / next_level_xp) * 100
            
            return {
                'level': user_level.current_level,
                'current_xp': user_level.current_xp,
                'total_xp': user_level.total_xp,
                'next_level_xp': next_level_xp,
                'progress': progress
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao obter nível do usuário: {e}")
            return {
                'level': 1,
                'current_xp': 0,
                'total_xp': 0,
                'next_level_xp': 100,
                'progress': 0
            }
    
    def get_earned_achievements(self):
        """Retorna todas as conquistas que o usuário já ganhou."""
        try:
            user_achievements = self.session.query(
                Achievement, UserAchievement.earned_at
            ).join(
                UserAchievement, UserAchievement.achievement_id == Achievement.id
            ).filter(
                UserAchievement.user_id == self.user_id
            ).all()
            
            return [
                {
                    'id': ach.id,
                    'name': ach.name,
                    'description': ach.description,
                    'type': ach.type,
                    'xp_reward': ach.xp_reward,
                    'earned_at': earned_at
                }
                for ach, earned_at in user_achievements
            ]
            
        except Exception as e:
            self.logger.error(f"Erro ao obter conquistas do usuário: {e}")
            return []
    
    def get_pending_achievements(self):
        """Retorna conquistas que o usuário ainda não ganhou."""
        try:
            # IDs das conquistas já ganhas
            earned_ids = [
                ua.achievement_id for ua in 
                self.session.query(UserAchievement).filter_by(user_id=self.user_id).all()
            ]
            
            # Conquistas pendentes
            pending = self.session.query(Achievement).filter(
                ~Achievement.id.in_(earned_ids) if earned_ids else True
            ).all()
            
            return [
                {
                    'id': ach.id,
                    'name': ach.name,
                    'description': ach.description,
                    'type': ach.type,
                    'xp_reward': ach.xp_reward
                }
                for ach in pending
            ]
            
        except Exception as e:
            self.logger.error(f"Erro ao obter conquistas pendentes: {e}")
            return []
    
    def get_recent_achievements(self, limit=5):
        """Retorna as conquistas mais recentes do usuário."""
        try:
            # Obtém as conquistas mais recentes do usuário
            user_achievements = self.session.query(
                Achievement, UserAchievement.earned_at
            ).join(
                UserAchievement, UserAchievement.achievement_id == Achievement.id
            ).filter(
                UserAchievement.user_id == self.user_id
            ).order_by(
                UserAchievement.earned_at.desc()
            ).limit(limit).all()
            
            return [
                {
                    'id': ach.id,
                    'name': ach.name,
                    'description': ach.description,
                    'type': ach.type,
                    'xp_reward': ach.xp_reward,
                    'earned_at': earned_at
                }
                for ach, earned_at in user_achievements
            ]
            
        except Exception as e:
            self.logger.error(f"Erro ao obter conquistas recentes do usuário: {e}")
            return []
        
    def __del__(self):
        """Fecha a sessão do banco de dados."""
        self.session.close()

    def check_new_achievements(self):
        """Verifica e registra novas conquistas do usuário."""
        new_achievements = []
        
        # Verificar cada tipo de conquista
        self.check_pomodoro_achievements()
        self.check_study_time_achievements()
        self.check_task_achievements()
        self.check_streak_achievements()
        
        # Retornar novas conquistas obtidas nesta verificação
        try:
            # Buscar conquistas obtidas nas últimas 24 horas
            recent = self.session.query(
                Achievement, UserAchievement.earned_at
            ).join(
                UserAchievement, UserAchievement.achievement_id == Achievement.id
            ).filter(
                UserAchievement.user_id == self.user_id,
                UserAchievement.earned_at >= datetime.now() - timedelta(hours=1)
            ).all()
            
            return [
                {
                    'id': ach.id,
                    'name': ach.name,
                    'description': ach.description,
                    'xp_reward': ach.xp_reward
                }
                for ach, _ in recent
            ]
        except Exception as e:
            self.logger.error(f"Erro ao verificar novas conquistas: {e}")
            return []

    def get_user_level_info(self):
        """Retorna informações sobre o nível do usuário."""
        try:
            user_level = self.session.query(UserLevel).filter_by(
                user_id=self.user_id
            ).first()
            
            if not user_level:
                # Se não encontrar, cria um novo registro
                user_level = UserLevel(user_id=self.user_id)
                self.session.add(user_level)
                self.session.commit()
            
            # Calcular XP necessário para o próximo nível
            # Fórmula: 100 * (nível atual)^1.5
            xp_for_next_level = int(100 * (user_level.current_level ** 1.5))
            
            return {
                'level': user_level.current_level,
                'current_xp': user_level.current_xp,
                'total_xp': user_level.total_xp,
                'xp_for_next_level': xp_for_next_level,
                'progress_percent': min(100, int((user_level.current_xp / xp_for_next_level) * 100))
            }
            
        except Exception as e:
            self.logger.error(f"Erro ao obter informações de nível: {e}")
            return {
                'level': 1,
                'current_xp': 0,
                'total_xp': 0,
                'xp_for_next_level': 100,
                'progress_percent': 0
            } 