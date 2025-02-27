from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

# Criar diretório de dados se não existir
data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data')
os.makedirs(data_dir, exist_ok=True)

# Configurar banco de dados
DATABASE_URL = f"sqlite:///{os.path.join(data_dir, 'animeproductivity.db')}"
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
            email="test@example.com"  # Opcional agora
        )
    
    session.close()

def get_session():
    """Retorna uma nova sessão do banco de dados."""
    return SessionLocal() 