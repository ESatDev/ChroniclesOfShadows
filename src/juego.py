import os
import random
from src.modelos import Item, Mision, Colores, Sonido, imprimir_lento
from src.entidades import Jugador, Enemigo, JefeFinal, ARCHIVO_GUARDADO
from src.mapa import Mapa2D, GeneradorMapaProcedimental

def combate(jugador, enemigo):
    imprimir_lento(f"\n{Colores.ROJO}{Colores.NEGRITA}=== ¡UN {enemigo.nombre.upper()} APARECE EN EL BOSQUE! ==={Colores.RESET}")
    jugador.cooldown_habilidad = 0
    jugador.cooldown_habilidad2 = 0
    
    while jugador.esta_vivo() and enemigo.esta_vivo():
        pierde_turno_jugador = jugador.procesar_estados_inicio_turno()
        if not jugador.esta_vivo():
            break

        cd1 = f"{Colores.VERDE}Lista{Colores.RESET}" if jugador.cooldown_habilidad == 0 else f"{Colores.ROJO}CD ({jugador.cooldown_habilidad}){Colores.RESET}"
        cd2 = f"{Colores.VERDE}Lista{Colores.RESET}" if jugador.cooldown_habilidad2 == 0 else f"{Colores.ROJO}CD ({jugador.cooldown_habilidad2}){Colores.RESET}"
        e_jugador = f" | Estados: {list(jugador.estados.keys())}" if jugador.estados else ""
        e_enemigo = f" | Estados: {list(enemigo.estados.keys())}" if enemigo.estados else ""

        print(f"\n--- {Colores.AMARILLO}{jugador.nombre}{Colores.RESET} HP: {Colores.barra_hp(jugador.hp, jugador.hp_max)}{e_jugador} vs {Colores.ROJO}{enemigo.nombre}{Colores.RESET} HP: {Colores.barra_hp(enemigo.hp, enemigo.hp_max)}{e_enemigo} ---")
        
        if not pierde_turno_jugador:
            print("1. Atacar")
            print(f"2. Habilidad 1 [{jugador.nombre_habilidad}] ({cd1})")
            print(f"3. Habilidad 2 [{jugador.nombre_habilidad2}] ({cd2})")
            print("4. Usar Objeto del Inventario")
            print("5. Huir")
            
            opcion = input("> ")
            
            if opcion == "1":
                dano = max(1, jugador.ataque_total - enemigo.defensa_base + random.randint(-2, 2))
                enemigo.hp -= dano
                Sonido.ataque()
                imprimir_lento(f"Atacas al {enemigo.nombre} y le infliges {dano} de daño.")
            elif opcion == "2":
                if not jugador.usar_habilidad(enemigo):
                    continue
            elif opcion == "3":
                if not jugador.usar_habilidad2(enemigo):
                    continue
            elif opcion == "4":
                jugador.abrir_inventario()
                continue
            elif opcion == "5":
                if random.random() < 0.5:
                    imprimir_lento(f"{Colores.VERDE}¡Lograste huir del combate de manera segura!{Colores.RESET}")
                    jugador.limpiar_estados()
                    return False
                else:
                    imprimir_lento(f"{Colores.ROJO}¡Fallaste al intentar huir!{Colores.RESET}")
            else:
                print("Opción inválida.")
                continue

            if jugador.cooldown_habilidad > 0:
                jugador.cooldown_habilidad -= 1
            if jugador.cooldown_habilidad2 > 0:
                jugador.cooldown_habilidad2 -= 1

        if enemigo.esta_vivo():
            pierde_turno_enemigo = enemigo.procesar_estados_inicio_turno()
            if enemigo.esta_vivo() and not pierde_turno_enemigo:
                enemigo.atacar_jugador(jugador)

    if jugador.esta_vivo():
        Sonido.fanfarria_victoria()
        imprimir_lento(f"\n{Colores.VERDE}¡Derrotaste al {enemigo.nombre}!{Colores.RESET}")
        jugador.oro += enemigo.oro_recompensa
        imprimir_lento(f"Obtuviste {Colores.AMARILLO}{enemigo.oro_recompensa} Oro{Colores.RESET}.")
        jugador.ganar_exp(enemigo.exp_recompensa)
        jugador.registrar_enemigo_derrotado(enemigo.nombre)
        jugador.limpiar_estados()
        return True
    else:
        Sonido.dano_recibido()
        imprimir_lento(f"\n{Colores.ROJO}Has sido derrotado... GAME OVER.{Colores.RESET}")
        if os.path.exists(ARCHIVO_GUARDADO):
            os.remove(ARCHIVO_GUARDADO)
        return False

