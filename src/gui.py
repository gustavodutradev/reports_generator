import sys
import os
from datetime import datetime
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QPushButton,
    QFileDialog, QVBoxLayout, QHBoxLayout, QMessageBox
)

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__))))
from main import main


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Top Investment Group - Gerador de Relatórios de Rentabilidade")
        self.setFixedSize(600, 450)

        # Ícone da janela (barra de título)
        icon_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "../data/topicon.ico")
        )
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        # Estilos gerais
        self.setStyleSheet("""
            QWidget {
                background-color: #193E55;
                color: white;
                font-family: 'Lucida Sans Unicode';
            }
            QLabel {
                color: white;
            }
            QComboBox, QPushButton {
                font-family: 'Lucida Sans Unicode';
            }
            QPushButton {
                background-color: #2A5F7D;
                border: none;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #396B89;
            }
            QComboBox {
                background-color: #2A5F7D;
                padding: 4px;
            }
        """)

        self.template_path = None
        self.destination_path = None
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # Cabeçalho com logo e título
        header = QHBoxLayout()
        header.setSpacing(10)

        # Logo
        logo_lbl = QLabel()
        pixmap = QPixmap(
            os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/topicon.ico"))
        )
        if not pixmap.isNull():
            pixmap = pixmap.scaled(48, 48, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            logo_lbl.setPixmap(pixmap)
        header.addWidget(logo_lbl, alignment=Qt.AlignCenter)

        # Título
        title_lbl = QLabel("Gerador de Relatórios de Rentabilidade")
        title_lbl.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        title_lbl.setStyleSheet("font-size: 24px; font-weight: bold;")
        header.addWidget(title_lbl, stretch=1, alignment=Qt.AlignCenter)

        layout.addLayout(header)

        # Seleção de Mês e Ano
        date_layout = QHBoxLayout()
        date_layout.setSpacing(20)

        date_layout.addWidget(QLabel("Mês de referência:"), alignment=Qt.AlignVCenter)
        self.month_combo = QComboBox()
        for i in range(1, 13):
            self.month_combo.addItem(f"{i:02d}")
        self.month_combo.setCurrentText(f"{datetime.now().month:02d}")
        self.month_combo.setFixedWidth(80)
        date_layout.addWidget(self.month_combo)

        date_layout.addWidget(QLabel("Ano de referência:"), alignment=Qt.AlignVCenter)
        self.year_combo = QComboBox()
        for y in range(2024, datetime.now().year + 3):
            self.year_combo.addItem(str(y))
        self.year_combo.setCurrentText(str(datetime.now().year))
        self.year_combo.setFixedWidth(80)
        date_layout.addWidget(self.year_combo)

        layout.addLayout(date_layout)

        # Botões de seleção de arquivo e pasta
        files_layout = QHBoxLayout()
        files_layout.setSpacing(20)

        self.btn_template = QPushButton("Selecionar Template (.docx)")
        self.btn_template.clicked.connect(self._pick_template)
        files_layout.addWidget(self.btn_template)

        self.btn_destination = QPushButton("Selecionar Pasta de Destino")
        self.btn_destination.clicked.connect(self._pick_destination)
        files_layout.addWidget(self.btn_destination)

        layout.addLayout(files_layout)

        # Botão Iniciar Processo
        self.btn_start = QPushButton("Iniciar Processo")
        self.btn_start.setFixedHeight(40)
        self.btn_start.setStyleSheet("font-size: 16px;")
        self.btn_start.clicked.connect(self._on_start)
        layout.addWidget(self.btn_start, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def _pick_template(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Selecione o template", "", "Word Documents (*.docx)"
        )
        if path:
            self.template_path = path
            self.btn_template.setText(f"Template: {os.path.basename(path)}")

    def _pick_destination(self):
        path = QFileDialog.getExistingDirectory(
            self, "Selecione a pasta de destino", ""
        )
        if path:
            self.destination_path = path
            self.btn_destination.setText(f"Pasta: {os.path.basename(path)}")

    def _on_start(self):
        mes = self.month_combo.currentText()
        ano = self.year_combo.currentText()
        tpl = self.template_path
        dst = self.destination_path

        if not mes or not ano:
            self._show_message("Selecione mês e ano de referência.", error=True)
            return
        if not tpl:
            self._show_message("Selecione o template (.docx).", error=True)
            return
        if not dst:
            self._show_message("Selecione a pasta de destino.", error=True)
            return

        self._show_message("Gerando relatórios...", info=True)
        try:
            success = main(dst, tpl, ano, mes)
            if success:
                self._show_message("Relatórios gerados com sucesso!", info=False)
            else:
                self._show_message("Não há dados disponíveis para o mês solicitado.", error=True)
        except Exception as e:
            self._show_message(f"Erro inesperado: {e}", error=True)

    def _show_message(self, text: str, error: bool = False, info: bool = False):
        if error:
            QMessageBox.critical(self, "Erro", text)
        elif info:
            QMessageBox.information(self, "Info", text)
        else:
            QMessageBox.information(self, "Sucesso", text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
