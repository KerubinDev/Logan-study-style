from datetime import datetime, timedelta
import random
import numpy as np
from src.database.models import StudySession, UserLevel
from src.database.database import get_session

class StudyRecommender:
    """Sistema de recomendação inteligente de tópicos de estudo."""
    
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = get_session()
        
        # Tópicos de matemática para recomendação
        self.study_topics = {
            "Álgebra": [
                "Equações lineares", "Inequações", "Funções polinomiais",
                "Álgebra de matrizes", "Sistemas lineares", "Determinantes",
                "Fatoração", "Espaços vetoriais", "Transformações lineares"
            ],
            "Geometria": [
                "Geometria Euclidiana", "Trigonometria", "Geometria Analítica",
                "Vetores no espaço", "Cônicas", "Geometria não-Euclidiana",
                "Geometria esférica", "Geometria projetiva", "Transformações geométricas"
            ],
            "Cálculo": [
                "Limites", "Derivadas", "Integrais", "Séries", "Equações diferenciais",
                "Cálculo vetorial", "Cálculo multivariável", "Teorema fundamental do cálculo",
                "Métodos numéricos"
            ],
            "Estatística": [
                "Estatística descritiva", "Probabilidade", "Distribuições estatísticas",
                "Inferência estatística", "Regressão linear", "Testes de hipóteses",
                "Correlação", "Análise de variância", "Métodos não-paramétricos"
            ],
            "Matemática Discreta": [
                "Teoria dos conjuntos", "Lógica matemática", "Combinatória",
                "Teoria dos grafos", "Relações", "Funções geradoras",
                "Recorrências", "Teoria dos números", "Criptografia"
            ]
        }
    
    def get_daily_recommendation(self, count=3):
        """Recomenda tópicos para estudo diário."""
        # Analisar histórico de estudo
        study_history = self.get_study_history(days=30)
        
        # Identificar áreas menos estudadas
        weak_areas = self.identify_weak_areas(study_history)
        
        # Obter nível do usuário
        user_level = self.get_user_level()
        
        # Gerar recomendações baseadas em áreas fracas e nível
        recommendations = []
        
        # 60% das recomendações de áreas fracas
        weak_count = int(count * 0.6) or 1
        for i in range(weak_count):
            if weak_areas:
                area = weak_areas[i % len(weak_areas)]
                topic = self.select_topic_by_level(area, user_level)
                recommendations.append({
                    "area": area,
                    "topic": topic,
                    "reason": "Este tópico precisa de mais atenção",
                    "priority": "Alta"
                })
        
        # 40% de outras áreas para variedade
        remaining = count - len(recommendations)
        other_areas = [area for area in self.study_topics.keys() if area not in weak_areas]
        
        if not other_areas:
            other_areas = list(self.study_topics.keys())
            
        for i in range(remaining):
            area = random.choice(other_areas)
            topic = self.select_topic_by_level(area, user_level)
            recommendations.append({
                "area": area,
                "topic": topic,
                "reason": "Para manter o equilíbrio no seu estudo",
                "priority": "Média"
            })
        
        return recommendations
    
    def get_study_history(self, days=30):
        """Recupera o histórico de estudo do usuário."""
        start_date = datetime.now() - timedelta(days=days)
        
        study_sessions = self.session.query(StudySession).filter(
            StudySession.user_id == self.user_id,
            StudySession.start_time >= start_date
        ).all()
        
        # Processar sessões por área
        history = {}
        for area in self.study_topics.keys():
            history[area] = 0
            
        for session in study_sessions:
            if session.subject in history:
                history[session.subject] += session.duration  # duração em minutos
            else:
                # Para sessões com assuntos que não estão nas categorias principais
                closest_area = self.find_closest_area(session.subject)
                if closest_area:
                    history[closest_area] += session.duration
        
        return history
    
    def find_closest_area(self, subject):
        """Encontra a área mais próxima para um assunto não catalogado."""
        subject = subject.lower()
        
        for area, topics in self.study_topics.items():
            area_lower = area.lower()
            if area_lower in subject or subject in area_lower:
                return area
            
            for topic in topics:
                topic_lower = topic.lower()
                if topic_lower in subject or subject in topic_lower:
                    return area
        
        return list(self.study_topics.keys())[0]  # Retorna a primeira área por padrão
    
    def identify_weak_areas(self, history):
        """Identifica áreas com menos tempo de estudo."""
        if not history or all(time == 0 for time in history.values()):
            # Se não houver histórico ou todos forem zero, retorna todas as áreas
            return list(self.study_topics.keys())
        
        # Ordenar áreas pelo tempo de estudo (crescente)
        sorted_areas = sorted(history.items(), key=lambda x: x[1])
        
        # Retornar até 3 áreas com menos tempo
        return [area for area, time in sorted_areas[:3]]
    
    def get_user_level(self):
        """Obtém o nível do usuário para ajustar a dificuldade das recomendações."""
        user_level = self.session.query(UserLevel).filter_by(
            user_id=self.user_id
        ).first()
        
        if not user_level:
            return 1  # Nível padrão
            
        return user_level.current_level
    
    def select_topic_by_level(self, area, level):
        """Seleciona um tópico adequado ao nível do usuário."""
        topics = self.study_topics.get(area, [])
        
        if not topics:
            return "Tópico geral"
            
        # Ajustar a dificuldade com base no nível
        if level <= 3:
            # Iniciante: primeiros 40% dos tópicos
            end_idx = max(1, int(len(topics) * 0.4))
            return random.choice(topics[:end_idx])
        elif level <= 7:
            # Intermediário: tópicos do meio (30%-70%)
            start_idx = int(len(topics) * 0.3)
            end_idx = int(len(topics) * 0.7)
            return random.choice(topics[start_idx:end_idx])
        else:
            # Avançado: últimos 60% dos tópicos
            start_idx = int(len(topics) * 0.4)
            return random.choice(topics[start_idx:])
    
    def get_trending_topics(self):
        """Retorna tópicos que estão em alta na matemática atualmente."""
        trending = [
            {
                "area": "Ciência de Dados",
                "topic": "Estatística Computacional",
                "reason": "Muito relevante para análise de dados moderna"
            },
            {
                "area": "Matemática Aplicada",
                "topic": "Equações Diferenciais Aplicadas",
                "reason": "Fundamental para modelagem de fenômenos naturais"
            },
            {
                "area": "Lógica",
                "topic": "Teoria dos Conjuntos Avançada",
                "reason": "Base para o pensamento matemático formal"
            }
        ]
        
        return trending
    
    def generate_study_plan(self, days=7):
        """Gera um plano de estudos para vários dias."""
        plan = {}
        
        for i in range(days):
            date = (datetime.now() + timedelta(days=i)).strftime("%Y-%m-%d")
            day_recommendations = self.get_daily_recommendation(count=random.randint(2, 4))
            
            plan[date] = {
                "main_focus": day_recommendations[0]["area"],
                "topics": day_recommendations
            }
        
        return plan 