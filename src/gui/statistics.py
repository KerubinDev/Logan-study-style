from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                              QFrame, QScrollArea, QPushButton, QComboBox, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime, timedelta
from src.database.models import PomodoroSession, Task
from src.database.database import get_session
from src.services.pomodoro import PomodoroTimer
from src.services.task_manager import TaskManager
from src.services.achievement_manager import AchievementManager

class MplCanvas(FigureCanvas):
    """Canvas para gráficos do Matplotlib."""
    
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)

class StatisticsPanel(QWidget):
    """Painel de estatísticas completo."""
    
    def __init__(self, user_id=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.pomodoro_timer = PomodoroTimer(user_id)
        self.task_manager = TaskManager(user_id)
        self.achievement_manager = AchievementManager(user_id)
        
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Configura a interface do painel de estatísticas."""
        main_layout = QVBoxLayout(self)
        
        # Scroll Area para comportar todos os gráficos
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        scroll_content = QWidget()
        content_layout = QVBoxLayout(scroll_content)
        content_layout.setSpacing(20)
        
        # Cabeçalho
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Estatísticas de Estudo")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)
        
        # Período
        period_selector = QComboBox()
        period_selector.addItems(["Últimos 7 dias", "Últimos 30 dias", "Este mês", "Este ano"])
        period_selector.setObjectName("periodSelector")
        period_selector.currentTextChanged.connect(self.change_period)
        header_layout.addWidget(period_selector)
        
        content_layout.addWidget(header)
        
        # Seção de resumo
        summary_section = QFrame()
        summary_section.setObjectName("sectionCard")
        summary_layout = QHBoxLayout(summary_section)
        
        # Cards de estatísticas resumidas
        self.create_stat_card(summary_layout, "Tempo Total de Estudo", "0h", "clockIcon")
        self.create_stat_card(summary_layout, "Pomodoros Completos", "0", "tomatoIcon")
        self.create_stat_card(summary_layout, "Tarefas Concluídas", "0", "checkIcon")
        self.create_stat_card(summary_layout, "Nível Atual", "1", "starIcon")
        
        content_layout.addWidget(summary_section)
        
        # Gráfico de tempo de estudo
        study_time_section = QFrame()
        study_time_section.setObjectName("sectionCard")
        study_time_layout = QVBoxLayout(study_time_section)
        
        study_time_header = QLabel("Tempo de Estudo por Dia")
        study_time_header.setObjectName("sectionTitle")
        study_time_layout.addWidget(study_time_header)
        
        self.study_time_chart = MplCanvas(self, width=5, height=4)
        study_time_layout.addWidget(self.study_time_chart)
        
        content_layout.addWidget(study_time_section)
        
        # Gráfico de produtividade por horário
        productivity_section = QFrame()
        productivity_section.setObjectName("sectionCard")
        productivity_layout = QVBoxLayout(productivity_section)
        
        productivity_header = QLabel("Produtividade por Horário")
        productivity_header.setObjectName("sectionTitle")
        productivity_layout.addWidget(productivity_header)
        
        self.productivity_chart = MplCanvas(self, width=5, height=4)
        productivity_layout.addWidget(self.productivity_chart)
        
        content_layout.addWidget(productivity_section)
        
        # Gráfico de distribuição de tarefas
        tasks_section = QFrame()
        tasks_section.setObjectName("sectionCard")
        tasks_layout = QVBoxLayout(tasks_section)
        
        tasks_header = QLabel("Distribuição de Tarefas")
        tasks_header.setObjectName("sectionTitle")
        tasks_layout.addWidget(tasks_header)
        
        self.tasks_chart = MplCanvas(self, width=5, height=4)
        tasks_layout.addWidget(self.tasks_chart)
        
        content_layout.addWidget(tasks_section)
        
        # Progresso no método Logan
        logan_section = QFrame()
        logan_section.setObjectName("sectionCard")
        logan_layout = QVBoxLayout(logan_section)
        
        logan_header = QLabel("Progresso no Método Logan")
        logan_header.setObjectName("sectionTitle")
        logan_layout.addWidget(logan_header)
        
        self.logan_chart = MplCanvas(self, width=5, height=4)
        logan_layout.addWidget(self.logan_chart)
        
        content_layout.addWidget(logan_section)
        
        # Adicionar botões de exportação
        export_section = QWidget()
        export_layout = QHBoxLayout(export_section)
        
        export_pdf = QPushButton("Exportar como PDF")
        export_pdf.setObjectName("primaryButton")
        export_pdf.clicked.connect(self.export_as_pdf)
        export_layout.addWidget(export_pdf)
        
        export_image = QPushButton("Salvar Gráficos")
        export_image.setObjectName("primaryButton")
        export_image.clicked.connect(self.save_charts)
        export_layout.addWidget(export_image)
        
        content_layout.addWidget(export_section)
        
        # Configurar scroll area
        scroll_area.setWidget(scroll_content)
        main_layout.addWidget(scroll_area)
    
    def create_stat_card(self, parent_layout, title, value, icon_name):
        """Cria um card de estatística resumida."""
        card = QFrame()
        card.setObjectName("statCard")
        card_layout = QVBoxLayout(card)
        
        # Ícone
        icon_label = QLabel()
        icon_label.setObjectName(icon_name)
        card_layout.addWidget(icon_label, alignment=Qt.AlignCenter)
        
        # Valor
        value_label = QLabel(value)
        value_label.setObjectName("statValue")
        card_layout.addWidget(value_label, alignment=Qt.AlignCenter)
        
        # Título
        title_label = QLabel(title)
        title_label.setObjectName("statTitle")
        card_layout.addWidget(title_label, alignment=Qt.AlignCenter)
        
        parent_layout.addWidget(card)
        return value_label
    
    def load_data(self):
        """Carrega os dados para as estatísticas."""
        try:
            # Período padrão (últimos 7 dias)
            start_date = datetime.now() - timedelta(days=7)
            end_date = datetime.now()
            
            self.update_study_time_chart(start_date, end_date)
            self.update_productivity_chart(start_date, end_date)
            self.update_tasks_chart(start_date, end_date)
            self.update_logan_chart(start_date, end_date)
            self.update_summary_stats(start_date, end_date)
            
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
    
    def change_period(self, period):
        """Muda o período das estatísticas."""
        end_date = datetime.now()
        
        if period == "Últimos 7 dias":
            start_date = end_date - timedelta(days=7)
        elif period == "Últimos 30 dias":
            start_date = end_date - timedelta(days=30)
        elif period == "Este mês":
            start_date = datetime(end_date.year, end_date.month, 1)
        elif period == "Este ano":
            start_date = datetime(end_date.year, 1, 1)
        else:
            start_date = end_date - timedelta(days=7)
        
        self.update_study_time_chart(start_date, end_date)
        self.update_productivity_chart(start_date, end_date)
        self.update_tasks_chart(start_date, end_date)
        self.update_logan_chart(start_date, end_date)
        self.update_summary_stats(start_date, end_date)
    
    def update_study_time_chart(self, start_date, end_date):
        """Atualiza o gráfico de tempo de estudo."""
        # Obter dados do pomodoro
        study_sessions = self.pomodoro_timer.get_study_sessions(start_date, end_date)
        
        # Preparar dados para o gráfico
        dates = []
        minutes = []
        
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date.strftime('%d/%m'))
            
            # Calcular minutos estudados neste dia
            day_minutes = sum([
                session['duration']
                for session in study_sessions
                if session['date'].date() == current_date.date()
            ])
            
            minutes.append(day_minutes)
            current_date += timedelta(days=1)
        
        # Criar gráfico
        ax = self.study_time_chart.axes
        ax.clear()
        ax.bar(dates, minutes, color='#4169E1')
        ax.set_ylabel('Minutos')
        ax.set_title('Tempo de Estudo por Dia')
        ax.tick_params(axis='x', rotation=45)
        self.study_time_chart.fig.tight_layout()
        self.study_time_chart.draw()
    
    def update_productivity_chart(self, start_date, end_date):
        """Atualiza o gráfico de produtividade por horário."""
        # Obter dados do pomodoro
        study_sessions = self.pomodoro_timer.get_study_sessions(start_date, end_date)
        
        # Preparar dados para o gráfico
        hours = list(range(24))
        productivity = [0] * 24
        
        for session in study_sessions:
            hour = session['date'].hour
            productivity[hour] += session['duration']
        
        # Criar gráfico
        ax = self.productivity_chart.axes
        ax.clear()
        ax.plot(hours, productivity, marker='o', color='#7289da', linewidth=2)
        ax.fill_between(hours, productivity, alpha=0.2, color='#7289da')
        ax.set_xlabel('Hora do Dia')
        ax.set_ylabel('Minutos Produtivos')
        ax.set_title('Produtividade por Horário')
        ax.set_xticks(range(0, 24, 2))
        ax.grid(True, linestyle='--', alpha=0.7)
        self.productivity_chart.fig.tight_layout()
        self.productivity_chart.draw()
    
    def update_tasks_chart(self, start_date, end_date):
        """Atualiza o gráfico de tarefas."""
        # Obter dados de tarefas
        tasks = self.task_manager.get_tasks(start_date, end_date)
        
        # Contar tarefas por status
        completed = len([t for t in tasks if t['completed']])
        pending = len([t for t in tasks if not t['completed'] and t['deadline'] > datetime.now()])
        overdue = len([t for t in tasks if not t['completed'] and t['deadline'] <= datetime.now()])
        
        # Criar gráfico
        ax = self.tasks_chart.axes
        ax.clear()
        labels = ['Completadas', 'Pendentes', 'Atrasadas']
        sizes = [completed, pending, overdue]
        colors = ['#43b581', '#faa61a', '#ed4245']
        
        ax.pie(
            sizes, 
            labels=labels, 
            colors=colors,
            autopct='%1.1f%%',
            startangle=90
        )
        ax.axis('equal')
        ax.set_title('Distribuição de Tarefas')
        self.tasks_chart.fig.tight_layout()
        self.tasks_chart.draw()
    
    def update_logan_chart(self, start_date, end_date):
        """Atualiza o gráfico de progresso no Método Logan."""
        # Obter dados do Método Logan
        subjects = [
            {"name": "Matemática", "completed": 70, "total": 100},
            {"name": "Física", "completed": 50, "total": 80},
            {"name": "Química", "completed": 30, "total": 60},
            {"name": "Biologia", "completed": 20, "total": 40},
            {"name": "História", "completed": 15, "total": 30}
        ]
        
        # Preparar dados para o gráfico
        names = [s["name"] for s in subjects]
        completion = [s["completed"] / s["total"] * 100 for s in subjects]
        
        # Criar gráfico
        ax = self.logan_chart.axes
        ax.clear()
        colors = plt.cm.viridis(np.linspace(0, 1, len(names)))
        ax.barh(names, completion, color=colors)
        ax.set_xlabel('Porcentagem Concluída')
        ax.set_title('Progresso por Matéria')
        ax.set_xlim(0, 100)
        
        # Adicionar rótulos de valor
        for i, v in enumerate(completion):
            ax.text(v + 2, i, f"{v:.1f}%", va='center')
        
        self.logan_chart.fig.tight_layout()
        self.logan_chart.draw()
    
    def update_summary_stats(self, start_date, end_date):
        """Atualiza as estatísticas resumidas."""
        # Total de tempo estudado
        study_sessions = self.pomodoro_timer.get_study_sessions(start_date, end_date)
        total_minutes = sum([session['duration'] for session in study_sessions])
        hours = total_minutes // 60
        minutes = total_minutes % 60
        
        # Total de pomodoros
        total_pomodoros = len(study_sessions)
        
        # Total de tarefas
        tasks = self.task_manager.get_tasks(start_date, end_date)
        completed_tasks = len([t for t in tasks if t['completed']])
        
        # Nível atual
        user_level = self.achievement_manager.get_user_level()
        
        # Atualizar valores
        self.findChild(QLabel, "statValue", Qt.FindChildrenRecursively)[0].setText(f"{hours}h {minutes}m")
        self.findChild(QLabel, "statValue", Qt.FindChildrenRecursively)[1].setText(str(total_pomodoros))
        self.findChild(QLabel, "statValue", Qt.FindChildrenRecursively)[2].setText(str(completed_tasks))
        self.findChild(QLabel, "statValue", Qt.FindChildrenRecursively)[3].setText(str(user_level['level']))
    
    def export_as_pdf(self):
        """Exporta as estatísticas como PDF."""
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas
        from reportlab.lib import colors
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
        from reportlab.lib.styles import getSampleStyleSheet
        import os
        
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar Relatório", "", "PDF Files (*.pdf)"
        )
        
        if not file_path:
            return
        
        # Salvar gráficos como imagens temporárias
        temp_dir = os.path.join(os.path.expanduser("~"), ".temp_charts")
        os.makedirs(temp_dir, exist_ok=True)
        
        self.study_time_chart.fig.savefig(os.path.join(temp_dir, "study_time.png"))
        self.productivity_chart.fig.savefig(os.path.join(temp_dir, "productivity.png"))
        self.tasks_chart.fig.savefig(os.path.join(temp_dir, "tasks.png"))
        self.logan_chart.fig.savefig(os.path.join(temp_dir, "logan.png"))
        
        # Criar PDF
        doc = SimpleDocTemplate(file_path, pagesize=letter)
        styles = getSampleStyleSheet()
        content = []
        
        # Título
        content.append(Paragraph("Relatório de Estudos", styles['Title']))
        content.append(Spacer(1, 20))
        
        # Data
        content.append(Paragraph(f"Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}", styles['Normal']))
        content.append(Spacer(1, 20))
        
        # Resumo
        content.append(Paragraph("Resumo Estatístico", styles['Heading2']))
        content.append(Spacer(1, 10))
        
        # Tabela de resumo
        summary_data = [
            ["Métrica", "Valor"],
            ["Tempo Total de Estudo", self.findChild(QLabel, "statValue", Qt.FindChildrenRecursively)[0].text()],
            ["Pomodoros Completos", self.findChild(QLabel, "statValue", Qt.FindChildrenRecursively)[1].text()],
            ["Tarefas Concluídas", self.findChild(QLabel, "statValue", Qt.FindChildrenRecursively)[2].text()],
            ["Nível Atual", self.findChild(QLabel, "statValue", Qt.FindChildrenRecursively)[3].text()]
        ]
        
        summary_table = Table(summary_data, colWidths=[250, 100])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        content.append(summary_table)
        content.append(Spacer(1, 20))
        
        # Gráficos
        for name, title in [
            ("study_time.png", "Tempo de Estudo por Dia"),
            ("productivity.png", "Produtividade por Horário"),
            ("tasks.png", "Distribuição de Tarefas"),
            ("logan.png", "Progresso por Matéria")
        ]:
            content.append(Paragraph(title, styles['Heading2']))
            content.append(Spacer(1, 10))
            
            img_path = os.path.join(temp_dir, name)
            img = Image(img_path, width=450, height=300)
            content.append(img)
            content.append(Spacer(1, 20))
        
        # Construir o PDF
        doc.build(content)
        
        # Limpar arquivos temporários
        for name in ["study_time.png", "productivity.png", "tasks.png", "logan.png"]:
            os.remove(os.path.join(temp_dir, name))
        
        QMessageBox.information(
            self, "Exportação Concluída", 
            f"Relatório salvo em:\n{file_path}"
        )
    
    def save_charts(self):
        """Salva os gráficos como imagens."""
        directory = QFileDialog.getExistingDirectory(
            self, "Selecionar Pasta para Salvar"
        )
        
        if not directory:
            return
        
        # Salvar cada gráfico
        self.study_time_chart.fig.savefig(os.path.join(directory, "tempo_estudo.png"))
        self.productivity_chart.fig.savefig(os.path.join(directory, "produtividade.png"))
        self.tasks_chart.fig.savefig(os.path.join(directory, "tarefas.png"))
        self.logan_chart.fig.savefig(os.path.join(directory, "progresso_materias.png"))
        
        QMessageBox.information(
            self, "Exportação Concluída", 
            f"Gráficos salvos em:\n{directory}"
        )

class StatisticsWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_id = parent.user_id
        self.session = get_session()
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Estatísticas")
        self.setMinimumSize(800, 600)
        
        layout = QVBoxLayout(self)
        
        # Header
        header = QFrame()
        header_layout = QHBoxLayout(header)
        title = QLabel("Estatísticas de Produtividade")
        title.setStyleSheet("font-size: 24pt; font-weight: bold;")
        header_layout.addWidget(title)
        layout.addWidget(header)
        
        # Estatísticas Gerais
        stats_frame = QFrame()
        stats_layout = QVBoxLayout(stats_frame)
        
        # Pomodoros completados hoje
        today = datetime.now().date()
        pomodoros_today = self.session.query(PomodoroSession).filter(
            PomodoroSession.user_id == self.user_id,
            PomodoroSession.start_time >= today,
            PomodoroSession.completed == True
        ).count()
        
        pomodoro_label = QLabel(f"Pomodoros Completados Hoje: {pomodoros_today}")
        pomodoro_label.setStyleSheet("font-size: 16pt;")
        stats_layout.addWidget(pomodoro_label)
        
        # Tarefas completadas hoje
        tasks_today = self.session.query(Task).filter(
            Task.user_id == self.user_id,
            Task.completed == True,
            Task.completion_date >= today
        ).count()
        
        tasks_label = QLabel(f"Tarefas Completadas Hoje: {tasks_today}")
        tasks_label.setStyleSheet("font-size: 16pt;")
        stats_layout.addWidget(tasks_label)
        
        # Tempo total focado
        total_time = self.session.query(PomodoroSession).filter(
            PomodoroSession.user_id == self.user_id,
            PomodoroSession.completed == True
        ).count() * 25  # 25 minutos por pomodoro
        
        hours = total_time // 60
        minutes = total_time % 60
        time_label = QLabel(f"Tempo Total Focado: {hours}h {minutes}m")
        time_label.setStyleSheet("font-size: 16pt;")
        stats_layout.addWidget(time_label)
        
        layout.addWidget(stats_frame)
        
        # Aqui você pode adicionar mais widgets para mostrar as estatísticas
        # Por exemplo: gráficos, números, etc. 