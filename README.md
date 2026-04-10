# 📊 Sistema de Análisis Predictivo — Compresor de Propano K-660
### Planta de Ajuste de Dew Point — Percheles | Bolivia, Sector Hidrocarburos

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![TensorFlow](https://img.shields.io/badge/TensorFlow-2.x-orange?logo=tensorflow)](https://www.tensorflow.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-dashboard-red?logo=streamlit)](https://streamlit.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green)](LICENSE)

---

## 🏭 Contexto Industrial

La **Planta de Ajuste de Dew Point — Percheles** reduce el punto de rocío del gas natural mediante refrigeración mecánica con propano, condensando hidrocarburos pesados (C3+) y agua para cumplir especificaciones de transporte y venta en la red de gas boliviana.

El **compresor de tornillo K-660** es el nodo central del sistema: modula su carga continuamente para satisfacer la demanda frigorífica total de la planta. Cualquier degradación del proceso — ensuciamiento de intercambiadores, pérdida de eficiencia del aeroenfriador, cambio en composición del gas — se refleja directamente en sus variables de operación.

**Objetivo del proyecto:** construir un sistema completo de análisis de datos, detección de anomalías y predicción del comportamiento del K-660 a partir de datos reales exportados del sistema SCADA de planta.

---

## 📁 Estructura del Repositorio

```
dew_point_k660/
├── dew_point_analisis_completo.py   ← Script maestro (Niveles 1–8)
├── app.py                           ← Dashboard interactivo Streamlit
├── requirements.txt                 ← Dependencias del proyecto
├── README.md                        ← Este archivo
├── .gitignore
├── data/
│   └── dew_point_clean.csv          ← Dataset procesado (raw no incluido)
└── outputs/
    ├── index.html                   ← Reporte HTML autocontenido
    ├── reporte_k660_dew_point.pdf   ← Reporte PDF con portada institucional
    └── fig1_series_temporales_k660.png ... fig18_gru_comparativo.png
```

---

## 📐 Dataset

| Parámetro | Valor |
|---|---|
| Fuente | HMI / SCADA Chacos — exportación Excel |
| Archivo original | `Dew Point Mensual_pro.xlsx` |
| Período | 07/03/2026 → 07/04/2026 (31 días continuos) |
| Registros | 44,640 (muestreo cada 1 minuto, sin gaps) |
| Variables con datos | 16 tags de proceso + 1 variable calculada |
| Variables pendientes SCADA | 4 (DPT_603, DPT_621, DPT_620, DPT_662) |

### Variables principales

| Tag | Descripción | Unidad | Rol |
|---|---|---|---|
| PT_664 | Presión descarga K-660 | PSI | Variable objetivo principal |
| TE_664 | Temperatura descarga K-660 | °F | Variable objetivo GRU Modelo B |
| TT_655 | Temperatura salida aeroenfriador AC-655 | °F | Driver dominante (r = 0.994) |
| TT_620 | Temperatura separador frío V-620 | °F | Driver secundario (r = 0.697) |
| TE_661/662 | Temperatura cojinetes | °F | Condición mecánica |
| TE_663 | Temperatura aceite lubricación | °F | Sistema de lubricación |
| PT_603/600 | Presión entrada / salida planta | PSI | dP_Planta (proxy ensuciamiento) |

---

## 🏗️ Arquitectura del Script — 8 Niveles

```
NIVEL 1 ── Ingesta, limpieza y estadística descriptiva
NIVEL 2 ── Análisis temporal de operación (perfiles, tendencias)
NIVEL 3 ── Drivers de carga del K-660 (correlación + regresión)
NIVEL 4 ── Operación normal y detección de anomalías (Z-Score dinámico)
NIVEL 5 ── Modelo predictivo GRU (Deep Learning — TensorFlow/Keras)
NIVEL 6 ── Exportar reporte a PDF (matplotlib PdfPages)
NIVEL 7 ── Exportar reporte HTML autocontenido (Base64)
NIVEL 8 ── Guía de despliegue GitHub / Streamlit / Render.com
```

---

## 📈 Resultados Clave

### Análisis estadístico y de drivers

- **TT_655 vs PT_664:** r = **0.994** — el aeroenfriador explica el **98.7%** de la variación de carga
- **Modelo lineal:** `PT_664 = 2.243 × TT_655 + 0.048 × TT_620 − 46.45` | R² = 98.74%
- **Impacto:** cada 1°F adicional en TT_655 genera **+2.25 PSI** en descarga
- **Patrón diario:** pico a las 14:00 hrs (176 PSI) · valle a las 05:00 hrs (140 PSI) · variación 35.8 PSI (23%)
- **Tendencia cojinetes:** +0.094 °F/día — estable, sin señal de degradación en el período
- **dP_Planta:** tendencia −0.03 PSI/día — sin ensuciamiento acumulado

### Detección de anomalías (Z-Score dinámico, ventana 60 min)

| Clasificación | Registros | Porcentaje |
|---|---|---|
| Normal | 41,456 | 92.87% |
| Alerta | 2,614 | 5.86% |
| Crítico | 570 | 1.28% |

- **178 eventos anómalos** detectados con duración ≥ 3 minutos

### Modelos GRU (Deep Learning)

**Arquitectura:** `GRU(64) → Dropout(0.20) → GRU(32) → Dropout(0.15) → Dense(16, ReLU) → Dense(1)`  
Parámetros: WINDOW=60 min · SPLIT=85/15 · MAX_EPOCHS=300 · PATIENCE=20 · BATCH=32

| Modelo | Target | MAE | RMSE | MAPE | Épocas | Calificación |
|---|---|---|---|---|---|---|
| GRU-A | PT_664 (PSI) | 1.417 | 1.953 | 0.85% | 29 | ✅ EXCELENTE |
| GRU-B | TE_664 (°F) | 0.681 | 0.872 | 0.52% | 25 | ✅ EXCELENTE |

---

## 🚀 Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/TU_USUARIO/dew-point-k660.git
cd dew-point-k660
```

### 2. Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS
pip install -r requirements.txt
```

### 3. Preparar los datos

Copiar el archivo Excel exportado del SCADA a la raíz del proyecto y actualizar las rutas en la sección `CONFIGURACION` del script principal:

```python
ARCHIVO_DATOS     = r"ruta\a\Dew Point Mensual_pro.xlsx"
ARCHIVO_CABECERAS = r"ruta\a\Dew_Point_Cabeceras_Correctas.xlsx"
CARPETA_SALIDA    = r"ruta\a\salida_proyecto"
```

### 4. Ejecutar el análisis completo

```bash
python dew_point_analisis_completo.py
```

El script genera automáticamente en `CARPETA_SALIDA`:
- 18 figuras PNG
- `reporte_k660_dew_point.pdf`
- `index.html` (reporte autocontenido, abre sin internet)
- `dew_point_clean.csv`

### 5. Lanzar el dashboard Streamlit

```bash
streamlit run app.py
```

---

## 🔧 Dependencias

Ver `requirements.txt`. Principales:

| Paquete | Uso |
|---|---|
| pandas / numpy | Manipulación de datos |
| matplotlib / scipy | Visualización y análisis estadístico |
| tensorflow / keras | Modelos GRU de predicción |
| scikit-learn | Normalización (MinMaxScaler) |
| streamlit | Dashboard interactivo |
| openpyxl | Lectura de archivos Excel HMI |

> **Nota:** TensorFlow es opcional. Si no está instalado, el script ejecuta los Niveles 1–4, 6, 7 y 8 sin interrupciones (bloque `try/except` en Nivel 5).

---

## 🔌 Equipos del Sistema (Contexto)

| Tag | Equipo | Función |
|---|---|---|
| K-660 | Compresor tornillo 2 etapas | Nodo central — comprime propano refrigerante |
| E-610 | Chiller tubo-coraza | Intercambiador principal gas/propano |
| AC-655 A/B | Aeroenfriadores | Condensan el propano comprimido |
| V-645 | Economizador | Optimiza el ciclo de refrigeración de 2 etapas |
| V-650 | Acumulador de propano | Inventario del refrigerante |
| V-670 | Separador aceite-refrigerante | Protege el sistema de lubricación |
| E-600/E-605 | Intercambiadores gas/gas | Recuperación de frío |

---

## 📌 Estado del Proyecto

- [x] Script completo Niveles 1–8 funcional y probado
- [x] 18 figuras generadas (15 sin GRU · 18 con GRU)
- [x] PDF con portada institucional
- [x] HTML autocontenido Base64
- [x] Modelos GRU entrenados — métricas excelentes
- [ ] Dashboard Streamlit con filtros dinámicos (`app.py`)
- [ ] Publicación en Streamlit Cloud
- [ ] Publicación HTML en Render.com
- [ ] Variables SCADA pendientes: amperios K-660, AIC_666 CV%, temperatura ambiente

---

## 👤 Autor

**Herland Daniel Melgar Velasquez**  
Ingeniero Electromecánico | PMP · IEC 61511 Functional Safety · CMRP  
Sector Hidrocarburos — Bolivia  

---

## 📄 Licencia

Este proyecto está bajo licencia [MIT](LICENSE). Los datos de proceso son propiedad de la empresa operadora y no se incluyen en el repositorio.
