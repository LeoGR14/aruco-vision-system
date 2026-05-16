import numpy as np
import cv2

# Definición del diccionario ArUco
ARUCO_DICT = {
    "DICT_5X5_100": cv2.aruco.getPredefinedDictionary(
        cv2.aruco.DICT_5X5_100
    )
}

def aruco_display(corners, ids, rejected, image):
    if len(corners) > 0:
        ids = ids.flatten()

        for i, markerCorner in enumerate(corners):

            markerID = ids[i]
            markerCorner = markerCorner.reshape((4, 2))

            (topLeft, topRight, bottomRight, bottomLeft) = markerCorner.astype(int)

            # Dibujar bordes
            cv2.line(image, tuple(topLeft), tuple(topRight), (0,255,0), 2)
            cv2.line(image, tuple(topRight), tuple(bottomRight), (0,255,0), 2)
            cv2.line(image, tuple(bottomRight), tuple(bottomLeft), (0,255,0), 2)
            cv2.line(image, tuple(bottomLeft), tuple(topLeft), (0,255,0), 2)

            # Centro
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)

            cv2.circle(image, (cX,cY), 4, (0,0,255), -1)

            cv2.putText(
                image,
                str(markerID),
                (topLeft[0], topLeft[1]-10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0,255,0),
                2
            )

            print("[INFO] ArUco ID:", markerID)

    return image


# Selección del diccionario
aruco_type = "DICT_5X5_100"
arucoDict = ARUCO_DICT[aruco_type]

# Crear parámetros
parametros = cv2.aruco.DetectorParameters()

# NUEVO detector (OpenCV 4.7+)
detector = cv2.aruco.ArucoDetector(
    arucoDict,
    parametros
)

# Cámara
cap = cv2.VideoCapture(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH,1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT,720)

while cap.isOpened():

    ret, img = cap.read()

    if not ret:
        break

    h, w, _ = img.shape

    width = 1000
    height = int(width*(h/w))

    img = cv2.resize(
        img,
        (width,height),
        interpolation=cv2.INTER_CUBIC
    )

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # Detectar marcadores
    corners, ids, rejected = detector.detectMarkers(gray)

    # Mostrar detección
    img = aruco_display(
        corners,
        ids,
        rejected,
        img
    )

    cv2.imshow(
        "Detector ArUco",
        img
    )

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()