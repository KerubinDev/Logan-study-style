from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from enum import Enum
import bcrypt
from src.database.database import get_session

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True)
    password_hash = Column(String, nullable=False)
    access_level = Column(Integer, default=0)  # 0=normal, 1=admin
    created_at = Column(DateTime, default=datetime.now)
    
    # Relacionamentos
    tasks = relationship("Task", back_populates="user")
    pomodoro_sessions = relationship("PomodoroSession", back_populates="user")
    pomodoro_config = relationship("PomodoroConfig", back_populates="user", uselist=False)
    app_config = relationship("AppConfig", back_populates="user", uselist=False)
    achievements = relationship("UserAchievement", back_populates="user")
    level = relationship("UserLevel", back_populates="user", uselist=False)
    study_sessions = relationship("StudySession", back_populates="user")

    @staticmethod
    def authenticate(username: str, password: str) -> 'User':
        """Autentica um usuário."""
        session = get_session()
        user = session.query(User).filter_by(username=username).first()
        
        if user and User.verify_password(password, user.password_hash):
            return user
        return None
    
    @staticmethod
    def create(username: str, password: str, email: str = None) -> 'User':
        """Cria um novo usuário com senha criptografada."""
        session = get_session()
        try:
            # Gerar hash da senha
            password_hash = bcrypt.hashpw(
                password.encode('utf-8'), 
                bcrypt.gensalt()
            ).decode('utf-8')
            
            # Criar usuário
            user = User(
                username=username,
                password_hash=password_hash,
                email=email
            )
            session.add(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
    
    def verify_password(self, password: str) -> bool:
        """Verifica se a senha está correta."""
        try:
            return bcrypt.checkpw(
                password.encode('utf-8'),
                self.password_hash.encode('utf-8')
            )
        except Exception as e:
            print(f"Erro ao verificar senha: {e}")
            return False

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String)
    description = Column(String)
    deadline = Column(DateTime)
    completed = Column(Boolean, default=False)
    completion_date = Column(DateTime)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    user = relationship("User", back_populates="tasks")

class PomodoroSession(Base):
    __tablename__ = 'pomodoro_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime, nullable=True)
    completed = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="pomodoro_sessions")

class PomodoroConfig(Base):
    __tablename__ = 'pomodoro_config'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    work_time = Column(Integer, default=25)
    break_time = Column(Integer, default=5)
    long_break_time = Column(Integer, default=15)
    block_distractions = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="pomodoro_config")

class AppConfig(Base):
    __tablename__ = 'app_config'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    theme = Column(String(20), default='dark')
    notifications_enabled = Column(Boolean, default=True)
    calendar_sync_enabled = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="app_config")

class AchievementType(Enum):
    POMODORO_COUNT = "pomodoro_count"
    STUDY_TIME = "study_time"
    TASK_COMPLETE = "task_complete"
    STREAK_DAYS = "streak_days"

class Achievement(Base):
    __tablename__ = 'achievements'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(500))
    type = Column(String(50), nullable=False)
    requirement = Column(Integer, nullable=False)  # Valor necessário para conquistar
    icon_path = Column(String(200))  # Caminho para o ícone anime temático
    xp_reward = Column(Integer, default=100)
    
class UserAchievement(Base):
    __tablename__ = 'user_achievements'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    achievement_id = Column(Integer, ForeignKey('achievements.id'))
    earned_at = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="achievements")
    achievement = relationship("Achievement")

class UserLevel(Base):
    __tablename__ = 'user_levels'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)
    current_level = Column(Integer, default=1)
    current_xp = Column(Integer, default=0)
    total_xp = Column(Integer, default=0)
    
    user = relationship("User", back_populates="level")

class StudySession(Base):
    __tablename__ = 'study_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    subject = Column(String(100))
    duration = Column(Integer)  # Duração em minutos
    start_time = Column(DateTime, default=datetime.now)
    end_time = Column(DateTime, nullable=True)
    
    user = relationship("User", back_populates="study_sessions")

# Adicionar relação na classe User
User.pomodoro_sessions = relationship("PomodoroSession", back_populates="user") 