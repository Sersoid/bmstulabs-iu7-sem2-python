from math import sin, cos, tan, copysign
import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import numpy as np
from PyQt6 import QtWidgets, uic
from PyQt6.QtCore import QRegularExpression
from PyQt6.QtGui import QPixmap, QRegularExpressionValidator
from scipy.signal import argrelextrema
import sys
from typing import Callable

matplotlib.use("QtAgg")

# Полезные регулярные выражения
re_float = r"\d*\.?\d+([eE][+-]?\d+)?"


def equals_with_eps(answer: float, real: float, eps: float) -> bool:
    return abs(answer - real) <= eps


def half_division(function: Callable, x1: float, x2: float, nmax: int, eps: float):
    result = None
    counter = 0

    if equals_with_eps(function(x1), 0, eps):
        result = x1
    elif equals_with_eps(function(x2), 0, eps):
        result = x2
    else:
        while x2 - x1 > eps and counter < nmax:
            delta = (x2 - x1) / 2
            result = x1 + delta
            if copysign(1, function(x1)) != copysign(1, function(result)):
                x2 = result
            else:
                x1 = result
            counter += 1

    return result


class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi("ui/main.ui", self)

        # Переменные
        self.about_window = AboutUI()
        self.graph_window = None

        # Поля для ввода
        self.lineEdit_a_validator = QRegularExpressionValidator(QRegularExpression(f"[+-]?{re_float}"))
        self.lineEdit_a.setValidator(self.lineEdit_a_validator)
        self.lineEdit_b_validator = QRegularExpressionValidator(QRegularExpression(f"[+-]?{re_float}"))
        self.lineEdit_b.setValidator(self.lineEdit_b_validator)
        self.lineEdit_h_validator = QRegularExpressionValidator(QRegularExpression(re_float))
        self.lineEdit_h.setValidator(self.lineEdit_h_validator)
        self.lineEdit_nmax_validator = QRegularExpressionValidator(QRegularExpression(r"\d*"))
        self.lineEdit_nmax.setValidator(self.lineEdit_nmax_validator)
        self.lineEdit_eps_validator = QRegularExpressionValidator(QRegularExpression(re_float))
        self.lineEdit_eps.setValidator(self.lineEdit_eps_validator)

        # Кнопка "Calculate"
        self.pushButton_calc.clicked.connect(self.on_calc_button_click())

        # Строка меню
        self.actionAbout.triggered.connect(self.about_window.show)

    def on_calc_button_click(self) -> Callable:
        def action():
            self.graph_window = GraphUI(
                self.lineEdit_f.text(),
                float(self.lineEdit_a.text()),
                float(self.lineEdit_b.text()),
                float(self.lineEdit_h.text()),
                int(self.lineEdit_nmax.text()),
                float(self.lineEdit_eps.text())
            )
            self.graph_window.show()

        return action


class AboutUI(QtWidgets.QMainWindow):
    def __init__(self):
        # Инициализация
        super(AboutUI, self).__init__()
        self.window = uic.loadUi("ui/about.ui", self)

        # Привязка картинки labelLogo
        self.labelLogo.setPixmap(QPixmap("ui/logo.png"))


class Canvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(Canvas, self).__init__(fig)


class GraphUI(QtWidgets.QMainWindow):
    def __init__(self, function: str, a: float, b: float, h: float, nmax: int, eps: float):
        # Инициализация
        super(GraphUI, self).__init__()

        self.function = lambda x: eval(function)
        self.a = a
        self.b = b
        self.h = h
        self.nmax = nmax
        self.eps = eps

        self.x_values = []
        self.y_values = []

        self.window = QtWidgets.QWidget()
        self.grid = QtWidgets.QGridLayout()
        self.canvas = Canvas()
        self.canvas.axes.grid(axis='both')
        self.table = QtWidgets.QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(("[xi; xi+1]", "x’", "f(x’)"))
        self.init_canvas()
        self.update_table()

        self.grid.addWidget(self.canvas, 0, 0)
        self.grid.addWidget(self.table, 1, 0)

        self.window.setLayout(self.grid)
        self.setCentralWidget(self.window)

    def init_canvas(self):
        temp = self.a

        while self.b >= temp:
            self.x_values.append(temp)
            self.y_values.append(self.function(temp))
            temp += self.h

        self.find_extremum()
        self.find_inflection()

        self.canvas.axes.plot(self.x_values, self.y_values)

    def find_extremum(self) -> None:
        min_ids: np.array = argrelextrema(np.array(self.y_values), np.less)[0]
        max_ids: np.array = argrelextrema(np.array(self.y_values), np.greater)[0]
        extremum = np.sort(np.concatenate((min_ids, max_ids)))
        self.canvas.axes.scatter([self.x_values[i] for i in extremum], [self.y_values[i] for i in extremum],
                                 color="red")

    def find_inflection(self) -> None:
        smoothed: np.array = np.gradient(np.gradient(np.array(self.y_values)))
        inflection: np.array = np.where(np.diff(np.sign(smoothed)))[0]
        if len(inflection) >= len(self.x_values) * 0.1:
            inflection: np.array = np.array([], dtype='int')
        self.canvas.axes.scatter([self.x_values[i] for i in inflection], [self.y_values[i] for i in inflection],
                                 color="green")

    def update_table(self):
        for i in range(len(self.y_values) - 1):
            x_result = half_division(self.function, self.x_values[i], self.x_values[i + 1], self.nmax, self.eps)
            y_result = self.function(x_result)

            if equals_with_eps(y_result, 0, self.eps):
                self.canvas.axes.scatter(x_result, y_result, color="blue")

                row_number = self.table.rowCount()
                self.table.insertRow(row_number)
                self.table.setItem(row_number, 0, QtWidgets.QTableWidgetItem(f"[{format(self.x_values[i], '.5g')}; "
                                                                             f"{format(self.x_values[i + 1], '.5g')}]"))
                self.table.setItem(row_number, 1, QtWidgets.QTableWidgetItem(str(format(x_result, ".5g"))))
                self.table.setItem(row_number, 2, QtWidgets.QTableWidgetItem(str(format(y_result, ".5g"))))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainUI()
    window.show()
    app.exec()
