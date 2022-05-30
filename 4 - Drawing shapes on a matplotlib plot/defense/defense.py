import math
import matplotlib
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from matplotlib.patches import Circle
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


# Main class
class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi("ui/main.ui", self)

        # About window
        self.about_window = AboutUI()

        # Settings
        self.color = "#000000"

        # Objects
        self.objects = []

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
        self.gridLayout.addWidget(self.canvas, 3, 2, 1, 2)

        # Menu
        self.action_about.triggered.connect(self.about_window.show)

    # Color change
    def on_button_color_click(self) -> Callable:
        def action():
            self.color = f"#{hex(QtWidgets.QColorDialog.getColor().rgb())[4:].upper()}"
            self.text_color.setText(f"Color: {self.color}")

        return action

    # Draw
    def on_button_draw_click(self) -> Callable:
        def action():
            try:
                dot = Dot(float(self.lineedit_x1.text()), float(self.lineedit_y1.text()))
                self.canvas.axes.scatter(dot.x, dot.y, c=self.color)
                self.objects.append(dot)
                self.canvas.draw()
            except ValueError:
                message = QtWidgets.QMessageBox(self, text="Incorrect coordinates")
                message.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                message.exec()

        return action

    # Searching dots by task
    def on_button_search_click(self) -> Callable:
        def action():
            if len(self.objects) < 3:
                message = QtWidgets.QMessageBox(self, text="Not enough dots to build a circle")
                message.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                message.exec()
            else:
                min_cx = None
                min_cy = None
                min_r = None

                for dot1 in self.objects:
                    for dot2 in self.objects:
                        for dot3 in self.objects:
                            if self.objects.index(dot1) != self.objects.index(dot2) and \
                                    self.objects.index(dot2) != self.objects.index(dot3) and \
                                    self.objects.index(dot1) != self.objects.index(dot3):
                                a = dot2.x - dot1.x
                                b = dot2.y - dot1.y
                                c = dot3.x - dot1.x
                                d = dot3.y - dot1.y
                                e = a * (dot1.x + dot2.x) + b * (dot1.y + dot2.y)
                                f = c * (dot1.x + dot3.x) + d * (dot1.y + dot3.y)
                                g = 2 * (a * (dot3.y - dot2.y) - b * (dot3.x - dot2.x))

                                if g:
                                    cx = (d * e - b * f) / g
                                    cy = (a * f - c * e) / g
                                    r = math.sqrt(math.pow(dot1.x - cx, 2) + math.pow(dot1.y - cy, 2))

                                    if not min_r or min_r > r:
                                        min_cx = cx
                                        min_cy = cy
                                        min_r = r
                                else:
                                    message = QtWidgets.QMessageBox(self, text="Circle not found")
                                    message.setIcon(QtWidgets.QMessageBox.Icon.Warning)
                                    message.exec()

                if all((min_cx, min_cy, min_r)):
                    e = Circle(xy=(min_cx, min_cy), radius=min_r)

                    self.canvas.axes.add_artist(e)
                    e.set_clip_box(self.canvas.axes.bbox)
                    e.set_edgecolor(self.color)
                    e.set_facecolor(None)
                    self.canvas.draw()

                    message = QtWidgets.QMessageBox(self, text="Circle with minimum radius:\n"
                                                               f"X: {min_cx}\n"
                                                               f"Y: {min_cy}\n"
                                                               f"Radius: {min_r}")
                    message.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    message.exec()

                    e.remove()
                    self.canvas.draw()

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
