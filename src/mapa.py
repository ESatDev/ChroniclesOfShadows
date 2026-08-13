import random
from src.modelos import Colores

class GeneradorMapaProcedimental:
    @staticmethod
    def generar_zona(filas=8, columnas=10, tipo_zona="bosque"):
        simbolo_fondo = "~" if tipo_zona == "bosque" else "."
        grilla = [[simbolo_fondo for _ in range(columnas)] for _ in range(filas)]

        for y in range(filas):
            for x in range(columnas):
                if y == 0 or y == filas - 1 or x == 0 or x == columnas - 1:
                    grilla[y][x] = "#"

        num_obstaculos = int((filas * columnas) * 0.15)
        for _ in range(num_obstaculos):
            rx, ry = random.randint(1, columnas - 2), random.randint(1, filas - 2)
            grilla[ry][rx] = "#"

        grilla[1][1] = "E"
        grilla[filas - 2][columnas - 2] = "S"

        num_elementos = random.randint(2, 4)
        for _ in range(num_elementos):
            rx, ry = random.randint(1, columnas - 2), random.randint(1, filas - 2)
            if grilla[ry][rx] not in ["#", "E", "S"]:
                grilla[ry][rx] = "C" if random.random() < 0.4 else "X"

        return grilla

class Mapa2D:
    def __init__(self):
        self.grilla = [
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
            ["#", "P", ".", "N", "#", "~", "~", "~", "~", "~", "~", "#"],
            ["#", ".", ".", ".", "#", "~", "~", "~", "~", "~", "~", "#"],
            ["#", ".", "T", ".", ".", ".", ".", "~", "~", "~", "~", "#"],
            ["#", "#", "#", ".", "#", "#", ".", "#", "#", "#", ".", "#"],
            ["#", "~", "~", ".", ".", ".", ".", ".", ".", "~", ".", "#"],
            ["#", "~", "~", "~", "~", "#", "#", "#", ".", "~", ".", "#"],
            ["#", "~", "~", "~", "~", "~", "~", "~", ".", ".", ".", "#"],
            ["#", "~", "~", "~", "~", "~", "~", "~", "~", "~", "M", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
        ]
        self.filas = len(self.grilla)
        self.columnas = len(self.grilla[0])

    def colorear_casilla(self, simbolo):
        colores_map = {
            "@": f"{Colores.AMARILLO}{Colores.NEGRITA}@{Colores.RESET}",
            "#": f"{Colores.GRIS}#{Colores.RESET}",
            "~": f"{Colores.VERDE}~{Colores.RESET}",
            "P": f"{Colores.AZUL}P{Colores.RESET}",
            "T": f"{Colores.AMARILLO}T{Colores.RESET}",
            "N": f"{Colores.CYAN}N{Colores.RESET}",
            "M": f"{Colores.ROJO}{Colores.NEGRITA}M{Colores.RESET}",
            "C": f"{Colores.AMARILLO}C{Colores.RESET}",
            "X": f"{Colores.ROJO}X{Colores.RESET}",
            "E": f"{Colores.MAGENTA}E{Colores.RESET}",
            "S": f"{Colores.CYAN}S{Colores.RESET}",
            ".": f"{Colores.BLANCO}.{Colores.RESET}"
        }
        return colores_map.get(simbolo, simbolo)

    def mostrar(self, jugador_x, jugador_y, grilla_custom=None, titulo="MAPA PRINCIPAL"):
        mapa_a_dibujar = grilla_custom if grilla_custom else self.grilla
        filas = len(mapa_a_dibujar)
        cols = len(mapa_a_dibujar[0])

        print("\n" + f"{Colores.CYAN}" + "=" * 36 + f"{Colores.RESET}")
        print(f"         {Colores.NEGRITA}{titulo.center(20)}{Colores.RESET}         ")
        print(f"{Colores.CYAN}" + "=" * 36 + f"{Colores.RESET}")
        for y in range(filas):
            linea = ""
            for x in range(cols):
                if x == jugador_x and y == jugador_y:
                    linea += self.colorear_casilla("@") + " "
                else:
                    linea += self.colorear_casilla(mapa_a_dibujar[y][x]) + " "
            print(f"  {linea}")
        print(f"{Colores.CYAN}" + "=" * 36 + f"{Colores.RESET}")

    def es_transitable(self, x, y, grilla_custom=None):
        mapa = grilla_custom if grilla_custom else self.grilla
        filas = len(mapa)
        cols = len(mapa[0])
        if 0 <= x < cols and 0 <= y < filas:
            return mapa[y][x] != "#"
        return False

    def obtener_casilla(self, x, y, grilla_custom=None):
        mapa = grilla_custom if grilla_custom else self.grilla
        return mapa[y][x]