# main_fp_es.py
import os
import copy # ¡Muy importante para la inmutabilidad!

# --- FUNCIONES PURAS Y DE GESTIÓN DE ESTADO ---

def crear_estado_inicial():
    """
    Crea y devuelve el diccionario que representa el estado inicial del juego.
    Es una función pura: siempre devuelve el mismo valor.
    """
    # El mapa base, solo con terreno. Las entidades se definen por separado.
    mapa_base = [
        "##########",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "#........#",
        "##########",
    ]
    
    # Definimos las entidades como diccionarios
    jugador = {'x': 1, 'y': 1, 'caracter': '@', 'hp': 10}
    
    monstruos = [
        {'x': 4, 'y': 3, 'caracter': 'M', 'hp': 3},
        {'x': 5, 'y': 6, 'caracter': 'M', 'hp': 3}
    ]

    # Devolvemos el diccionario de estado completo
    return {
        'mapa': mapa_base,
        'jugador': jugador,
        'monstruos': monstruos,
        'juego_terminado': False,
        'mensaje': "¡Bienvenido al roguelike funcional!"
    }


def renderizar_estado(estado_juego):
    """
    Toma un estado del juego y lo muestra en pantalla.
    Esta función es 'impura' por naturaleza porque interactúa con la terminal.
    """
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Crear una copia en memoria del mapa para poder colocar entidades
    mapa_a_mostrar = [list(fila) for fila in estado_juego['mapa']]
    
    # Colocar al jugador
    jugador = estado_juego['jugador']
    if jugador['hp'] > 0:
        mapa_a_mostrar[jugador['y']][jugador['x']] = jugador['caracter']
        
    # Colocar monstruos vivos
    for monstruo in estado_juego['monstruos']:
        if monstruo['hp'] > 0:
            mapa_a_mostrar[monstruo['y']][monstruo['x']] = monstruo['caracter']
            
    # Imprimir el mapa
    for fila in mapa_a_mostrar:
        print("".join(fila))

    # Imprimir información
    print(f"HP del Jugador: {estado_juego['jugador']['hp']}")
    monstruos_vivos = sum(1 for m in estado_juego['monstruos'] if m['hp'] > 0)
    print(f"Monstruos restantes: {monstruos_vivos}")
    print(estado_juego['mensaje'])


def procesar_entrada(estado_juego, tecla):
    """
    La función pura más importante. Toma el estado actual y una acción,
    y devuelve un NUEVO estado del juego con los cambios aplicados.
    NO MODIFICA el 'estado_juego' original.
    """
    # 1. Crear una copia profunda para garantizar la inmutabilidad
    nuevo_estado = copy.deepcopy(estado_juego)
    
    # 2. Limpiar el mensaje para el nuevo estado
    nuevo_estado['mensaje'] = ""
    
    movimientos = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}
    if tecla not in movimientos:
        nuevo_estado['mensaje'] = "Tecla inválida. Usa W/A/S/D."
        return nuevo_estado # Devolvemos el estado nuevo pero sin cambios de lógica

    # 3. Calcular el nuevo movimiento
    dx, dy = movimientos[tecla]
    jugador = nuevo_estado['jugador']
    nueva_x, nueva_y = jugador['x'] + dx, jugador['y'] + dy

    # 4. Lógica de colisión con el mapa
    ancho_mapa, alto_mapa = len(nuevo_estado['mapa'][0]), len(nuevo_estado['mapa'])
    if not (0 <= nueva_x < ancho_mapa and 0 <= nueva_y < alto_mapa) or \
       nuevo_estado['mapa'][nueva_y][nueva_x] == '#':
        nuevo_estado['mensaje'] = "No puedes moverte ahí."
        return nuevo_estado

    # 5. Lógica de combate
    monstruo_objetivo_idx = -1
    for i, monstruo in enumerate(nuevo_estado['monstruos']):
        if monstruo['x'] == nueva_x and monstruo['y'] == nueva_y and monstruo['hp'] > 0:
            monstruo_objetivo_idx = i
            break
            
    if monstruo_objetivo_idx != -1:
        # Atacar al monstruo (modificando la copia)
        monstruo_atacado = nuevo_estado['monstruos'][monstruo_objetivo_idx]
        monstruo_atacado['hp'] -= 1
        nuevo_estado['mensaje'] = f"¡Atacas al monstruo! Le quedan {monstruo_atacado['hp']} HP."
        if monstruo_atacado['hp'] == 0:
            nuevo_estado['mensaje'] += " ¡El monstruo ha muerto!"
    else:
        # Mover al jugador (modificando la copia)
        nuevo_estado['jugador']['x'] = nueva_x
        nuevo_estado['jugador']['y'] = nueva_y
        
    # 6. Comprobar condición de victoria
    if all(m['hp'] == 0 for m in nuevo_estado['monstruos']):
        nuevo_estado['juego_terminado'] = True
        nuevo_estado['mensaje'] = "¡Felicidades! Has derrotado a todos los monstruos."
        
    # 7. Devolver el estado completamente nuevo
    return nuevo_estado


def bucle_juego(estado_juego):
    """
    El motor principal del juego. Orquesta el flujo de estados.
    """
    renderizar_estado(estado_juego)

    if estado_juego['juego_terminado']:
        return # Termina la ejecución

    tecla = input("Mover (W/A/S/D): ").lower()
    siguiente_estado = procesar_entrada(estado_juego, tecla)
    bucle_juego(siguiente_estado) # Llamada recursiva con el nuevo estado


# --- PUNTO DE ENTRADA DEL PROGRAMA ---
if __name__ == "__main__":
    estado_inicial = crear_estado_inicial()
    bucle_juego(estado_inicial)