def combate_jefe(jugador):
    jefe = JefeFinal()
    imprimir_lento("\n" + f"{Colores.ROJO}" + "#" * 50)
    imprimir_lento("   ¡HAS ENTRADO EN EL ALTAR DEL REY DEMONIO MALAKOR!   ", velocidad=0.03)
    imprimir_lento("#" * 50 + f"{Colores.RESET}")
    
    jugador.cooldown_habilidad = 0
    jugador.cooldown_habilidad2 = 0

    while jugador.esta_vivo() and jefe.esta_vivo():
        print("\n--- INICIO DE TURNO ---")
        pierde_turno_jugador = jugador.procesar_estados_inicio_turno()
        if not jugador.esta_vivo():
            break

        cd1 = f"{Colores.VERDE}Lista{Colores.RESET}" if jugador.cooldown_habilidad == 0 else f"{Colores.ROJO}CD ({jugador.cooldown_habilidad}){Colores.RESET}"
        cd2 = f"{Colores.VERDE}Lista{Colores.RESET}" if jugador.cooldown_habilidad2 == 0 else f"{Colores.ROJO}CD ({jugador.cooldown_habilidad2}){Colores.RESET}"
        e_jugador = f" | Estados: {list(jugador.estados.keys())}" if jugador.estados else ""
        e_jefe = f" | Estados: {list(jefe.estados.keys())}" if jefe.estados else ""

        print(f"\n--- {Colores.AMARILLO}{jugador.nombre}{Colores.RESET} HP: {Colores.barra_hp(jugador.hp, jugador.hp_max)}{e_jugador} VS {Colores.ROJO}{jefe.nombre} [FASE {jefe.fase}]{Colores.RESET} HP: {Colores.barra_hp(jefe.hp, jefe.hp_max)}{e_jefe} ---")

        if not pierde_turno_jugador:
            print("1. Atacar")
            print(f"2. Habilidad 1 [{jugador.nombre_habilidad}] ({cd1})")
            print(f"3. Habilidad 2 [{jugador.nombre_habilidad2}] ({cd2})")
            print("4. Usar Objeto del Inventario")
            print("5. Intentar Huir")
            
            opcion = input("> ")
            
            if opcion == "1":
                dano = max(1, jugador.ataque_total - jefe.defensa_base + random.randint(-2, 2))
                jefe.hp -= dano
                Sonido.ataque()
                imprimir_lento(f"Golpeas a Malakor e infliges {dano} de daño.")
            elif opcion == "2":
                if not jugador.usar_habilidad(jefe):
                    continue
            elif opcion == "3":
                if not jugador.usar_habilidad2(jefe):
                    continue
            elif opcion == "4":
                jugador.abrir_inventario()
                continue
            elif opcion == "5":
                imprimir_lento(f"\n{Colores.ROJO}¡Una barrera mágica bloquea la salida! No puedes huir de esta batalla.{Colores.RESET}")
                continue
            else:
                print("Opción inválida.")
                continue

            if jugador.cooldown_habilidad > 0:
                jugador.cooldown_habilidad -= 1
            if jugador.cooldown_habilidad2 > 0:
                jugador.cooldown_habilidad2 -= 1

        if jefe.verificar_cambio_fase():
            continue

        if jefe.esta_vivo():
            pierde_turno_jefe = jefe.procesar_estados_inicio_turno()
            if jefe.esta_vivo() and not pierde_turno_jefe:
                jefe.atacar_especial(jugador)

        jefe.verificar_cambio_fase()

    if jugador.esta_vivo():
        Sonido.fanfarria_victoria()
        imprimir_lento("\n" + f"{Colores.AMARILLO}" + "=" * 50)
        imprimir_lento("¡HAS DERROTADO AL REY DEMONIO MALAKOR!", velocidad=0.03)
        imprimir_lento("El reino ha sido liberado de la oscuridad gracias a tu valentía.")
        imprimir_lento("¡FELICIDADES, HAS COMPLETADO EL JUEGO!")
        imprimir_lento("=" * 50 + f"{Colores.RESET}\n")
        if os.path.exists(ARCHIVO_GUARDADO):
            os.remove(ARCHIVO_GUARDADO)
        return True
    else:
        Sonido.dano_recibido()
        imprimir_lento(f"\n{Colores.ROJO}Has sucumbido ante el poder de Malakor... GAME OVER.{Colores.RESET}")
        if os.path.exists(ARCHIVO_GUARDADO):
            os.remove(ARCHIVO_GUARDADO)
        return False

