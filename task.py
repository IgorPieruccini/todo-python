from PySide6 import QtWidgets, QtGui


class Task(QtWidgets.QWidget):
    def __init__(self, task_id, main):
        super().__init__()
        self.main = main
        self.id = task_id

        # create layouts
        self.layout = QtWidgets.QVBoxLayout(self)
        self.actionLayout = QtWidgets.QHBoxLayout()

        # font
        self.font = QtGui.QFont()
        self.font.setItalic(main.tasks_data[task_id]["is_complete"])
        self.font.setStrikeOut(main.tasks_data[task_id]["is_complete"])

        # description text
        self.descriptionText = QtWidgets.QTextEdit(main.tasks_data[task_id]["description"])
        self.descriptionText.setFont(self.font)
        self.descriptionText.textChanged.connect(
            lambda: main.update_task_description(task_id, self.descriptionText.toPlainText()))
        self.layout.addWidget(self.descriptionText)

        # complete toggle
        self.completeToggle = QtWidgets.QRadioButton("is done")
        self.completeToggle.setChecked(main.tasks_data[task_id]["is_complete"])
        self.completeToggle.toggled.connect(self.toggle_is_complete)
        self.actionLayout.addWidget(self.completeToggle)

        # delete button
        self.deleteButton = QtWidgets.QPushButton("Delete")
        self.deleteButton.clicked.connect(lambda: main.delete_task(self.id))
        self.actionLayout.addWidget(self.deleteButton)

        self.layout.addLayout(self.actionLayout)

    def toggle_is_complete(self):
        is_checked = self.completeToggle.isChecked()
        self.font.setItalic(is_checked)
        self.font.setStrikeOut(is_checked)
        self.descriptionText.setFont(self.font)
        self.main.update_task_is_complete(self.id, is_checked)
