from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import os.path
import pickle
from src.database.models import Task
from src.database.database import get_session
from src.config.settings import GOOGLE_API

class GoogleCalendarService:
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session = get_session()
        self.creds = None
        self.service = None
        self.token_path = os.path.join(
            'tokens', f'token_{user_id}.pickle'
        )
        
    def authenticate(self):
        """Autentica o usuário com o Google Calendar."""
        # Carregar credenciais existentes
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.creds = pickle.load(token)
                
        # Renovar credenciais se necessário
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    GOOGLE_API['credentials_file'],
                    self.SCOPES
                )
                self.creds = flow.run_local_server(port=0)
                
            # Salvar credenciais
            os.makedirs('tokens', exist_ok=True)
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.creds, token)
                
        self.service = build('calendar', 'v3', credentials=self.creds)
        return True
        
    def sync_tasks(self):
        """Sincroniza tarefas com o Google Calendar."""
        if not self.service:
            if not self.authenticate():
                return False, "Falha na autenticação"
                
        try:
            # Buscar tarefas não sincronizadas
            tasks = self.session.query(Task).filter(
                Task.user_id == self.user_id,
                Task.calendar_event_id.is_(None)
            ).all()
            
            for task in tasks:
                # Criar evento
                event = {
                    'summary': task.title,
                    'description': task.description,
                    'start': {
                        'dateTime': task.deadline.isoformat() if task.deadline else None,
                        'timeZone': 'America/Sao_Paulo',
                    },
                    'end': {
                        'dateTime': (task.deadline + timedelta(hours=1)).isoformat() if task.deadline else None,
                        'timeZone': 'America/Sao_Paulo',
                    },
                }
                
                # Adicionar evento ao calendário
                created_event = self.service.events().insert(
                    calendarId='primary',
                    body=event
                ).execute()
                
                # Atualizar task com ID do evento
                task.calendar_event_id = created_event['id']
                
            self.session.commit()
            return True, "Tarefas sincronizadas com sucesso"
            
        except Exception as e:
            return False, f"Erro ao sincronizar: {str(e)}"
            
    def update_task_event(self, task: Task):
        """Atualiza um evento existente no calendário."""
        if not self.service:
            if not self.authenticate():
                return False
                
        if not task.calendar_event_id:
            return False
            
        try:
            event = {
                'summary': task.title,
                'description': task.description,
                'start': {
                    'dateTime': task.deadline.isoformat() if task.deadline else None,
                    'timeZone': 'America/Sao_Paulo',
                },
                'end': {
                    'dateTime': (task.deadline + timedelta(hours=1)).isoformat() if task.deadline else None,
                    'timeZone': 'America/Sao_Paulo',
                },
            }
            
            self.service.events().update(
                calendarId='primary',
                eventId=task.calendar_event_id,
                body=event
            ).execute()
            
            return True
        except:
            return False
            
    def delete_task_event(self, task: Task):
        """Remove um evento do calendário."""
        if not self.service or not task.calendar_event_id:
            return False
            
        try:
            self.service.events().delete(
                calendarId='primary',
                eventId=task.calendar_event_id
            ).execute()
            return True
        except:
            return False
            
    def __del__(self):
        """Fecha a sessão do banco de dados."""
        self.session.close() 