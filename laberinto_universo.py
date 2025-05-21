import json
import os

# Ruta del archivo JSON
ruta_archivo = os.path.join(os.path.dirname(__file__), 'public', 'matriz_universo.json')

# Leer el archivo JSON
with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)

# Mostrar los elementos del JSON
print("Tamaño de la matriz:")
print(f"  Filas: {datos['matriz']['filas']}, Columnas: {datos['matriz']['columnas']}")

print("\nOrigen:", datos["origen"])
print("Destino:", datos["destino"])

print("\nAgujeros Negros:")
for agujero in datos["agujerosNegros"]:
    print(" ", agujero)

print("\nEstrellas Gigantes:")
for estrella in datos["estrellasGigantes"]:
    print(" ", estrella)

print("\nAgujeros de Gusano:")
for gusano in datos["agujerosGusano"]:
    print("  Entrada:", gusano["entrada"], "-> Salida:", gusano["salida"])

print("\nZonas de Recarga:")
for zona in datos["zonasRecarga"]:
    print("  Coordenada:", zona[:2], " - Multiplicador:", zona[2])

print("\nCeldas con carga requerida:")
for celda in datos["celdasCargaRequerida"]:
    print("  Coordenada:", celda["coordenada"], " - Carga gastada:", celda["cargaGastada"])

print("\nCarga Inicial de la nave:", datos["cargaInicial"])

# Mostrar una parte de la matriz inicial si es muy grande
print("\nMATRIZ")
for fila in datos["matrizInicial"]:
    print(" ", fila[:], "...")  # muestra solo las primeras 10 columnas de cada fila
