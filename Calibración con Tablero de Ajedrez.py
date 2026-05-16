import numpy as np
import cv2

# Tablero de 8x8 cuadros = 7x7 esquinas internas
patron_size = (7,7)

# Tamaño de cada cuadro en cm
tamano_cuadro = 2.5

criterio = (
    cv2.TERM_CRITERIA_EPS +
    cv2.TERM_CRITERIA_MAX_ITER,
    30,
    0.001
)

# Crear puntos 3D reales
objp = np.zeros(
    (patron_size[0]*patron_size[1],3),
    np.float32
)

objp[:,:2] = np.mgrid[
    0:patron_size[0],
    0:patron_size[1]
].T.reshape(-1,2)

objp *= tamano_cuadro

objetos_puntos=[]
imagen_puntos=[]

cap=cv2.VideoCapture(0)

contador=0

while True:

    ret,frame=cap.read()

    if not ret:
        break

    gray=cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    encontrado, esquinas = cv2.findChessboardCorners(
        gray,
        patron_size,
        None
    )

    if encontrado:

        esquinas2=cv2.cornerSubPix(
            gray,
            esquinas,
            (11,11),
            (-1,-1),
            criterio
        )

        cv2.drawChessboardCorners(
            frame,
            patron_size,
            esquinas2,
            encontrado
        )

    cv2.putText(
        frame,
        f"Capturas: {contador}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0,255,0),
        2
    )

    cv2.imshow(
        "Calibracion",
        frame
    )

    tecla=cv2.waitKey(1)&0xFF

    # Guardar imagen con S
    if tecla==ord("s") and encontrado:

        objetos_puntos.append(objp)
        imagen_puntos.append(esquinas2)

        contador+=1

        print(
            f"Imagen {contador} guardada"
        )

    # Salir con Q
    if tecla==ord("q"):
        break

cap.release()
cv2.destroyAllWindows()


# Verificar cantidad mínima
if contador<10:

    print("Muy pocas capturas.")
    print("Toma al menos 10-20 imágenes.")
    exit()


ret, matriz_camara, distorsion, rvecs, tvecs = cv2.calibrateCamera(
    objetos_puntos,
    imagen_puntos,
    gray.shape[::-1],
    None,
    None
)

print("\nMatriz camara:")
print(matriz_camara)

print("\nDistorsion:")
print(distorsion)