from datetime import datetime, date
from sqlalchemy import and_
from src.database.models import Task
from src.database.database import get_session

class TaskManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = get_session()
        
    def add_task(self, title: str, description: str = None, deadline: str = None):
        """Adiciona uma nova tarefa."""
        try:
            # Converter deadline string para datetime se fornecido
            deadline_date = None
            if deadline:
                try:
                    deadline_date = datetime.strptime(deadline, "%Y-%m-%d %H:%M")
                except ValueError:
                    try:
                        deadline_date = datetime.strptime(deadline, "%Y-%m-%d")
                    except ValueError:
                        pass
            
            # Criar nova tarefa
            task = Task(
                user_id=self.user_id,
                title=title,
                description=description,
                deadline=deadline_date,
                completed=False,
                created_at=datetime.now()
            )
            
            self.session.add(task)
            self.session.commit()
            return True
            
        except Exception as e:
            print(f"Erro ao adicionar tarefa: {str(e)}")
            self.session.rollback()
            return False
            
    def get_today_tasks(self):
        """Retorna as tarefas do dia."""
        today = date.today()
        tomorrow = date.today().replace(day=today.day + 1)
        
        return self.session.query(Task).filter(
            and_(
                Task.user_id == self.user_id,
                Task.created_at >= today,
                Task.created_at < tomorrow
            )
        ).all()
        
    def complete_task(self, task_id: int):
        """Marca uma tarefa como concluída."""
        task = self.session.query(Task).get(task_id)
        if task and task.user_id == self.user_id:
            task.completed = True
            task.completion_date = datetime.now()
            self.session.commit()
            return True
        return False
        
    def delete_task(self, task_id: int):
        """Remove uma tarefa."""
        task = self.session.query(Task).get(task_id)
        if task and task.user_id == self.user_id:
            self.session.delete(task)
            self.session.commit()
            return True
        return False
        
    def __del__(self):
        """Fecha a sessão do banco de dados."""
        self.session.close() 