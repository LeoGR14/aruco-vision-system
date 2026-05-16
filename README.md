# ArUco Vision System

Proyecto desarrollado utilizando Python, OpenCV, PyQt5 y marcadores ArUco para aplicaciones de visión artificial, medición de objetos y seguimiento de trayectorias.

## Descripción

Este proyecto reúne distintos módulos desarrollados como parte de un proceso de aprendizaje y experimentación con visión artificial. El objetivo fue trabajar con calibración de cámaras, detección de marcadores ArUco, medición automática y seguimiento de trayectorias utilizando referencias visuales.

---

## Tecnologías utilizadas

* Python
* OpenCV
* OpenCV Contrib
* NumPy
* Pandas
* PyQt5
* OpenPyXL
  
---

## Módulo 1: Calibración de cámara

Archivo:

```text
Calibración con Tablero de Ajedrez.py
```

### Función

Este módulo realiza la calibración de una cámara utilizando un tablero tipo ajedrez (checkerboard).

### Objetivo

Obtener parámetros necesarios para corregir distorsiones y mejorar la precisión de los demás módulos.

### Resultados generados

* Matriz de cámara:

```text
camera_matrix.npy
```

* Coeficientes de distorsión:

```text
dist_coeffs.npy
```

### Proceso

1. Detecta esquinas del tablero.
2. Captura diferentes posiciones y ángulos.
3. Calcula parámetros intrínsecos de la cámara.
4. Guarda los resultados.

---

## Módulo 2: Detector de marcadores ArUco

Archivo:

```text
Detector ArUco.py
```

### Función

Detecta marcadores ArUco en tiempo real utilizando una cámara.

### Características

* Detección automática de marcadores.
* Identificación de IDs.
* Dibujo de bordes y puntos centrales.
* Visualización en tiempo real.

### Uso

Permite utilizar los marcadores como referencias para otros sistemas.

---

## Módulo 3: Medición automática de objetos mediante ArUco

Archivo:

```text
Medidor de Objetos con ArUco.py
```

### Función

Utiliza un marcador ArUco como referencia de tamaño real para medir objetos detectados por color.

### Características

* Detección de objetos:

  * Azul
  * Verde
  * Rojo

* Conversión:

```text
Píxeles → centímetros
```

### Proceso

1. Detecta un marcador ArUco.
2. Usa el marcador como escala de referencia.
3. Detecta objetos mediante color.
4. Calcula ancho y alto aproximado.
5. Muestra resultados en tiempo real.

---

## Módulo 4: Seguimiento de trayectoria mediante ArUco

Archivo:

```text
Seguimiento Robot ArUco.py
```

### Función

El objetivo de este módulo era realizar seguimiento de un robot utilizando un marcador ArUco instalado sobre él.

### Características diseñadas

* Detección de un marcador específico.
* Obtención de coordenadas.
* Seguimiento de posiciones.
* Generación de trayectoria.
* Interfaz gráfica mediante PyQt5.
* Exportación de datos a Excel.

### Estado del módulo

Este módulo no pudo ser implementado completamente debido a limitaciones de hardware durante el desarrollo, ya que no se contó con un robot físico disponible para realizar pruebas y validaciones.

A pesar de ello, se desarrolló la lógica principal y se diseñó una pista con marcadores ArUco para futuras implementaciones.

El plano fue incluido dentro del proyecto para que pueda ser utilizado por otros usuarios.

Archivo incluido:

```text
mapa_arucos.pdf
```

---

## Instalación

Instalar dependencias:

```bash
pip install opencv-contrib-python
pip install pyqt5
pip install pandas
pip install openpyxl
pip install numpy

```

## Futuras mejoras

* Integración completa con robot físico.
* Navegación automática.
* Algoritmos de planificación de rutas.
* Seguimiento avanzado.
* Mapeo inteligente.
* Integración con Arduino o Raspberry Pi.

---

## Autor

Leonardo Matias Godoy Riquelme

Proyecto desarrollado con fines académicos y de aprendizaje en visión artificial y robótica.
