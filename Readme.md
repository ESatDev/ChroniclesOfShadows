markdown
# ⚔️ Chronicles of Shadows (v1.0)

**Chronicles of Shadows** es un RPG táctico de fantasía oscura desarrollado en Python para ser ejecutado directamente en la terminal. El juego combina mecánicas clásicas de exploración en 2D, combate por turnos con estados alterados, generación procedimental de mazmorras y bosques, sistema de talentos, efectos de sonido retro de 8-bits y soporte para colores ANSI.

## 📸 Estructura del Proyecto

El código está completamente modularizado para garantizar un mantenimiento limpio, escalable y profesional:

```text
ChroniclesOfShadows/
│
├── main.py                   # Punto de entrada principal e inicio de la terminal
├── partida.json              # Archivo de guardado automático (se genera al jugar)
│
├── assets/                   # Galería de arte pixel art (Sprites 16-bits)
│   ├── Arquero.png
│   ├── Guerrero.png
│   ├── Mago.png
│   ├── Malakor-fase1.png
│   ├── Malakor-fase2.png
│   └── Malakor-fase3.png
│
└── src/                      # Paquete principal del código fuente
    ├── __init__.py           # Identificador de paquete de Python
    ├── modelos.py            # Items, Misiones, Colores ANSI, Sonido (winsound) y Entidades base
    ├── entidades.py          # Lógica de Jugador, Enemigos, Jefes y Árbol de Talentos
    ├── mapa.py               # Renderizado del mapa 2D y Generador Procedimental
    └── juego.py              # Bucles de combate, Tienda, Posada, NPC y Eventos

```

---

## 🔥 Características de la Versión 1.0

* **🎭 Clases de Personajes:**
* **Guerrero:** Gran vida y defensa. Habilidades: *Golpe Devastador* y *Escudo de Sangre*.
* **Mago:** Alto daño mágico. Habilidades: *Bola de Fuego* y *Meteoro*.
* **Cazador / Arquero Elfo:** Ataques rápidos y veneno. Habilidades: *Disparo Doble* y *Lluvia de Flechas*.


* **🗺️ Exploración y Mapas Procedimentales:**
* Mapa principal del pueblo con accesos a la Tienda (`T`), Posada (`P`), NPC Anciano (`N`) y Mazmorras (`M`).
* Generación de sub-mapas aleatorios al explorar el Bosque (`~`) o adentrarse en las Mazmorras (`M`), con cofres (`C`) y enemigos visibles (`X`).


* **⚔️ Sistema de Combate Táctico por Turnos:**
* Gestión de Cooldowns de habilidades.
* Estados alterados: *Quemadura* 🔥, *Veneno* 🧪, *Congelamiento* ❄️ y *Aturdimiento* ⚡.
* **Jefe Final Multifase (Rey Demonio Malakor):** Batalla épica de 3 fases que cambia de patrón de ataque y estadísticas conforme se le inflige daño.


* **📈 Progresión y Árbol de Talentos:**
* Sistema de Niveles y Experiencia.
* +2 Puntos de Talento por nivel para asignar a *Fuerza*, *Resistencia* o *Vitalidad*.


* **🎨 Experiencia Visual y Sonora:**
* Interfaz coloreada mediante secuencias ANSI (barras de vida dinámicas en verde/amarillo/rojo).
* Efectos de sonido retro de 8-bits impulsados por `winsound` para pisadas, impactos, pociones, monedas, hechizos y fanfarrias.


* **💾 Persistencia de Datos:**
* Guardado y carga automática del estado de la partida mediante formato JSON (`partida.json`).



---

## 🚀 Cómo Ejecutar el Juego

1. Asegúrate de tener instalado **Python 3.10+**.
2. Clona o descarga la carpeta del proyecto.
3. Abre una terminal dentro del directorio raíz (`ChroniclesOfShadows`).
4. Ejecuta el archivo principal:

```bash
# En Windows (CMD o PowerShell):
py main.py

# O bien:
python main.py

```

---

## 🎮 Controles

| Tecla | Acción |
| --- | --- |
| `W` `A` `S` `D` | Moverse por el mapa |
| **`I`** | Abrir Mochila / Inventario |
| **`M`** | Ver Diario de Misiones |
| **`T`** | Menú del Árbol de Talentos |
| **`E`** | Ver Estado del Héroe |
| **`G`** | Guardar Partida |
| **`Q`** | Guardar y Salir |

---

## 🚀 Hoja de Ruta / Próximas Mejoras (v1.1+)

* [ ] **Sistema de Mascotas / Compañeros:** Añadir adiestramiento de criaturas que apoyen de forma pasiva en combate.
* [ ] **Bestiario y Logros:** Registro de monstruos derrotados y sistema de medallas.
* [ ] **Interfaz Gráfica (GUI):** Integración con Pygame o CustomTkinter para renderizar directamente los sprites de la carpeta `assets/`.
* [ ] **Nuevas Misiones Secundarias y Mazmorras de Pisos Infinitos.**

---

*¡Desarrollado como proyecto modular en Python para amantes de los RPGs clásicos!*