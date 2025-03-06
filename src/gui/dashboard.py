from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
from src.services.study_recommender import StudyRecommender
from src.services.achievement_manager import AchievementManager
from src.gui.timer_widget import AdvancedTimerWidget
from datetime import datetime, timedelta
import random

class DashboardWidget(QWidget):
    """Widget de dashboard personalizado com recomendações e estatísticas."""
    
    def __init__(self, user_id=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.recommender = StudyRecommender(user_id)
        self.achievement_manager = AchievementManager(user_id)
        self.setup_ui()
        self.load_data()
    
    def setup_ui(self):
        """Configura a interface do dashboard."""
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        
        # Cabeçalho personalizado
        header = QWidget()
        header.setObjectName("dashboardHeader")
        header_layout = QHBoxLayout(header)
        
        greeting_container = QWidget()
        greeting_layout = QVBoxLayout(greeting_container)
        
        self.greeting_label = QLabel("Olá, Estudante!")
        self.greeting_label.setObjectName("greetingLabel")
        greeting_layout.addWidget(self.greeting_label)
        
        current_date = QLabel(datetime.now().strftime("%A, %d de %B de %Y"))
        current_date.setObjectName("dateLabel")
        greeting_layout.addWidget(current_date)
        
        header_layout.addWidget(greeting_container)
        
        # Nível e Progresso
        level_widget = QWidget()
        level_widget.setObjectName("levelWidget")
        level_layout = QVBoxLayout(level_widget)
        
        level_info = QHBoxLayout()
        level_label = QLabel("Nível:")
        level_label.setObjectName("levelLabel")
        level_info.addWidget(level_label)
        
        self.level_value = QLabel("1")
        self.level_value.setObjectName("levelValue")
        level_info.addWidget(self.level_value)
        
        level_layout.addLayout(level_info)
        
        # Barra de progresso do nível
        self.level_progress = QProgressBar()
        self.level_progress.setRange(0, 100)
        self.level_progress.setValue(0)
        self.level_progress.setFormat("%p% para o próximo nível")
        self.level_progress.setObjectName("levelProgressBar")
        level_layout.addWidget(self.level_progress)
        
        header_layout.addWidget(level_widget)
        
        main_layout.addWidget(header)
        
        # Conteúdo principal em 2 colunas
        content = QWidget()
        content_layout = QHBoxLayout(content)
        content_layout.setSpacing(20)
        
        # Coluna da esquerda (70%)
        left_column = QWidget()
        left_layout = QVBoxLayout(left_column)
        left_layout.setSpacing(20)
        
        # Timer avançado
        timer_section = QFrame()
        timer_section.setObjectName("sectionCard")
        timer_layout = QVBoxLayout(timer_section)
        
        timer_header = QLabel("Tempo de Estudo")
        timer_header.setObjectName("sectionTitle")
        timer_layout.addWidget(timer_header)
        
        # Adicionar widget de timer
        self.timer_widget = AdvancedTimerWidget(self.user_id)
        timer_layout.addWidget(self.timer_widget)
        
        left_layout.addWidget(timer_section)
        
        # Recomendações de estudo
        recommendations = QFrame()
        recommendations.setObjectName("sectionCard")
        rec_layout = QVBoxLayout(recommendations)
        
        rec_header = QLabel("Recomendações para Hoje")
        rec_header.setObjectName("sectionTitle")
        rec_layout.addWidget(rec_header)
        
        self.rec_list = QVBoxLayout()
        rec_layout.addLayout(self.rec_list)
        
        # Botão para gerar plano de estudos
        gen_plan_btn = QPushButton("Gerar Plano de Estudos")
        gen_plan_btn.setObjectName("primaryButton")
        gen_plan_btn.clicked.connect(self.generate_study_plan)
        rec_layout.addWidget(gen_plan_btn, alignment=Qt.AlignRight)
        
        left_layout.addWidget(recommendations)
        
        content_layout.addWidget(left_column, 70)
        
        # Coluna da direita (30%)
        right_column = QWidget()
        right_layout = QVBoxLayout(right_column)
        right_layout.setSpacing(20)
        
        # Tópicos em destaque
        trending = QFrame()
        trending.setObjectName("sectionCard")
        trending_layout = QVBoxLayout(trending)
        
        trending_header = QLabel("Tópicos em Destaque")
        trending_header.setObjectName("sectionTitle")
        trending_layout.addWidget(trending_header)
        
        self.trending_list = QVBoxLayout()
        trending_layout.addLayout(self.trending_list)
        
        right_layout.addWidget(trending)
        
        # Conquistas recentes
        achievements = QFrame()
        achievements.setObjectName("sectionCard")
        ach_layout = QVBoxLayout(achievements)
        
        ach_header = QLabel("Suas Conquistas")
        ach_header.setObjectName("sectionTitle")
        ach_layout.addWidget(ach_header)
        
        self.ach_list = QVBoxLayout()
        ach_layout.addLayout(self.ach_list)
        
        # Ver todas as conquistas
        all_ach_btn = QPushButton("Ver Todas")
        all_ach_btn.setObjectName("secondaryButton")
        all_ach_btn.clicked.connect(self.show_all_achievements)
        ach_layout.addWidget(all_ach_btn, alignment=Qt.AlignRight)
        
        right_layout.addWidget(achievements)
        
        # Dica do dia
        tip = QFrame()
        tip.setObjectName("tipCard")
        tip_layout = QVBoxLayout(tip)
        
        tip_title = QLabel("Dica do Dia")
        tip_title.setObjectName("tipTitle")
        tip_layout.addWidget(tip_title)
        
        self.tip_content = QLabel("Carregando dica...")
        self.tip_content.setObjectName("tipContent")
        self.tip_content.setWordWrap(True)
        tip_layout.addWidget(self.tip_content)
        
        right_layout.addWidget(tip)
        
        content_layout.addWidget(right_column, 30)
        
        main_layout.addWidget(content)
        
        # Estilizando o cabeçalho
        self.setStyleSheet("""
            #dashboardHeader {
                background-color: #3E3E3E;
                border-radius: 10px;
                padding: 10px;
            }
            #greetingLabel {
                font-size: 24px;
                font-weight: bold;
                color: white;
            }
            #dateLabel {
                font-size: 16px;
                color: #B0B0B0;
            }
            #sectionCard {
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            #sectionTitle {
                font-size: 20px;
                font-weight: bold;
                color: #333333;
            }
            #primaryButton, #actionButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 10px;
            }
            #primaryButton:hover, #actionButton:hover {
                background-color: #0056b3;
            }
        """)
    
    def clear_layout(self, layout):
        """Remove todos os widgets de um layout."""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()
    
    def load_data(self):
        """Carrega os dados para exibição no dashboard."""
        try:
            # Carregar informações de nível
            level_info = self.achievement_manager.get_user_level_info()
            self.level_value.setText(str(level_info['level']))
            self.level_progress.setValue(level_info['progress_percent'])
            
            # Carregar recomendações de estudo
            recommendations = self.recommender.get_daily_recommendation()
            self.display_recommendations(recommendations)
            
            # Carregar tópicos em destaque
            trending = self.recommender.get_trending_topics()
            self.display_trending_topics(trending)
            
            # Carregar conquistas recentes
            achievements = self.achievement_manager.get_recent_achievements(3)
            self.display_achievements(achievements)
            
            # Carregar dica aleatória
            self.load_random_tip()
        except Exception as e:
            # Lidar com erros de carregamento
            print(f"Erro ao carregar dados do dashboard: {e}")
    
    def get_user_name(self):
        """Obtém o nome do usuário atual."""
        # Implementar lógica para buscar o nome do usuário
        # Por enquanto, retorna um nome genérico
        return "Estudante"
    
    def display_recommendations(self, recommendations):
        """Exibe as recomendações de estudo."""
        self.clear_layout(self.rec_list)
        
        for rec in recommendations:
            rec_card = QFrame()
            rec_card.setObjectName("recommendationCard")
            card_layout = QVBoxLayout(rec_card)
            
            topic_label = QLabel(f"{rec['topic']}")
            topic_label.setObjectName("recTopicLabel")
            card_layout.addWidget(topic_label)
            
            area_label = QLabel(f"Área: {rec['area']}")
            area_label.setObjectName("recAreaLabel")
            card_layout.addWidget(area_label)
            
            reason_label = QLabel(rec['reason'])
            reason_label.setObjectName("recReasonLabel")
            card_layout.addWidget(reason_label)
            
            priority_label = QLabel(f"Prioridade: {rec.get('priority', 'Normal')}")
            priority_label.setObjectName("recPriorityLabel")
            card_layout.addWidget(priority_label)
            
            # Botão de iniciar estudo
            study_btn = QPushButton("Estudar Agora")
            study_btn.setObjectName("actionButton")
            study_btn.clicked.connect(lambda checked=False, t=rec['topic']: self.start_study_session(t))
            card_layout.addWidget(study_btn, alignment=Qt.AlignRight)
            
            self.rec_list.addWidget(rec_card)
    
    def display_trending_topics(self, topics):
        """Exibe os tópicos em destaque."""
        self.clear_layout(self.trending_list)
        
        for topic in topics:
            topic_card = QFrame()
            topic_card.setObjectName("trendingCard")
            card_layout = QVBoxLayout(topic_card)
            
            topic_label = QLabel(f"{topic['topic']}")
            topic_label.setObjectName("trendingTopicLabel")
            card_layout.addWidget(topic_label)
            
            area_label = QLabel(f"Área: {topic['area']}")
            area_label.setObjectName("trendingAreaLabel")
            card_layout.addWidget(area_label)
            
            reason_label = QLabel(topic['reason'])
            reason_label.setObjectName("trendingReasonLabel")
            card_layout.addWidget(reason_label)
            
            self.trending_list.addWidget(topic_card)
    
    def display_achievements(self, achievements):
        """Exibe as conquistas recentes."""
        self.clear_layout(self.ach_list)
        
        if not achievements:
            no_ach = QLabel("Nenhuma conquista ainda. Continue estudando!")
            no_ach.setObjectName("emptyMessage")
            no_ach.setAlignment(Qt.AlignCenter)
            self.ach_list.addWidget(no_ach)
            return
        
        for ach in achievements:
            ach_card = QFrame()
            ach_card.setObjectName("achievementCard")
            card_layout = QHBoxLayout(ach_card)
            
            # Ícone
            icon_label = QLabel()
            icon_label.setObjectName("achievementIcon")
            icon_label.setFixedSize(32, 32)
            card_layout.addWidget(icon_label)
            
            # Informações
            info_widget = QWidget()
            info_layout = QVBoxLayout(info_widget)
            info_layout.setContentsMargins(0, 0, 0, 0)
            
            name_label = QLabel(ach['name'])
            name_label.setObjectName("achievementName")
            info_layout.addWidget(name_label)
            
            desc_label = QLabel(ach['description'])
            desc_label.setObjectName("achievementDesc")
            info_layout.addWidget(desc_label)
            
            date_label = QLabel(f"Conquistado em: {ach['earned_at'].strftime('%d/%m/%Y')}")
            date_label.setObjectName("achievementDate")
            info_layout.addWidget(date_label)
            
            card_layout.addWidget(info_widget)
            
            self.ach_list.addWidget(ach_card)
    
    def load_random_tip(self):
        """Carrega uma dica aleatória para exibição."""
        tips = [
            "Estudar por períodos curtos e frequentes é mais eficaz que maratonas ocasionais.",
            "Use a técnica Pomodoro para melhorar seu foco: 25 minutos de estudo, 5 de pausa.",
            "Ensinar o que você aprendeu a outra pessoa é uma das melhores formas de fixar o conteúdo.",
            "Intercale assuntos diferentes em vez de focar em apenas um por longos períodos.",
            "Teste a si mesmo frequentemente. Recuperar informações da memória fortalece seu aprendizado.",
            "Estude em ambientes diferentes para evitar associar o conhecimento a apenas um local.",
            "Faça esquemas e resumos com suas próprias palavras para consolidar o aprendizado.",
            "Dormir bem após estudar ajuda o cérebro a consolidar as informações aprendidas.",
            "Relacione novos conceitos com conhecimentos que você já possui.",
            "A prática espaçada é mais eficaz: revise o conteúdo em intervalos crescentes."
        ]
        
        self.tip_content.setText(random.choice(tips))
    
    def start_study_session(self, topic):
        """Inicia uma sessão de estudo para um tópico específico."""
        # Aqui você pode implementar a integração com o timer ou outra funcionalidade
        
        msg = QMessageBox()
        msg.setWindowTitle("Iniciar Estudo")
        msg.setText(f"Iniciando sessão de estudo para: {topic}")
        msg.setInformativeText("O cronômetro foi configurado. Bons estudos!")
        msg.setIcon(QMessageBox.Information)
        msg.exec()
        
        # Configurar o timer para o tema selecionado
        self.timer_widget.reset_timer()
    
    def generate_study_plan(self):
        """Gera e exibe um plano de estudos."""
        plan = self.recommender.generate_study_plan(days=7)
        
        # Criar uma janela para exibir o plano
        plan_dialog = QDialog(self)
        plan_dialog.setWindowTitle("Seu Plano de Estudos")
        plan_dialog.resize(600, 400)
        
        layout = QVBoxLayout(plan_dialog)
        
        title = QLabel("Plano de Estudos para a Próxima Semana")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)
        
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        
        # Adicionar cada dia ao plano
        for date, day_plan in plan.items():
            day_widget = QFrame()
            day_widget.setObjectName("planDayCard")
            day_layout = QVBoxLayout(day_widget)
            
            # Cabeçalho do dia
            header = QLabel(f"Data: {date} - Foco: {day_plan['main_focus']}")
            header.setObjectName("planDayHeader")
            day_layout.addWidget(header)
            
            # Tópicos do dia
            for topic in day_plan['topics']:
                topic_widget = QFrame()
                topic_widget.setObjectName("planTopicCard")
                topic_layout = QHBoxLayout(topic_widget)
                
                # Ícone de dificuldade (baseado na prioridade)
                priority_label = QLabel()
                priority_label.setFixedSize(24, 24)
                topic_layout.addWidget(priority_label)
                
                # Informações do tópico
                info = QVBoxLayout()
                topic_title = QLabel(f"{topic['topic']}")
                topic_title.setObjectName("planTopicTitle")
                info.addWidget(topic_title)
                
                topic_area = QLabel(f"Área: {topic['area']}")
                topic_area.setObjectName("planTopicArea")
                info.addWidget(topic_area)
                
                topic_layout.addLayout(info)
                day_layout.addWidget(topic_widget)
            
            scroll_layout.addWidget(day_widget)
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # Botões
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Save)
        buttons.accepted.connect(plan_dialog.accept)
        buttons.button(QDialogButtonBox.Save).clicked.connect(lambda: self.save_study_plan(plan))
        layout.addWidget(buttons)
        
        plan_dialog.exec()
    
    def save_study_plan(self, plan):
        """Salva o plano de estudos em um arquivo."""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Salvar Plano de Estudos", "", "Arquivos de Texto (*.txt);;Todos os Arquivos (*)"
        )
        
        if not file_path:
            return
            
        try:
            with open(file_path, 'w') as f:
                f.write("PLANO DE ESTUDOS - MATEMÁTICA EM EVIDÊNCIA\n")
                f.write("===========================================\n\n")
                
                for date, day_plan in plan.items():
                    f.write(f"DATA: {date} - FOCO PRINCIPAL: {day_plan['main_focus']}\n")
                    f.write("-" * 50 + "\n")
                    
                    for i, topic in enumerate(day_plan['topics'], 1):
                        f.write(f"{i}. Tópico: {topic['topic']}\n")
                        f.write(f"   Área: {topic['area']}\n")
                        f.write(f"   Motivo: {topic['reason']}\n")
                        f.write(f"   Prioridade: {topic.get('priority', 'Normal')}\n\n")
                    
                    f.write("\n")
            
            QMessageBox.information(
                self, "Plano Salvo", 
                f"Seu plano de estudos foi salvo em:\n{file_path}"
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Erro ao Salvar", 
                f"Ocorreu um erro ao salvar o plano:\n{str(e)}"
            )
    
    def show_all_achievements(self):
        """Mostra todas as conquistas do usuário."""
        # Implementar diálogo com todas as conquistas
        # Aqui você pode criar um diálogo semelhante ao de plano de estudos
        
        all_achievements = self.achievement_manager.get_earned_achievements()
        pending = self.achievement_manager.get_pending_achievements()[:5]  # Mostrar apenas 5 pendentes
        
        ach_dialog = QDialog(self)
        ach_dialog.setWindowTitle("Suas Conquistas")
        ach_dialog.resize(700, 500)
        
        layout = QVBoxLayout(ach_dialog)
        
        title = QLabel("Conquistas e Progresso")
        title.setObjectName("dialogTitle")
        layout.addWidget(title)
        
        # Abas para separar conquistas obtidas e pendentes
        tabs = QTabWidget()
        
        # Aba de conquistas obtidas
        earned_widget = QWidget()
        earned_layout = QVBoxLayout(earned_widget)
        
        if all_achievements:
            earned_scroll = QScrollArea()
            earned_scroll.setWidgetResizable(True)
            earned_content = QWidget()
            earned_content_layout = QVBoxLayout(earned_content)
            
            for ach in all_achievements:
                ach_card = QFrame()
                ach_card.setObjectName("achievementCardLarge")
                card_layout = QHBoxLayout(ach_card)
                
                # Ícone
                icon_label = QLabel()
                icon_label.setObjectName("achievementIconLarge")
                icon_label.setFixedSize(48, 48)
                card_layout.addWidget(icon_label)
                
                # Informações
                info_widget = QWidget()
                info_layout = QVBoxLayout(info_widget)
                info_layout.setContentsMargins(0, 0, 0, 0)
                
                name_label = QLabel(ach['name'])
                name_label.setObjectName("achievementNameLarge")
                info_layout.addWidget(name_label)
                
                desc_label = QLabel(ach['description'])
                desc_label.setObjectName("achievementDescLarge")
                info_layout.addWidget(desc_label)
                
                date_label = QLabel(f"Conquistado em: {ach['earned_at'].strftime('%d/%m/%Y')}")
                date_label.setObjectName("achievementDateLarge")
                info_layout.addWidget(date_label)
                
                card_layout.addWidget(info_widget)
                
                earned_content_layout.addWidget(ach_card)
            
            earned_scroll.setWidget(earned_content)
            earned_layout.addWidget(earned_scroll)
        else:
            no_ach = QLabel("Você ainda não conquistou nenhuma conquista.")
            no_ach.setObjectName("emptyMessage")
            no_ach.setAlignment(Qt.AlignCenter)
            earned_layout.addWidget(no_ach)
        
        # Aba de conquistas pendentes
        pending_widget = QWidget()
        pending_layout = QVBoxLayout(pending_widget)
        
        if pending:
            pending_scroll = QScrollArea()
            pending_scroll.setWidgetResizable(True)
            pending_content = QWidget()
            pending_content_layout = QVBoxLayout(pending_content)
            
            for ach in pending:
                ach_card = QFrame()
                ach_card.setObjectName("pendingAchievementCard")
                card_layout = QHBoxLayout(ach_card)
                
                # Ícone bloqueado
                icon_label = QLabel()
                icon_label.setObjectName("pendingAchievementIcon")
                icon_label.setFixedSize(48, 48)
                card_layout.addWidget(icon_label)
                
                # Informações
                info_widget = QWidget()
                info_layout = QVBoxLayout(info_widget)
                info_layout.setContentsMargins(0, 0, 0, 0)
                
                name_label = QLabel(ach['name'])
                name_label.setObjectName("pendingAchievementName")
                info_layout.addWidget(name_label)
                
                desc_label = QLabel(ach['description'])
                desc_label.setObjectName("pendingAchievementDesc")
                info_layout.addWidget(desc_label)
                
                card_layout.addWidget(info_widget)
                
                pending_content_layout.addWidget(ach_card)
            
            pending_scroll.setWidget(pending_content)
            pending_layout.addWidget(pending_scroll)
        else:
            all_done = QLabel("Você já conquistou todas as conquistas disponíveis!")
            all_done.setObjectName("successMessage")
            all_done.setAlignment(Qt.AlignCenter)
            pending_layout.addWidget(all_done)
        
        tabs.addTab(earned_widget, f"Conquistadas ({len(all_achievements)})")
        tabs.addTab(pending_widget, f"Pendentes ({len(pending)})")
        
        layout.addWidget(tabs)
        
        # Botão de fechar
        close_btn = QPushButton("Fechar")
        close_btn.clicked.connect(ach_dialog.accept)
        layout.addWidget(close_btn)
        
        ach_dialog.exec() 