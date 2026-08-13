import json
import os
import random
from src.modelos import EntidadCombate, Item, Mision, Colores, Sonido, imprimir_lento

ARCHIVO_GUARDADO = "partida.json"

class Jugador(EntidadCombate):
    def __init__(self, nombre, clase_nombre):
        self.clase = clase_nombre
        self.nivel = 1
        self.exp = 0
        self.oro = 25
        self.puntos_talento = 0
        self.cooldown_habilidad = 0
        self.cooldown_habilidad2 = 0
        
        self.x = 2
        self.y = 1

        self.inventario = [
            Item("Poción de Vida", "consumible", 25, 10, "Restaura 25 de HP"),
            Item("Hierba Curativa", "curativo_estado", 0, 12, "Limpia todos los estados alterados")
        ]
        self.misiones = []
        self.arma_equipada = None
        self.armadura_equipada = None

        self.configurar_atributos_clase()
        super().__init__(nombre, self.hp_base, self.ataque_base, self.defensa_base)

    def configurar_atributos_clase(self):
        if self.clase == "Guerrero":
            self.hp_base = 40
            self.hp = 40
            self.ataque_base = 8
            self.defensa_base = 3
            self.nombre_habilidad = "Golpe Devastador"
            self.nombre_habilidad2 = "Escudo de Sangre"
            self.arma_equipada = Item("Espada de Madera", "arma", 3, 10, "+3 Ataque")
        elif self.clase == "Mago":
            self.hp_base = 25
            self.hp = 25
            self.ataque_base = 12
            self.defensa_base = 1
            self.nombre_habilidad = "Bola de Fuego"
            self.nombre_habilidad2 = "Meteoro"
            self.arma_equipada = Item("Báculo Básico", "arma", 4, 10, "+4 Ataque Mágico")
        else:
            self.clase = "Cazador"
            self.hp_base = 32
            self.hp = 32
            self.ataque_base = 9
            self.defensa_base = 2
            self.nombre_habilidad = "Disparo Doble"
            self.nombre_habilidad2 = "Lluvia de Flechas"
            self.arma_equipada = Item("Arco Simple", "arma", 3, 10, "+3 Ataque")

        self.armadura_equipada = Item("Ropa de Tela", "armadura", 1, 5, "+1 Defensa")

    @property
    def ataque_total(self):
        bono = self.arma_equipada.bonificador if self.arma_equipada else 0
        atq = self.ataque_base + bono
        if "Congelamiento" in self.estados:
            atq = int(atq * 0.7)
        return atq

    @property
    def defensa_total(self):
        bono = self.armadura_equipada.bonificador if self.armadura_equipada else 0
        return self.defensa_base + bono

    def esta_vivo(self):
        return self.hp > 0

    def registrar_enemigo_derrotado(self, nombre_enemigo):
        for mision in self.misiones:
            mision.registrar_baja(nombre_enemigo)

    def usar_habilidad(self, enemigo):
        if self.cooldown_habilidad > 0:
            imprimir_lento(f"\n{Colores.AMARILLO}¡La habilidad está en recarga! Faltan {self.cooldown_habilidad} turnos.{Colores.RESET}")
            return False

        Sonido.magia()
        if self.clase == "Guerrero":
            dano = max(1, int((self.ataque_total * 1.8) - enemigo.defensa_base))
            enemigo.hp -= dano
            imprimir_lento(f"\n{Colores.AMARILLO}¡Usas {self.nombre_habilidad}! Asestas un golpe brutal y causas {dano} de daño.{Colores.RESET}")
            if random.random() < 0.35:
                enemigo.aplicar_estado("Aturdimiento", 1)

        elif self.clase == "Mago":
            dano = int(self.ataque_total * 1.5)
            enemigo.hp -= dano
            imprimir_lento(f"\n{Colores.ROJO}¡Lanzas una {self.nombre_habilidad}! Ignoras la defensa y causas {dano} de daño mágico.{Colores.RESET}")
            if random.random() < 0.50:
                enemigo.aplicar_estado("Quemadura", 3)

        elif self.clase == "Cazador":
            dano1 = max(1, int(self.ataque_total * 0.8) - enemigo.defensa_base)
            dano2 = max(1, int(self.ataque_total * 0.8) - enemigo.defensa_base)
            enemigo.hp -= (dano1 + dano2)
            imprimir_lento(f"\n{Colores.VERDE}¡Ejecutas un {self.nombre_habilidad}! Disparas dos flechas causando {dano1 + dano2} de daño total.{Colores.RESET}")
            if random.random() < 0.40:
                enemigo.aplicar_estado("Veneno", 3)

        self.cooldown_habilidad = 3
        return True

    def usar_habilidad2(self, enemigo):
        if self.cooldown_habilidad2 > 0:
            imprimir_lento(f"\n{Colores.AMARILLO}¡La segunda habilidad está en recarga! Faltan {self.cooldown_habilidad2} turnos.{Colores.RESET}")
            return False

        Sonido.magia()
        if self.clase == "Guerrero":
            self.hp = min(self.hp_max, self.hp + 15)
            imprimir_lento(f"\n{Colores.VERDE}¡Activas {self.nombre_habilidad2}! Te fortaleces recuperando 15 HP.{Colores.RESET}")
            self.aplicar_estado("Aturdimiento", 0)

        elif self.clase == "Mago":
            dano = int(self.ataque_total * 2.2)
            enemigo.hp -= dano
            imprimir_lento(f"\n{Colores.ROJO}{Colores.NEGRITA}¡Invocas un {self.nombre_habilidad2}! Cae del cielo causando {dano} de daño devastador.{Colores.RESET}")
            enemigo.aplicar_estado("Quemadura", 3)

        elif self.clase == "Cazador":
            dano1 = max(1, int(self.ataque_total * 0.6) - enemigo.defensa_base)
            dano2 = max(1, int(self.ataque_total * 0.6) - enemigo.defensa_base)
            dano3 = max(1, int(self.ataque_total * 0.6) - enemigo.defensa_base)
            total = dano1 + dano2 + dano3
            enemigo.hp -= total
            imprimir_lento(f"\n{Colores.VERDE}¡Desatas una {self.nombre_habilidad2}! 3 flechas impactan causando {total} de daño total.{Colores.RESET}")
            if random.random() < 0.50:
                enemigo.aplicar_estado("Veneno", 3)

        self.cooldown_habilidad2 = 4
        return True

    def ganar_exp(self, cantidad):
        self.exp += cantidad
        imprimir_lento(f"{Colores.CYAN}Ganaste {cantidad} puntos de experiencia.{Colores.RESET}")
        if self.exp >= self.nivel * 20:
            self.nivel += 1
            self.puntos_talento += 2
            if self.clase == "Guerrero":
                self.hp_base += 12
                self.ataque_base += 3
                self.defensa_base += 2
            elif self.clase == "Mago":
                self.hp_base += 6
                self.ataque_base += 5
                self.defensa_base += 1
            else:
                self.hp_base += 9
                self.ataque_base += 4
                self.defensa_base += 1
            self.hp = self.hp_max
            Sonido.subida_nivel()
            imprimir_lento(f"\n{Colores.AMARILLO}{Colores.NEGRITA}¡SUBISTE AL NIVEL {self.nivel}! Ganaste +2 Puntos de Talento (Total: {self.puntos_talento}).{Colores.RESET}")

    def gestionar_talentos(self):
        while True:
            print(f"\n{Colores.AMARILLO}=== ÁRBOL DE TALENTOS ==={Colores.RESET}")
            print(f"Puntos de Talento Disponibles: {Colores.AMARILLO}{self.puntos_talento}{Colores.RESET}")
            print(f"1. Fuerza (+2 Ataque Base) - Actual: {self.ataque_base}")
            print(f"2. Resistencia (+1 Defensa Base) - Actual: {self.defensa_base}")
            print(f"3. Vitalidad (+10 HP Máximo Base) - Actual: {self.hp_base}")
            print(f"4. Salir del Menú de Talentos")

            opcion = input("> ").strip()
            if opcion == "4":
                break

            if self.puntos_talento <= 0:
                imprimir_lento(f"{Colores.ROJO}No tienes puntos de talento disponibles.{Colores.RESET}")
                continue

            if opcion == "1":
                self.ataque_base += 2
                self.puntos_talento -= 1
                Sonido.moneda()
                imprimir_lento(f"{Colores.VERDE}¡Aumentaste tu Fuerza! Ataque Base: {self.ataque_base}{Colores.RESET}")
            elif opcion == "2":
                self.defensa_base += 1
                self.puntos_talento -= 1
                Sonido.moneda()
                imprimir_lento(f"{Colores.VERDE}¡Aumentaste tu Resistencia! Defensa Base: {self.defensa_base}{Colores.RESET}")
            elif opcion == "3":
                self.hp_base += 10
                self.hp += 10
                self.puntos_talento -= 1
                Sonido.moneda()
                imprimir_lento(f"{Colores.VERDE}¡Aumentaste tu Vitalidad! HP Máximo: {self.hp_base}{Colores.RESET}")

    def abrir_inventario(self):
        while True:
            print(f"\n{Colores.CYAN}=== MOCHILA E INVENTARIO ==={Colores.RESET}")
            print(f"Arma equipada: {Colores.AMARILLO}{self.arma_equipada.nombre if self.arma_equipada else 'Ninguna'}{Colores.RESET} (+{self.arma_equipada.bonificador if self.arma_equipada else 0} Atq)")
            print(f"Armadura equipada: {Colores.AZUL}{self.armadura_equipada.nombre if self.armadura_equipada else 'Ninguna'}{Colores.RESET} (+{self.armadura_equipada.bonificador if self.armadura_equipada else 0} Def)")
            print("-" * 35)
            
            if not self.inventario:
                print("Tu mochila está vacía.")
            else:
                for idx, item in enumerate(self.inventario, 1):
                    print(f"{idx}. {item.nombre} ({item.tipo.capitalize()}) - {item.descripcion}")

            print(f"\nOpciones: [{Colores.AMARILLO}Número{Colores.RESET}] Usar/Equipar | [{Colores.ROJO}S{Colores.RESET}] Salir")
            opcion = input("> ").strip().lower()

            if opcion == "s":
                break

            if opcion.isdigit():
                idx = int(opcion) - 1
                if 0 <= idx < len(self.inventario):
                    item = self.inventario[idx]
                    
                    if item.tipo == "consumible":
                        curacion = item.bonificador
                        self.hp = min(self.hp_max, self.hp + curacion)
                        Sonido.curacion()
                        imprimir_lento(f"{Colores.VERDE}Usaste {item.nombre}. Recuperaste {curacion} HP. (HP: {self.hp}/{self.hp_max}){Colores.RESET}")
                        self.inventario.pop(idx)
                    
                    elif item.tipo == "curativo_estado":
                        self.limpiar_estados()
                        Sonido.curacion()
                        imprimir_lento(f"{Colores.VERDE}Usaste {item.nombre}. ¡Todos tus estados alterados fueron purificados!{Colores.RESET}")
                        self.inventario.pop(idx)

                    elif item.tipo == "arma":
                        if self.arma_equipada:
                            self.inventario.append(self.arma_equipada)
                        self.arma_equipada = item
                        self.inventario.pop(idx)
                        Sonido.paso()
                        imprimir_lento(f"{Colores.AMARILLO}Te equipaste: {item.nombre}.{Colores.RESET}")

                    elif item.tipo == "armadura":
                        if self.armadura_equipada:
                            self.inventario.append(self.armadura_equipada)
                        self.armadura_equipada = item
                        self.inventario.pop(idx)
                        Sonido.paso()
                        imprimir_lento(f"{Colores.AZUL}Te equipaste: {item.nombre}.{Colores.RESET}")
                else:
                    print("Número inválido.")

    def ver_misiones(self):
        print(f"\n{Colores.CYAN}=== DIARIO DE MISIONES ==={Colores.RESET}")
        if not self.misiones:
            print("No tienes misiones activas en este momento.")
            return

        for m in self.misiones:
            estado = f"{Colores.VERDE}✅ Completada{Colores.RESET}" if m.completada and not m.entregada else (f"{Colores.CYAN}🏆 Entregada{Colores.RESET}" if m.entregada else f"{Colores.AMARILLO}⏳ En curso ({m.progreso}/{m.cantidad_objetivo}){Colores.RESET}")
            print(f"- [{Colores.NEGRITA}{m.titulo}{Colores.RESET}] Estado: {estado}")
            print(f"  Descripción: {m.descripcion}")

    def guardar_datos(self):
        datos = {
            "nombre": self.nombre,
            "clase": self.clase,
            "nivel": self.nivel,
            "exp": self.exp,
            "hp": self.hp,
            "hp_base": self.hp_base,
            "ataque_base": self.ataque_base,
            "defensa_base": self.defensa_base,
            "oro": self.oro,
            "puntos_talento": self.puntos_talento,
            "x": self.x,
            "y": self.y,
            "arma_equipada": self.arma_equipada.a_dict() if self.arma_equipada else None,
            "armadura_equipada": self.armadura_equipada.a_dict() if self.armadura_equipada else None,
            "inventario": [item.a_dict() for item in self.inventario],
            "misiones": [m.a_dict() for m in self.misiones]
        }
        with open(ARCHIVO_GUARDADO, "w") as f:
            json.dump(datos, f, indent=4)
        Sonido.moneda()
        imprimir_lento(f"\n{Colores.VERDE}¡Partida guardada exitosamente en partida.json!{Colores.RESET}")

    @classmethod
    def cargar_datos(cls):
        if not os.path.exists(ARCHIVO_GUARDADO):
            return None
        try:
            with open(ARCHIVO_GUARDADO, "r") as f:
                datos = json.load(f)
            jugador = cls(datos["nombre"], datos["clase"])
            jugador.nivel = datos["nivel"]
            jugador.exp = datos["exp"]
            jugador.hp = datos["hp"]
            jugador.hp_base = datos["hp_base"]
            jugador.ataque_base = datos["ataque_base"]
            jugador.defensa_base = datos["defensa_base"]
            jugador.oro = datos["oro"]
            jugador.puntos_talento = datos.get("puntos_talento", 0)
            jugador.x = datos["x"]
            jugador.y = datos["y"]
            
            jugador.arma_equipada = Item.desde_dict(datos["arma_equipada"]) if datos["arma_equipada"] else None
            jugador.armadura_equipada = Item.desde_dict(datos["armadura_equipada"]) if datos["armadura_equipada"] else None
            jugador.inventario = [Item.desde_dict(i) for i in datos["inventario"]]
            jugador.misiones = [Mision.desde_dict(m) for m in datos.get("misiones", [])]
            return jugador
        except Exception:
            imprimir_lento(f"{Colores.ROJO}Error al cargar la partida guardada.{Colores.RESET}")
            return None

