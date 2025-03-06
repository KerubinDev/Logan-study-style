from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *

class MethodWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.checkboxes_by_subject = {}

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Cabeçalho
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(10)
        
        title = QLabel("Método Logan de Estudos")
        title.setObjectName("pageTitle")
        
        desc = QLabel(
            "Este método organiza seus estudos baseado no nível de "
            "dificuldade de cada matéria, criando um ciclo personalizado."
        )
        desc.setWordWrap(True)
        desc.setObjectName("pageDescription")
        
        header_layout.addWidget(title)
        header_layout.addWidget(desc)
        main_layout.addWidget(header)

        # Seção de Matérias
        subjects_section = QFrame()
        subjects_section.setObjectName("sectionCard")
        subjects_layout = QVBoxLayout(subjects_section)
        
        # Tabela de matérias
        self.subjects_list = QTableWidget()
        self.subjects_list.setColumnCount(4)
        self.subjects_list.setHorizontalHeaderLabels([
            "Matéria", "Dificuldade", "Peso (x)", "Horas/Semana"
        ])
        self.subjects_list.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.subjects_list.setObjectName("subjectsTable")
        subjects_layout.addWidget(self.subjects_list)
        
        # Botões de ação
        buttons = QWidget()
        buttons_layout = QHBoxLayout(buttons)
        buttons_layout.setSpacing(10)
        
        add_btn = QPushButton("+ Adicionar Matéria")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_subject)
        
        calc_btn = QPushButton("⚡ Calcular Horas")
        calc_btn.setObjectName("primaryButton")
        calc_btn.clicked.connect(self.calculate_hours)
        
        buttons_layout.addWidget(add_btn)
        buttons_layout.addWidget(calc_btn)
        subjects_layout.addWidget(buttons)
        
        main_layout.addWidget(subjects_section)

        # Seção do Ciclo de Estudos
        study_section = QFrame()
        study_section.setObjectName("sectionCard")
        study_layout = QVBoxLayout(study_section)
        
        cycle_header = QWidget()
        cycle_header_layout = QHBoxLayout(cycle_header)
        
        cycle_title = QLabel("Ciclo de Estudos")
        cycle_title.setObjectName("sectionTitle")
        cycle_header_layout.addWidget(cycle_title)
        
        self.finish_button = QPushButton("✨ Finalizar Ciclo")
        self.finish_button.setObjectName("accentButton")
        self.finish_button.clicked.connect(self.handle_finish)
        self.finish_button.hide()
        cycle_header_layout.addWidget(self.finish_button)
        
        study_layout.addWidget(cycle_header)
        
        # Container para os cards de matéria
        self.study_container = QWidget()
        self.study_layout = QVBoxLayout(self.study_container)
        self.study_layout.setSpacing(15)
        self.study_layout.setContentsMargins(0, 0, 0, 0)
        study_layout.addWidget(self.study_container)
        
        main_layout.addWidget(study_section)

        # Seção de Instruções
        help_section = QFrame()
        help_section.setObjectName("helpCard")
        help_layout = QVBoxLayout(help_section)
        
        help_title = QLabel("Como Funciona")
        help_title.setObjectName("sectionTitle")
        help_layout.addWidget(help_title)
        
        steps = [
            "1. Adicione suas matérias e classifique-as:",
            "   • Péssimo: 5x (matéria muito difícil)",
            "   • Ruim: 4x (matéria difícil)",
            "   • Mais ou menos: 3x (dificuldade média)",
            "   • Bom: 2x (matéria fácil)",
            "   • Ótimo: 1x (matéria muito fácil)",
            "",
            "2. Defina suas horas de estudo semanais",
            "3. O sistema calculará as horas por matéria baseado na dificuldade",
            "4. Cada quadrado representa 1 hora de estudo",
            "5. Marque os quadrados conforme completa as horas",
            "6. Só passe para a próxima matéria após completar todos os quadrados",
            "7. Quando completar todas as matérias, reinicie o ciclo"
        ]
        
        help_text = QLabel("\n".join(steps))
        help_text.setWordWrap(True)
        help_text.setObjectName("helpText")
        help_layout.addWidget(help_text)
        
        main_layout.addWidget(help_section)

    def add_subject(self):
        dialog = SubjectDialog(self)
        if dialog.exec():
            row = self.subjects_list.rowCount()
            self.subjects_list.insertRow(row)
            
            # Matéria
            self.subjects_list.setItem(row, 0, QTableWidgetItem(dialog.subject))
            
            # Dificuldade
            self.subjects_list.setItem(row, 1, QTableWidgetItem(dialog.difficulty))
            
            # Peso
            weights = {
                "Péssimo": "5",
                "Ruim": "4",
                "Mais ou menos": "3",
                "Bom": "2",
                "Ótimo": "1"
            }
            self.subjects_list.setItem(row, 2, QTableWidgetItem(weights[dialog.difficulty]))
            
            # Horas (inicialmente 0)
            self.subjects_list.setItem(row, 3, QTableWidgetItem("0"))

    def calculate_hours(self):
        dialog = HoursDialog(self)
        if dialog.exec():
            total_hours = dialog.hours_per_week
            total_x = 0
            
            for row in range(self.subjects_list.rowCount()):
                weight = int(self.subjects_list.item(row, 2).text())
                total_x += weight
            
            hours_per_x = total_hours / total_x if total_x > 0 else 0
            
            self.clear_study_grid()
            self.checkboxes_by_subject = {}
            
            for row in range(self.subjects_list.rowCount()):
                subject = self.subjects_list.item(row, 0).text()
                weight = int(self.subjects_list.item(row, 2).text())
                hours = max(2, round(weight * hours_per_x))
                
                self.subjects_list.setItem(row, 3, QTableWidgetItem(str(hours)))
                
                # Card da matéria
                subject_card = QFrame()
                subject_card.setObjectName("subjectCard")
                card_layout = QVBoxLayout(subject_card)
                
                # Cabeçalho do card
                header = QWidget()
                header_layout = QHBoxLayout(header)
                header_layout.setContentsMargins(0, 0, 0, 0)
                
                title = QLabel(subject)
                title.setObjectName("cardTitle")
                header_layout.addWidget(title)
                
                hours_label = QLabel(f"{hours}h")
                hours_label.setObjectName("hoursLabel")
                header_layout.addWidget(hours_label)
                
                card_layout.addWidget(header)
                
                # Grid de checkboxes
                checkboxes = QWidget()
                checkboxes_layout = QHBoxLayout(checkboxes)
                checkboxes_layout.setSpacing(10)
                checkboxes_layout.setAlignment(Qt.AlignLeft)
                
                subject_checkboxes = []
                
                for i in range(hours):
                    hour_widget = QWidget()
                    hour_layout = QVBoxLayout(hour_widget)
                    hour_layout.setSpacing(5)
                    
                    checkbox = QCheckBox()
                    checkbox.setObjectName("studyBox")
                    checkbox.stateChanged.connect(self.check_completion)
                    
                    hour_label = QLabel(f"{i+1}")
                    hour_label.setObjectName("hourLabel")
                    hour_label.setAlignment(Qt.AlignCenter)
                    
                    hour_layout.addWidget(checkbox, alignment=Qt.AlignCenter)
                    hour_layout.addWidget(hour_label)
                    
                    checkboxes_layout.addWidget(hour_widget)
                    subject_checkboxes.append(checkbox)
                
                card_layout.addWidget(checkboxes)
                self.study_layout.addWidget(subject_card)
                self.checkboxes_by_subject[subject] = subject_checkboxes
            
            self.finish_button.hide()

    def check_completion(self):
        """Verifica se todas as horas foram completadas."""
        all_completed = True
        
        for subject, checkboxes in self.checkboxes_by_subject.items():
            subject_completed = all(cb.isChecked() for cb in checkboxes)
            if not subject_completed:
                all_completed = False
                break
        
        self.finish_button.setVisible(all_completed)

    def handle_finish(self):
        """Processa a finalização do ciclo de estudos."""
        msg = QMessageBox()
        msg.setWindowTitle("Parabéns! 🎉")
        msg.setIcon(QMessageBox.Information)
        msg.setText("Você completou seu ciclo de estudos!")
        msg.setInformativeText(
            "Incrível trabalho! Você manteve a disciplina e completou "
            "todas as horas de estudo planejadas.\n\n"
            "Que tal começar um novo ciclo para continuar evoluindo?"
        )
        
        # Adicionar botões personalizados
        restart_button = msg.addButton("Iniciar Novo Ciclo", QMessageBox.AcceptRole)
        close_button = msg.addButton("Fechar", QMessageBox.RejectRole)
        
        msg.exec()
        
        if msg.clickedButton() == restart_button:
            self.reset_cycle()

    def reset_cycle(self):
        """Reinicia o ciclo de estudos."""
        # Limpar todos os checkboxes
        for checkboxes in self.checkboxes_by_subject.values():
            for checkbox in checkboxes:
                checkbox.setChecked(False)
        
        self.finish_button.hide()

    def clear_study_grid(self):
        """Limpa todos os widgets do layout de estudo."""
        while self.study_layout.count():
            item = self.study_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

class SubjectDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Adicionar Matéria")
        layout = QVBoxLayout(self)
        
        # Campo de matéria
        self.subject_input = QLineEdit()
        self.subject_input.setPlaceholderText("Nome da matéria")
        layout.addWidget(self.subject_input)
        
        # Seleção de dificuldade
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(["Péssimo", "Ruim", "Mais ou menos", "Bom", "Ótimo"])
        layout.addWidget(self.difficulty_combo)
        
        # Botões
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def accept(self):
        self.subject = self.subject_input.text()
        self.difficulty = self.difficulty_combo.currentText()
        super().accept()

class HoursDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        self.setWindowTitle("Definir Horas de Estudo")
        layout = QVBoxLayout(self)
        
        form_layout = QFormLayout()
        
        self.hours_per_day = QSpinBox()
        self.hours_per_day.setRange(1, 24)
        form_layout.addRow("Horas por dia:", self.hours_per_day)
        
        self.days_per_week = QSpinBox()
        self.days_per_week.setRange(1, 7)
        form_layout.addRow("Dias por semana:", self.days_per_week)
        
        layout.addLayout(form_layout)
        
        buttons = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def accept(self):
        self.hours_per_week = self.hours_per_day.value() * self.days_per_week.value()
        super().accept()

class QFlowLayout(QLayout):
    """Layout que organiza widgets em linhas, quebrando quando necessário."""
    
    def __init__(self, parent=None, margin=0, spacing=-1):
        super().__init__(parent)
        self.itemList = []
        self.m_hSpace = spacing
        self.m_vSpace = spacing
        self.setContentsMargins(margin, margin, margin, margin)

    def addItem(self, item):
        self.itemList.append(item)

    def horizontalSpacing(self):
        if self.m_hSpace >= 0:
            return self.m_hSpace
        else:
            return self.smartSpacing(QStyle.PM_LayoutHorizontalSpacing)

    def verticalSpacing(self):
        if self.m_vSpace >= 0:
            return self.m_vSpace
        else:
            return self.smartSpacing(QStyle.PM_LayoutVerticalSpacing)

    def count(self):
        return len(self.itemList)

    def itemAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList[index]
        return None

    def takeAt(self, index):
        if 0 <= index < len(self.itemList):
            return self.itemList.pop(index)
        return None

    def expandingDirections(self):
        return Qt.Orientations(0)

    def hasHeightForWidth(self):
        return True

    def heightForWidth(self, width):
        return self.doLayout(QRect(0, 0, width, 0), True)

    def setGeometry(self, rect):
        super().setGeometry(rect)
        self.doLayout(rect, False)

    def sizeHint(self):
        return self.minimumSize()

    def minimumSize(self):
        size = QSize()
        for item in self.itemList:
            size = size.expandedTo(item.minimumSize())
        size += QSize(2 * self.contentsMargins().top(), 2 * self.contentsMargins().top())
        return size

    def doLayout(self, rect, testOnly):
        left, top, right, bottom = self.getContentsMargins()
        effectiveRect = rect.adjusted(+left, +top, -right, -bottom)
        x = effectiveRect.x()
        y = effectiveRect.y()
        lineHeight = 0

        for item in self.itemList:
            widget = item.widget()
            spaceX = self.horizontalSpacing()
            if spaceX == -1:
                spaceX = widget.style().layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Horizontal)
            spaceY = self.verticalSpacing()
            if spaceY == -1:
                spaceY = widget.style().layoutSpacing(
                    QSizePolicy.PushButton, QSizePolicy.PushButton, Qt.Vertical)

            nextX = x + item.sizeHint().width() + spaceX
            if nextX - spaceX > effectiveRect.right() and lineHeight > 0:
                x = effectiveRect.x()
                y = y + lineHeight + spaceY
                nextX = x + item.sizeHint().width() + spaceX
                lineHeight = 0

            if not testOnly:
                item.setGeometry(QRect(QPoint(x, y), item.sizeHint()))

            x = nextX
            lineHeight = max(lineHeight, item.sizeHint().height())

        return y + lineHeight - rect.y() + bottom

    def smartSpacing(self, pm):
        parent = self.parent()
        if parent is None:
            return -1
        elif parent.isWidgetType():
            return parent.style().pixelMetric(pm, None, parent)
        else:
            return parent.spacing() 