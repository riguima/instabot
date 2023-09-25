from instagrapi import Client
from instagrapi.exceptions import BadPassword, ProxyAddressIsBlocked
from PySide6 import QtWidgets
from PySide6.QtCore import Slot
from sqlalchemy import select

from instabot.browser import Browser
from instabot.database import Session
from instabot.models import Account
from instabot.widgets.utils import FileDialog


class MainWindow(QtWidgets.QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setFixedSize(800, 400)
        with open('styles.qss', 'r') as f:
            self.setStyleSheet(f.read())

        self.browser = Browser()
        self.message_box = QtWidgets.QMessageBox()

        self.account_label = QtWidgets.QLabel('Conta')
        self.account_combobox = QtWidgets.QComboBox()
        self.update_account_combobox()

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

        self.remove_account_button = QtWidgets.QPushButton('Remover conta')
        self.remove_account_button.clicked.connect(self.remove_account)

        self.run_buttons_layout = QtWidgets.QHBoxLayout()
        self.run_buttons_layout.addWidget(self.run_button)
        self.run_buttons_layout.addWidget(self.remove_account_button)

        self.run_layout = QtWidgets.QVBoxLayout()
        self.run_layout.addWidget(self.account_label)
        self.run_layout.addWidget(self.account_combobox)
        self.run_layout.addWidget(self.mentions_label)
        self.run_layout.addWidget(self.mentions_line_edit)
        self.run_layout.addWidget(self.links_label)
        self.run_layout.addWidget(self.links_line_edit)
        self.run_layout.addWidget(self.file_dialog_label)
        self.run_layout.addLayout(self.file_dialog_layout)
        self.run_layout.addLayout(self.run_buttons_layout)

        self.login_label = QtWidgets.QLabel('Login')
        self.login_line_edit = QtWidgets.QLineEdit()

        self.password_label = QtWidgets.QLabel('Senha')
        self.password_line_edit = QtWidgets.QLineEdit()
        self.password_line_edit.setEchoMode(
            QtWidgets.QLineEdit.EchoMode.Password
        )

        self.add_account_button = QtWidgets.QPushButton('Adicionar conta')
        self.add_account_button.clicked.connect(self.add_account)

        self.account_layout = QtWidgets.QVBoxLayout()
        self.account_layout.addWidget(self.login_label)
        self.account_layout.addWidget(self.login_line_edit)
        self.account_layout.addWidget(self.password_label)
        self.account_layout.addWidget(self.password_line_edit)
        self.account_layout.addWidget(self.add_account_button)
        self.account_layout.addStretch()

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.addLayout(self.run_layout)
        self.main_layout.addLayout(self.account_layout)

    @Slot()
    def run(self) -> None:
        with Session() as session:
            query = select(Account).where(
                Account.login == self.account_combobox.currentText()
            )
            account = session.scalars(query).first()
            client = Client()
            client.login(account.login, account.password)
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

    @Slot()
    def add_account(self) -> None:
        try:
            client = Client()
            client.login(
                self.login_line_edit.text(), self.password_line_edit.text()
            )
            with Session() as session:
                account = Account(
                    login=self.login_line_edit.text(),
                    password=self.password_line_edit.text(),
                )
                session.add(account)
                session.commit()
            self.message_box.setText('Conta adicionada')
            self.message_box.show()
            self.update_account_combobox()
        except (BadPassword, ProxyAddressIsBlocked):
            self.message_box.setText('Login inválido')
            self.message_box.show()
        self.login_line_edit.setText('')
        self.password_line_edit.setText('')

    @Slot()
    def remove_account(self) -> None:
        with Session() as session:
            query = select(Account).where(
                Account.login == self.account_combobox.currentText()
            )
            account = session.scalars(query).first()
            session.delete(account)
            session.commit()
            self.message_box.setText('Conta removida')
            self.message_box.show()
            self.update_account_combobox()

    def update_account_combobox(self) -> None:
        with Session() as session:
            self.account_combobox.clear()
            for account in session.scalars(select(Account)).all():
                self.account_combobox.addItem(account.login)
