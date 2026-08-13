import random
import sys
import time

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

def imprimir_lento(texto, velocidad=0.01):
    for caracter in texto:
        sys.stdout.write(caracter)
        sys.stdout.flush()
        time.sleep(velocidad)
    print()

class Sonido:
    @staticmethod
    def _reproducir(frecuencia, duracion):
        if HAS_WINSOUND:
            try:
                winsound.Beep(frecuencia, duracion)
            except Exception:
                pass

    @staticmethod
    def paso():
        Sonido._reproducir(150, 20)

    @staticmethod
    def ataque():
        Sonido._reproducir(400, 40)
        Sonido._reproducir(200, 60)

    @staticmethod
    def magia():
        Sonido._reproducir(600, 30)
        Sonido._reproducir(900, 30)
        Sonido._reproducir(1200, 50)

    @staticmethod
    def curacion():
        Sonido._reproducir(523, 40)
        Sonido._reproducir(659, 40)
        Sonido._reproducir(784, 60)

    @staticmethod
    def moneda():
        Sonido._reproducir(988, 40)
        Sonido._reproducir(1318, 80)

    @staticmethod
    def subida_nivel():
        notas = [523, 659, 784, 1046]
        for f in notas:
            Sonido._reproducir(f, 50)

    @staticmethod
    def dano_recibido():
        Sonido._reproducir(220, 60)
        Sonido._reproducir(110, 80)

    @staticmethod
    def fanfarria_victoria():
        Sonido._reproducir(523, 80)
        Sonido._reproducir(659, 80)
        Sonido._reproducir(784, 80)
        Sonido._reproducir(1046, 200)

class Colores:
    RESET = "\033[0m"
    NEGRITA = "\033[1m"
    
    ROJO = "\033[91m"
    VERDE = "\033[92m"
    AMARILLO = "\033[93m"
    AZUL = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BLANCO = "\033[97m"
    GRIS = "\033[90m"

    @staticmethod
    def barra_hp(actual, maximo, longitud=10):
        porcentaje = max(0, actual / maximo) if maximo > 0 else 0
        bloques = int(porcentaje * longitud)
        
        color = Colores.VERDE
        if porcentaje < 0.3:
            color = Colores.ROJO
        elif porcentaje < 0.6:
            color = Colores.AMARILLO
            
        barra = "█" * bloques + "░" * (longitud - bloques)
        return f"{color}[{barra}] {actual}/{maximo}{Colores.RESET}"

class Item:
    def __init__(self, nombre, tipo, bonificador=0, valor=0, descripcion=""):
        self.nombre = nombre
        self.tipo = tipo
        self.bonificador = bonificador
        self.valor = valor
        self.descripcion = descripcion

    def a_dict(self):
        return {
            "nombre": self.nombre,
            "tipo": self.tipo,
            "bonificador": self.bonificador,
            "valor": self.valor,
            "descripcion": self.descripcion
        }

    @classmethod
    def desde_dict(cls, datos):
        return cls(datos["nombre"], datos["tipo"], datos["bonificador"], datos["valor"], datos["descripcion"])

