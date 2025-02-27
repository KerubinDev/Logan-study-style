from datetime import datetime, timedelta
from sqlalchemy import and_
from src.database.models import Task
from src.database.database import get_session

class TaskManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.session = get_session()
        
    def add_task(self, title: str, description: str = "", deadline: str = None) -> Task:
        """Adiciona uma nova tarefa."""
        try:
            deadline_date = datetime.strptime(deadline, "%Y-%m-%d") if deadline else None
        except ValueError:
            deadline_date = None
            
        task = Task(
            user_id=self.user_id,
            title=title,
            description=description,
            deadline=deadline_date,
            status='pending'
        )
        
        self.session.add(task)
        self.session.commit()
        return task
        
    def get_today_tasks(self) -> list[Task]:
        """Retorna as tarefas do dia atual."""
        today = datetime.now().date()
        tomorrow = today + timedelta(days=1)
        
        return self.session.query(Task).filter(
            and_(
                Task.user_id == self.user_id,
                Task.created_at >= today,
                Task.created_at < tomorrow
            )
        ).all()
        
    def toggle_task(self, task_id: int) -> bool:
        """Alterna o status da tarefa entre pendente e concluída."""
        task = self.session.query(Task).filter(
            and_(
                Task.id == task_id,
                Task.user_id == self.user_id
            )
        ).first()
        
        if task:
            task.status = 'completed' if task.status == 'pending' else 'pending'
            self.session.commit()
            return True
        return False
        
    def delete_task(self, task_id: int) -> bool:
        """Deleta uma tarefa."""
        task = self.session.query(Task).filter(
            and_(
                Task.id == task_id,
                Task.user_id == self.user_id
            )
        ).first()
        
        if task:
            self.session.delete(task)
            self.session.commit()
            return True
        return False
        
    def __del__(self):
        """Fecha a sessão do banco de dados."""
        self.session.close() 