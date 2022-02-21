import sys
from typing import Callable
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QRegularExpressionValidator


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        # Инициализация
        super(MainUI, self).__init__()
        uic.loadUi("ui/defense.ui", self)

        # Переменные
        self.is_error = False

        # Поле для ввода
        self.decLineEditValidator = QRegularExpressionValidator(QRegularExpression(r"[0-9]*"))
        self.decLineEdit.setValidator(self.decLineEditValidator)

        # Кнопки с цифрами
        self.pushButton0.clicked.connect(self.on_numeric_button_click("0"))
        self.pushButton1.clicked.connect(self.on_numeric_button_click("1"))
        self.pushButton2.clicked.connect(self.on_numeric_button_click("2"))
        self.pushButton3.clicked.connect(self.on_numeric_button_click("3"))
        self.pushButton4.clicked.connect(self.on_numeric_button_click("4"))
        self.pushButton5.clicked.connect(self.on_numeric_button_click("5"))
        self.pushButton6.clicked.connect(self.on_numeric_button_click("6"))
        self.pushButton7.clicked.connect(self.on_numeric_button_click("7"))
        self.pushButton8.clicked.connect(self.on_numeric_button_click("8"))
        self.pushButton9.clicked.connect(self.on_numeric_button_click("9"))

        # Служебные кнопки
        self.pushButtonEquals.clicked.connect(self.dec_to_oct())

    def on_numeric_button_click(self, number) -> Callable:
        def action() -> None:
            self.decLineEdit.setText(self.decLineEdit.text() + number)

        return action

    def dec_to_oct(self) -> Callable:
        def action() -> None:
            number = int(self.decLineEdit.text())
            result = ""

            while number // 16 != 0:
                result += str(number % 8)
                number //= 8
            result += str(number)

            self.octLineEdit.setText(result[::-1])

        return action


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainUI()
    window.show()
    app.exec()
