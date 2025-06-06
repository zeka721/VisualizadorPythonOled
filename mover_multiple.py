import pygame

def seleccionar_figuras_en_area(dibujos, area_rect):
    seleccionados = []
    for i, shape in enumerate(dibujos):
        if len(shape) == 2:
            tool, datos = shape
            if isinstance(datos, list):  # línea o triángulo
                puntos = datos
                xs = [p[0] for p in puntos]
                ys = [p[1] for p in puntos]
                bounds = pygame.Rect(min(xs), min(ys), max(xs) - min(xs), max(ys) - min(ys))
            else:
                start, end = datos
                bounds = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]),
                                     abs(end[0] - start[0]), abs(end[1] - start[1]))
        elif len(shape) == 3:
            tool, start, end = shape
            bounds = pygame.Rect(min(start[0], end[0]), min(start[1], end[1]),
                                 abs(end[0] - start[0]), abs(end[1] - start[1]))
        else:
            continue

        if area_rect.contains(bounds):
            seleccionados.append(i)

    return seleccionados

def mover_varias_figuras(dibujos, indices, dx, dy):
    for i in indices:
        shape = dibujos[i]
        if len(shape) == 2:
            tool, datos = shape
            if isinstance(datos, list):  # lista de puntos
                nuevos_puntos = [(x + dx, y + dy) for x, y in datos]
                dibujos[i] = (tool, nuevos_puntos)
            else:
                start, end = datos
                nuevos = ((start[0] + dx, start[1] + dy), (end[0] + dx, end[1] + dy))
                dibujos[i] = (tool, nuevos)
        elif len(shape) == 3:
            tool, start, end = shape
            nuevos = ((start[0] + dx, start[1] + dy), (end[0] + dx, end[1] + dy))
            dibujos[i] = (tool, *nuevos)
