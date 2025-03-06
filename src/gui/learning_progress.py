from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *
import json
import os
from src.database.database import get_data_dir

class LearningProgressWidget(QWidget):
    """Widget para acompanhamento do progresso de aprendizagem."""
    
    def __init__(self, user_id=None, parent=None):
        super().__init__(parent)
        self.user_id = user_id
        self.topics = self.load_topics()
        self.setup_ui()
    
    def setup_ui(self):
        """Configura a interface do widget."""
        main_layout = QVBoxLayout(self)
        
        # Cabeçalho
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        title = QLabel("Progresso de Aprendizagem")
        title.setObjectName("pageTitle")
        header_layout.addWidget(title)
        
        add_btn = QPushButton("Adicionar Tópico")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_topic)
        header_layout.addWidget(add_btn, alignment=Qt.AlignRight)
        
        main_layout.addWidget(header)
        
        # Área de conteúdo com scroll
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        
        content_widget = QWidget()
        self.content_layout = QVBoxLayout(content_widget)
        self.content_layout.setSpacing(15)
        
        # Mensagem para quando não há tópicos
        self.empty_message = QLabel("Você ainda não adicionou nenhum tópico de aprendizagem.")
        self.empty_message.setObjectName("emptyMessage")
        self.empty_message.setAlignment(Qt.AlignCenter)
        self.content_layout.addWidget(self.empty_message)
        
        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)
        
        # Carregar tópicos
        self.load_topic_widgets()
        
        # Estilizando os cartões de tópicos
        self.setStyleSheet("""
            #topicCard {
                background-color: #FFFFFF;
                border-radius: 10px;
                padding: 15px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
            #pageTitle {
                font-size: 24px;
                font-weight: bold;
                color: #333333;
            }
            #cardTitle {
                font-size: 20px;
                font-weight: bold;
                color: #007BFF;
            }
            #cardDescription {
                font-size: 14px;
                color: #666666;
            }
            #smallButton {
                background-color: #007BFF;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 5px;
            }
            #smallButton:hover {
                background-color: #0056b3;
            }
            #linkButton {
                background-color: transparent;
                color: #007BFF;
                border: none;
                text-decoration: underline;
            }
            #linkButton:hover {
                color: #0056b3;
            }
        """)
    
    def load_topics(self):
        """Carrega os tópicos de aprendizagem do usuário."""
        try:
            # Diretório para dados do usuário
            user_dir = os.path.join(get_data_dir(), f"user_{self.user_id}")
            os.makedirs(user_dir, exist_ok=True)
            
            # Arquivo de tópicos
            topics_file = os.path.join(user_dir, "learning_topics.json")
            
            if os.path.exists(topics_file):
                with open(topics_file, 'r') as f:
                    return json.load(f)
            
            # Criar arquivo com tópicos padrão se não existir
            default_topics = [
                {
                    "id": 1,
                    "title": "Matemática - Álgebra Linear",
                    "description": "Estudo de matrizes, vetores e transformações lineares.",
                    "progress": 0,
                    "subtopics": [
                        {"id": 1, "title": "Sistemas Lineares", "completed": False},
                        {"id": 2, "title": "Matrizes", "completed": False},
                        {"id": 3, "title": "Determinantes", "completed": False},
                        {"id": 4, "title": "Espaços Vetoriais", "completed": False},
                        {"id": 5, "title": "Transformações Lineares", "completed": False}
                    ]
                }
            ]
            
            with open(topics_file, 'w') as f:
                json.dump(default_topics, f, indent=4)
            
            return default_topics
            
        except Exception as e:
            print(f"Erro ao carregar tópicos: {e}")
            return []
    
    def save_topics(self):
        """Salva os tópicos de aprendizagem do usuário."""
        try:
            user_dir = os.path.join(get_data_dir(), f"user_{self.user_id}")
            os.makedirs(user_dir, exist_ok=True)
            
            topics_file = os.path.join(user_dir, "learning_topics.json")
            
            with open(topics_file, 'w') as f:
                json.dump(self.topics, f, indent=4)
                
        except Exception as e:
            print(f"Erro ao salvar tópicos: {e}")
    
    def load_topic_widgets(self):
        """Carrega os widgets de tópicos."""
        # Limpar layout
        for i in reversed(range(self.content_layout.count())):
            widget = self.content_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
        
        # Mostrar mensagem se não houver tópicos
        if not self.topics:
            self.empty_message = QLabel("Você ainda não adicionou nenhum tópico de aprendizagem.")
            self.empty_message.setObjectName("emptyMessage")
            self.empty_message.setAlignment(Qt.AlignCenter)
            self.content_layout.addWidget(self.empty_message)
            return
        
        # Adicionar cada tópico
        for topic in self.topics:
            self.create_topic_widget(topic)
    
    def create_topic_widget(self, topic):
        """Cria um widget para um tópico específico."""
        topic_frame = QFrame()
        topic_frame.setObjectName("topicCard")
        topic_layout = QVBoxLayout(topic_frame)
        
        # Cabeçalho do tópico
        header = QWidget()
        header_layout = QHBoxLayout(header)
        
        title = QLabel(topic["title"])
        title.setObjectName("cardTitle")
        header_layout.addWidget(title)
        
        # Botões de ação
        edit_btn = QPushButton("Editar")
        edit_btn.setObjectName("smallButton")
        edit_btn.clicked.connect(lambda: self.edit_topic(topic))
        header_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Excluir")
        delete_btn.setObjectName("smallButton")
        delete_btn.clicked.connect(lambda: self.delete_topic(topic))
        header_layout.addWidget(delete_btn)
        
        topic_layout.addWidget(header)
        
        # Descrição
        if topic.get("description"):
            desc = QLabel(topic["description"])
            desc.setWordWrap(True)
            desc.setObjectName("cardDescription")
            topic_layout.addWidget(desc)
        
        # Barra de progresso
        progress_layout = QHBoxLayout()
        
        progress_bar = QProgressBar()
        progress_bar.setRange(0, 100)
        progress_bar.setValue(topic["progress"])
        progress_bar.setFormat("%p% concluído")
        progress_bar.setObjectName("topicProgress")
        progress_layout.addWidget(progress_bar)
        
        progress_label = QLabel(f"{topic['progress']}%")
        progress_label.setObjectName("progressValue")
        progress_layout.addWidget(progress_label)
        
        topic_layout.addLayout(progress_layout)
        
        # Subtópicos
        if topic.get("subtopics"):
            subtopics_widget = QWidget()
            subtopics_layout = QVBoxLayout(subtopics_widget)
            subtopics_layout.setSpacing(5)
            
            subtopics_label = QLabel("Subtópicos:")
            subtopics_label.setObjectName("subtopicsTitle")
            subtopics_layout.addWidget(subtopics_label)
            
            for subtopic in topic["subtopics"]:
                checkbox = QCheckBox(subtopic["title"])
                checkbox.setChecked(subtopic["completed"])
                checkbox.stateChanged.connect(
                    lambda state, t=topic, s=subtopic: self.toggle_subtopic(t, s, state)
                )
                subtopics_layout.addWidget(checkbox)
            
            topic_layout.addWidget(subtopics_widget)
        
        # Botão para adicionar subtópico
        add_subtopic_btn = QPushButton("+ Adicionar Subtópico")
        add_subtopic_btn.setObjectName("linkButton")
        add_subtopic_btn.clicked.connect(lambda: self.add_subtopic(topic))
        topic_layout.addWidget(add_subtopic_btn)
        
        self.content_layout.addWidget(topic_frame)
    
    def add_topic(self):
        """Adiciona um novo tópico de aprendizagem."""
        dialog = TopicDialog(self)
        
        if dialog.exec():
            next_id = 1
            if self.topics:
                next_id = max(topic["id"] for topic in self.topics) + 1
            
            new_topic = {
                "id": next_id,
                "title": dialog.title_input.text(),
                "description": dialog.description_input.toPlainText(),
                "progress": 0,
                "subtopics": []
            }
            
            self.topics.append(new_topic)
            self.save_topics()
            self.load_topic_widgets()
    
    def edit_topic(self, topic):
        """Edita um tópico existente."""
        dialog = TopicDialog(self, topic)
        
        if dialog.exec():
            topic["title"] = dialog.title_input.text()
            topic["description"] = dialog.description_input.toPlainText()
            
            self.save_topics()
            self.load_topic_widgets()
    
    def delete_topic(self, topic):
        """Exclui um tópico."""
        confirm = QMessageBox.question(
            self,
            "Confirmar Exclusão",
            f"Tem certeza que deseja excluir o tópico '{topic['title']}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if confirm == QMessageBox.Yes:
            self.topics.remove(topic)
            self.save_topics()
            self.load_topic_widgets()
    
    def add_subtopic(self, topic):
        """Adiciona um subtópico a um tópico existente."""
        text, ok = QInputDialog.getText(
            self, "Adicionar Subtópico", 
            "Nome do subtópico:"
        )
        
        if ok and text:
            next_id = 1
            if topic.get("subtopics"):
                next_id = max(subtopic["id"] for subtopic in topic["subtopics"]) + 1
            
            new_subtopic = {
                "id": next_id,
                "title": text,
                "completed": False
            }
            
            if "subtopics" not in topic:
                topic["subtopics"] = []
                
            topic["subtopics"].append(new_subtopic)
            self.save_topics()
            self.load_topic_widgets()
    
    def toggle_subtopic(self, topic, subtopic, state):
        """Altera o estado de conclusão de um subtópico."""
        for st in topic["subtopics"]:
            if st["id"] == subtopic["id"]:
                st["completed"] = bool(state)
                break
        
        # Atualizar progresso do tópico
        total = len(topic["subtopics"])
        completed = len([st for st in topic["subtopics"] if st["completed"]])
        topic["progress"] = int((completed / total) * 100) if total > 0 else 0
        
        self.save_topics()
        self.load_topic_widgets()

class TopicDialog(QDialog):
    """Diálogo para adicionar ou editar tópicos."""
    
    def __init__(self, parent=None, topic=None):
        super().__init__(parent)
        self.topic = topic
        self.setup_ui()
        
        if topic:
            self.setWindowTitle("Editar Tópico")
            self.title_input.setText(topic["title"])
            self.description_input.setPlainText(topic.get("description", ""))
        else:
            self.setWindowTitle("Novo Tópico")
    
    def setup_ui(self):
        """Configura a interface do diálogo."""
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel("Título:")
        self.title_input = QLineEdit()
        layout.addWidget(title_label)
        layout.addWidget(self.title_input)
        
        # Descrição
        description_label = QLabel("Descrição:")
        self.description_input = QTextEdit()
        layout.addWidget(description_label)
        layout.addWidget(self.description_input)
        
        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons) 