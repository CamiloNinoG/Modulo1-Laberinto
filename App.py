import streamlit as st
import json
import os
import time
from SolveMaze import resolver_laberinto
from SolveMaze import imprimir_resultado

st.set_page_config(layout="wide")

ruta_archivo = os.path.join(os.path.dirname(__file__), 'public', 'matriz_universo.json')
with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)

filas = datos['matriz']['filas']
columnas = datos['matriz']['columnas']
matriz_valores = datos["matrizInicial"]
matriz_visual = [[str(matriz_valores[i][j]) for j in range(columnas)] for i in range(filas)]

# === Colocar símbolos especiales ===
def colocar_simbolo(x, y, simbolo):
    matriz_visual[x][y] = simbolo
    
def imprimir_resultado_interfaz(encontrado, camino):
    st.subheader("Resultado de la búsqueda")
    
    st.write("¿Camino encontrado?:", "Sí" if encontrado else "No")
    
    if encontrado:
        st.markdown("Pasos del camino:")
        for paso, energia in camino:
            st.markdown(f"-Posición: `{paso}`, Energía restante: `{energia}`")
    else:
        st.warning("No se encontró un camino con la energía disponible.")

colocar_simbolo(*datos["origen"], "🛫")
colocar_simbolo(*datos["destino"], "🛬")

for agujero in datos["agujerosNegros"]:
    colocar_simbolo(*agujero, "⚫")

for estrella in datos["estrellasGigantes"]:
    colocar_simbolo(*estrella, "⭐")

for gusano in datos["agujerosGusano"]:
    colocar_simbolo(*gusano["entrada"], "🌀")
    colocar_simbolo(*gusano["salida"], "🌀")

for zona in datos["zonasRecarga"]:
    x, y, _ = zona
    colocar_simbolo(x, y, "🔋")

# for celda in datos["celdasCargaRequerida"]:
#     x, y = celda["coordenada"]
#     colocar_simbolo(x, y, "⚡")

# === Leyenda e interfaz ===
st.title("Visualización de la Matriz del Universo")
st.markdown("### Significado Simbolos:")
st.write("🛫 Origen")
st.write("🛬 Destino")
st.write("⚫ Agujero Negro")
st.write("⭐ Estrella Gigante")
st.write("🌀 Agujero de Gusano")
st.write("🔋 Zona de Recarga")
st.write("⚡ Celda con carga requerida")

# === Función para generar HTML de la matriz ===
def generar_html(ruta_coords=set()):
    html = """
    <style>
        table {
            border-collapse: collapse;
            font-family: monospace;
            font-size: 15px;
        }
        td {
            border: 1px solid #999;
            padding: 5px 5px;
            text-align: center;
            min-width: 5px;
        }
    </style>
    <table>
    """
    for i in range(filas):
        html += "<tr>"
        for j in range(columnas):
            celda = matriz_visual[i][j]
            estilo = ""
            if (i, j) in ruta_coords and celda == "🚀":
                estilo = ' style="background-color: lightblue;"'
            html += f"<td{estilo}>{celda}</td>"
        html += "</tr>"
    html += "</table>"
    return html

# === Área para mostrar la matriz ===
espacio_matriz = st.empty()

# === Cargar datos desde JSON ===
ruta = os.path.join(os.path.dirname(__file__), 'matriz_universo.json')


# === Mostrar matriz inicial antes de animación ===
st.markdown("### Matriz del Universo (inicial)")
espacio_matriz = st.empty()
html_inicial = generar_html()
espacio_matriz.markdown(html_inicial, unsafe_allow_html=True)

# === Botón para ejecutar animación ===
if st.button("🚀 Ejecutar algoritmo con animación"):
    encontrado, ruta_coords = resolver_laberinto(datos)
    st.write(encontrado)
    
    if encontrado:
        ruta_ordenada = [tuple(coord_info[0]) for coord_info in ruta_coords]
        
        
        for i, (x, y) in enumerate(ruta_ordenada):
            if matriz_visual[x][y] not in ["🛫", "🛬"]:
                colocar_simbolo(x, y, "🚀")
            html_actualizado = generar_html(set(ruta_ordenada[:i + 1]))
            espacio_matriz.markdown(html_actualizado, unsafe_allow_html=True)
            time.sleep(0.1)
            
        st.success("¡Ruta animada mostrada con éxito!")

        imprimir_resultado_interfaz(encontrado, ruta_coords)
    else:
        st.error("No se encontró una ruta válida.")

