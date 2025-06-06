import json
import os

# Ruta del archivo JSON
ruta_archivo = os.path.join(os.path.dirname(__file__), 'matriz_universo.json')

# Leer el archivo JSON
with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
    datos = json.load(archivo)


# Mostrar los elementos del JSON
print("Tamaño de la matriz:")
print(f"  Filas: {datos['matriz']['filas']}, Columnas: {datos['matriz']['columnas']}")


def backtracking(laberinto, x, y, visitados, resultado, energia):
    filas = laberinto['matriz']['filas']
    columnas = laberinto['matriz']['columnas']
    destino = laberinto['destino']
    
    if x == destino[0] and y == destino[1]:
        resultado.update(visitados)
        return True

    if (x, y) in visitados:
        return False
    
    clave = (x, y)
    if clave in energia_por_celda and energia <= energia_por_celda[clave]:
        return False
    energia_por_celda[clave] = energia


    # Validar límites
    if not (0 <= x < filas and 0 <= y < columnas):
        return False

    # Gasto de energía por celda
    gasto_celda = laberinto['matrizInicial'][x][y]
    energia -= gasto_celda
    if energia < 0:
        return False

    # Celdas con requisito de carga mínima
    for celda in laberinto['celdasCargaRequerida']:
        if celda['coordenada'] == [x, y] and energia < celda['cargaGastada']:
            return False

    # Agujeros negros
    if [x, y] in laberinto['agujerosNegros']:
        return False

    # Estrella gigante destruye 1 agujero negro adyacente
    if [x, y] in laberinto['estrellasGigantes']:
        for dx, dy in [(0,1), (0,-1), (1,0), (-1,0)]:
            adj = [x + dx, y + dy]
            if adj in laberinto['agujerosNegros']:
                laberinto['agujerosNegros'].remove(adj)
                print(f"Estrella en {x},{y} destruye agujero negro en {adj}")
                break

    # Agujero de gusano (redirige la nave)
    for agujero in laberinto['agujerosGusano']:
        if [x, y] == agujero['entrada']:
            print(f"Agujero de gusano de {x,y} a {agujero['salida']}")
            return backtracking(laberinto, agujero['salida'][0], agujero['salida'][1], visitados, resultado, energia)

    # Recarga de energía
    # Recarga de energía (una sola vez por celda)
    zona_recargada = False
    if (x, y) not in visitados:
        for zona in laberinto['zonasRecarga']:
            if [x, y] == zona[:2]:
                energia *= zona[2]
                zona_recargada = True
                print(f"Recarga en {x,y}. Energía ahora: {energia}")
                break


    visitados.add((x, y))

    for dx, dy in [(1,0), (-1,0), (0,1), (0,-1)]:
        nx, ny = x + dx, y + dy
        if backtracking(laberinto, nx, ny, visitados, resultado, energia):
            return True

    visitados.remove((x, y))
    return False

energia_por_celda = {}
visitados = set()
resultado = set()
energia_inicial = datos['cargaInicial']
origen = datos['origen']

encontrado = backtracking(datos, origen[0], origen[1], visitados, resultado, energia_inicial)

print("¿Camino encontrado?", encontrado)
print("Ruta:")
for paso in resultado:
    print(paso)
