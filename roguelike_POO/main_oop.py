import os

# --- CLASE BASE ---
class Entidad:
    """Un objeto genérico para representar al jugador, monstruos, etc."""
    def __init__(self, x, y, caracter, hp):
        self.x = x            
        self.y = y          
        self.caracter = caracter 
        self.hp = hp          

    def mover(self, dx, dy):
        """Mueve la entidad una cierta cantidad."""
        self.x += dx
        self.y += dy

    def recibir_danio(self, cantidad):
        """Reduce el HP de la entidad y maneja la muerte."""
        self.hp -= cantidad
        if self.hp < 0:
            self.hp = 0

# --- CLASES QUE HEREDAN ---
class Jugador(Entidad):
    pass

class Monstruo(Entidad):
    pass

# --- CLASES DE GESTIÓN ---
class MapaJuego:
    def __init__(self, ancho, alto):
        self.ancho = ancho
        self.alto = alto
        self.celdas = [
            list("##########"),
            list("#@.......#"),
            list("#........#"),
            list("#...M....#"),
            list("#........#"),
            list("#........#"),
            list("#....M...#"),
            list("#........#"),
            list("#........#"),
            list("##########"),
        ]

    def es_transitable(self, x, y):
        if not (0 <= x < self.ancho and 0 <= y < self.alto):
            return False
        if self.celdas[y][x] == '#':
            return False
        return True

class Juego:
    """Orquesta todo el juego. Contiene el bucle principal y todos los objetos del juego."""
    def __init__(self):
        self.mapa_juego = MapaJuego(10, 10)
        self.jugador = None
        self.monstruos = []
        self.juego_terminado = False
        self.mensaje = ""
        
        self.configurar_juego()

    def configurar_juego(self):
        """Inicializa el mapa y las entidades basándose en los caracteres del mapa."""
        for y, fila in enumerate(self.mapa_juego.celdas):
            for x, caracter in enumerate(fila):
                if caracter == '@':
                    self.jugador = Jugador(x, y, '@', 10) 
                    self.mapa_juego.celdas[y][x] = '.'
                elif caracter == 'M':
                    self.monstruos.append(Monstruo(x, y, 'M', 3)) 
                    self.mapa_juego.celdas[y][x] = '.'

    def obtener_monstruo_en(self, x, y):
        """Busca un monstruo en una ubicación específica."""
        for monstruo in self.monstruos:
            if monstruo.x == x and monstruo.y == y and monstruo.hp > 0:
                return monstruo
        return None

    def renderizar(self):
        """Dibuja todo en la pantalla."""
        os.system('cls' if os.name == 'nt' else 'clear')

        mapa_a_mostrar = [list(fila) for fila in self.mapa_juego.celdas]

        for monstruo in self.monstruos:
            if monstruo.hp > 0:
                mapa_a_mostrar[monstruo.y][monstruo.x] = monstruo.caracter

        if self.jugador.hp > 0:
            mapa_a_mostrar[self.jugador.y][self.jugador.x] = self.jugador.caracter

        for fila in mapa_a_mostrar:
            print("".join(fila))

        print(f"HP del Jugador: {self.jugador.hp}")
        monstruos_vivos = sum(1 for m in self.monstruos if m.hp > 0)
        print(f"Monstruos restantes: {monstruos_vivos}")
        print(self.mensaje)

    def manejar_entrada(self, tecla):
        """Procesa la entrada del jugador."""
        self.mensaje = ""
        movimientos = {'w': (0, -1), 'a': (-1, 0), 's': (0, 1), 'd': (1, 0)}

        if tecla in movimientos:
            dx, dy = movimientos[tecla]
            nueva_x = self.jugador.x + dx
            nueva_y = self.jugador.y + dy

            if self.mapa_juego.es_transitable(nueva_x, nueva_y):
                monstruo_objetivo = self.obtener_monstruo_en(nueva_x, nueva_y)
                if monstruo_objetivo:
                    monstruo_objetivo.recibir_danio(1)
                    self.mensaje = f"¡Atacas al monstruo! Le quedan {monstruo_objetivo.hp} HP."
                    if monstruo_objetivo.hp == 0:
                        self.mensaje += " ¡El monstruo ha muerto!"
                else:
                    self.jugador.mover(dx, dy)
            else:
                self.mensaje = "No puedes moverte ahí."
        else:
            self.mensaje = "Tecla inválida. Usa W/A/S/D."

        if all(monstruo.hp == 0 for monstruo in self.monstruos):
            self.juego_terminado = True
            self.mensaje = "¡Felicidades! Has derrotado a todos los monstruos."

    def ejecutar(self):
        """El bucle principal del juego."""
        while not self.juego_terminado:
            self.renderizar()
            tecla = input("Mover (W/A/S/D): ").lower()
            self.manejar_entrada(tecla)
        
        self.renderizar()

# --- PUNTO DE ENTRADA DEL PROGRAMA ---
if __name__ == "__main__":
    instancia_juego = Juego()
    instancia_juego.ejecutar()