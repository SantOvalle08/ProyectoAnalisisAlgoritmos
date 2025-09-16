# Proyecto Análisis de Algoritmos Aplicados a Bibliometría

Plataforma automatizada para el análisis bibliométrico de publicaciones científicas sobre inteligencia artificial generativa, desarrollada en el contexto del curso "Análisis de Algoritmos" (2025-2), Universidad del Quindío.

## Descripción

Este repositorio contiene herramientas y scripts para:
- Descargar y unificar datos bibliográficos provenientes de diversas fuentes científicas.
- Implementar y comparar algoritmos de similitud textual (clásicos y de IA generativa) sobre resúmenes académicos.
- Extraer conceptos clave y calcular frecuencias de palabras relacionadas con IA generativa en educación.
- Realizar agrupamientos (clustering) de resúmenes con representación visual tipo dendrograma.
- Visualizar resultados mediante nubes de palabras, mapas de calor y líneas temporales científicas.
- Documentar detalladamente la arquitectura, algoritmos y resultados obtenidos.

## Funcionalidades

- **Descarga y Unificación de Datos:** Automatización para consolidar registros en formatos estándar (BibTex, RIS, CSV) eliminando duplicados.
- **Similitud Textual:** Análisis a través de algoritmos de distancia e inteligencia artificial.
- **Extracción y Análisis de Conceptos:** Estadísticas sobre términos clave en los resúmenes.
- **Clustering Jerárquico:** Agrupación visual y comparación de algoritmos de clusterización.
- **Visualización:** Generación de reportes gráficos y exportación de resultados a PDF.

## Tecnologías

- Python 3.x
- Bibliotecas: pandas, scikit-learn, matplotlib, seaborn, nltk, wordcloud, PyPDF
- Jupyter Notebook para análisis reproducibles

## Uso

1. Clona este repositorio.
2. Instala los requerimientos ejecutando:
pip install -r requirements.txt
3. Sigue los notebooks y scripts descritos en la documentación para cada etapa del análisis.
4. Consulta la [documentación técnica](docs/) para detalles de arquitectura, lógica y visualizaciones.

---

*Proyecto desarrollado para el curso Análisis de Algoritmos, UQ, 2025-2.*
*Santiago Ovalle Cortes, Juan Sebastián Noreña*
