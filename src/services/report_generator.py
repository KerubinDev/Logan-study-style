from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.linecharts import HorizontalLineChart
from datetime import datetime, timedelta
from sqlalchemy import and_
from src.database.models import PomodoroSession, Task, User
from src.database.database import get_session
import os

class ReportGenerator:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.session = get_session()
        self.styles = getSampleStyleSheet()
        
        # Criar estilo personalizado para títulos de anime
        self.styles.add(ParagraphStyle(
            name='AnimeTitle',
            parent=self.styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=24,
            textColor=colors.HexColor('#7aa2f7'),
            spaceAfter=30
        ))
        
    def generate_weekly_report(self, output_path: str):
        """Gera um relatório semanal em PDF."""
        doc = SimpleDocTemplate(
            output_path,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        # Lista de elementos do PDF
        elements = []
        
        # Adicionar cabeçalho
        self._add_header(elements)
        
        # Adicionar resumo da semana
        self._add_weekly_summary(elements)
        
        # Adicionar gráfico de produtividade
        self._add_productivity_chart(elements)
        
        # Adicionar lista de tarefas concluídas
        self._add_completed_tasks(elements)
        
        # Gerar o PDF
        doc.build(elements)
        
    def _add_header(self, elements):
        """Adiciona o cabeçalho do relatório."""
        # Logo ou imagem temática
        if os.path.exists('assets/logo.png'):
            elements.append(Image('assets/logo.png', width=200, height=100))
            elements.append(Spacer(1, 20))
        
        # Título
        title = Paragraph(
            "Relatório Semanal de Produtividade",
            self.styles['AnimeTitle']
        )
        elements.append(title)
        
        # Período do relatório
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        period = Paragraph(
            f"Período: {start_date.strftime('%d/%m/%Y')} - {end_date.strftime('%d/%m/%Y')}",
            self.styles['Normal']
        )
        elements.append(period)
        elements.append(Spacer(1, 30))
        
    def _add_weekly_summary(self, elements):
        """Adiciona o resumo da semana."""
        # Buscar dados do banco
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        pomodoro_sessions = self.session.query(PomodoroSession).filter(
            PomodoroSession.user_id == self.user_id,
            PomodoroSession.start_time >= start_date,
            PomodoroSession.start_time <= end_date
        ).all()
        
        completed_tasks = self.session.query(Task).filter(
            Task.user_id == self.user_id,
            Task.status == 'completed',
            Task.created_at >= start_date,
            Task.created_at <= end_date
        ).all()
        
        # Calcular estatísticas
        total_duration = sum(
            session.duration for session in pomodoro_sessions if session.completed
        )
        
        completed_sessions = len([s for s in pomodoro_sessions if s.completed])
        
        # Criar tabela de resumo
        pomodoro_data = [
            ['Total de Sessões', str(len(pomodoro_sessions))],
            ['Sessões Completadas', str(completed_sessions)],
            ['Tempo Total (minutos)', str(total_duration)]
        ]
        
        pomodoro_table = Table(pomodoro_data, colWidths=[200, 100])
        pomodoro_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 14),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
            ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 1), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(pomodoro_table)
        elements.append(Spacer(1, 20))
        
    def _add_productivity_chart(self, elements):
        """Adiciona um gráfico de produtividade diária."""
        # Criar o gráfico
        drawing = Drawing(400, 200)
        
        # Dados do gráfico
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        # Calcular horas estudadas por dia
        daily_hours = []
        dates = []
        current_date = start_date
        
        while current_date <= end_date:
            next_date = current_date + timedelta(days=1)
            
            # Buscar sessões do dia
            sessions = self.session.query(PomodoroSession).filter(
                and_(
                    PomodoroSession.user_id == self.user_id,
                    PomodoroSession.start_time >= current_date,
                    PomodoroSession.start_time < next_date
                )
            ).all()
            
            # Calcular horas
            hours = sum(
                session.duration / 60
                for session in sessions
                if session.completed
            )
            
            daily_hours.append(hours)
            dates.append(current_date.strftime('%d/%m'))
            current_date = next_date
        
        # Configurar o gráfico
        chart = HorizontalLineChart()
        chart.x = 50
        chart.y = 50
        chart.height = 125
        chart.width = 300
        chart.data = [daily_hours]
        chart.categoryAxis.categoryNames = dates
        chart.categoryAxis.labels.boxAnchor = 'n'
        chart.valueAxis.valueMin = 0
        chart.valueAxis.valueMax = max(daily_hours) + 1
        chart.lines[0].strokeColor = colors.HexColor('#7aa2f7')
        chart.lines[0].strokeWidth = 2
        
        drawing.add(chart)
        elements.append(drawing)
        elements.append(Spacer(1, 30))
        
    def _add_completed_tasks(self, elements):
        """Adiciona a lista de tarefas concluídas."""
        elements.append(Paragraph(
            "Tarefas Concluídas",
            self.styles['Heading2']
        ))
        elements.append(Spacer(1, 12))
        
        # Buscar tarefas concluídas
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        tasks = self.session.query(Task).filter(
            and_(
                Task.user_id == self.user_id,
                Task.status == 'completed',
                Task.created_at >= start_date,
                Task.created_at <= end_date
            )
        ).all()
        
        # Criar tabela de tarefas
        if tasks:
            task_data = [[
                'Título',
                'Descrição',
                'Data de Conclusão'
            ]]
            
            for task in tasks:
                task_data.append([
                    task.title,
                    task.description[:50] + '...' if task.description else '',
                    task.created_at.strftime('%d/%m/%Y')
                ])
            
            task_table = Table(task_data, colWidths=[150, 200, 100])
            task_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 12),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 1), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            elements.append(task_table)
        else:
            elements.append(Paragraph(
                "Nenhuma tarefa concluída neste período.",
                self.styles['Normal']
            ))
            
    def __del__(self):
        """Fecha a sessão do banco de dados."""
        self.session.close() 