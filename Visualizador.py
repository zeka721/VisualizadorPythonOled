import pygame

pygame.init()

SCALE = 6
OLED_WIDTH = 128
OLED_HEIGHT = 64
DISPLAY_WIDTH = OLED_WIDTH * SCALE
DISPLAY_HEIGHT = OLED_HEIGHT * SCALE
TOOLBAR_WIDTH = 130
WINDOW_WIDTH = DISPLAY_WIDTH + TOOLBAR_WIDTH
WINDOW_HEIGHT = DISPLAY_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BLUE = (0, 0, 255)

screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulador OLED u8g2")
font = pygame.font.SysFont(None, 20)

tools = [
    "Pixel", "Línea", "Rect", "Rect llena", "Círculo", "Círculo lleno",
    "Elipse", "Elipse llena", "Triángulo", "Triángulo lleno",
    "Caja red", "Marco red", "Borrar", "Guardar"
]
selected_tool = "Pixel"
u8g2_commands = []
drawn_shapes = []

drawing = False
start_pos = (0, 0)
end_pos = (0, 0)

def draw_toolbar():
    pygame.draw.rect(screen, GRAY, (0, 0, TOOLBAR_WIDTH, WINDOW_HEIGHT))
    for i, tool in enumerate(tools):
        color = BLUE if tool == selected_tool else WHITE
        text = font.render(tool, True, color)
        screen.blit(text, (5, 10 + i * 25))

def add_command(cmd):
    if cmd not in u8g2_commands:
        u8g2_commands.append(cmd)

def draw_shape(tool, start, end, preview=False, save=True):
    sx, sy = start
    ex, ey = end

    sx_oled = (sx - TOOLBAR_WIDTH) // SCALE
    sy_oled = sy // SCALE
    ex_oled = (ex - TOOLBAR_WIDTH) // SCALE
    ey_oled = ey // SCALE

    w = abs(ex - sx)
    h = abs(ey - sy)
    w_oled = w // SCALE
    h_oled = h // SCALE

    x0, y0 = min(sx, ex), min(sy, ey)
    x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
    y0_oled = y0 // SCALE

    if tool == "Pixel":
        if TOOLBAR_WIDTH <= sx < WINDOW_WIDTH and 0 <= sy < WINDOW_HEIGHT:
            pygame.draw.rect(screen, WHITE, (sx, sy, SCALE, SCALE))
            if not preview:
                add_command(f"u8g2.drawPixel({sx_oled}, {sy_oled});")
                if save:
                    drawn_shapes.append((tool, start, end))

    elif tool == "Línea":
        pygame.draw.line(screen, WHITE, start, end)
        if not preview:
            add_command(f"u8g2.drawLine({sx_oled}, {sy_oled}, {ex_oled}, {ey_oled});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Rect":
        pygame.draw.rect(screen, WHITE, (x0, y0, w, h), 1)
        if not preview:
            add_command(f"u8g2.drawFrame({x0_oled}, {y0_oled}, {w_oled}, {h_oled});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Rect llena":
        pygame.draw.rect(screen, WHITE, (x0, y0, w, h))
        if not preview:
            add_command(f"u8g2.drawBox({x0_oled}, {y0_oled}, {w_oled}, {h_oled});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Círculo":
        bbox = pygame.Rect(x0, y0, w, h)
        pygame.draw.ellipse(screen, WHITE, bbox, 1)
        if not preview:
            rx = w_oled // 2
            ry = h_oled // 2
            cx_oled = x0_oled + rx
            cy_oled = y0_oled + ry
            add_command(f"u8g2.drawCircle({cx_oled}, {cy_oled}, {min(rx, ry)});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Círculo lleno":
        bbox = pygame.Rect(x0, y0, w, h)
        pygame.draw.ellipse(screen, WHITE, bbox)
        if not preview:
            rx = w_oled // 2
            ry = h_oled // 2
            cx_oled = x0_oled + rx
            cy_oled = y0_oled + ry
            add_command(f"u8g2.drawDisc({cx_oled}, {cy_oled}, {min(rx, ry)});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Elipse":
        pygame.draw.ellipse(screen, WHITE, (x0, y0, w, h), 1)
        if not preview:
            add_command(f"u8g2.drawEllipse({x0_oled}, {y0_oled}, {w_oled // 2}, {h_oled // 2});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Elipse llena":
        pygame.draw.ellipse(screen, WHITE, (x0, y0, w, h))
        if not preview:
            add_command(f"u8g2.drawFilledEllipse({x0_oled}, {y0_oled}, {w_oled // 2}, {h_oled // 2});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Triángulo":
        mid_x = (sx + ex) // 2
        top_y = min(sy, ey)
        base_y = max(sy, ey)
        points = [(sx, base_y), (ex, base_y), (mid_x, top_y)]
        pygame.draw.polygon(screen, WHITE, points, 1)
        if not preview:
            mid_x_oled = (mid_x - TOOLBAR_WIDTH) // SCALE
            top_y_oled = top_y // SCALE
            base_y_oled = base_y // SCALE
            add_command(f"u8g2.drawTriangle({sx_oled}, {base_y_oled}, {ex_oled}, {base_y_oled}, {mid_x_oled}, {top_y_oled});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Triángulo lleno":
        mid_x = (sx + ex) // 2
        top_y = min(sy, ey)
        base_y = max(sy, ey)
        points = [(sx, base_y), (ex, base_y), (mid_x, top_y)]
        pygame.draw.polygon(screen, WHITE, points)
        if not preview:
            mid_x_oled = (mid_x - TOOLBAR_WIDTH) // SCALE
            top_y_oled = top_y // SCALE
            base_y_oled = base_y // SCALE
            add_command(f"u8g2.drawFilledTriangle({sx_oled}, {base_y_oled}, {ex_oled}, {base_y_oled}, {mid_x_oled}, {top_y_oled});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Caja red":
        radius = min(w_oled, h_oled) // 4
        pygame.draw.rect(screen, WHITE, (x0, y0, w, h), 1, border_radius=10)
        if not preview:
            add_command(f"u8g2.drawRBox({x0_oled}, {y0_oled}, {w_oled}, {h_oled}, {radius});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Marco red":
        radius = min(w_oled, h_oled) // 4
        pygame.draw.rect(screen, WHITE, (x0, y0, w, h), 1, border_radius=10)
        if not preview:
            add_command(f"u8g2.drawRFrame({x0_oled}, {y0_oled}, {w_oled}, {h_oled}, {radius});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Borrar":
        pygame.draw.rect(screen, BLACK, (TOOLBAR_WIDTH, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT))
        u8g2_commands.clear()
        drawn_shapes.clear()

    elif tool == "Guardar":
        with open("u8g2_output.txt", "w") as f:
            for cmd in u8g2_commands:
                f.write(cmd + "\n")
        print("Guardado en u8g2_output.txt")

# Bucle principal
running = True
while running:
    screen.fill(BLACK)
    draw_toolbar()

    for shape in drawn_shapes:
        draw_shape(*shape, preview=False, save=False)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < TOOLBAR_WIDTH:
                index = (y - 10) // 25
                if 0 <= index < len(tools):
                    selected_tool = tools[index]
                    if selected_tool == "Guardar":
                        draw_shape("Guardar", (0, 0), (0, 0))
            else:
                drawing = True
                start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = pygame.mouse.get_pos()
                draw_shape(selected_tool, start_pos, end_pos, preview=False, save=True)
                drawing = False

    if drawing:
        end_pos = pygame.mouse.get_pos()
        draw_shape(selected_tool, start_pos, end_pos, preview=True, save=False)

    pygame.display.flip()

pygame.quit()
