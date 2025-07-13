# main_oop.py

# --- CLASE BASE ---
# El plano para cualquier cosa que ocupe un lugar en el mapa y tenga vida.
class Entity:
    """Un objeto genérico para representar al jugador, monstruos, etc."""
    def __init__(self, x, y, char, hp):
        self.x = x          # Posición en el eje X
        self.y = y          # Posición en el eje Y
        self.char = char    # Carácter visual (e.g., '@')
        self.hp = hp        # Puntos de vida

    def move(self, dx, dy):
        """Mueve la entidad una cierta cantidad."""
        pass  # La lógica irá aquí

    def take_damage(self, amount):
        """Reduce el HP de la entidad."""
        pass  # La lógica irá aquí


# --- CLASES QUE HEREDAN ---
# Especializaciones de la clase Entity. Por ahora, no necesitan nada extra.
class Player(Entity):
    """La clase que representa al jugador."""
    pass


class Monster(Entity):
    """La clase que representa a un enemigo."""
    pass


# --- CLASES DE GESTIÓN ---
class GameMap:
    """Gestiona el mapa del juego, incluyendo los muros y el suelo."""
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.tiles = []  # Esto será una cuadrícula 2D (lista de listas)

    def is_walkable(self, x, y):
        """Devuelve True si la casilla (x,y) no es un muro."""
        pass  # La lógica irá aquí


class Game:
    """Orquesta todo el juego. Contiene el bucle principal y todos los objetos del juego."""
    def __init__(self):
        self.game_map = None    # Se creará un objeto GameMap aquí
        self.player = None      # Se creará un objeto Player aquí
        self.monsters = []      # Se llenará con objetos Monster
        self.game_over = False

    def setup_game(self):
        """Inicializa el mapa y las entidades."""
        pass  # La lógica para crear el mapa, jugador y monstruos irá aquí

    def render(self):
        """Dibuja todo en la pantalla."""
        pass  # La lógica de dibujado irá aquí

    def handle_input(self):
        """Procesa la entrada del jugador."""
        pass  # La lógica para leer el teclado e iniciar acciones irá aquí

    def run(self):
        """El bucle principal del juego."""
        # Este será el ciclo: renderizar, pedir input, procesar, repetir.
        print("El juego ha comenzado. (Estructura lista)")
        # while not self.game_over:
        #     self.render()
        #     self.handle_input()


# --- PUNTO DE ENTRADA DEL PROGRAMA ---
# Esto solo se ejecuta cuando corres el archivo directamente.
if __name__ == "__main__":
    game_instance = Game()
    game_instance.run()