import streamlit as st
import json

st.set_page_config(layout="wide")
# Cargar datos
ruta_archivo = 'matriz_universo.json'
with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)

# Dimensiones de la matriz
filas = datos['matriz']['filas']
columnas = datos['matriz']['columnas']

# Cargar la matriz inicial de valores
matriz_valores = datos["matrizInicial"]

# Crear matriz visual con los valores por defecto
matriz_visual = [[str(matriz_valores[i][j]) for j in range(columnas)] for i in range(filas)]

# Función para sobrescribir una celda con un símbolo
def colocar_simbolo(x, y, simbolo):
    matriz_visual[x][y] = simbolo

# Origen y destino
colocar_simbolo(*datos["origen"], "🛫")
colocar_simbolo(*datos["destino"], "🛬")

# Agujeros Negros
for agujero in datos["agujerosNegros"]:
    colocar_simbolo(*agujero, "⚫")

# Estrellas Gigantes
for estrella in datos["estrellasGigantes"]:
    colocar_simbolo(*estrella, "⭐")

# Agujeros de Gusano
for gusano in datos["agujerosGusano"]:
    colocar_simbolo(*gusano["entrada"], "🌀")
    colocar_simbolo(*gusano["salida"], "🌀")

# Zonas de Recarga
for zona in datos["zonasRecarga"]:
    x, y, _ = zona
    colocar_simbolo(x, y, "🔋")

# Celdas con carga requerida
for celda in datos["celdasCargaRequerida"]:
    x, y = celda["coordenada"]
    colocar_simbolo(x, y, "⚡")

# Mostrar en Streamlit
st.title("Visualización de la Matriz del Universo")

st.markdown("### Leyenda:")
st.write("🛫 Origen")
st.write("🛬 Destino")
st.write("⚫ Agujero Negro")
st.write("⭐ Estrella Gigante")
st.write("🌀 Agujero de Gusano")
st.write("🔋 Zona de Recarga")
st.write("⚡ Celda con carga requerida")

st.markdown("### Matriz Visual con valores:")

# # Mostrar cada fila con las celdas separadas
# for fila in matriz_visual:
#     st.write(" ||| ".join(fila))

# Crear tabla HTML cuadriculada
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

for fila in matriz_visual:
    html += "<tr>"
    for valor in fila:
        html += f"<td>{valor}</td>"
    html += "</tr>"

html += "</table>"

# Mostrar la tabla en Streamlit
st.markdown(html, unsafe_allow_html=True)