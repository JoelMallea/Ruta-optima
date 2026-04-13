from flask import Flask, render_template_string, request
import networkx as nx
import folium
from geopy.distance import geodesic

app = Flask(__name__)

# 1. Base de Datos Completa: Las 24 Capitales de Departamento del Perú
capitales = {
    "Amazonas": (-6.2294, -77.8728), "Ancash": (-9.5278, -77.5278), "Apurímac": (-13.6339, -72.8814),
    "Arequipa": (-16.4090, -71.5375), "Ayacucho": (-13.1588, -74.2239), "Cajamarca": (-7.1638, -78.5003),
    "Callao": (-12.0560, -77.1181), "Cusco": (-13.5319, -71.9675), "Huancavelica": (-12.7826, -74.9727),
    "Huánuco": (-9.9306, -76.2422), "Ica": (-14.0678, -75.7286), "Junín": (-12.0651, -75.2045),
    "La Libertad": (-8.1160, -79.0299), "Lambayeque": (-6.7711, -79.8441), "Lima": (-12.0464, -77.0428),
    "Loreto": (-3.7491, -73.2538), "Madre de Dios": (-12.5933, -69.1833), "Moquegua": (-17.1983, -70.9357),
    "Pasco": (-10.6675, -76.2567), "Piura": (-5.1945, -80.6328), "Puno": (-15.8402, -70.0219),
    "San Martín": (-6.4850, -76.3597), "Tacna": (-18.0117, -70.2536), "Tumbes": (-3.5669, -80.4515),
    "Ucayali": (-8.3791, -74.5539)
}

# 2. Conexiones Lógicas (Grafo Vial Simplificado)
conexiones = [
    ("Tumbes", "Piura"), ("Piura", "Lambayeque"), ("Lambayeque", "La Libertad"),
    ("La Libertad", "Ancash"), ("Ancash", "Lima"), ("Lima", "Callao"), ("Lima", "Ica"),
    ("Ica", "Arequipa"), ("Arequipa", "Moquegua"), ("Moquegua", "Tacna"),
    ("Lima", "Junín"), ("Junín", "Pasco"), ("Pasco", "Huánuco"), ("Huánuco", "San Martín"),
    ("San Martín", "Amazonas"), ("Amazonas", "Cajamarca"), ("Cajamarca", "La Libertad"),
    ("Junín", "Huancavelica"), ("Huancavelica", "Ayacucho"), ("Ayacucho", "Apurímac"),
    ("Apurímac", "Cusco"), ("Cusco", "Puno"), ("Puno", "Arequipa"),
    ("Cusco", "Madre de Dios"), ("Huánuco", "Ucayali"), ("Loreto", "Amazonas"), ("Loreto", "Ucayali")
]

def obtener_ruta_optima(origen, destino):
    G = nx.Graph()
    for ciudad, coords in capitales.items():
        G.add_node(ciudad, pos=coords)
    for u, v in conexiones:
        dist = geodesic(capitales[u], capitales[v]).km
        G.add_edge(u, v, weight=dist)
    
    try:
        ruta = nx.dijkstra_path(G, origen, destino, weight='weight')
        distancia = nx.dijkstra_path_length(G, origen, destino, weight='weight')
        return ruta, distancia
    except: return None, 0

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Dijkstra Perú - 24 Departamentos</title>
    <style>
        body { margin: 0; display: flex; font-family: sans-serif; height: 100vh; background: #eee; }
        .sidebar { width: 320px; background: #1a1a1a; color: white; padding: 20px; z-index: 1000; overflow-y: auto; }
        .map-box { flex-grow: 1; }
        select, button { width: 100%; padding: 12px; margin: 8px 0; border-radius: 4px; border: none; font-size: 14px; }
        button { background: #007bff; color: white; cursor: pointer; font-weight: bold; }
        .resumen { background: #333; padding: 15px; border-radius: 5px; margin-top: 20px; border-left: 4px solid #007bff; }
        h2 { color: #007bff; margin-top: 0; }
    </style>
</head>
<body>
    <div class="sidebar">
        <h2>Ruta Dijkstra Perú</h2>
        <form method="POST">
            <label>Origen:</label>
            <select name="origen">
                {% for c in lista %}<option value="{{c}}" {% if c == o_sel %}selected{% endif %}>{{c}}</option>{% endfor %}
            </select>
            <label>Destino:</label>
            <select name="destino">
                {% for c in lista %}<option value="{{c}}" {% if c == d_sel %}selected{% endif %}>{{c}}</option>{% endfor %}
            </select>
            <button type="submit">CALCULAR RUTA</button>
        </form>
        {% if dist > 0 %}
        <div class="resumen">
            <p><strong>Distancia:</strong> {{ dist|round(2) }} km</p>
            <p><strong>Nodos:</strong> {{ " -> ".join(ruta) }}</p>
        </div>
        {% endif %}
    </div>
    <div class="map-box">{{ mapa|safe }}</div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def main():
    o, d = "Puno", "Lima"
    ruta, dist = [], 0
    if request.method == 'POST':
        o, d = request.form.get('origen'), request.form.get('destino')
        ruta, dist = obtener_ruta_optima(o, d)

    m = folium.Map(location=[-9.19, -75.01], zoom_start=6)
    
    # Marcamos TODOS los departamentos en el mapa
    for depto, coords in capitales.items():
        folium.CircleMarker(coords, radius=4, color="black", fill=True, popup=depto).add_to(m)

    if ruta:
        puntos = [capitales[n] for n in ruta]
        folium.PolyLine(puntos, color="blue", weight=5, opacity=0.7).add_to(m)
        folium.Marker(puntos[0], icon=folium.Icon(color='green', icon='play')).add_to(m)
        folium.Marker(puntos[-1], icon=folium.Icon(color='red', icon='stop')).add_to(m)

    return render_template_string(HTML_TEMPLATE, lista=sorted(capitales.keys()), 
                                  mapa=m._repr_html_(), dist=dist, ruta=ruta, o_sel=o, d_sel=d)

if __name__ == '__main__':
    app.run(debug=True)