#Codigo total completo con la falta de hacer los comandos Rehacer y Deshacer
# import pygame
import tkinter as tk
from tkinter import filedialog
from PIL import Image
import re

pygame.init()

SCALE = 7
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

# Quitar "Imagen" y "Guardar PNG"
tools = [
    "Pixel", "Línea", "Rectangulo", "Rectangulo lleno", "Círculo", "Borrar", "Guardar", "Cargar", "Círculo lleno",
    "Elipse", "Elipse llena" , "Triángulo", "Triángulo lleno", "Caja redonda llena", "Marco redondo"
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


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

def draw_shape(tool, start, end, preview=False, save=True):
    sx, sy = start
    ex, ey = end

    sx_oled = (sx - TOOLBAR_WIDTH) // SCALE
    sy_oled = sy // SCALE
    ex_oled = (ex - TOOLBAR_WIDTH) // SCALE
    ey_oled = ey // SCALE

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

    elif tool == "Rectangulo":
        x0 = min(sx, ex)
        y0 = min(sy, ey)
        w = abs(ex - sx)
        h = abs(ey - sy)

        x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
        y0_oled = y0 // SCALE
        w_oled = w // SCALE
        h_oled = h // SCALE

        pygame.draw.rect(screen, WHITE, (x0, y0, w, h), 1)

        if not preview:
            add_command(f"u8g2.drawFrame({x0_oled}, {y0_oled}, {w_oled}, {h_oled});")
            if save:
                drawn_shapes.append((tool, start, end))

    elif tool == "Rectangulo lleno":
        x0 = min(sx, ex)
        y0 = min(sy, ey)
        w = abs(ex - sx)
        h = abs(ey - sy)

        x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
        y0_oled = y0 // SCALE
        w_oled = w // SCALE
        h_oled = h // SCALE

        pygame.draw.rect(screen, WHITE, (x0, y0, w, h))

        if not preview:
            add_command(f"u8g2.drawBox({x0_oled}, {y0_oled}, {w_oled}, {h_oled});")
            if save:
                drawn_shapes.append((tool, start, end))



    elif tool == "Círculo":
        x0 = min(sx, ex)
        y0 = min(sy, ey)
        w = abs(ex - sx)
        h = abs(ey - sy)
        size = min(w, h)  # ← Forzamos círculo perfecto
        x0 = sx if sx < ex else sx - size
        y0 = sy if sy < ey else sy - size
        x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
        y0_oled = y0 // SCALE
        size_oled = size // SCALE
        bbox = pygame.Rect(x0, y0, size, size)
        pygame.draw.ellipse(screen, WHITE, bbox, 1)

        if not preview:
            r = size_oled // 2
            cx_oled = x0_oled + r
            cy_oled = y0_oled + r
            add_command(f"u8g2.drawCircle({cx_oled}, {cy_oled}, {r});")

            if save:
                drawn_shapes.append((tool, (x0, y0), (x0 + size, y0 + size)))


    elif tool == "Círculo lleno":
        x0 = min(sx, ex)
        y0 = min(sy, ey)
        w = abs(ex - sx)
        h = abs(ey - sy)
        size = min(w, h)  # Aseguramos círculo perfecto
        x0 = sx if sx < ex else sx - size
        y0 = sy if sy < ey else sy - size
        x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
        y0_oled = y0 // SCALE
        size_oled = size // SCALE
        bbox = pygame.Rect(x0, y0, size, size)
        pygame.draw.ellipse(screen, WHITE, bbox)  # Sin grosor => lleno

        if not preview:
            r = size_oled // 2
            cx_oled = x0_oled + r
            cy_oled = y0_oled + r
            add_command(f"u8g2.drawDisc({cx_oled}, {cy_oled}, {r});")

            if save:
                drawn_shapes.append((tool, (x0, y0), (x0 + size, y0 + size)))


    elif tool == "Elipse":
        x0 = min(sx, ex)
        y0 = min(sy, ey)
        w = abs(ex - sx)
        h = abs(ey - sy)

        x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
        y0_oled = y0 // SCALE
        w_oled = w // SCALE
        h_oled = h // SCALE

        pygame.draw.ellipse(screen, WHITE, (x0, y0, w, h), 1)

        if not preview:
            rx = w_oled // 2
            ry = h_oled // 2
            add_command(f"u8g2.drawEllipse({x0_oled}, {y0_oled}, {rx}, {ry});")
            if save:
                drawn_shapes.append((tool, (x0, y0), (x0 + w, y0 + h)))


    elif tool == "Elipse llena":
        x0 = min(sx, ex)
        y0 = min(sy, ey)
        w = abs(ex - sx)
        h = abs(ey - sy)

        x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
        y0_oled = y0 // SCALE
        w_oled = w // SCALE
        h_oled = h // SCALE

        pygame.draw.ellipse(screen, WHITE, (x0, y0, w, h))  # Sin grosor → llena

        if not preview:
            rx = w_oled // 2
            ry = h_oled // 2
            add_command(f"u8g2.drawFilledEllipse({x0_oled}, {y0_oled}, {rx}, {ry});")
            if save:
                drawn_shapes.append((tool, (x0, y0), (x0 + w, y0 + h)))



    elif tool == "Triángulo":
        mid_x = (sx + ex) // 2
        top_y = min(sy, ey)
        base_y = max(sy, ey)

        points = [(sx, base_y), (ex, base_y), (mid_x, top_y)]

        sx_oled = (sx - TOOLBAR_WIDTH) // SCALE
        ex_oled = (ex - TOOLBAR_WIDTH) // SCALE
        mid_x_oled = (mid_x - TOOLBAR_WIDTH) // SCALE
        top_y_oled = top_y // SCALE
        base_y_oled = base_y // SCALE

        pygame.draw.polygon(screen, WHITE, points, 1)

        if not preview:
            add_command(
                f"u8g2.drawTriangle({sx_oled}, {base_y_oled}, {ex_oled}, {base_y_oled}, {mid_x_oled}, {top_y_oled});")
            if save:
                drawn_shapes.append((tool, (sx, top_y), (ex, base_y)))


    elif tool == "Triángulo lleno":
        mid_x = (sx + ex) // 2
        top_y = min(sy, ey)
        base_y = max(sy, ey)

        points = [(sx, base_y), (ex, base_y), (mid_x, top_y)]

        sx_oled = (sx - TOOLBAR_WIDTH) // SCALE
        ex_oled = (ex - TOOLBAR_WIDTH) // SCALE
        mid_x_oled = (mid_x - TOOLBAR_WIDTH) // SCALE
        top_y_oled = top_y // SCALE
        base_y_oled = base_y // SCALE

        pygame.draw.polygon(screen, WHITE, points)

        if not preview:
            add_command(
                f"u8g2.drawFilledTriangle({sx_oled}, {base_y_oled}, {ex_oled}, {base_y_oled}, {mid_x_oled}, {top_y_oled});")
            if save:
                drawn_shapes.append((tool, (sx, top_y), (ex, base_y)))


    elif tool == "Caja redonda llena":
        x0 = min(sx, ex)
        y0 = min(sy, ey)
        w = abs(ex - sx)
        h = abs(ey - sy)

        x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
        y0_oled = y0 // SCALE
        w_oled = w // SCALE
        h_oled = h // SCALE

        radius = min(w_oled, h_oled) // 4  # radio proporcional

        pygame.draw.rect(screen, WHITE, (x0, y0, w, h), border_radius=10)

        if not preview:
            add_command(f"u8g2.drawRBox({x0_oled}, {y0_oled}, {w_oled}, {h_oled}, {radius});")
            if save:
                drawn_shapes.append((tool, (sx, sy), (ex, ey)))


    elif tool == "Marco redondo":
        x0 = min(sx, ex)
        y0 = min(sy, ey)
        w = abs(ex - sx)
        h = abs(ey - sy)

        x0_oled = (x0 - TOOLBAR_WIDTH) // SCALE
        y0_oled = y0 // SCALE
        w_oled = w // SCALE
        h_oled = h // SCALE

        radius = min(w_oled, h_oled) // 4  # radio proporcional

        pygame.draw.rect(screen, WHITE, (x0, y0, w, h), 1, border_radius=10)

        if not preview:
            add_command(f"u8g2.drawRFrame({x0_oled}, {y0_oled}, {w_oled}, {h_oled}, {radius});")
            if save:
                drawn_shapes.append((tool, (sx, sy), (ex, ey)))


    #XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

    elif tool == "Borrar":
        pygame.draw.rect(screen, BLACK, (TOOLBAR_WIDTH, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT))
        u8g2_commands.clear()
        drawn_shapes.clear()

    elif tool == "Guardar":
        root = tk.Tk()
        root.withdraw()
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="Guardar como..."
        )

        if file_path:
            with open(file_path, "w") as f:
                for cmd in u8g2_commands:
                    f.write(cmd + "\n")
            print(f"Guardado en {file_path}")

    elif tool == "Cargar":
        load_commands()

