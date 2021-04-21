import sys
import uuid
import json
from PySide6 import QtWidgets, QtCore
from task import Task
from utils import debounce
from stylesheet import stylesheet

STORAGE_PATH = 'storage.json'


class Main(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout(self)
        self.taskLayout = QtWidgets.QVBoxLayout()
        self.layout.addLayout(self.taskLayout)
        self.tasks_data = load_storage()
        self.editButton = QtWidgets.QPushButton("add task")
        self.editButton.clicked.connect(self.add_task)
        self.layout.addWidget(self.editButton)
        self.display_tasks()

    def display_tasks(self):
        self.clear_task_display()
        for taskID in self.tasks_data:
            self.taskLayout.addWidget(Task(taskID, self))

    def clear_task_display(self):
        for i in reversed(range(self.taskLayout.count())):
            self.taskLayout.itemAt(i).widget().setParent(None)

    def add_task(self):
        self.tasks_data[str(uuid.uuid4())] = {"description": "type here", "is_complete": False}
        self.update_storage()
        self.display_tasks()

    def delete_task(self, task_id):
        del self.tasks_data[task_id]
        self.update_storage()
        self.display_tasks()

    def update_task_description(self, task_id, description):
        self.tasks_data[task_id]["description"] = description
        self.update_storage_debounce()

    def update_task_is_complete(self, task_id, is_complete):
        self.tasks_data[task_id]["is_complete"] = is_complete
        self.update_storage_debounce()

    @debounce(2)
    def update_storage_debounce(self):
        self.update_storage()

    def update_storage(self):
        data = json.dumps(self.tasks_data)
        file = open(STORAGE_PATH, 'w')
        file.write(data)
        file.close()


def load_storage():
    data = open(STORAGE_PATH, 'r').read()
    return json.loads(data)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    app.setStyleSheet(stylesheet)
    widget = Main()
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec_())
