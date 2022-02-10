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
from PyQt6 import QtWidgets

# Импорт файла интерфейса
import qt_ui


# Шестнадцатеричное число в десятеричное
def hex_to_int(hex_value: str) -> int:
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
class Application(QtWidgets.QMainWindow, qt_ui.Ui_MainWindow):
    def __init__(self):
        # Инициализация
        super().__init__()
        self.need_clean_up = False
        self.setupUi(self)

        # Кнопки с цифрами
        self.Button0.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "0")])
        self.Button1.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "1")])
        self.Button2.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "2")])
        self.Button3.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "3")])
        self.Button4.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "4")])
        self.Button5.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "5")])
        self.Button6.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "6")])
        self.Button7.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "7")])
        self.Button8.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "8")])
        self.Button9.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "9")])
        self.ButtonA.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "A")])
        self.ButtonB.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "B")])
        self.ButtonC.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "C")])
        self.ButtonD.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "D")])
        self.ButtonE.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "E")])
        self.ButtonF.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                              self.LineEdit.setText(self.LineEdit.text() + "F")])

        # Служебные кнопки
        self.ButtonClear.clicked.connect(lambda: self.clean_up(True))
        self.ButtonPlus.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                                 self.LineEdit.setText(self.LineEdit.text() + "+")])
        self.ButtonMinus.clicked.connect(lambda: [self.clean_up(self.need_clean_up),
                                                  self.LineEdit.setText(self.LineEdit.text() + "-")])
        self.ButtonEquals.clicked.connect(self.do_math)

    # Очистка поля
    def clean_up(self, check: bool) -> None:
        if check:
            self.LineEdit.setText("")
        self.need_clean_up = False

    # Вычисление значения введенного выражения
    def do_math(self):
        search = re.search(r"[+-]?[ ]*[0-9a-fA-F]+([ ]*[+-][ ]*[0-9a-fA-F]+)+", self.LineEdit.text())
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
                self.LineEdit.setText("-" + int_to_hex(-answer))
            else:
                self.LineEdit.setText(int_to_hex(answer))
            self.need_clean_up = True
        else:
            # Виджет ошибки нужно добавить
            self.clean_up(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Application()
    window.show()
    app.exec()
