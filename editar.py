# editar.py
from configuracion import SCALE

TOLERANCIA = SCALE  # radio para detectar vértice cercano


def detectar_vertice_cercano(dibujos, mouse_pos):
    mx, my = mouse_pos

    for i, shape in enumerate(dibujos):
        if len(shape) == 2:
            tool, puntos = shape

            # Línea: 2 puntos
            if tool == "Línea" and isinstance(puntos, list) and len(puntos) == 2:
                for j, (px, py) in enumerate(puntos):
                    if abs(px - mx) <= TOLERANCIA and abs(py - my) <= TOLERANCIA:
                        return i, j

            # Triángulo o Triángulo lleno: 3 puntos
            elif tool in ["Triángulo", "Triángulo lleno"] and isinstance(puntos, list) and len(puntos) == 3:
                for j, (px, py) in enumerate(puntos):
                    if abs(px - mx) <= TOLERANCIA and abs(py - my) <= TOLERANCIA:
                        return i, j

    return None, None


def mover_vertice(dibujos, figura_idx, punto_idx, nueva_pos):
    if 0 <= figura_idx < len(dibujos):
        shape = dibujos[figura_idx]

        if len(shape) == 2:
            tool, puntos = shape

            if tool == "Línea" and isinstance(puntos, list) and 0 <= punto_idx < 2:
                puntos[punto_idx] = nueva_pos
                dibujos[figura_idx] = (tool, puntos)

            elif tool in ["Triángulo", "Triángulo lleno"] and isinstance(puntos, list) and 0 <= punto_idx < 3:
                puntos[punto_idx] = nueva_pos
                dibujos[figura_idx] = (tool, puntos)
