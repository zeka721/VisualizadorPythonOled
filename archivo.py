# archivo.py
import tkinter as tk
from tkinter import filedialog
from comandos import clear_commands, get_commands
from dibujo import draw_shape
from configuracion import TOOLBAR_WIDTH, WINDOW_WIDTH, WINDOW_HEIGHT

def dentro_area_valida(puntos):
    """Verifica que todos los puntos estén dentro del área OLED"""
    for x, y in puntos:
        if x < TOOLBAR_WIDTH or x >= WINDOW_WIDTH or y < 0 or y >= WINDOW_HEIGHT:
            return False
    return True

def guardar_comandos(dibujos):
    clear_commands()

    for shape in dibujos:
        if len(shape) == 2:
            tool, datos = shape

            if isinstance(datos, list):
                if not dentro_area_valida(datos):
                    continue
                draw_shape(None, tool, datos, datos, preview=False, save=True, drawn_shapes=[], export_only=True)

            elif isinstance(datos, tuple) and len(datos) == 2:
                start, end = datos
                if not dentro_area_valida([start, end]):
                    continue
                draw_shape(None, tool, start, end, preview=False, save=True, drawn_shapes=[], export_only=True)

        elif len(shape) == 3:
            tool, start, end = shape
            if not dentro_area_valida([start, end]):
                continue
            draw_shape(None, tool, start, end, preview=False, save=True, drawn_shapes=[], export_only=True)

    # Guardar en archivo
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")],
        title="Guardar como..."
    )
    if file_path:
        with open(file_path, "w") as f:
            for cmd in get_commands():
                f.write(cmd + "\n")
        print(f"Guardado en {file_path}")

def cargar_comandos():
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt")],
        title="Cargar archivo de comandos"
    )
    if not file_path:
        return None
    with open(file_path, "r") as f:
        return f.readlines()
