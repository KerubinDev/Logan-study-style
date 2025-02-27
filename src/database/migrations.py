from sqlalchemy import create_engine, MetaData, Table, Column, Boolean, DateTime
from src.database.database import DATABASE_URL

def upgrade_database():
    """Executa as migrações necessárias."""
    engine = create_engine(DATABASE_URL)
    metadata = MetaData()
    
    # Obter a tabela tasks
    tasks = Table('tasks', metadata, autoload_with=engine)
    
    # Adicionar novas colunas se não existirem
    with engine.begin() as connection:
        # Verificar se a coluna completed existe
        if 'completed' not in tasks.columns:
            connection.execute('''
                ALTER TABLE tasks 
                ADD COLUMN completed BOOLEAN DEFAULT FALSE
            ''')
            
        # Verificar se a coluna completion_date existe
        if 'completion_date' not in tasks.columns:
            connection.execute('''
                ALTER TABLE tasks 
                ADD COLUMN completion_date DATETIME
            ''')
            
        connection.commit()

if __name__ == "__main__":
    upgrade_database() 