# E747 EmbeddedML Abschlussprojekt

## ArUco-basierte visuelle Navigation mit dem LeKiwi Roboter

Dieses Projekt implementiert eine kamerabasierte Navigation für den mobilen
LeKiwi Roboter. Mithilfe von ArUco-Markern werden Objekte im Kamerabild erkannt
und ihre relative Position zur Kamera bestimmt.

Der Roboter kann mehrere Marker gleichzeitig erkennen und deren Position
schätzen. Für die Navigation wird jedoch nur ein zuvor definierter Zielmarker
verwendet. Der LeKiwi soll diesem Marker folgen und einen definierten Abstand
zum Ziel einhalten.

Die Bildverarbeitung und Navigation laufen lokal auf dem Raspberry Pi 5 des
LeKiwi. 

### Thema: ArUco-basierte visuelle Navigation mit dem LeKiwi Roboter

- **Autor 1:** Kebab, Mohamad Laith

#### Motivation

Für autonome mobile Roboter ist es notwendig, Objekte in ihrer Umgebung nicht
nur zu erkennen, sondern auch deren relative Position zu bestimmen und daraus
geeignete Bewegungen abzuleiten.

ArUco-Marker bieten hierfür eine einfache und robuste Möglichkeit. Jeder Marker
besitzt eine eindeutige ID und kann mit Verfahren der Computer Vision zuverlässig
im Kamerabild erkannt werden. Bei bekannter Markergröße und kalibrierter Kamera
kann zusätzlich die räumliche Position und Orientierung des Markers relativ zur
Kamera berechnet werden.

Ziel dieses Projekts ist es, eine vollständige Verarbeitungskette von der
Kameraaufnahme bis zur Bewegungsentscheidung des Roboters zu entwickeln. Der
LeKiwi soll mehrere Marker erkennen können, aber ausschließlich einem
definierten Zielmarker folgen.
Dabei soll die implementierte Modul Struktur mögliche Erweiterungen vereinfachen,
denn die implementierte Navigation isst einer von zahlreichen möglichen Anwendungen der ArUco Posenschätzung. 
Auch soll eine implementierung der Vision Module auf andere Plattforme wie Roboterarme und andere mobile Roboter
durch die definierten Schnittstellen möglich sein.

Die persönliche Motivation für das Projekt ist deren Durchführung für das LeoBots Team der HTWK Leipzig. Das Team könnte von diesen Modulen sowohl für den LEkiwi als auch für andere Roboterprojekte profitieren.

#### Methoden

Die Umsetzung besteht aus mehreren aufeinanderfolgenden Verarbeitungsschritten.

**1. Kamerakalibrierung**

Vor der Positionsbestimmung wird die verwendete Kamera mit einem
Schachbrettmuster kalibriert. Dabei werden die intrinsischen Kameraparameter
sowie die Koeffizienten der Linsenverzerrung bestimmt.

Die Kalibrierungsparameter werden gespeichert und anschließend für die
Pose-Schätzung der Marker verwendet.

**2. ArUco-Marker-Erkennung**

Die Marker werden mit der ArUco-Funktionalität von OpenCV erkannt. Für jeden
gefundenen Marker werden

- die Marker-ID und
- die vier Eckpunkte im Kamerabild

bestimmt.

Dadurch können mehrere Marker gleichzeitig erkannt und voneinander
unterschieden werden.

**3. Pose Estimation**

Aus den vier erkannten Bildecken, der bekannten realen Markergröße (Seitenlänge) und den
intrinsischen Kameraparametern wird die Pose jedes Markers relativ zur Kamera
bestimmt.

Dafür wird OpenCV `solvePnP()` mit dem Verfahren
`SOLVEPNP_IPPE_SQUARE` verwendet, das für quadratische planare Objekte geeignet
ist.

Als Ergebnis werden

- ein Rotationsvektor und
- ein Translationsvektor

berechnet.

Der Translationsvektor beschreibt die relative Position des Markers im
Kamerakoordinatensystem. Für die Navigation am Boden sind insbesondere

- `x`: seitlicher Abstand und
- `z`: Abstand in Blickrichtung der Kamera

relevant.

**4. Zielauswahl und Navigation**

Für die Navigation wird eine bestimmte Marker-ID als Ziel festgelegt.
Andere Marker können weiterhin erkannt und lokalisiert werden, beeinflussen
die Bewegung des Roboters jedoch nicht.

Ein einfacher Follow-Controller erzeugt abhängig von der gemessenen
Zielposition diskrete Bewegungsbefehle:

- `MOVE_LEFT`
- `MOVE_RIGHT`
- `MOVE_FORWARD`
- `MOVE_BACKWARD`
- `STOP`

