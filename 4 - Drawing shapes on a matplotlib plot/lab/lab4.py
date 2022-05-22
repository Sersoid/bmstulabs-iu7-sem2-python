import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
import sys
from typing import Callable

matplotlib.use("QtAgg")


# Dot class
class Dot:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


# Line class
class Line:
    def __init__(self, x1: float, y1: float, x2: float, y2: float):
        self.dot1 = Dot(x1, y1)
        self.dot2 = Dot(x2, y2)

    def check(self):
        return not (self.dot1.x == self.dot2.x and self.dot1.y == self.dot2.y)


# Check for parallelism
def check_parallel(dot1: Dot, dot2: Dot, line: Line):
    return dot1.x - dot2.x == line.dot1.x - line.dot2.x == 0 or \
           dot1.y - dot2.y == line.dot1.y - line.dot2.y == 0 or \
           dot1.y - dot2.y != 0 and line.dot1.y - line.dot2.y and \
           (dot1.x - dot2.x) / (dot1.y - dot2.y) == (line.dot1.x - line.dot2.x) / (line.dot1.y - line.dot2.y)


# Main class
class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi("ui/main.ui", self)

        # About window
        self.about_window = AboutUI()

        # Settings
        self.tool = 0
        self.color = "#000000"

        # Objects
        self.objects = []

        # Dot/Line
        self.combobox_tool.currentIndexChanged.connect(self.on_combobox_tool_changed())
        # Button "Select Color"
        self.button_color.clicked.connect(self.on_button_color_click())
        # Button "Draw"
        self.button_draw.clicked.connect(self.on_button_draw_click())
        # Button "Search"
        self.button_search.clicked.connect(self.on_button_search_click())

        # matplotlib
        self.canvas = Canvas(self)
        self.canvas.axes.grid(axis="both")
        self.canvas.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self.gridLayout.addWidget(self.canvas, 2, 2, 1, 5)

        # Menu
        self.action_about.triggered.connect(self.about_window.show)

    # Tool change
    def on_combobox_tool_changed(self) -> Callable:
        def action():
            self.tool = self.combobox_tool.currentIndex()
            self.lineedit_x2.setEnabled(bool(self.tool))
            self.lineedit_y2.setEnabled(bool(self.tool))

            self.text_tool.setText(f"Tool: {self.combobox_tool.currentText()}")

        return action

    # Color change
    def on_button_color_click(self) -> Callable:
        def action():
            self.color = f"#{hex(QtWidgets.QColorDialog.getColor().rgb())[4:].upper()}"
            self.text_color.setText(f"Color: {self.color}")

        return action

    # Draw
    def on_button_draw_click(self) -> Callable:
        def action():
            if self.tool:
                line = Line(float(self.lineedit_x1.text()), float(self.lineedit_y1.text()),
                            float(self.lineedit_x2.text()), float(self.lineedit_y2.text()))
                if line.check():
                    self.canvas.axes.scatter((line.dot1.x, line.dot2.x), (line.dot1.y, line.dot2.y), c=self.color)
                    self.canvas.axes.plot((line.dot1.x, line.dot2.x), (line.dot1.y, line.dot2.y), c=self.color)
                    self.objects.append(line)
                    self.canvas.draw()
                else:
                    message = QtWidgets.QMessageBox(self, text="Line cannot be a dot")
                    message.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                    message.exec()
            else:
                dot = Dot(float(self.lineedit_x1.text()), float(self.lineedit_y1.text()))
                self.canvas.axes.scatter(dot.x, dot.y, c=self.color)
                self.objects.append(dot)
                self.canvas.draw()

        return action

    # Searching dots by task
    def on_button_search_click(self) -> Callable:
        def action():
            max_counter = 0
            dots = None

            for figure_dot1 in self.objects:
                if isinstance(figure_dot1, Dot):
                    for figure_dot2 in self.objects:
                        if isinstance(figure_dot2, Dot) and \
                                self.objects.index(figure_dot1) != self.objects.index(figure_dot2):
                            counter = 0

                            for figure_line in self.objects:
                                if isinstance(figure_line, Line):
                                    if check_parallel(figure_dot1, figure_dot2, figure_line):
                                        counter += 1

                            if counter > max_counter:
                                dots = (figure_dot1, figure_dot2)
                                max_counter = counter

            if dots:
                message = QtWidgets.QMessageBox(self, text="Dots:\n"
                                                           f"1) {dots[0].x, dots[0].y}\n"
                                                           f"2) {dots[1].x, dots[1].y}")
                message.setIcon(QtWidgets.QMessageBox.Icon.Information)
            else:
                message = QtWidgets.QMessageBox(self, text="Dots not found")
                message.setIcon(QtWidgets.QMessageBox.Icon.Warning)

            message.exec()

        return action


# About class
class AboutUI(QtWidgets.QMainWindow):
    def __init__(self):
        # Initialization
        super(AboutUI, self).__init__()
        self.window = uic.loadUi("ui/about.ui", self)

        # Link labelLogo
        self.labelLogo.setPixmap(QPixmap("ui/logo.png"))


# Matplotlib canvas for drawing
class Canvas(FigureCanvasQTAgg):
    def __init__(self, main_ui, parent=None, width=5, height=4, dpi=100):
        self.main_ui = main_ui
        self.parent = parent

        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(Canvas, self).__init__(fig)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainUI()
    window.show()
    app.exec()
