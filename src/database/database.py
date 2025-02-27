from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import sys

def get_data_dir():
    """Retorna o diretório de dados apropriado para o ambiente."""
    if getattr(sys, 'frozen', False):  # Se estiver rodando como executável
        # Usar AppData no Windows
        app_data = os.path.join(os.environ['APPDATA'], 'AnimeProductivity')
    else:
        # Se estiver rodando como código fonte
        app_data = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
    
    # Criar diretório se não existir
    os.makedirs(app_data, exist_ok=True)
    return app_data

# Configurar banco de dados
DATA_DIR = get_data_dir()
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'animeproductivity.db')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Inicializa o banco de dados."""
    from src.database.models import Base
    Base.metadata.create_all(bind=engine)
    
    # Executar migrações
    from src.database.migrations import upgrade_database
    upgrade_database()
    
    # Criar usuário de teste se não existir
    session = get_session()
    from src.database.models import User
    
    if not session.query(User).filter_by(username="test").first():
        User.create(
            username="test",
            password="test123",
            email="test@example.com"
        )
    
    session.close()

def get_session():
    """Retorna uma nova sessão do banco de dados."""
    return SessionLocal() 