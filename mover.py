# mover.py

import pygame

def seleccionar_figura(dibujos, cursor_pos):
    """Busca una figura bajo el cursor y devuelve su índice y offset"""
    cx, cy = cursor_pos
    for i in reversed(range(len(dibujos))):
        shape = dibujos[i]

        if len(shape) == 3:
            _, start, end = shape
        elif len(shape) == 2:
            _, puntos = shape
            if isinstance(puntos, list) and len(puntos) >= 2:
                start, end = puntos[0], puntos[-1]
            else:
                continue
        else:
            continue

        x0, y0 = start
        x1, y1 = end
        rect = pygame.Rect(min(x0, x1), min(y0, y1), abs(x1 - x0), abs(y1 - y0))
        if rect.collidepoint(cx, cy):
            offset = (cx - x0, cy - y0)
            return i, offset

    return None, (0, 0)


def mover_figura(dibujos, index, cursor_pos, offset):
    """Mueve una figura completa manteniendo su forma"""
    if index is None or index >= len(dibujos):
        return

    mouse_x, mouse_y = cursor_pos
    dx, dy = offset

    figura = dibujos[index]

    if len(figura) == 2:
        tool, datos = figura
    elif len(figura) == 3:
        tool, start, end = figura
        datos = (start, end)
    else:
        return

    # Si es formato con vértices
    if isinstance(datos, list) and all(isinstance(p, tuple) for p in datos):
        x0, y0 = datos[0]
        offset_x = mouse_x - dx - x0
        offset_y = mouse_y - dy - y0
        nuevos_puntos = [(x + offset_x, y + offset_y) for x, y in datos]
        dibujos[index] = (tool, nuevos_puntos)

    # Formato clásico (start, end)
    elif isinstance(datos, tuple) and len(datos) == 2:
        old_start, old_end = datos
        delta_x = old_end[0] - old_start[0]
        delta_y = old_end[1] - old_start[1]
        new_start = (mouse_x - dx, mouse_y - dy)
        new_end = (new_start[0] + delta_x, new_start[1] + delta_y)
        dibujos[index] = (tool, (new_start, new_end))