class Mision:
    def __init__(self, id_mision, titulo, descripcion, objetivo_tipo, cantidad_objetivo, recompensa_oro, recompensa_exp, recompensa_item=None):
        self.id_mision = id_mision
        self.titulo = titulo
        self.descripcion = descripcion
        self.objetivo_tipo = objetivo_tipo
        self.cantidad_objetivo = cantidad_objetivo
        self.progreso = 0
        self.recompensa_oro = recompensa_oro
        self.recompensa_exp = recompensa_exp
        self.recompensa_item = recompensa_item
        self.completada = False
        self.entregada = False

    def registrar_baja(self, nombre_enemigo):
        if self.completada or self.entregada:
            return
        if self.objetivo_tipo == "enemigo_cualquiera" or self.objetivo_tipo == nombre_enemigo:
            self.progreso += 1
            Sonido.moneda()
            imprimir_lento(f"{Colores.CYAN}📜 [Misión: {self.titulo}] Progreso: {self.progreso}/{self.cantidad_objetivo}{Colores.RESET}")
            if self.progreso >= self.cantidad_objetivo:
                self.completada = True
                Sonido.subida_nivel()
                imprimir_lento(f"{Colores.VERDE}¡Has completado la misión '{self.titulo}'! Habla con el Anciano (N).{Colores.RESET}")

    def a_dict(self):
        return {
            "id_mision": self.id_mision,
            "titulo": self.titulo,
            "descripcion": self.descripcion,
            "objetivo_tipo": self.objetivo_tipo,
            "cantidad_objetivo": self.cantidad_objetivo,
            "progreso": self.progreso,
            "recompensa_oro": self.recompensa_oro,
            "recompensa_exp": self.recompensa_exp,
            "recompensa_item": self.recompensa_item.a_dict() if self.recompensa_item else None,
            "completada": self.completada,
            "entregada": self.entregada
        }

    @classmethod
    def desde_dict(cls, datos):
        item = Item.desde_dict(datos["recompensa_item"]) if datos["recompensa_item"] else None
        m = cls(
            datos["id_mision"], datos["titulo"], datos["descripcion"],
            datos["objetivo_tipo"], datos["cantidad_objetivo"],
            datos["recompensa_oro"], datos["recompensa_exp"], item
        )
        m.progreso = datos["progreso"]
        m.completada = datos["completada"]
        m.entregada = datos["entregada"]
        return m

class EntidadCombate:
    def __init__(self, nombre, hp_max, ataque_base, defensa_base):
        self.nombre = nombre
        self.hp_base = hp_max
        self.hp = hp_max
        self.ataque_base = ataque_base
        self.defensa_base = defensa_base
        self.estados = {}

    @property
    def hp_max(self):
        return self.hp_base

    def aplicar_estado(self, nombre_estado, duracion):
        self.estados[nombre_estado] = duracion
        Sonido.dano_recibido()
        imprimir_lento(f"{Colores.AMARILLO}¡{self.nombre} ha sido afectado por [{nombre_estado}] durante {duracion} turnos!{Colores.RESET}")

    def procesar_estados_inicio_turno(self):
        pierde_turno = False
        estados_a_eliminar = []

        for estado, turnos in list(self.estados.items()):
            if turnos <= 0:
                estados_a_eliminar.append(estado)
                continue

            if estado == "Quemadura":
                dano_q = max(1, int(self.hp_max * 0.10))
                self.hp -= dano_q
                Sonido.dano_recibido()
                imprimir_lento(f"{Colores.ROJO}🔥 ¡{self.nombre} sufre {dano_q} de daño por Quemadura!{Colores.RESET}")

            elif estado == "Veneno":
                dano_v = 5
                self.hp -= dano_v
                Sonido.dano_recibido()
                imprimir_lento(f"{Colores.VERDE}🧪 ¡{self.nombre} sufre {dano_v} de daño por Veneno!{Colores.RESET}")

            elif estado == "Congelamiento":
                if random.random() < 0.4:
                    imprimir_lento(f"{Colores.AZUL}❄️ ¡{self.nombre} está Congelado y no puede moverse!{Colores.RESET}")
                    pierde_turno = True

            elif estado == "Aturdimiento":
                imprimir_lento(f"{Colores.AMARILLO}⚡ ¡{self.nombre} está Aturdido y pierde su turno!{Colores.RESET}")
                pierde_turno = True

            self.estados[estado] -= 1
            if self.estados[estado] <= 0:
                estados_a_eliminar.append(estado)

        for e in estados_a_eliminar:
            del self.estados[e]
            imprimir_lento(f"{Colores.GRIS}El efecto [{e}] sobre {self.nombre} ha terminado.{Colores.RESET}")

        return pierde_turno

    def limpiar_estados(self):
        self.estados.clear()