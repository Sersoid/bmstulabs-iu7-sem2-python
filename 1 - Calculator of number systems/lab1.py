# Составить приложение, используя модуль создания оконных приложений Tkinter, реализующее индивидуальное задание.
# Интерфейс должен предоставлять ввод символов: как числовых, так и знаков операций -- и с использованием клавиатуры, и
# с помощью кнопок приложения. Также в приложении необходимо создать меню, в котором должны быть следующие пункты:
# 1) заданные действия,
# 2) очистка полей ввода/вывода (по одному и всех сразу),
# 3) информация о программе и авторе.
# Использование встроенных функций bin(), oct(), hex() запрещено.
# Вариант 19: Сложение и вычитание вещественных чисел в 16-й системе счисления.
# Степнов Сергей
# Группа ИУ7-26Б

# Импорт модулей
import re
import sys
from typing import Callable
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap


# Шестнадцатеричное число в десятеричное
def hex_to_int(hex_value: str) -> int:
    hex_value = hex_value.upper()
    hex_translate = {"0": 0, "1": 1, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
                     "A": 10, "B": 11, "C": 12, "D": 13, "E": 14, "F": 15}

    int_value = 0
    for degree in range(len(hex_value) - 1, -1, -1):
        int_value += hex_translate[hex_value[len(hex_value) - 1 - degree]] * 16 ** degree

    return int_value


# Десятеричное число в шестнадцатеричное
def int_to_hex(int_value: int) -> str:
    int_translate = {0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 7: "7", 8: "8", 9: "9",
                     10: "A", 11: "B", 12: "C", 13: "D", 14: "E", 15: "F"}

    hex_value = ""
    while int_value // 16 != 0:
        hex_value += int_translate[int_value % 16]
        int_value //= 16
    hex_value += int_translate[int_value]

    return hex_value[::-1]


# Класс приложения
class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        # Инициализация
        super(MainUI, self).__init__()
        uic.loadUi("ui/main.ui", self)

        # Переменные
        self.about_window = AboutUI()
        self.need_clean_up = False
        self.is_error = False

        # Кнопки с цифрами
        self.button0.clicked.connect(self.on_numeric_button_click("0"))
        self.button1.clicked.connect(self.on_numeric_button_click("1"))
        self.button2.clicked.connect(self.on_numeric_button_click("2"))
        self.button3.clicked.connect(self.on_numeric_button_click("3"))
        self.button4.clicked.connect(self.on_numeric_button_click("4"))
        self.button5.clicked.connect(self.on_numeric_button_click("5"))
        self.button6.clicked.connect(self.on_numeric_button_click("6"))
        self.button7.clicked.connect(self.on_numeric_button_click("7"))
        self.button8.clicked.connect(self.on_numeric_button_click("8"))
        self.button9.clicked.connect(self.on_numeric_button_click("9"))
        self.buttonA.clicked.connect(self.on_numeric_button_click("A"))
        self.buttonB.clicked.connect(self.on_numeric_button_click("B"))
        self.buttonC.clicked.connect(self.on_numeric_button_click("C"))
        self.buttonD.clicked.connect(self.on_numeric_button_click("D"))
        self.buttonE.clicked.connect(self.on_numeric_button_click("E"))
        self.buttonF.clicked.connect(self.on_numeric_button_click("F"))

        # Служебные кнопки
        self.buttonPlus.clicked.connect(self.on_plus_minus_button_click(True))
        self.buttonMinus.clicked.connect(self.on_plus_minus_button_click(False))
        self.buttonEquals.clicked.connect(self.do_math)

        # Строка меню
        self.actionAbout.triggered.connect(self.about_window.show)

    def on_numeric_button_click(self, number) -> Callable:
        def action():
            if self.need_clean_up or self.is_error:
                self.lineEdit.clear()
                self.need_clean_up = self.is_error = False
            self.lineEdit.setText(self.lineEdit.text() + number)

        return action

    def on_plus_minus_button_click(self, is_plus: bool) -> Callable:
        def action():
            if self.is_error:
                self.lineEdit.clear()
                self.is_error = False
            self.lineEdit.setText(self.lineEdit.text() + ("+" if is_plus else "-")),
            self.need_clean_up = False

        return action

    # Вычисление значения введенного выражения
    def do_math(self) -> None:
        search = re.search(r"[+-]?[ ]*[0-9a-fA-F]+([ ]*[+-][ ]*[0-9a-fA-F]+)*", self.lineEdit.text())
        if search:
            answer = 0
            expression = search.group()
            expression_search = re.search(r"[+-]?[ ]*[0-9a-fA-F]+", expression)
            while expression_search:
                if expression_search.group()[0] == "-":
                    answer -= hex_to_int(expression_search.group()[1:])
                elif expression_search.group()[0] == "+":
                    answer += hex_to_int(expression_search.group()[1:])
                else:
                    answer += hex_to_int(expression_search.group())
                expression = expression[len(expression_search.group()):]
                expression_search = re.search(r"[+-]?[ ]*[0-9a-fA-F]+", expression)
            if answer < 0:
                self.lineEdit.setText("-" + int_to_hex(-answer))
            else:
                self.lineEdit.setText(int_to_hex(answer))
            self.need_clean_up = True
        else:
            self.lineEdit.setText("Error!")
            self.is_error = True


class AboutUI(QtWidgets.QMainWindow):
    def __init__(self):
        # Инициализация
        super(AboutUI, self).__init__()
        self.window = uic.loadUi("ui/about.ui", self)

        # Привязка картинки LabelLogo
        self.labelLogo.setPixmap(QPixmap("ui/logo.png"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainUI()
    window.show()
    app.exec()
