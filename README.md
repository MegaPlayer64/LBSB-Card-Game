# Chacalitos TCG

## 1. Descripción del Proyecto
Chacalitos TCG es un juego de cartas coleccionables (TCG) táctico por turnos 1vs1. El proyecto combina mecánicas de posicionamiento en cuadrícula inspiradas en la estrategia táctica clásica (como *Fire Emblem* o *Advance Wars*), un sistema de gestión de recursos por cartas similar a *PvZ Heroes*, y dinámicas de progresión de personajes.

El motor simula de forma abstracta las interacciones y dinámicas grupales ("Tags") de un entorno escolar en Santiago de Chile, sirviendo como plataforma de desarrollo activo y balanceo matemático para la versión final del juego.

---

## 2. Arquitectura del Motor y Sistema de Juego

### Tablero, Movimiento y Rango de Acción
La simulación se ejecuta sobre una matriz discreta de **5x6 casillas**. 
- Las primeras dos columnas en cada extremo del eje horizontal representan las zonas de invocación controladas por cada jugador; el espacio central actúa como zona neutral de combate. Los jugadores inician con 80 HP y el objetivo es reducir la salud del oponente a 0.

### Entidades y Flujo de Datos
El motor procesa tres tipos abstractos de entidades a través de un paradigma **Orientado a Objetos (POO)**:
1. **Unidades:** Agentes activos con estados dinámicos de posición, ataque, velocidad, rango y salud, capaces de realizar una acción de movimiento y una de ataque por turno bajo las restricciones del mapa.
2. **Hechizos:** Modificadores algorítmicos instantáneos que alteran los estados del tablero, salud o recursos.
3. **Entornos:** Variables globales simétricas que modifican de manera activa las reglas del campo para ambos jugadores simultáneamente.

---

## 3. Especificaciones Técnicas y Portabilidad
- **Lenguaje:** Python 3.x
- **Framework Gráfico:** Kivy (Seleccionado estratégicamente en reemplazo de Pygame para garantizar una óptima gestión de recursos, renderizado nativo y portabilidad eficiente hacia dispositivos móviles).
- **Persistencia de Datos:** Serialización y parseo mediante archivos **CSV** y **JSON** para la gestión de de mazos (40 cartas), atributos y persistencia de la base de datos de cartas en fase Alpha.
- **Plataformas Objetivo:** Windows, Linux, MacOS, Android e iOS.

---

## 4. Estado del Proyecto
Este repositorio representa la **versión principal y en producción activa** del motor. Se actualiza periódicamente mediante un pipeline de desarrollo enfocado en la inyección de nuevas funcionalidades, optimización del código base y corrección iterativa de bugs.

---

## 5. Cómo Ejecutar el Motor (Desarrollo Local)

Asegúrate de tener instalado Python 3 y el framework Kivy en tu entorno.

```bash
# 1. Clonar el repositorio
git clone [https://github.com/MegaPlayer64/LBSB-Card-Game.git](https://github.com/MegaPlayer64/LBSB-Card-Game.git)

# 2. Acceder al directorio del proyecto
cd LBSB-Card-Game

# 3. Instalar las dependencias necesarias
pip install kivy

# 4. Iniciar la aplicación
python main.py