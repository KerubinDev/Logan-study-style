from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
import sys

def get_data_dir():
    """Retorna o diretório de dados da aplicação."""
    # Usar diretório na pasta do usuário para garantir permissões de escrita
    home = os.path.expanduser("~")
    data_dir = os.path.join(home, ".matematica_em_evidencia")
    os.makedirs(data_dir, exist_ok=True)
    return data_dir

# Configurar banco de dados
DATA_DIR = get_data_dir()
DATABASE_URL = f"sqlite:///{os.path.join(DATA_DIR, 'animeproductivity.db')}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    """Inicializa o banco de dados."""
    from src.database.models import Base, User
    Base.metadata.create_all(bind=engine)
    
    # Criar usuário de teste se não existir
    session = get_session()
    try:
        if not session.query(User).filter_by(username="test").first():
            User.create(
                username="test",
                password="test123",
                email="test@example.com"
            )
            print("Usuário de teste criado com sucesso")
    except Exception as e:
        print(f"Erro ao criar usuário de teste: {e}")
    finally:
        session.close()

def get_session():
    """Retorna uma nova sessão do banco de dados."""
    return SessionLocal() 