#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX


def load_commands():
    global drawn_shapes
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(
        filetypes=[("Text files", "*.txt")],
        title="Cargar archivo de comandos"
    )

    if not file_path:
        return

    with open(file_path, "r") as f:
        lines = f.readlines()

    pattern = re.compile(r"-?\d+")

    drawn_shapes.clear()
    u8g2_commands.clear()

    for cmd in lines:
        cmd = cmd.strip()
        if not cmd:
            continue

        paren_content = re.search(r'\((.*?)\)', cmd)
        if not paren_content:
            continue

        nums = pattern.findall(paren_content.group(1))
        print(f"Cargando comando: {cmd}")
        print(f"Coordenadas extraídas: {nums}")

        if cmd.startswith("u8g2.drawPixel"):
            if len(nums) >= 2:
                x, y = map(int, nums[:2])
                sx = x * SCALE + TOOLBAR_WIDTH
                sy = y * SCALE
                print(f"Pixel en pantalla: {(sx, sy)}")
                drawn_shapes.append(("Pixel", (sx, sy), (sx, sy)))
                u8g2_commands.append(cmd)

        elif cmd.startswith("u8g2.drawLine"):
            if len(nums) >= 4:
                x0, y0, x1, y1 = map(int, nums[:4])
                sx0 = x0 * SCALE + TOOLBAR_WIDTH
                sy0 = y0 * SCALE
                sx1 = x1 * SCALE + TOOLBAR_WIDTH
                sy1 = y1 * SCALE
                print(f"Línea en pantalla: {(sx0, sy0)} a {(sx1, sy1)}")
                drawn_shapes.append(("Línea", (sx0, sy0), (sx1, sy1)))
                u8g2_commands.append(cmd)

        elif cmd.startswith("u8g2.drawFrame"):
            if len(nums) >= 4:
                x0, y0, w, h = map(int, nums[:4])
                sx = x0 * SCALE + TOOLBAR_WIDTH
                sy = y0 * SCALE
                ex = sx + w * SCALE
                ey = sy + h * SCALE
                print(f"Rectángulo en pantalla: esquina {(sx, sy)} tamaño {(ex - sx, ey - sy)}")
                drawn_shapes.append(("Rectangulo", (sx, sy), (ex, ey)))
                u8g2_commands.append(cmd)


        elif cmd.startswith("u8g2.drawBox"):
            if len(nums) >= 4:
                x, y, w, h = map(int, nums[:4])
                sx = x * SCALE + TOOLBAR_WIDTH
                sy = y * SCALE
                sw = w * SCALE
                sh = h * SCALE
                drawn_shapes.append(("Rectangulo lleno", (sx, sy), (sx + sw, sy + sh)))
                u8g2_commands.append(cmd)


        elif cmd.startswith("u8g2.drawCircle"):
            if len(nums) >= 3:
                cx, cy, r = map(int, nums[:3])
                sx = (cx - r) * SCALE + TOOLBAR_WIDTH
                sy = (cy - r) * SCALE
                d = 2 * r * SCALE
                drawn_shapes.append(("Círculo", (sx, sy), (sx + d, sy + d)))
                u8g2_commands.append(cmd)


        elif cmd.startswith("u8g2.drawDisc"):
            if len(nums) >= 3:
                cx, cy, r = map(int, nums[:3])
                sx = (cx - r) * SCALE + TOOLBAR_WIDTH
                sy = (cy - r) * SCALE
                d = 2 * r * SCALE
                drawn_shapes.append(("Círculo lleno", (sx, sy), (sx + d, sy + d)))
                u8g2_commands.append(cmd)

        elif cmd.startswith("u8g2.drawEllipse"):
            if len(nums) >= 4:
                x, y, rx, ry = map(int, nums[:4])
                sx = x * SCALE + TOOLBAR_WIDTH
                sy = y * SCALE
                w = 2 * rx * SCALE
                h = 2 * ry * SCALE
                drawn_shapes.append(("Elipse", (sx, sy), (sx + w, sy + h)))
                u8g2_commands.append(cmd)

        elif cmd.startswith("u8g2.drawFilledEllipse"):
            if len(nums) >= 4:
                x, y, rx, ry = map(int, nums[:4])
                sx = x * SCALE + TOOLBAR_WIDTH
                sy = y * SCALE
                w = 2 * rx * SCALE
                h = 2 * ry * SCALE
                drawn_shapes.append(("Elipse llena", (sx, sy), (sx + w, sy + h)))
                u8g2_commands.append(cmd)

        elif cmd.startswith("u8g2.drawTriangle"):
            if len(nums) >= 6:
                x0, y0, x1, y1, x2, y2 = map(int, nums[:6])
                points = [
                    (x0 * SCALE + TOOLBAR_WIDTH, y0 * SCALE),
                    (x1 * SCALE + TOOLBAR_WIDTH, y1 * SCALE),
                    (x2 * SCALE + TOOLBAR_WIDTH, y2 * SCALE)
                ]
                xs = [pt[0] for pt in points]
                ys = [pt[1] for pt in points]
                drawn_shapes.append(("Triángulo", (min(xs), min(ys)), (max(xs), max(ys))))
                u8g2_commands.append(cmd)

        elif cmd.startswith("u8g2.drawFilledTriangle"):
            if len(nums) >= 6:
                x0, y0, x1, y1, x2, y2 = map(int, nums[:6])
                points = [
                    (x0 * SCALE + TOOLBAR_WIDTH, y0 * SCALE),
                    (x1 * SCALE + TOOLBAR_WIDTH, y1 * SCALE),
                    (x2 * SCALE + TOOLBAR_WIDTH, y2 * SCALE)
                ]
                xs = [pt[0] for pt in points]
                ys = [pt[1] for pt in points]
                drawn_shapes.append(("Triángulo lleno", (min(xs), min(ys)), (max(xs), max(ys))))
                u8g2_commands.append(cmd)

        elif cmd.startswith("u8g2.drawRBox") or cmd.startswith("u8g2.drawRFrame"):
            if len(nums) >= 5:
                x0, y0, w, h, r = map(int, nums[:5])
                sx = x0 * SCALE + TOOLBAR_WIDTH
                sy = y0 * SCALE
                ex = sx + w * SCALE
                ey = sy + h * SCALE
                shape_type = "Caja redonda llena" if cmd.startswith("u8g2.drawRBox") else "Marco redondo"
                drawn_shapes.append((shape_type, (sx, sy), (ex, ey)))
                u8g2_commands.append(cmd)


#XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

#Codigo base
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
                    if selected_tool in ["Guardar", "Cargar", "Borrar"]:
                        draw_shape(selected_tool, (0, 0), (0, 0))
            else:
                drawing = True
                start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            if drawing:
                end_pos = pygame.mouse.get_pos()
                draw_shape(selected_tool, start_pos, end_pos, preview=False, save=True)
                drawing = False

#xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
#Aqui se da la opcion de generar la VISTA PREVIA DINAMICA de la plataforma
    if drawing and selected_tool in ["Pixel", "Línea", "Rectangulo", "Rectangulo lleno", "Círculo",
                                     "Elipse", "Elipse llena", "Triángulo", "Triángulo lleno",
                                     "Caja redonda llena", "Marco redondo"]:


        end_pos = pygame.mouse.get_pos()
        draw_shape(selected_tool, start_pos, end_pos, preview=True, save=False)

    pygame.display.flip()

pygame.quit()
