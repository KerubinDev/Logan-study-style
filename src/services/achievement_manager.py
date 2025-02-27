from datetime import datetime, timedelta
from src.database.models import (
    Achievement, UserAchievement, UserLevel, 
    AchievementType, StudySession, Task
)
from src.database.database import get_session
from sqlalchemy import and_, func
import math

class AchievementManager:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session = get_session()
        self._ensure_user_level()
        
    def _ensure_user_level(self):
        """Garante que o usuário tenha um registro de nível."""
        user_level = self.session.query(UserLevel).filter_by(
            user_id=self.user_id
        ).first()
        
        if not user_level:
            user_level = UserLevel(user_id=self.user_id)
            self.session.add(user_level)
            self.session.commit()
            
    def check_achievements(self):
        """Verifica e concede conquistas pendentes."""
        self._check_pomodoro_achievements()
        self._check_study_time_achievements()
        self._check_task_achievements()
        self._check_streak_achievements()
        
    def _check_pomodoro_achievements(self):
        """Verifica conquistas relacionadas a pomodoros completados."""
        total_pomodoros = self.session.query(StudySession).filter(
            and_(
                StudySession.user_id == self.user_id,
                StudySession.session_type == 'pomodoro',
                StudySession.end_time.isnot(None)
            )
        ).count()
        
        achievements = self.session.query(Achievement).filter(
            Achievement.type == AchievementType.POMODORO_COUNT.value
        ).all()
        
        for achievement in achievements:
            if total_pomodoros >= achievement.requirement:
                self._grant_achievement(achievement)
                
    def _check_study_time_achievements(self):
        """Verifica conquistas relacionadas ao tempo total de estudo."""
        total_hours = self.session.query(
            func.sum(StudySession.end_time - StudySession.start_time)
        ).filter(
            and_(
                StudySession.user_id == self.user_id,
                StudySession.end_time.isnot(None)
            )
        ).scalar()
        
        if total_hours:
            total_hours = total_hours.total_seconds() / 3600
            
            achievements = self.session.query(Achievement).filter(
                Achievement.type == AchievementType.STUDY_TIME.value
            ).all()
            
            for achievement in achievements:
                if total_hours >= achievement.requirement:
                    self._grant_achievement(achievement)
                    
    def _grant_achievement(self, achievement: Achievement):
        """Concede uma conquista ao usuário se ainda não a possui."""
        existing = self.session.query(UserAchievement).filter(
            and_(
                UserAchievement.user_id == self.user_id,
                UserAchievement.achievement_id == achievement.id
            )
        ).first()
        
        if not existing:
            user_achievement = UserAchievement(
                user_id=self.user_id,
                achievement_id=achievement.id
            )
            self.session.add(user_achievement)
            
            # Adicionar XP
            self._add_experience(achievement.xp_reward)
            
            self.session.commit()
            return True
        return False
        
    def _add_experience(self, xp_amount: int):
        """Adiciona experiência ao usuário e verifica level up."""
        user_level = self.session.query(UserLevel).filter_by(
            user_id=self.user_id
        ).first()
        
        user_level.current_xp += xp_amount
        user_level.total_xp += xp_amount
        
        # Verificar level up
        while user_level.current_xp >= self._xp_for_next_level(user_level.current_level):
            user_level.current_xp -= self._xp_for_next_level(user_level.current_level)
            user_level.current_level += 1
            
        self.session.commit()
        
    def _xp_for_next_level(self, current_level: int) -> int:
        """Calcula XP necessária para o próximo nível."""
        return int(100 * (current_level ** 1.5))
        
    def get_user_progress(self) -> dict:
        """Retorna informações sobre o progresso do usuário."""
        user_level = self.session.query(UserLevel).filter_by(
            user_id=self.user_id
        ).first()
        
        next_level_xp = self._xp_for_next_level(user_level.current_level)
        
        return {
            'level': user_level.current_level,
            'current_xp': user_level.current_xp,
            'next_level_xp': next_level_xp,
            'total_xp': user_level.total_xp,
            'progress': (user_level.current_xp / next_level_xp) * 100
        }
        
    def get_recent_achievements(self, limit: int = 5) -> list[UserAchievement]:
        """Retorna as conquistas mais recentes do usuário."""
        return self.session.query(UserAchievement).filter_by(
            user_id=self.user_id
        ).order_by(
            UserAchievement.earned_at.desc()
        ).limit(limit).all()
        
    def __del__(self):
        """Fecha a sessão do banco de dados."""
        self.session.close() 