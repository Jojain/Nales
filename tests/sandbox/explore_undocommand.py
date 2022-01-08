
##################################################
##################################################
##################################################

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout, QAction
from PyQt5.QtWidgets import QUndoView, QUndoCommand, QUndoStack
import sys
from PyQt5 import QtCore
import typing

from PyQt5 import QtWidgets

class AddCommand(QUndoCommand):
    def __init__(self, label):
        self.l = label
        self.old_state = int(label.text())
        super().__init__()
        self.setText("Add")


    def redo(self) -> None:
        val = int(self.l.text())
        t = val +1
        self.l.setText(str(t))
    def undo(self):
        self.l.setText(str(self.old_state))
        
class MinCommand(QUndoCommand):
    def __init__(self,label):
        self.l = label
        self.old_state = int(label.text())

        super().__init__()
        self.setText("Remove")


    def redo(self) -> None:
        val = int(self.l.text())
        t = val -1
        self.l.setText(str(t))
        return super().redo()
    
    def undo(self):
        self.l.setText(str(self.old_state))

class MainWindow(QMainWindow):

    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        self.central = QWidget(self)
        
        btn_widget = QWidget(self)
        btn_layout = QHBoxLayout()
        lb = QPushButton(btn_widget)
        lb.setText("+1")
        rb = QPushButton(btn_widget)
        rb.setText("-1")
        btn_layout.addWidget(lb)
        btn_layout.addWidget(rb)

        self.label = QLabel("0",self.central)
        self.label.move(20,0)
        vertical = QVBoxLayout()

        vertical.addWidget(btn_widget)
        vertical.addWidget(self.label)

        self.central.setLayout(btn_layout)
        self.setCentralWidget(self.central)



        def plus():
            val = int(self.label.text())
            t = val +1
            self.label.setText(str(t))

        def moins():
            val = int(self.label.text())
            t = val -1
            self.label.setText(str(t))
        
        lb.clicked.connect(plus)
        rb.clicked.connect(moins)
    

        self.menu = self.menuBar()
        self.menu.addMenu("&File")

        self.undostack = QUndoStack(self)
        undo = self.undostack.createUndoAction(self, "Undo")
        redo = self.undostack.createRedoAction(self, "Redo")
        self.menu.addAction(undo)
        self.menu.addAction(redo)

        self.uview = QUndoView(self.undostack)
        self.uview.setWindowTitle("Commands")
        self.uview.show()

    def addcmd(self):
        self.undostack.push(AddCommand(self.label))

    def mincmd(self):
        self.undostack.push(MinCommand(self.label))


    def setup_actions(self):
        
        self.add_action = QAction(self)
        self.add_action.setShortcut("+")
        self.add_action.setText("+")
        self.add_action.triggered.connect(self.addcmd)
        self.min_action = QAction(self)
        self.min_action.setShortcut("-")
        self.min_action.setText("-")
        self.min_action.triggered.connect(self.mincmd)

        self.menu.addAction(self.add_action)
        self.menu.addAction(self.min_action)

app = QApplication(sys.argv)
window = MainWindow()
window.setup_actions()

window.show()


app.exec_()
