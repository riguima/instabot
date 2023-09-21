from PySide6 import QtWidgets
from PySide6.QtCore import Slot


class FileDialog(QtWidgets.QFileDialog):
    def __init__(
        self,
        line_edit: QtWidgets.QLineEdit,
        button: QtWidgets.QPushButton,
        parent_widget: QtWidgets.QWidget,
    ) -> None:
        super().__init__(parent_widget)
        self.parent_widget = parent_widget
        self.line_edit = line_edit
        button.clicked.connect(self.set_line_edit_path)

    @Slot()
    def set_line_edit_path(self) -> None:
        self.line_edit.setText(
            str(
                QtWidgets.QFileDialog.getOpenFileNames(
                    self.parent_widget, 'Selecionar'
                )[0]
            )
        )
