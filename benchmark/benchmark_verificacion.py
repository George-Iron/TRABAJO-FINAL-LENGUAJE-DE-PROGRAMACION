# benchmark_verificacion.py
import sys
import os
import timeit
import copy

# --- AJUSTE DE RUTA (igual que antes) ---
ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ruta_proyecto)

# --- IMPORTACIONES (igual que antes) ---
try:
    from roguelike_POO.main_oop import Juego as JuegoOOP
    from roguelike_Funcional import main_fun
except ImportError as e:
    print(f"!!! ERROR DE IMPORTACIÓN: {e} !!!")
    print("Asegúrate de que los archivos '__init__.py' existen en todas las subcarpetas.")
    sys.exit()

# --- DESACTIVAR SALIDA VISUAL (igual que antes) ---
def funcion_vacia(*args, **kwargs):
    pass
JuegoOOP.renderizar = funcion_vacia
main_fun.renderizar_estado = funcion_vacia

# --- SIMULACIONES (igual que antes) ---
acciones_para_ganar = (['d'] * 3 + ['s'] * 2 + ['s'] * 3 + ['d'] * 1 + ['s'] * 3 + ['s'] * 3)
acciones = [accion for sublista in acciones_para_ganar for accion in sublista]

# ------------------------------------------------------------------
# --- !!! LA PRUEBA: AÑADIMOS CONTADORES GLOBALES !!! ---
# ------------------------------------------------------------------
contador_oop = 0
contador_fp = 0

def simular_partida_oop_con_contador():
    global contador_oop
    contador_oop += 1 # Incrementamos el contador cada vez que se llama a esta función
    juego = JuegoOOP()
    for accion in acciones:
        if juego.juego_terminado:
            break
        juego.manejar_entrada(accion)

def simular_partida_fp_con_contador():
    global contador_fp
    contador_fp += 1 # Incrementamos el contador
    estado_juego = main_fun.crear_estado_inicial()
    for accion in acciones:
        if estado_juego['juego_terminado']:
            break
        estado_juego = main_fun.procesar_entrada(estado_juego, accion)

# --- EJECUCIÓN DE LA VERIFICACIÓN ---
if __name__ == "__main__":
    num_ejecuciones = 1000
    print("--- VERIFICANDO EL NÚMERO DE EJECUCIONES ---")
    print(f"Se intentarán ejecutar {num_ejecuciones} partidas para cada paradigma.")

    # Ejecutamos timeit, pero ignoramos su resultado de tiempo.
    # Solo nos interesa el efecto secundario sobre nuestros contadores.
    timeit.timeit(simular_partida_oop_con_contador, number=num_ejecuciones)
    timeit.timeit(simular_partida_fp_con_contador, number=num_ejecuciones)

    print("\n--- RESULTADOS DE LA VERIFICACIÓN ---")
    print(f"La función de simulación OOP fue llamada: {contador_oop} veces.")
    print(f"La función de simulación FP fue llamada:  {contador_fp} veces.")

    print("\n--- CONCLUSIÓN DE LA PRUEBA ---")
    if contador_oop == num_ejecuciones and contador_fp == num_ejecuciones:
        print("¡Prueba superada! El módulo 'timeit' ejecutó cada simulación exactamente 1000 veces.")
    else:
        print("¡Prueba fallida! Algo inesperado ocurrió.")