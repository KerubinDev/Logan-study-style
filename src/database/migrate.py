from src.database.database import get_data_dir, Base, engine
import os

def migrate_database():
    """Executa a migração do banco de dados."""
    try:
        # Criar todas as tabelas definidas em models.py
        Base.metadata.create_all(engine)
        print("Migração do banco de dados concluída com sucesso.")
        return True
    except Exception as e:
        print(f"Erro durante a migração do banco de dados: {e}")
        return False

if __name__ == "__main__":
    migrate_database() 