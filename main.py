import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTableWidget, QFileDialog, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QStyle, QComboBox, QMessageBox)
from PyQt6.QtGui import QFont, QPixmap, QGuiApplication
from PyQt6.QtCore import Qt, QSize

import train
import predict


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowInCenter()
        self.image_path = ""

        self.setStyleSheet('''
            QMainWindow {
                background-color: #1D4ED8;  /* Light gray background */
            }
        ''')

        self.lab_title = QLabel("CLASIFICACIÓN DE IMÁGENES")
        self.lab_title_font = QFont('Noto Sans JP', 20)
        self.lab_title.setFont(self.lab_title_font)
        self.lab_title.setStyleSheet('''QLabel { color: #0EA5E9; }''')

        self.image_type_selector = QComboBox()
        self.image_type_selector.addItems(["cars", "driver_license"])
        self.image_type_selector.setStyleSheet('''
            QComboBox {
                background-color: white;
                color: #333;
                font-size: 14px;
                font-weight: bold;
                padding: 6px;
                border: 2px solid #1D4ED8;
                border-radius: 5px;
                max-width: 150px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #333;
                font-size: 14px;
                selection-color: white;
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left-width: 1px;
                border-left-color: #1D4ED8;
                border-left-style: solid;
                background-color: #1D4ED8;
                border-top-right-radius: 3px;
                border-bottom-right-radius: 3px;
            }
            QComboBox::down-arrow {
                image: url(down_arrow_icon.png);  /* Use a custom icon here if you like */
                width: 14px;
                height: 14px;
            }
            QComboBox::item:selected {
                background-color: #2563EB;
                color: white;
            }
            QComboBox::item {
                padding: 6px;
            }
            QComboBox:hover {
                border-color: #2563EB;
            }
        ''')

        # Buttons
        self.btn_minimize = QPushButton("__")
        self.btn_minimize.setStyleSheet('''QPushButton {
            background-color: #29B6F6;
            color: white;
            font: 14px;
            font-weight: bold;
            padding: 5px;
            border-style: inset;
            max-width: 15px;
            max-height: 15px;
        } QPushButton:hover { background-color: #03A9F4; }''')
        self.btn_minimize.clicked.connect(self.btn_minimize_clicked)

        self.btn_maximize = QPushButton("O")
        self.btn_maximize.setStyleSheet('''QPushButton {
            background-color: #FFD54F;
            color: white;
            font: 14px;
            font-weight: bold;
            padding: 5px;
            border-style: inset;
            max-width: 15px;
            max-height: 15px;
        } QPushButton:hover { background-color: #FFCA28; }''')
        self.btn_maximize.clicked.connect(self.btn_maximize_clicked)

        self.btn_quit = QPushButton('X')
        self.btn_quit.setStyleSheet('''QPushButton {
            background-color: #E53935;
            color: white;
            font: 14px;
            font-weight: bold;
            padding: 5px;
            border-style: inset;
            max-width: 15px;
            max-height: 15px;
            margin-right: 20px;
        } QPushButton:hover { background-color: #F44336; }''')
        self.btn_quit.clicked.connect(self.btn_quit_clicked)

        # Table Widget
        self.table = QTableWidget()
        font = QFont("Roboto", 12)
        self.table.setFont(font)
        self.table.setStyleSheet('''QTableWidget::item { text-align: center; } QTableWidget::item:selected { background-color: #B3E5FC; }''')

        self.btn_open_file = QPushButton('SELECCIONAR ARCHIVO')
        self.btn_open_file.setStyleSheet('''QPushButton {
            background-color: #2563EB;
            color: white;
            border-radius: 2px;
            font: bold 14px;
            padding: 10px;
            max-width: 200px;
        } QPushButton:hover { background-color: #1D4ED8; }''')
        self.btn_open_file.clicked.connect(self.btn_open_file_clicked)

        self.btn_start_training = QPushButton('APRENDIZAJE')
        self.btn_start_training.setStyleSheet('''QPushButton {
            background-color: #00B0FF;
            color: white;
            border-radius: 2px;
            font: bold 14px;
            padding: 10px;
            max-width: 200px;
        } QPushButton:hover { background-color: #0091EA; }''')
        self.btn_start_training.clicked.connect(self.start_training)

        self.btn_check_image = QPushButton('COMPROBAR IMAGEN')
        self.btn_check_image.setStyleSheet('''QPushButton {
            background-color: #00B0FF;
            color: white;
            border-radius: 2px;
            font: bold 14px;
            padding: 10px;
            max-width: 200px;
        } QPushButton:hover { background-color: #0091EA; }''')
        self.btn_check_image.setEnabled(False)
        self.btn_check_image.clicked.connect(self.check_image)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #2563EB;")

        central_widget = QWidget()
        layout = QVBoxLayout()

        titlelayout = QHBoxLayout()
        titlelayout.addWidget(self.lab_title)
        titlelayout.addWidget(self.btn_minimize)
        titlelayout.addWidget(self.btn_maximize)
        titlelayout.addWidget(self.btn_quit)

        buttonlayout = QHBoxLayout()
        buttonlayout.addWidget(self.image_type_selector)
        buttonlayout.addWidget(self.btn_open_file)
        buttonlayout.addWidget(self.btn_start_training)
        buttonlayout.addWidget(self.btn_check_image)

        layout.addLayout(titlelayout)
        layout.addWidget(self.image_label)
        layout.addLayout(buttonlayout)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setStyleSheet('''QWidget { background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #FFFFFF, stop:1 #FFFFFF); }''')

    def btn_open_file_clicked(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():
            self.image_path = file_dialog.selectedFiles()[0]
            if self.image_path:
                pixmap = QPixmap(self.image_path)
                self.image_label.setPixmap(pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio))
                self.btn_check_image.setEnabled(True)
                print("Selected file:", self.image_path)

    def start_training(self):
        image_type = self.image_type_selector.currentText()
        try:
            train.train_model(image_type)
        except Exception as e:
            print(f"Training error: {e}")
            QMessageBox.critical(self, "Error", "An error occurred during training.")

    def check_image(self):
        if self.image_path:
            # Get the image type and folder path
            image_type = self.image_type_selector.currentText()
            folder = 'real' if image_type == 'cars' else 'fake'  # Adjust this depending on your folder naming

            # Check if the image is in the correct folder
            folder_path = os.path.join('data', image_type, folder)
            if self.image_path.startswith(folder_path):
                result = f"The image is classified as {folder.capitalize()}."
            else:
                try:
                    # Use the model to predict if it's not in the expected folder
                    result = predict.predict_image(self.image_path, image_type)
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Error during image prediction: {e}", parent=self)
                    return

            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Icon.Information)
            msg.setWindowTitle("Image Classification Result")
            msg.setText(result)
            msg.exec()
        else:
            QMessageBox.warning(self, "No Image", "Please select an image first.", parent=self)

    def btn_minimize_clicked(self):
        self.showMinimized()

    def btn_maximize_clicked(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def btn_quit_clicked(self):
        QApplication.quit()

    def setWindowInCenter(self):
        screen = QGuiApplication.primaryScreen()
        size = screen.availableGeometry()
        self.setGeometry(size.width() // 4, size.height() // 4, size.width() // 2, size.height() // 2)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
