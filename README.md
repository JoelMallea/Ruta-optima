# Ruta-optima
🗺️ Peru Ruta - Dijkstra Algorithm
Este proyecto es una aplicación web interactiva desarrollada con Flask que implementa el Algoritmo de Dijkstra para encontrar la ruta más corta entre las capitales de los 24 departamentos del Perú. La visualización se realiza sobre mapas reales de OpenStreetMap.

🚀 Características
Algoritmo de Dijkstra: Cálculo preciso de la ruta mínima basado en la distancia geodésica (km) entre coordenadas.

Mapa Interactivo: Integración con Folium para mostrar la ruta, marcadores y nodos de red.

Red Vial Lógica: El sistema considera conexiones reales entre departamentos adyacentes.

Interfaz Moderna: Panel lateral para selección de origen/destino y visualización de resultados.

🛠️ Tecnologías Utilizadas
Backend: Python & Flask

Algoritmos de Grafos: NetworkX

Mapas: Folium (OpenStreetMap)

Cálculos Geográficos: Geopy

Frontend: HTML5, CSS3 (JinJa2 Templates)

📋 Requisitos
Antes de correr el proyecto, asegúrate de tener instalado Python 3.x y las siguientes librerías:

Bash
pip install flask networkx folium geopy
💻 Instalación y Uso
Clona este repositorio o descarga el archivo app.py.

Abre una terminal en la carpeta del proyecto.

Ejecuta la aplicación:

Bash
python app.py
Abre tu navegador y dirígete a: http://127.0.0.1:5000

📊 Funcionamiento
El sistema modela a Perú como un grafo no dirigido donde:

Nodos: Son las capitales de los departamentos (Latitud, Longitud).

Aristas: Representan las conexiones viales principales.

Pesos: Se calculan dinámicamente usando la distancia de círculo máximo entre coordenadas para asegurar que el "camino más corto" sea geográficamente óptimo.

💡 Ejemplo de Visualización
Al seleccionar un origen (ej. Puno) y un destino (ej. Lima), el algoritmo procesará los nodos intermedios (ej. Cusco, Junín) y trazará una polilínea en el mapa indicando la distancia total en kilómetros.
