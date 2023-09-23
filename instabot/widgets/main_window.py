from instagrapi import Client
from instagrapi.exceptions import BadPassword
from PySide6 import QtWidgets
from PySide6.QtCore import Slot

from instabot.browser import Browser
from instabot.widgets.utils import FileDialog


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setFixedSize(800, 400)

        self.browser = Browser()
        self.message_box = QtWidgets.QMessageBox()

        self.login_label = QtWidgets.QLabel('Login')
        self.login_line_edit = QtWidgets.QLineEdit()

        self.password_label = QtWidgets.QLabel('Senha')
        self.password_line_edit = QtWidgets.QLineEdit()
        self.password_line_edit.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Password
        )

        self.mentions_label = QtWidgets.QLabel('Menções')
        self.mentions_line_edit = QtWidgets.QLineEdit()

        self.links_label = QtWidgets.QLabel('Links')
        self.links_line_edit = QtWidgets.QLineEdit()

        self.file_dialog_label = QtWidgets.QLabel('Imagens/Videos')
        self.file_dialog_line_edit = QtWidgets.QLineEdit()
        self.file_dialog_button = QtWidgets.QPushButton('Selecionar')
        self.file_dialog = FileDialog(
            self.file_dialog_line_edit,
            self.file_dialog_button,
            self,
        )
        self.file_dialog_layout = QtWidgets.QHBoxLayout()
        self.file_dialog_layout.addWidget(self.file_dialog_line_edit)
        self.file_dialog_layout.addWidget(self.file_dialog_button)

        self.run_button = QtWidgets.QPushButton('Rodar')
        self.run_button.clicked.connect(self.run)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addWidget(self.login_label)
        self.main_layout.addWidget(self.login_line_edit)
        self.main_layout.addWidget(self.password_label)
        self.main_layout.addWidget(self.password_line_edit)
        self.main_layout.addWidget(self.mentions_label)
        self.main_layout.addWidget(self.mentions_line_edit)
        self.main_layout.addWidget(self.links_label)
        self.main_layout.addWidget(self.links_line_edit)
        self.main_layout.addWidget(self.file_dialog_label)
        self.main_layout.addLayout(self.file_dialog_layout)
        self.main_layout.addWidget(self.run_button)

    @Slot()
    def run(self) -> None:
        try:
            client = Client()
            client.login(
                self.login_line_edit.text(), self.password_line_edit.text()
            )
            for file_path in [
                p for p in self.file_dialog_line_edit.text().split(';') if p
            ]:
                self.browser.post_story(
                    client,
                    file_path,
                    mentions=self.mentions_line_edit.text()
                    .replace('@', '')
                    .split(),
                    links=self.links_line_edit.text().split(),
                )
            self.message_box.setText('Finalizado')
            self.message_box.show()
        except BadPassword:
            self.message_box.setText('Login inválido')
            self.message_box.show()
