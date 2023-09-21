from pathlib import Path

from PySide6.QtCore import Slot
from PySide6 import QtWidgets
import toml

from instabot.widgets.utils import FileDialog
from instabot.browser import Browser


secrets = toml.load(open('.secrets.toml')) if Path('.secrets.toml').exists() else {}


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setStyleSheet('font-size: 20px;')
        self.setFixedSize(800, 200)

        self.browser = None
        self.message_box = QtWidgets.QMessageBox()

        self.mentions_label = QtWidgets.QLabel('Menções')
        self.mentions_line_edit = QtWidgets.QLineEdit()

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

        self.run_layout = QtWidgets.QVBoxLayout()
        self.run_layout.addWidget(self.mentions_label)
        self.run_layout.addWidget(self.mentions_line_edit)
        self.run_layout.addWidget(self.file_dialog_label)
        self.run_layout.addLayout(self.file_dialog_layout)
        self.run_layout.addWidget(self.run_button)

        self.login_label = QtWidgets.QLabel('Login')
        self.login_line_edit = QtWidgets.QLineEdit()

        self.password_label = QtWidgets.QLabel('Senha')
        self.password_line_edit = QtWidgets.QLineEdit()
        self.password_line_edit.setEchoMode(QtWidgets.QLineEdit.EchoMode.Password)

        self.login_button = QtWidgets.QPushButton('Fazer login')
        self.login_button.clicked.connect(self.make_login)

        self.login_layout = QtWidgets.QVBoxLayout()
        self.login_layout.addWidget(self.login_label)
        self.login_layout.addWidget(self.login_line_edit)
        self.login_layout.addWidget(self.password_label)
        self.login_layout.addWidget(self.password_line_edit)
        self.login_layout.addWidget(self.login_button)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.addLayout(self.run_layout)
        self.main_layout.addLayout(self.login_layout)

    @Slot()
    def run(self) -> None:
        if secrets.get('login') is None:
            self.message_box.setText('Primeiro faça o login')
            self.message_box.show()
        else:
            if self.browser is None:
                self.browser = Browser(secrets['login'] + '_user_data')
            if not self.browser.is_logged():
                self.browser.make_login(secrets['login'], secrets['password'])
            self.browser.driver.get('chrome-extension://bcocdbombenodlegijagbhdjbifpiijp/inssist.html')
            self.message_box.setText('Aperte Ok quando a página carregar')
            self.message_box.exec()
            for file_path in list(self.file_dialog_line_edit.text()):
                self.browser.post_story(
                    file_path,
                    self.mentions_line_edit.text().replace('@', '').split()
                )

    @Slot()
    def make_login(self) -> None:
        self.browser = Browser(self.login_line_edit.text() + '_user_data')
        if not self.browser.is_logged():
            self.browser.make_login(
                self.login_line_edit.text(),
                self.password_line_edit.text(),
            )
        if self.browser.is_logged():
            self.message_box.setText('Login realizado com sucesso')
            secrets['login'] = self.login_line_edit.text()
            secrets['password'] = self.password_line_edit.text()
            toml.dump(secrets, open('.secrets.toml', 'w'))
        else:
            self.message_box.setText('Login inválido')
        self.message_box.show()
