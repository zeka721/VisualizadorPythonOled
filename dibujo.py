import pygame
from configuracion import *
from comandos import add_command

def draw_toolbar(screen, font, selected_tool):
    pygame.draw.rect(screen, GRAY, (0, 0, TOOLBAR_WIDTH, WINDOW_HEIGHT))
    for i, tool in enumerate(TOOLS):
        color = BLUE if tool == selected_tool else WHITE
        text = font.render(tool, True, color)
        screen.blit(text, (5, 10 + i * 25))

def draw_shape(screen, tool, start, end, preview=False, save=True, drawn_shapes=None, export_only=False, color=WHITE):
    if export_only:
        screen = None

    puntos = None
    sx = sy = ex = ey = None

    if isinstance(start, list) and all(isinstance(p, tuple) for p in start):
        puntos = start
        if len(puntos) == 2:
            sx, sy = puntos[0]
            ex, ey = puntos[1]
        elif len(puntos) == 3:
            pass
    else:
        sx, sy = start
        ex, ey = end

    if not export_only and sx is not None and sy is not None:
        if sx < TOOLBAR_WIDTH or sx >= WINDOW_WIDTH or sy < 0 or sy >= WINDOW_HEIGHT:
            return

    if sx is not None and sy is not None:
        sx_oled = (sx - TOOLBAR_WIDTH) // SCALE
        sy_oled = sy // SCALE
    if ex is not None and ey is not None:
        ex_oled = (ex - TOOLBAR_WIDTH) // SCALE
        ey_oled = ey // SCALE

    if tool == "Pixel":
        if screen:
            pygame.draw.rect(screen, color, (sx, sy, SCALE, SCALE))
        if not preview:
            add_command(f"u8g2.drawPixel({sx_oled}, {sy_oled});")
            if save and drawn_shapes is not None:
                drawn_shapes.append((tool, (sx, sy), (sx, sy)))

    elif tool == "Línea":
        if isinstance(start, list) and len(start) == 2:
            start, end = start[0], start[1]
            sx, sy = start
            ex, ey = end
            sx_oled = (sx - TOOLBAR_WIDTH) // SCALE
            sy_oled = sy // SCALE
            ex_oled = (ex - TOOLBAR_WIDTH) // SCALE
            ey_oled = ey // SCALE

        if screen:
            pygame.draw.line(screen, color, start, end, SCALE)
        if not preview:
            add_command(f"u8g2.drawLine({sx_oled}, {sy_oled}, {ex_oled}, {ey_oled});")
            if save and drawn_shapes is not None:
                drawn_shapes.append((tool, [start, end]))

    elif tool in ["Rectangulo", "Rectangulo lleno", "Caja redonda llena", "Marco redondo"]:
        x0 = min(sx, ex)
        y0 = min(sy, ey)
        w = abs(ex - sx)
        h = abs(ey - sy)
        x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
        y0_oled = y0 // SCALE
        w_oled = w // SCALE
        h_oled = h // SCALE
        radius = min(w_oled, h_oled) // 4

        if tool == "Rectangulo":
            if screen:
                pygame.draw.rect(screen, color, (x0, y0, w, h), SCALE)
            if not preview:
                add_command(f"u8g2.drawFrame({x0_oled}, {y0_oled}, {w_oled}, {h_oled});")

        elif tool == "Rectangulo lleno":
            if screen:
                pygame.draw.rect(screen, color, (x0, y0, w, h))
            if not preview:
                add_command(f"u8g2.drawBox({x0_oled}, {y0_oled}, {w_oled}, {h_oled});")

        elif tool == "Caja redonda llena":
            if screen:
                pygame.draw.rect(screen, color, (x0, y0, w, h), border_radius=10)
            if not preview:
                add_command(f"u8g2.drawRBox({x0_oled}, {y0_oled}, {w_oled}, {h_oled}, {radius});")

        elif tool == "Marco redondo":
            if screen:
                pygame.draw.rect(screen, color, (x0, y0, w, h), SCALE, border_radius=10)
            if not preview:
                add_command(f"u8g2.drawRFrame({x0_oled}, {y0_oled}, {w_oled}, {h_oled}, {radius});")

        if not preview and save and drawn_shapes is not None:
            drawn_shapes.append((tool, (sx, sy), (ex, ey)))

    elif tool in ["Círculo", "Círculo lleno"]:
        x0 = min(sx, ex)
        y0 = min(sy, ey)
        size = min(abs(ex - sx), abs(ey - sy))
        x0 = sx if sx < ex else sx - size
        y0 = sy if sy < ey else sy - size
        x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
        y0_oled = y0 // SCALE
        r = (size // SCALE) // 2
        cx_oled = x0_oled + r
        cy_oled = y0_oled + r
        bbox = pygame.Rect(x0, y0, size, size)

        if tool == "Círculo":
            if screen:
                pygame.draw.ellipse(screen, color, bbox, SCALE)
            if not preview:
                add_command(f"u8g2.drawCircle({cx_oled}, {cy_oled}, {r});")
        else:
            if screen:
                pygame.draw.ellipse(screen, color, bbox)
            if not preview:
                add_command(f"u8g2.drawDisc({cx_oled}, {cy_oled}, {r});")

        if not preview and save and drawn_shapes is not None:
            drawn_shapes.append((tool, (x0, y0), (x0 + size, y0 + size)))

    elif tool in ["Elipse", "Elipse llena"]:
        x0 = min(sx, ex)
        y0 = min(sy, ey)
        w = abs(ex - sx)
        h = abs(ey - sy)
        x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
        y0_oled = y0 // SCALE
        rx = (w // SCALE) // 2
        ry = (h // SCALE) // 2

        if tool == "Elipse":
            if screen:
                pygame.draw.ellipse(screen, color, (x0, y0, w, h), SCALE)
            if not preview:
                add_command(f"u8g2.drawEllipse({x0_oled}, {y0_oled}, {rx}, {ry});")
        else:
            if screen:
                pygame.draw.ellipse(screen, color, (x0, y0, w, h))
            if not preview:
                add_command(f"u8g2.drawFilledEllipse({x0_oled}, {y0_oled}, {rx}, {ry});")

        if not preview and save and drawn_shapes is not None:
            drawn_shapes.append((tool, (x0, y0), (x0 + w, y0 + h)))

    elif tool in ["Triángulo", "Triángulo lleno"]:
        if isinstance(start, list) and len(start) == 3:
            points = start
        else:
            mid_x = (sx + ex) // 2
            top_y = min(sy, ey)
            base_y = max(sy, ey)
            points = [(sx, base_y), (ex, base_y), (mid_x, top_y)]

        oled_points = [((x - TOOLBAR_WIDTH) // SCALE, y // SCALE) for x, y in points]

        if tool == "Triángulo":
            if screen:
                pygame.draw.polygon(screen, color, points, SCALE)
            if not preview:
                x0, y0 = oled_points[0]
                x1, y1 = oled_points[1]
                x2, y2 = oled_points[2]
                add_command(f"u8g2.drawTriangle({x0}, {y0}, {x1}, {y1}, {x2}, {y2});")
        else:
            if screen:
                pygame.draw.polygon(screen, color, points)
            if not preview:
                x0, y0 = oled_points[0]
                x1, y1 = oled_points[1]
                x2, y2 = oled_points[2]
                add_command(f"u8g2.drawFilledTriangle({x0}, {y0}, {x1}, {y1}, {x2}, {y2});")

        if not preview and save and drawn_shapes is not None:
            drawn_shapes.append((tool, points))
