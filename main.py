import os
from src.modelos import Colores, Sonido, imprimir_lento
from src.entidades import Jugador, ARCHIVO_GUARDADO
from src.mapa import Mapa2D
from src.juego import verificar_evento_casilla

def crear_nuevo_jugador():
    nombre = input("\nIngresa el nombre de tu héroe: ").strip()
    if not nombre:
        nombre = "Aventurero"

    print(f"\n{Colores.CYAN}Elige tu Clase:{Colores.RESET}")
    print(f"1. {Colores.AMARILLO}Guerrero{Colores.RESET} | 2. {Colores.ROJO}Mago{Colores.RESET} | 3. {Colores.VERDE}Cazador{Colores.RESET}")
    clase_opcion = ""
    while clase_opcion not in ["1", "2", "3"]:
        clase_opcion = input("Selecciona una clase (1-3): ")

    clases_map = {"1": "Guerrero", "2": "Mago", "3": "Cazador"}
    return Jugador(nombre, clases_map[clase_opcion])

def main():
    print(f"""{Colores.CYAN}
 ___________________________________________________________________
|                                                                   |
|   ____ _  _ ___  ____ _  _ _ ____ _    ____ ____   ____ ____      |
|   |    |__| |__] |  | |\ | | |    |    |___ [__    |  | |___      |
|   |___ |  | |  \ |__| | \| | |___ |___ |___ ___]   |__| |         |
|                                                                   |
|         ____ _  _ ____ ___  ____ _ me_                    |
|         [__  |__| |__| |  \ |  | |  |  |                  |
|         ___] |  | |  | |__/ |__| |__|  |___               |
|___________________________________________________________________|
    {Colores.RESET}""")
    imprimir_lento(f"          {Colores.AMARILLO}--- UN RPG TÁCTICO PARA LA TERMINAL ---{Colores.RESET}          ", velocidad=0.01)
    print()

    jugador = None

    if os.path.exists(ARCHIVO_GUARDADO):
        print(f"{Colores.CYAN}Se encontró una partida guardada.{Colores.RESET}")
        print("1. Cargar Partida")
        print("2. Nueva Partida")
        opcion_inicio = input("> ").strip()
        if opcion_inicio == "1":
            jugador = Jugador.cargar_datos()
            if jugador:
                Sonido.subida_nivel()
                imprimir_lento(f"\n{Colores.VERDE}¡Bienvenido de vuelta, {jugador.nombre}!{Colores.RESET}")

    if not jugador:
        jugador = crear_nuevo_jugador()
        Sonido.subida_nivel()
        imprimir_lento(f"\n¡Bienvenido, {Colores.AMARILLO}{jugador.nombre}{Colores.RESET}! Muévete usando W, A, S, D para explorar el reino.")

    mapa = Mapa2D()

    while jugador.esta_vivo():
        mapa.mostrar(jugador.x, jugador.y, titulo="PUEBLO PRINCIPAL")
        pts_talento_str = f" | {Colores.AMARILLO}Talentos (+{jugador.puntos_talento}){Colores.RESET}" if jugador.puntos_talento > 0 else ""
        print(f"\n[ {Colores.AMARILLO}{jugador.nombre}{Colores.RESET} el {jugador.clase} | HP: {Colores.barra_hp(jugador.hp, jugador.hp_max)} | Atq: {jugador.ataque_total} | Def: {jugador.defensa_total} | Oro: {Colores.AMARILLO}{jugador.oro}{Colores.RESET}{pts_talento_str} ]")
        print(f"Controles: [WASD] Moverse | [{Colores.AMARILLO}I{Colores.RESET}] Inventario | [{Colores.CYAN}M{Colores.RESET}] Misiones | [{Colores.AMARILLO}T{Colores.RESET}] Talentos | [{Colores.VERDE}E{Colores.RESET}] Estado | [{Colores.AMARILLO}G{Colores.RESET}] Guardar | [{Colores.ROJO}Q{Colores.RESET}] Salir")
        
        accion = input("> ").strip().lower()

        nueva_x, nueva_y = jugador.x, jugador.y

        if accion == "w":
            nueva_y -= 1
        elif accion == "s":
            nueva_y += 1
        elif accion == "a":
            nueva_x -= 1
        elif accion == "d":
            nueva_x += 1
        elif accion == "i":
            jugador.abrir_inventario()
            continue
        elif accion == "m":
            jugador.ver_misiones()
            input("\nPresiona Enter para continuar...")
            continue
        elif accion == "t":
            jugador.gestionar_talentos()
            continue
        elif accion == "e":
            print(f"\n--- ESTADO DE {Colores.AMARILLO}{jugador.nombre.upper()}{Colores.RESET} ---")
            print(f"Nivel: {jugador.nivel} | EXP: {jugador.exp}/{jugador.nivel * 20}")
            print(f"Puntos de Talento no asignados: {jugador.puntos_talento}")
            print(f"Ataque Base: {jugador.ataque_base} (+{jugador.arma_equipada.bonificador if jugador.arma_equipada else 0} Arma) = {jugador.ataque_total}")
            print(f"Defensa Base: {jugador.defensa_base} (+{jugador.armadura_equipada.bonificador if jugador.armadura_equipada else 0} Armadura) = {jugador.defensa_total}")
            print(f"Habilidad 1: {jugador.nombre_habilidad}")
            print(f"Habilidad 2: {jugador.nombre_habilidad2}")
            print(f"Estados activos: {list(jugador.estados.keys()) if jugador.estados else 'Ninguno'}")
            input("\nPresiona Enter para continuar...")
            continue
        elif accion == "g":
            jugador.guardar_datos()
            input("\nPresiona Enter para continuar...")
            continue
        elif accion == "q":
            guardar_salir = input("¿Deseas guardar antes de salir? (s/n): ").strip().lower()
            if guardar_salir == "s":
                jugador.guardar_datos()
            imprimir_lento(f"{Colores.VERDE}Gracias por jugar. ¡Hasta la próxima!{Colores.RESET}")
            break
        else:
            continue

        if mapa.es_transitable(nueva_x, nueva_y):
            jugador.x = nueva_x
            jugador.y = nueva_y
            Sonido.paso()
            casilla_actual = mapa.obtener_casilla(jugador.x, jugador.y)
            verificar_evento_casilla(jugador, mapa, casilla_actual)
        else:
            imprimir_lento(f"\n{Colores.ROJO}¡Hay un obstáculo en esa dirección! No puedes pasar.{Colores.RESET}")

if __name__ == "__main__":
    main()