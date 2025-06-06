# herramientas.py
from configuracion import TOOLS, TOOLBAR_WIDTH

def detectar_herramienta(x, y):
    if x < TOOLBAR_WIDTH:
        index = (y - 10) // 25
        if 0 <= index < len(TOOLS):
            return TOOLS[index]
    return None
