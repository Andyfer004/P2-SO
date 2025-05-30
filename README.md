# Simulador de Sistemas Operativos

**Universidad del Valle de Guatemala**  
**Curso:** Sistemas Operativos  
**Docentes:** Sebastián Galindo, Juan Luis García, Juan Carlos Canteo  
**Estudiante:** Andy Fuentes 22944  
**Fecha de entrega:** 30 de mayo de 2025  

## Descripción

Este proyecto es un simulador visual desarrollado en **Python** utilizando **Streamlit** y **Plotly**, el cual permite reforzar los conocimientos sobre:

- Algoritmos de **planificación de procesos**
- Mecanismos de **sincronización concurrente** como **mutex** y **semáforos**

El sistema es capaz de cargar archivos `.txt` con procesos, acciones y recursos, y mostrar visualmente el comportamiento del sistema bajo diferentes configuraciones.

---

## Funcionalidades

### A. Simulador de Algoritmos de Calendarización

- Algoritmos soportados:
  - FIFO (First In First Out)
  - SJF (Shortest Job First)
  - SRTF (Shortest Remaining Time First)
  - RR (Round Robin) con quantum configurable
  - Priority Scheduling
- Carga dinámica desde archivo `processes.txt`
- Visualización en tiempo real del diagrama de Gantt
- Cálculo del tiempo promedio de espera (`Avg Waiting Time`)

### B. Simulador de Sincronización

- Modos soportados:
  - Mutex
  - Semáforo
- Carga de:
  - Procesos desde `processes.txt`
  - Recursos desde `resources.txt`
  - Acciones desde `actions.txt`
- Visualización de los estados `ACCESSED` y `WAITING`
- Diagrama de tiempo con scroll horizontal dinámico

---

## 📂 Estructura del Proyecto

```bash
📁 src/
│   ├── main.py                # Archivo principal con interfaz Streamlit
│   ├── scheduling.py          # Lógica de algoritmos de calendarización
│   ├── synchronization.py     # Lógica de mutex y semáforos
│   ├── loader.py              # Carga y validación de archivos
│   └── visualizer.py          # Visualización con Plotly
📁 inputs/
│   ├── processes.txt
│   ├── resources.txt
│   └── actions.txt
📄 README.md