def explorar_zona_procedimental(jugador, mapa, tipo_zona="bosque"):
    grilla_zona = GeneradorMapaProcedimental.generar_zona(filas=8, columnas=10, tipo_zona=tipo_zona)
    px, py = 1, 1
    titulo_mapa = "BOSQUE PROFUNDO" if tipo_zona == "bosque" else "PISO DE LA MAZMORRA"

    imprimir_lento(f"\n{Colores.VERDE}¡Entraste a una nueva zona en el {titulo_mapa.lower()}!{Colores.RESET}")

    while jugador.esta_vivo():
        mapa.mostrar(px, py, grilla_custom=grilla_zona, titulo=titulo_mapa)
        print(f"\n[ {Colores.AMARILLO}{jugador.nombre}{Colores.RESET} | HP: {Colores.barra_hp(jugador.hp, jugador.hp_max)} | Oro: {Colores.AMARILLO}{jugador.oro}{Colores.RESET} ]")
        print("Moverse: [WASD] | [I] Inventario | [Q] Regresar al Mapa Principal")

        accion = input("> ").strip().lower()
        if accion == "q":
            imprimir_lento("Decides retirarte de esta zona.")
            break
        elif accion == "i":
            jugador.abrir_inventario()
            continue

        nx, ny = px, py
        if accion == "w": ny -= 1
        elif accion == "s": ny += 1
        elif accion == "a": nx -= 1
        elif accion == "d": nx += 1
        else: continue

        if mapa.es_transitable(nx, ny, grilla_custom=grilla_zona):
            px, py = nx, ny
            Sonido.paso()
            casilla = mapa.obtener_casilla(px, py, grilla_custom=grilla_zona)

            if casilla == "C":
                Sonido.moneda()
                oro_hallado = random.randint(15, 30)
                jugador.oro += oro_hallado
                grilla_zona[py][px] = "." if tipo_zona == "mazmorra" else "~"
                imprimir_lento(f"\n{Colores.AMARILLO}¡Abriste un Cofre y hallaste {oro_hallado} monedas de oro!{Colores.RESET}")

            elif casilla == "X":
                enemigos = [
                    Enemigo("Duendecillo", hp=15, ataque=5, defensa=1, oro_recompensa=8, exp_recompensa=10, efecto_ataque=("Aturdimiento", 1)),
                    Enemigo("Lobo Salvaje", hp=22, ataque=7, defensa=2, oro_recompensa=12, exp_recompensa=15, efecto_ataque=("Veneno", 3)),
                    Enemigo("Orco Explorador", hp=35, ataque=10, defensa=3, oro_recompensa=25, exp_recompensa=30, efecto_ataque=("Quemadura", 2))
                ]
                enemigo_actual = random.choice(enemigos)
                if combate(jugador, enemigo_actual):
                    grilla_zona[py][px] = "." if tipo_zona == "mazmorra" else "~"

            elif casilla == "S":
                if tipo_zona == "bosque":
                    imprimir_lento(f"\n{Colores.CYAN}Llegaste al final del sendero del bosque y regresas al mapa principal.{Colores.RESET}")
                    break
                else:
                    imprimir_lento(f"\n{Colores.ROJO}¡Encontraste la bajada al Altar de Malakor!{Colores.RESET}")
                    combate_jefe(jugador)
                    break

def tienda(jugador):
    catalogo = [
        Item("Poción de Vida", "consumible", 25, 10, "Restaura 25 HP"),
        Item("Hierba Curativa", "curativo_estado", 0, 12, "Limpia todos los estados alterados"),
        Item("Espada de Hierro", "arma", 6, 30, "+6 Ataque"),
        Item("Báculo Rúnico", "arma", 8, 35, "+8 Ataque Mágico"),
        Item("Arco Recurvo", "arma", 7, 32, "+7 Ataque"),
        Item("Cota de Malla", "armadura", 4, 30, "+4 Defensa"),
        Item("Armadura de Placas", "armadura", 8, 60, "+8 Defensa")
    ]

    while True:
        print(f"\n{Colores.AMARILLO}=== TIENDA DEL MERCADER ==={Colores.RESET}")
        print(f"Tu Oro: {Colores.AMARILLO}{jugador.oro}{Colores.RESET}")
        for idx, item in enumerate(catalogo, 1):
            print(f"{idx}. {item.nombre} ({item.tipo.capitalize()}) - {Colores.AMARILLO}{item.valor} Oro{Colores.RESET} | {item.descripcion}")
        print(f"{len(catalogo)+1}. Salir de la tienda")

        opcion = input("> ")
        if opcion.isdigit():
            idx = int(opcion) - 1
            if idx == len(catalogo):
                break
            elif 0 <= idx < len(catalogo):
                item_comprar = catalogo[idx]
                if jugador.oro >= item_comprar.valor:
                    jugador.oro -= item_comprar.valor
                    nuevo_item = Item(item_comprar.nombre, item_comprar.tipo, item_comprar.bonificador, item_comprar.valor, item_comprar.descripcion)
                    jugador.inventario.append(nuevo_item)
                    Sonido.moneda()
                    imprimir_lento(f"{Colores.VERDE}Compraste {item_comprar.nombre}. ¡Guardado en la mochila!{Colores.RESET}")
                else:
                    imprimir_lento(f"{Colores.ROJO}No tienes suficiente oro.{Colores.RESET}")