Dabei werden Toleranzbereiche für den seitlichen Fehler und den gewünschten
Abstand verwendet. Dadurch soll verhindert werden, dass der Roboter aufgrund
kleiner Messschwankungen ständig zwischen verschiedenen Bewegungen wechselt.

Wird der Zielmarker nicht erkannt, wird als sicherer Standardzustand `STOP`
verwendet.

**5. Integration in LeKiwi**

Für die reale Roboterplattform wurde eine separate Schnittstelle zu LeRobot
implementiert.

Über diese Schnittstelle werden

- Frames der Frontkamera gelesen und
- Bewegungsbefehle für die holonome LeKiwi-Basis ausgegeben.
 
Die Bildverarbeitung, Pose Estimation und Navigation können dadurch lokal auf
dem Raspberry Pi 5 des Roboters ausgeführt werden.

Die bestehende Vision- und Navigationslogik bleibt von der verwendeten Hardware
weitgehend unabhängig.

---

#### Ergebnisse

Die ArUco-Erkennung wurde zunächst mit einer externen Webcam entwickelt und
getestet. Mehrere Marker können gleichzeitig erkannt und anhand ihrer IDs
unterschieden werden.

Nach der Kamerakalibrierung konnte mit der Pose Estimation die relative
3D-Position der Marker bestimmt werden. Vergleichsmessungen mit bekannten
Abständen zeigten plausible Werte für die berechnete Entfernung.

Der Follow-Controller wurde zunächst ohne reale Roboterbewegung getestet.
Abhängig von Position und Entfernung des Zielmarkers werden die erwarteten
Bewegungsbefehle erzeugt. Marker mit anderen IDs werden zwar erkannt und
lokalisiert, aber für die Navigation ignoriert.

Die Anbindung der Frontkamera des LeKiwi über LeRobot wurde ebenfalls getestet.
Die Kamera liefert Bilder mit einer Auflösung von 640 × 480 Pixeln direkt an
die Bildverarbeitung auf dem Raspberry Pi.

Die abschließende Demonstration verwendet zwei ArUco-Marker mit den IDs 0
und 2. Beide Marker werden erkannt und lokalisiert. Marker 0 ist als
Navigationsziel definiert, sodass der Roboter ausschließlich auf dessen
Position reagieren soll.

Während des Hardwaretests wurden einige Parameter angepasst um die Ergebnisse zu verbessern.
Dabei wurden verschiedene Geschwindigkeiten getestet. Bei der Validierung der gemessenen Abstände mit der Lekiwi Kamera
schienen die Abweichungen größer als im Webcam Test, obwohl der Reproduction Error beider Kalibrierungen ähnliche Werte lieferte.
Grund dafür war dass die gedruckten ArUco Marker für den Test am Roboter doch eine Seitenlänge von 9,5 cm statt 10,0 cm hatten.
Nach der Korrektur der Seitenlänge wurden die Ergebnisse verbessert.

---

## Demonstration

Für die Demonstration wurden eineige Videos aufgenommen. Einige Videos zeigen die grundsätzliche Posenschätzung
mehrerer IDs, während andere Videos zwei bewegliche Objekte mit den ArUco-Markern
ID 0 und ID 2 verwenden, um die Navigation zu zeigen.

Die Demonstrationen zeigen:

1. gleichzeitige Erkennung mehrerer Marker,
2. Berechnung ihrer relativen Position,
3. Auswahl von Marker ID 0 als Navigationsziel,
4. Ignorieren der Marker ID 2 für die Navigation,
5. Bewegung des Roboters in Richtung des Zielmarkers,
6. Einhalten eines definierten Zielabstands,
7. Stoppen des Roboters, wenn der Zielmarker nicht mehr erkannt wird.

### Video

Zum Playlist mit den Demovideos:

---

## Quellcode

Der entwickelte Quellcode befindet sich im Ordner:

`1_Quellcode`

Die wichtigsten Komponenten sind:

- `vision/aruco_detector.py` – Erkennung und Identifikation der ArUco-Marker
- `vision/pose_estimator.py` – Berechnung von Rotation und Translation
- `navigation/follow_controller.py` – Erzeugung der Navigationsbefehle
- `robot/lekiwi_interface.py` – Schnittstelle zur LeKiwi-Hardware
- `main.py` – Entwicklung und Tests mit externer Webcam
- `main_lekiwi.py` – Integration auf dem LeKiwi/Raspberry Pi
- `calibration/` – Aufnahme und Berechnung der Kamerakalibrierung

An einigen Stellen im Code können die definierten Pfade für Speicherung und Aufruf
von Daten wie Kalibrierbilder oder Ergebnisse der Kamerakalibrierung sowie Parameter für die 
Roboterkonfiguration oder Seitenlänge der Marker angepasst werden. Diese Stellen sind im Code entsprechend dokumentiert.

---
