import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTabWidget, QWidget, QLabel
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QTimer
import cv2
import numpy as np
import pandas as pd

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.tabs = QTabWidget()
        self.tabs.setFixedSize(960, 720)
        self.tab1 = QWidget()
        self.tab2 = QWidget()

        self.tabs.addTab(self.tab1, "Cámara web")
        self.tabs.addTab(self.tab2, "Recorrido del robot")

        self.movimiento_df = pd.DataFrame(columns=['x', 'y', 'direccion'])

        self.label = QLabel(self.tab1)
        self.label.setGeometry(0, 0, 960, 720)

        self.label2 = QLabel(self.tab2)
        self.label2.setGeometry(0, 0, 960, 720)

        self.cap = cv2.VideoCapture(0)
        self.arucoDict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_100)
        self.parametros = cv2.aruco.DetectorParameters()
        self.ruta = []

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)  # Ajusta el intervalo si es necesario

        self.setCentralWidget(self.tabs)

    def update_image(self):
        ret, frame = self.cap.read()
        if not ret:
            return

        frame = cv2.resize(frame, (960, 720))
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(gray, self.arucoDict, parameters=self.parametros)

        recorrido_img = np.zeros_like(frame)
        if ids is not None:
            frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)
            for i, corner in enumerate(corners):
                marker_id = ids[i][0]  # `ids` es una lista de arrays, toma el valor del primer elemento
                if marker_id == 99:
                    cX = int(corner[0][:, 0].mean())
                    cY = int(corner[0][:, 1].mean())
                    self.ruta.append((cX, cY))

            if len(self.ruta) > 1:
                puntos_ruta = np.array(self.ruta, dtype=np.int32)
                cv2.polylines(recorrido_img, [puntos_ruta], False, (0, 255, 0), thickness=2)

        # Actualiza la imagen de la cámara en la primera pestaña
        self.update_label(self.label, frame)

        # Actualiza el recorrido en la segunda pestaña
        recorrido_img_rgb = cv2.cvtColor(recorrido_img, cv2.COLOR_BGR2RGB)
        img2 = QPixmap.fromImage(QImage(recorrido_img_rgb.data, recorrido_img_rgb.shape[1], recorrido_img_rgb.shape[0], QImage.Format_RGB888))
        self.label2.setPixmap(img2)

    def update_label(self, label, frame):
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = QPixmap.fromImage(QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QImage.Format_RGB888))
        label.setPixmap(img)

    def closeEvent(self, event):
        self.cap.release()
        super().closeEvent(event)

    def guardar_datos(self):
        self.movimiento_df.to_excel('movimiento_robot.xlsx', index=False)
        print("Datos guardados en movimiento_robot.xlsx")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
