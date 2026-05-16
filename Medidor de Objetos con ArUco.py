import numpy as np
import cv2

# Parámetros ArUco
parametros = cv2.aruco.DetectorParameters()

diccionario = cv2.aruco.getPredefinedDictionary(
    cv2.aruco.DICT_5X5_100
)

# NUEVO detector
detector = cv2.aruco.ArucoDetector(
    diccionario,
    parametros
)

# Rangos HSV
LowAzul=np.array([96,144,106],np.uint8)
HighAzul=np.array([124,255,255],np.uint8)

LowVerde=np.array([43,52,106],np.uint8)
HighVerde=np.array([91,255,255],np.uint8)

LowRojo1=np.array([0,100,20],np.uint8)
HighRojo1=np.array([10,255,255],np.uint8)

LowRojo2=np.array([175,100,20],np.uint8)
HighRojo2=np.array([180,255,255],np.uint8)


def medir(contorno,frame,proporcion_cm):

    for c in contorno:

        area=cv2.contourArea(c)

        if area>2000:

            rectangulo=cv2.minAreaRect(c)

            (x,y),(an,al),angulo=rectangulo

            ancho=an/proporcion_cm
            alto=al/proporcion_cm

            rect=cv2.boxPoints(rectangulo)
            rect=np.int32(rect)

            cv2.polylines(
                frame,
                [rect],
                True,
                (0,255,255),
                2
            )

            cv2.putText(
                frame,
                f"Ancho:{round(ancho,1)} cm",
                (int(x),int(y-15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (150,0,255),
                2
            )

            cv2.putText(
                frame,
                f"Alto:{round(alto,1)} cm",
                (int(x),int(y+15)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (75,0,75),
                2
            )


def procesar_colores(frame,hsv,proporcion_cm):

    maskAzul=cv2.inRange(hsv,LowAzul,HighAzul)
    maskVerde=cv2.inRange(hsv,LowVerde,HighVerde)

    maskRojo1=cv2.inRange(hsv,LowRojo1,HighRojo1)
    maskRojo2=cv2.inRange(hsv,LowRojo2,HighRojo2)

    contornoAzul,_=cv2.findContours(
        maskAzul,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contornoVerde,_=cv2.findContours(
        maskVerde,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contornoRojo1,_=cv2.findContours(
        maskRojo1,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    contornoRojo2,_=cv2.findContours(
        maskRojo2,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    medir(contornoAzul,frame,proporcion_cm)
    medir(contornoVerde,frame,proporcion_cm)
    medir(contornoRojo1,frame,proporcion_cm)
    medir(contornoRojo2,frame,proporcion_cm)


def main():

    cap=cv2.VideoCapture(0)

    marcado_anterior=False

    while True:

        ret,frame=cap.read()

        if not ret:
            break

        frame=cv2.resize(
            frame,
            (650,550)
        )

        hsv=cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV
        )

        # NUEVA detección
        esquinas,ids,rechazados=detector.detectMarkers(frame)

        if ids is not None:

            esquinasInt=np.int32(esquinas)

            cv2.polylines(
                frame,
                esquinasInt,
                True,
                (0,0,255),
                2
            )

            per_Aruco=cv2.arcLength(
                esquinasInt[0],
                True
            )

            proporcion_cm=per_Aruco/13

            procesar_colores(
                frame,
                hsv,
                proporcion_cm
            )

        cv2.imshow(
            "Camara",
            frame
        )

        if cv2.waitKey(5)==27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__=="__main__":
    main()