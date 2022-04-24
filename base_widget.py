from ctypes import alignment
import sys
import random
from PySide6 import QtCore, QtWidgets, QtGui
from qt_material import apply_stylesheet


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])


class Widget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.hello = ["Messi", "Ronaldo", "Benzema", "Lewandowski"]

        self.button = QtWidgets.QPushButton("Randomize")
        self.text = QtWidgets.QLabel("Get a random player", alignment=QtCore.Qt.AlignCenter)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.button)

        self.search_results_widget = QtWidgets.QListView()
        self.search_results_widget.setSpacing(5)
        model = QtCore.QStringListModel()
        self.list = [
            "Lewandowski is good. Lewandowski is good. \nLewandowski is good.Lewandowski is good. Lewandowski is good.Lewandowski is good. ", 
            "Benzema is better. Benzema is better. \nBenzema is better. Benzema is better", 
            "Ronaldo is the best. Ronaldo is the best. \n Ronaldo is the best. Ronaldo is the best. ", 
             "Messi is God. Messi is God.\n Messi is God. Messi is God."]
        model.setStringList(self.list)

        self.model = model
        self.search_results_widget.setModel(self.model)
        self.layout.addWidget(self.search_results_widget)
        self.button.clicked.connect(self.clicked_callback)


    @QtCore.Slot()
    def clicked_callback(self):
        choice = random.choice(self.hello)
        self.text.setText(choice)
        self.list.append("Hello user, thank you for choosing our application. \nYou chose {}. Please continue playing to maximize your chances of winning.".format(choice))
        self.model.setStringList(self.list)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    apply_stylesheet(app, theme='light_blue.xml')
    widget = Widget()
    widget.resize(400, 800)
    widget.show()

    sys.exit(app.exec())