def posada(jugador):
    print(f"\n{Colores.AZUL}=== POSADA DEL PUEBLO ==={Colores.RESET}")
    if jugador.hp == jugador.hp_max and not jugador.estados:
        imprimir_lento("El posadero te dice: '¡Ya estás completamente sano! No necesitas descansar.'")
        return

    print("Descansar cuesta 5 de oro. Recupera todo tu HP y curará tus estados alterados.")
    confirmar = input("¿Deseas descansar? (s/n): ").strip().lower()
    if confirmar == 's':
        if jugador.oro >= 5:
            jugador.oro -= 5
            jugador.hp = jugador.hp_max
            jugador.limpiar_estados()
            Sonido.curacion()
            imprimir_lento(f"{Colores.VERDE}Te echas a dormir... Despiertas completamente renovado. (HP Restaurado y Estados Purificados){Colores.RESET}")
        else:
            imprimir_lento(f"{Colores.ROJO}No tienes suficiente oro para la posada.{Colores.RESET}")

def npc_anciano(jugador):
    print(f"\n{Colores.CYAN}=== EL ANCIANO DE LA ALDEA ==={Colores.RESET}")
    imprimir_lento("El Anciano te mira detenidamente: 'Ah, joven aventurero... El bosque está más agitado de lo normal.'")

    misiones_disponibles = [
        Mision(1, "Limpieza del Bosque", "Elimina a 3 enemigos en el bosque.", "enemigo_cualquiera", 3, 40, 30, Item("Poción de Vida", "consumible", 25, 10, "Restaura 25 HP")),
        Mision(2, "Caza del Orco", "Derrota a 1 Orco Explorador para dispersar a la horda.", "Orco Explorador", 1, 60, 50, Item("Hierba Curativa", "curativo_estado", 0, 12, "Limpia estados alterados"))
    ]

    for m_disp in misiones_disponibles:
        m_jugador = next((m for m in jugador.misiones if m.id_mision == m_disp.id_mision), None)

        if not m_jugador:
            print(f"\n Misión Disponible: [{Colores.AMARILLO}{m_disp.titulo}{Colores.RESET}]")
            print(f"  Objetivo: {m_disp.descripcion}")
            print(f"  Recompensa: {Colores.AMARILLO}{m_disp.recompensa_oro} Oro{Colores.RESET} | {Colores.CYAN}{m_disp.recompensa_exp} EXP{Colores.RESET}")
            
            aceptar = input("¿Aceptas esta misión? (s/n): ").strip().lower()
            if aceptar == "s":
                jugador.misiones.append(m_disp)
                Sonido.moneda()
                imprimir_lento(f"{Colores.VERDE}¡Aceptaste la misión '{m_disp.titulo}'!{Colores.RESET}")
        else:
            if m_jugador.completada and not m_jugador.entregada:
                Sonido.fanfarria_victoria()
                imprimir_lento(f"\n{Colores.VERDE}¡Excelente trabajo! Has completado [{m_jugador.titulo}].{Colores.RESET}")
                jugador.oro += m_jugador.recompensa_oro
                jugador.ganar_exp(m_jugador.recompensa_exp)
                if m_jugador.recompensa_item:
                    jugador.inventario.append(m_jugador.recompensa_item)
                    imprimir_lento(f"{Colores.AMARILLO}¡Recibiste un objeto de recompensa: {m_jugador.recompensa_item.nombre}!{Colores.RESET}")
                m_jugador.entregada = True
            elif m_jugador.entregada:
                print(f"\n Ya has entregado la misión: [{m_jugador.titulo}].")
            else:
                print(f"\n Misión en curso: [{m_jugador.titulo}] ({m_jugador.progreso}/{m_jugador.cantidad_objetivo})")

    input("\nPresiona Enter para salir de la conversación...")

def verificar_evento_casilla(jugador, mapa, tipo_casilla):
    if tipo_casilla == "~":
        explorar_zona_procedimental(jugador, mapa, tipo_zona="bosque")
    elif tipo_casilla == "T":
        tienda(jugador)
    elif tipo_casilla == "P":
        posada(jugador)
    elif tipo_casilla == "N":
        npc_anciano(jugador)
    elif tipo_casilla == "M":
        imprimir_lento(f"\n{Colores.ROJO}Te encuentras frente al gran portón de la Mazmorra del Rey Demonio.{Colores.RESET}")
        entrar = input("¿Deseas adentrarte en las profundidades de la mazmorra? (s/n): ").strip().lower()
        if entrar == "s":
            explorar_zona_procedimental(jugador, mapa, tipo_zona="mazmorra")