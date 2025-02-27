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
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=True)  # Tornando email opcional
    password_hash = Column(String(128), nullable=False)
    access_level = Column(Integer, default=0)  # 0=normal, 1=admin
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    tasks = relationship("Task", back_populates="user")
    pomodoro_sessions = relationship("PomodoroSession", back_populates="user")
    pomodoro_config = relationship("PomodoroConfig", back_populates="user", uselist=False)
    app_config = relationship("AppConfig", back_populates="user", uselist=False)
    achievements = relationship("UserAchievement", back_populates="user")
    level = relationship("UserLevel", back_populates="user", uselist=False)

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
        """Cria um novo usuário."""
        session = get_session()
        
        # Verificar se usuário já existe
        if session.query(User).filter_by(username=username).first():
            return None
            
        # Criar novo usuário
        password_hash = User.hash_password(password)
        user = User(
            username=username,
            email=email,
            password_hash=password_hash
        )
        
        session.add(user)
        session.commit()
        
        return user
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Gera um hash da senha."""
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
    
    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verifica se a senha está correta."""
        return bcrypt.checkpw(password.encode(), password_hash.encode())

class Task(Base):
    __tablename__ = 'tasks'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    deadline = Column(DateTime)
    status = Column(String(20), default='pending')  # pending, completed, cancelled
    created_at = Column(DateTime, default=datetime.utcnow)
    calendar_event_id = Column(String(100))  # ID do evento no Google Calendar
    
    user = relationship("User", back_populates="tasks")

class PomodoroSession(Base):
    __tablename__ = 'pomodoro_sessions'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    duration = Column(Integer)  # em minutos
    completed = Column(Boolean, default=False)
    
    # Relacionamento
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