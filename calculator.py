import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt


class Calculator(QMainWindow):

    def __init__(self):
        super().__init__()
        loadUi('calculator.ui', self)

        self.setWindowTitle("Calculator")
        self.new_input = True

        for i in range(10):
            getattr(self, f"b{i}").clicked.connect(lambda _, x=str(i): self.digit_pressed(x))

        self.bdot.clicked.connect(self.dot_pressed)
        self.bac.clicked.connect(self.method_ac)
        self.bc.clicked.connect(self.method_c)
        self.bad.clicked.connect(lambda: self.op_pressed("+"))
        self.bsub.clicked.connect(lambda: self.op_pressed("-"))
        self.bpr.clicked.connect(lambda: self.op_pressed("*"))
        self.bdiv.clicked.connect(lambda: self.op_pressed("/"))
        self.beq.clicked.connect(self.result)

    def digit_pressed(self, num):
        if self.opdisplay.text() == "0" or self.new_input:
            self.opdisplay.setText(num)
            self.new_input = False
        else:
            self.opdisplay.setText(self.opdisplay.text() + num)

    def dot_pressed(self):
        text = self.opdisplay.text()

        if self.new_input:
            self.opdisplay.setText("0.")
            self.new_input = False
            return

        parts = text.replace("+", " ").replace("-", " ") \
                    .replace("*", " ").replace("/", " ").split()
        current = parts[-1] if parts else ""

        if "." not in current:
            if text.endswith(("+", "-", "*", "/")):
                self.opdisplay.setText(text + "0.")
            else:
                self.opdisplay.setText(text + ".")

    def method_ac(self):
        self.opdisplay.setText("0")
        self.new_input = True

    def method_c(self):
        text = self.opdisplay.text()
        if len(text) <= 1:
            self.opdisplay.setText("0")
        else:
            self.opdisplay.setText(text[:-1])

    def op_pressed(self, op):
        text = self.opdisplay.text()
        if text.endswith(("+", "-", "*", "/")):
            self.opdisplay.setText(text[:-1] + op)
        else:
            self.opdisplay.setText(text + op)
        self.new_input = False

    def result(self):
        text = self.opdisplay.text()
        if text.endswith(("+", "-", "*", "/")):
            text = text[:-1]
        try:
            res = eval(text)
            self.opdisplay.setText(str(res))
        except:
            self.opdisplay.setText("Error")
        self.new_input = True

    def keyPressEvent(self, event):
        key = event.key()

        if Qt.Key_0 <= key <= Qt.Key_9:
            self.digit_pressed(str(key - Qt.Key_0))

        elif key == Qt.Key_Plus:
            self.op_pressed("+")
        elif key == Qt.Key_Minus:
            self.op_pressed("-")
        elif key == Qt.Key_Asterisk:
            self.op_pressed("*")
        elif key == Qt.Key_Slash:
            self.op_pressed("/")
        elif key == Qt.Key_Period:
            self.dot_pressed()
        elif key in (Qt.Key_Return, Qt.Key_Enter):
            self.result()
        elif key == Qt.Key_Backspace:
            self.method_c()
        elif key == Qt.Key_Escape:
            self.method_ac()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())
