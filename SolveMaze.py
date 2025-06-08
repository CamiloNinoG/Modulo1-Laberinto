import json
import os

# Función que permite cargar los datos JSON
def cargar_datos(ruta_archivo):
    with open(ruta_archivo, 'r', encoding='utf-8') as archivo:
        return json.load(archivo)

# Funcion que permite validar si la ubicacion esta en los limites permitidos
def es_valido(x, y, filas, columnas):
    return 0 <= x < filas and 0 <= y < columnas

# Movimientos
def obtener_movimientos():
    return [
        (1, 0),   # abajo
        (-1, 0),  # arriba
        (0, 1),   # derecha
        (0, -1),  # izquierda
        (1, 1),   # diagonal inferior derecha
        (1, -1),  # diagonal inferior izquierda
        (-1, 1),  # diagonal superior derecha
        (-1, -1)  # diagonal superior izquierda
    ]

# Función que permite aplicar recarga si hay una celda de recarga en la posición
def recargar_energia(x, y, energia, zonas_recarga):
    for zx, zy, factor in zonas_recarga:
        if (x, y) == (zx, zy):
            return energia + factor
    return energia

# Funcion que permite obtener los vecinos adyacentes de una celda
def obtener_vecinos_adyacentes(x, y, filas, columnas):
    movimientos = obtener_movimientos()
    vecinos = []
    for dx, dy in movimientos:
        nx, ny = x + dx, y + dy
        if 0 <= nx < filas and 0 <= ny < columnas:
            vecinos.append((nx, ny))
    return vecinos

# Funcion que permite destruir un agujero negro si estamos en una estrellaGigante
def destruir_agujero_negro(laberinto):
    filas = laberinto['matriz']['filas']
    columnas = laberinto['matriz']['columnas']
    matriz_gasto = laberinto['matrizInicial']
    agujeros_negros = laberinto['agujerosNegros']
    estrellas = laberinto['estrellasGigantes']

    # Convertimos agujeros a conjunto para fácil eliminación
    agujeros_set = set(tuple(a) for a in agujeros_negros)

    for estrella in estrellas:
        vecinos = obtener_vecinos_adyacentes(estrella[0], estrella[1], filas, columnas)
        for vecino in vecinos:
            if vecino in agujeros_set:
                # Destruir agujero negro: lo removemos del set
                agujeros_set.remove(vecino)
                # Actualizar matriz gasto para que sea 0 (sin gasto, libre)
                matriz_gasto[vecino[0]][vecino[1]] = 0
                break  # solo destruye uno por estrella

    # Actualizar la lista original en laberinto
    laberinto['agujerosNegros'] = [list(pos) for pos in agujeros_set]


def obtener_salida_agujero_gusano(pos, agujeros_gusano_act):
    for i, agujero in enumerate(agujeros_gusano_act):
        if agujero['entrada'] == list(pos):
            return i, tuple(agujero['salida'])
    return None, None


# Función de la logica principal del backtracking
def backtracking(laberinto, x, y, camino, energia_actual, energia_por_celda, agujeros_negros_act, agujeros_gusano_act):
    filas = laberinto['matriz']['filas']
    columnas = laberinto['matriz']['columnas']
    destino = laberinto['destino']
    matriz_gasto = laberinto['matrizInicial']

    if not es_valido(x, y, filas, columnas):
        return False

    if (x, y) in [pos for pos, _ in camino]:
        return False

    if [x, y] in agujeros_negros_act:
        return False

    gasto = matriz_gasto[x][y]
    energia_restante = energia_actual - gasto
    if energia_restante < 0:
        return False

    if (x, y) in energia_por_celda and energia_restante <= energia_por_celda[(x, y)]:
        return False

    energia_por_celda[(x, y)] = energia_restante
    camino.append(((x, y), energia_restante))

    if [x, y] in laberinto.get('estrellasGigantes', []):
        vecinos = obtener_vecinos_adyacentes(x, y, filas, columnas)
        for vecino in vecinos:
            if list(vecino) in agujeros_negros_act:
                agujeros_negros_act.remove(list(vecino))
                matriz_gasto[vecino[0]][vecino[1]] = 0
                break

    idx_gusano, salida = obtener_salida_agujero_gusano((x, y), agujeros_gusano_act)
    if salida:
        agujeros_gusano_act.pop(idx_gusano)
        # Seguir desde la salida, pasando el camino y energía actual (ya descontada)
        if backtracking(laberinto, salida[0], salida[1], camino, energia_restante, energia_por_celda, agujeros_negros_act.copy(), agujeros_gusano_act.copy()):
            return True
        # Si no funciona, deshacer el pop para esta rama
        agujeros_gusano_act.insert(idx_gusano, {'entrada': list((x,y)), 'salida': list(salida)})

    if [x, y] == destino:
        return True

    for dx, dy in obtener_movimientos():
        if backtracking(laberinto, x + dx, y + dy, camino, energia_restante, energia_por_celda, agujeros_negros_act.copy(), agujeros_gusano_act.copy()):
            return True

    camino.pop()
    return False


def resolver_laberinto(laberinto):
    origen = laberinto['origen']
    energia_inicial = laberinto['cargaInicial']
    camino = []
    energia_por_celda = {}
    agujeros_negros_act = laberinto.get('agujerosNegros', []).copy()
    agujeros_gusano_act = laberinto.get('agujerosGusano', []).copy()
    exito = backtracking(laberinto, origen[0], origen[1], camino, energia_inicial, energia_por_celda, agujeros_negros_act, agujeros_gusano_act)
    return exito, camino

def imprimir_resultado(encontrado, camino):
    print("¿Camino encontrado?", encontrado)
    if encontrado:
        print("\nPasos del camino:")
        for paso, energia in camino:
            print(f"Posición: {paso}, Energía restante: {energia}")
    else:
        print("No se encontró un camino con la energía disponible.")

# === Main ===
if __name__ == "__main__":
    ruta = os.path.join(os.path.dirname(__file__), 'public/matriz_universo.json')
    datos = cargar_datos(ruta)
    exito, camino = resolver_laberinto(datos)
    imprimir_resultado(exito, camino)
