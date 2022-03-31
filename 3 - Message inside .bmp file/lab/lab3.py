from io import BytesIO
from PyQt6 import QtWidgets, uic
from PyQt6.QtGui import QPixmap
from PIL import Image
import sys
from typing import Callable


class EncodeUI(QtWidgets.QMainWindow):
    def __init__(self, about_window):
        # Инициализация
        super(EncodeUI, self).__init__()
        self.window = uic.loadUi("ui/encode.ui", self)
        self.decode_window = None
        self.about_window = about_window

        self.file = None
        self.file_button.clicked.connect(self.on_file_button_click())
        self.encode_button.clicked.connect(self.on_encode_button_click())

        self.action_decode.triggered.connect(self.on_action_decode())
        self.action_about.triggered.connect(self.about_window.show)

    def set_decode_window(self, new_window):
        self.decode_window = new_window

    def on_action_decode(self):
        def action():
            self.hide()
            self.decode_window.show()

        return action

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

    def on_encode_button_click(self) -> Callable:
        def action():
            buf = BytesIO()
            Image.open(self.file).convert("RGB").save(buf, format="BMP")
            int_values = list(buf.getvalue())

            data = self.encode_text.text()
            data_limit = (len(int_values) - 54) // 3

            bin_data = [0] * (32 - len(bin(len(data))[2:])) + [int(bit) for bit in bin(len(data))[2:]]
            for char in data:
                for bit in [0] * (8 - len(bin(ord(char))[2:])) + [int(bit) for bit in bin(ord(char))[2:]]:
                    bin_data.append(bit)

            if len(bin_data) <= data_limit:
                for i in range(54, 54 + len(bin_data) * 3, 3):
                    int_values[i] = int(bin(int_values[i])[2:-1] + str(bin_data[(i - 54) // 3]), 2)

                with open(f"{self.file[:-4]}_new.bmp", 'wb') as new_image:
                    new_image.write(bytes(int_values))
            else:
                print("FUCK")

        return action


class DecodeUI(QtWidgets.QMainWindow):
    def __init__(self, about_window):
        # Инициализация
        super(DecodeUI, self).__init__()
        self.window = uic.loadUi("ui/decode.ui", self)
        self.encode_window = None
        self.about_window = about_window

        self.file = None
        self.file_button.clicked.connect(self.on_file_button_click())
        self.decode_button.clicked.connect(self.on_decode_button_click())

        self.action_encode.triggered.connect(self.on_action_encode())
        self.action_about.triggered.connect(self.about_window.show)

    def set_encode_window(self, new_window):
        self.encode_window = new_window

    def on_action_encode(self):
        def action():
            self.hide()
            self.encode_window.show()

        return action

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

    def on_decode_button_click(self) -> Callable:
        def action():
            buf = BytesIO()
            Image.open(self.file).convert("RGB").save(buf, format="BMP")
            int_values = list(buf.getvalue())

            message_length = ""
            for i in range(54, 150, 3):
                message_length += bin(int_values[i])[-1]
            message_length = int(message_length[2:], 2)

            decode_text = ""
            for i in range(150, 150 + 24 * message_length, 24):
                bin_char = ""
                for j in range(i, i + 24, 3):
                    bin_char += bin(int_values[j])[-1]
                decode_text += chr(int(bin_char, 2))

            self.decode_text.setText(f"Декодированный текст: {decode_text}")

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
    about_window = AboutUI()
    encode_window = EncodeUI(about_window)
    decode_window = DecodeUI(about_window)
    encode_window.set_decode_window(decode_window)
    decode_window.set_encode_window(encode_window)
    encode_window.show()
    app.exec()
