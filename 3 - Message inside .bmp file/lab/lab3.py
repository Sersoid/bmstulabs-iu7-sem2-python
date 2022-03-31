from io import BytesIO
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PIL import Image
import sys
from typing import Callable


class EncodeUI(QtWidgets.QMainWindow):
    def __init__(self):
        # Инициализация
        super(EncodeUI, self).__init__()
        self.window = uic.loadUi("ui/encode.ui", self)

        self.file = None
        self.file_button.clicked.connect(self.on_file_button_click())
        self.enter_button.clicked.connect(self.on_enter_button_click())

    def init_image_preview(self):
        scene = QtWidgets.QGraphicsScene(self)
        scene.addItem(QtWidgets.QGraphicsPixmapItem(QPixmap(self.file)))
        self.graphics_view.setScene(scene)

    def on_file_button_click(self) -> Callable:
        def action():
            self.file = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "./", "Image *.bmp")[0]
            self.file_label.setText(f"Выбранный файл: {self.file}")
            self.init_image_preview()

        return action

    def on_enter_button_click(self) -> Callable:
        def action():
            buf = BytesIO()
            Image.open(self.file).convert("RGB").save(buf, format="BMP")
            int_values = list(buf.getvalue())

            data = self.text.text()
            data_limit = (len(int_values) - 54) // 3

            bin_data = [0] * (32 - len(bin(len(data))[2:])) + [int(bit) for bit in bin(len(data))[2:]]
            for char in data:
                for bit in [0] * (8 - len(bin(ord(char))[2:])) + [int(bit) for bit in bin(ord(char))[2:]]:
                    bin_data.append(bit)

            if len(bin_data) <= data_limit:
                for i in range(54, 54 + len(bin_data) * 3, 3):
                    int_values[i] = (int_values[i] + bin_data[(i - 54) // 3]) % 256

                with open(f"{self.file[:-4]}_new.bmp", 'wb') as new_image:
                    new_image.write(bytes(int_values))
            else:
                print("FUCK")

        return action


class AboutUI(QtWidgets.QMainWindow):
    def __init__(self):
        # Инициализация
        super(AboutUI, self).__init__()
        self.window = uic.loadUi("ui/about.ui", self)

        # Привязка картинки labelLogo
        self.labelLogo.setPixmap(QPixmap("ui/logo.png"))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EncodeUI()
    window.show()
    app.exec()