class Enemigo(EntidadCombate):
    def __init__(self, nombre, hp, ataque, defensa, oro_recompensa, exp_recompensa, efecto_ataque=None):
        super().__init__(nombre, hp, ataque, defensa)
        self.oro_recompensa = oro_recompensa
        self.exp_recompensa = exp_recompensa
        self.efecto_ataque = efecto_ataque

    def esta_vivo(self):
        return self.hp > 0

    def atacar_jugador(self, jugador):
        dano = max(1, self.ataque_base - jugador.defensa_total + random.randint(-1, 2))
        jugador.hp -= dano
        Sonido.dano_recibido()
        imprimir_lento(f"{Colores.ROJO}El {self.nombre} te ataca y te causa {dano} de daño.{Colores.RESET}")
        
        if self.efecto_ataque and random.random() < 0.30:
            estado, duracion = self.efecto_ataque
            jugador.aplicar_estado(estado, duracion)

class JefeFinal(Enemigo):
    def __init__(self):
        super().__init__("Rey Demonio Malakor", hp=60, ataque=12, defensa=4, oro_recompensa=200, exp_recompensa=100)
        self.fase = 1
        self.turnos_fase2 = 0

    def verificar_cambio_fase(self):
        if self.fase == 1 and self.hp <= 0:
            self.fase = 2
            self.hp = 80
            self.hp_base = 80
            self.ataque_base = 18
            self.defensa_base = 2
            self.limpiar_estados()
            Sonido.magia()
            imprimir_lento(f"\n{Colores.MAGENTA}" + "!" * 50)
            imprimir_lento("¡MALAKOR RETA A LA MUERTE Y ABSORBE ENERGÍA OSCURA!")
            imprimir_lento("¡FASE 2: REY DEMONIO DESATADO!")
            imprimir_lento("!" * 50 + f"{Colores.RESET}\n")
            return True

        elif self.fase == 2 and self.hp <= 0:
            self.fase = 3
            self.hp = 100
            self.hp_base = 100
            self.ataque_base = 22
            self.defensa_base = 8
            self.limpiar_estados()
            Sonido.magia()
            imprimir_lento(f"\n{Colores.ROJO}" + "!" * 50)
            imprimir_lento("¡EL CUERPO DE MALAKOR SE COLAPSA EN UNA SOMBRA ETERNA!")
            imprimir_lento("¡FASE 3: FORMA ESPECTRAL DE MALAKOR!")
            imprimir_lento("!" * 50 + f"{Colores.RESET}\n")
            return True

        return False

    def atacar_especial(self, jugador):
        if self.fase == 1:
            dano = max(1, self.ataque_base - jugador.defensa_total + random.randint(-1, 2))
            jugador.hp -= dano
            Sonido.dano_recibido()
            imprimir_lento(f"{Colores.ROJO}El Rey Demonio te ataca con su Espada Maldita y te inflige {dano} de daño.{Colores.RESET}")
            if random.random() < 0.25:
                jugador.aplicar_estado("Quemadura", 2)

        elif self.fase == 2:
            self.turnos_fase2 += 1
            if self.turnos_fase2 % 3 == 0:
                dano = max(1, int(self.ataque_base * 1.5) - jugador.defensa_total)
                jugador.hp -= dano
                Sonido.magia()
                imprimir_lento(f"{Colores.ROJO}{Colores.NEGRITA}¡MALAKOR CANALIZA 'LLAMARADA INFERNAL'! Te causa un impacto brutal de {dano} de daño.{Colores.RESET}")
                jugador.aplicar_estado("Quemadura", 3)
            else:
                dano = max(1, self.ataque_base - jugador.defensa_total + random.randint(-1, 2))
                jugador.hp -= dano
                Sonido.dano_recibido()
                imprimir_lento(f"{Colores.ROJO}Malakor arremete con furia demoníaca y te inflige {dano} de daño.{Colores.RESET}")

        elif self.fase == 3:
            if random.random() < 0.4:
                dano = max(1, self.ataque_base - jugador.defensa_total + 5)
                jugador.hp -= dano
                Sonido.magia()
                imprimir_lento(f"{Colores.MAGENTA}¡LAS SOMBRAS TE ENVOLVENTAN! El ataque espectral te resta {dano} de HP.{Colores.RESET}")
                jugador.aplicar_estado("Aturdimiento", 1)
            else:
                dano = max(1, self.ataque_base - jugador.defensa_total + random.randint(-2, 2))
                jugador.hp -= dano
                Sonido.dano_recibido()
                imprimir_lento(f"{Colores.ROJO}El Espectro de Malakor te ataca con garras de sombra causando {dano} de daño.{Colores.RESET}")