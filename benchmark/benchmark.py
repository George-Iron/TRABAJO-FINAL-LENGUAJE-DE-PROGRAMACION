# benchmark.py
import sys
import os
import timeit
import copy

# --- AJUSTE DE RUTA PARA ENCONTRAR LOS MÓDULOS ---
ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ruta_proyecto)

# --- IMPORTACIONES ---
try:
    from roguelike_POO.main_oop import Juego as JuegoOOP
    from roguelike_Funcional import main_fun
except ImportError as e:
    print(f"!!! ERROR DE IMPORTACIÓN: {e} !!!")
    print("Asegúrate de que los archivos '__init__.py' existen en todas las subcarpetas.")
    sys.exit()

# ----------------------------------------------------------------------
# --- !!! PARCHE PARA DESACTIVAR LA SALIDA VISUAL (LA CLAVE) !!! ---
#
# Creamos una función que no hace absolutamente nada.
def funcion_vacia(*args, **kwargs):
    pass

# Reemplazamos las funciones/métodos que imprimen en pantalla
# por nuestra función vacía. Esto silenciará los juegos durante el benchmark.
JuegoOOP.renderizar = funcion_vacia
main_fun.renderizar_estado = funcion_vacia
# ----------------------------------------------------------------------


# --- CONFIGURACIÓN DEL BENCHMARK ---
acciones_para_ganar = (
    ['d'] * 3 + ['s'] * 2 + # Moverse a (4,3)
    ['s'] * 3 +             # Atacar al primer monstruo
    ['d'] * 1 + ['s'] * 3 + # Moverse a (5,6)
    ['s'] * 3               # Atacar al segundo monstruo
)
acciones = [accion for sublista in acciones_para_ganar for accion in sublista]

def simular_partida_oop():
    juego = JuegoOOP()
    # Desactivamos el input interactivo que está en el bucle 'ejecutar'
    for accion in acciones:
        if juego.juego_terminado:
            break
        juego.manejar_entrada(accion)

def simular_partida_fp():
    # El bucle de FP también es interactivo, así que lo replicamos aquí
    estado_juego = main_fun.crear_estado_inicial()
    for accion in acciones:
        if estado_juego['juego_terminado']:
            break
        estado_juego = main_fun.procesar_entrada(estado_juego, accion)

# --- EJECUCIÓN Y ANÁLISIS DEL BENCHMARK ---
if __name__ == "__main__":
    num_ejecuciones = 1000
    print("--- Iniciando Benchmark ---")
    print(f"Estructura de proyecto: {os.path.basename(ruta_proyecto)}")
    print(f"Se simularán {num_ejecuciones} partidas completas para cada paradigma.")
    print("La salida visual de los juegos ha sido desactivada para una medición precisa.")
    print("Esto puede tardar unos segundos...")
    
    tiempo_oop = timeit.timeit(simular_partida_oop, number=num_ejecuciones)
    print(f"\n[RESULTADO] Tiempo total OOP: {tiempo_oop:.4f} segundos")

    tiempo_fp = timeit.timeit(simular_partida_fp, number=num_ejecuciones)
    print(f"[RESULTADO] Tiempo total FP:  {tiempo_fp:.4f} segundos")
    
    print("\n--- ANÁLISIS DE RENDIMIENTO ---")
    if tiempo_oop < tiempo_fp:
        diferencia = tiempo_fp - tiempo_oop
        porcentaje = (tiempo_fp / tiempo_oop - 1) * 100
        print(f"El paradigma Orientado a Objetos (OOP) fue más rápido.")
        print(f"Fue {diferencia:.4f} segundos más rápido ({porcentaje:.2f}% más rápido) que el paradigma Funcional (FP).")
    else:
        diferencia = tiempo_oop - tiempo_fp
        porcentaje = (tiempo_oop / tiempo_fp - 1) * 100
        print(f"El paradigma Funcional (FP) fue más rápido.")
        print(f"Fue {diferencia:.4f} segundos más rápido ({porcentaje:.2f}% más rápido) que el paradigma Orientado a Objetos (OOP).")
    
    print("\n--- ¿POR QUÉ ESTE RESULTADO? ---")
    print("OOP (Modificación Directa):")
    print("  - En cada turno, solo se modifican pequeños fragmentos de memoria (ej: 'self.hp -= 1').")
    print("  - Esta operación de mutar estado existente es extremadamente rápida para el procesador.")
    
    print("\nFP (Inmutabilidad y Copia):")
    print("  - En cada turno, se crea una COPIA PROFUNDA (`copy.deepcopy`) de TODO el estado del juego.")
    print("  - Copiar estructuras de datos complejas es una operación muy costosa en tiempo y memoria.")
    print("  - Este es el 'precio' que se paga por la seguridad y predictibilidad de la inmutabilidad.")