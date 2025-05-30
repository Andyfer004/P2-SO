# 🎛️ Simulador de Sistemas Operativos

**Universidad del Valle de Guatemala**  
**Curso:** Sistemas Operativos  
**Docentes:** Sebastián Galindo, Juan Luis García, Juan Carlos Canteo  
**Estudiante:** Andy Fuentes 
**Fecha de entrega:** 30 de mayo de 2025  

---

## Descripción

Este proyecto es un simulador visual interactivo desarrollado en **Python** con **Streamlit** y **Plotly**, cuyo objetivo es reforzar los conceptos de:

- Planificación de procesos (scheduling)
- Concurrencia y sincronización (mutex y semáforos)

La aplicación permite la carga dinámica de archivos `.txt` y la visualización de algoritmos de planificación y sincronización en tiempo real mediante diagramas de Gantt animados.

---

## Funcionalidades

### A. Simulador de Algoritmos de Calendarización

#### Algoritmos soportados:
- ✅ FIFO (First In First Out)  
- ✅ SJF (Shortest Job First)  
- ✅ SRTF (Shortest Remaining Time First)  
- ✅ RR (Round Robin con quantum configurable)  
- ✅ Priority Scheduling

#### Características:
- Carga dinámica desde `processes.txt`
- Visualización dinámica con animación paso a paso
- Diagrama de Gantt con scroll horizontal
- Cálculo del **Avg Waiting Time**

---

### B. Simulador de Sincronización

#### Mecanismos soportados:
- ✅ Mutex
- ✅ Semáforos

#### Archivos requeridos:
- `processes.txt` → Procesos con BT, AT y prioridad  
- `resources.txt` → Recursos con contador inicial  
- `actions.txt` → Acciones READ/WRITE con ciclo

#### Visualización:
- Línea de tiempo animada con estados: 🟩 `ACCESSED` y 🟥 `WAITING`
- Scroll dinámico si excede el espacio visual disponible

---

## 📂 Formato de Archivos

### 📝 processes.txt
```
<PID>, <BT>, <AT>, <Priority>
```
Ejemplo:
```
P1, 8, 0, 1
P2, 6, 2, 2
```

### 📝 resources.txt
```
<RESOURCE_NAME>, <COUNT>
```
Ejemplo:
```
R1, 1
R2, 2
```

### 📝 actions.txt
```
<PID>, <ACTION>, <RESOURCE>, <CYCLE>
```
Ejemplo:
```
P1, READ, R1, 0
P2, WRITE, R2, 3
```

---

## 🧪 Cómo ejecutar

1. Instala Python 3.9+  
2. Instala dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta el simulador:
```bash
streamlit run src/main.py
```

---

## 📦 Estructura del Proyecto

```
src/
├── main.py
├── scheduling.py
├── synchronization.py
├── loader.py
└── visualizer.py
inputs/
├── processes.txt
├── resources.txt
└── actions.txt
README.md
requirements.txt
```

---

## ✅ Requerimientos cumplidos

- [x] Calendarización dinámica y visual
- [x] Implementación completa de los algoritmos
- [x] Simulación con semáforos y mutex
- [x] Validación robusta de entradas (programación defensiva)
- [x] GUI intuitiva con scroll y animación

---

## 👤 Autor

- Andy Fuentes
- Fue22944@mail.com

---
