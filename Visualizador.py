# Visualizador.py

import pygame
from configuracion import *
from dibujo import draw_toolbar, draw_shape
from comandos import get_commands, clear_commands
from archivo import guardar_comandos, cargar_comandos
from herramientas import detectar_herramienta
from mover import seleccionar_figura, mover_figura
from editar import detectar_vertice_cercano, mover_vertice

def dentro_area_oled(x, y):
    return TOOLBAR_WIDTH <= x < WINDOW_WIDTH and 0 <= y < WINDOW_HEIGHT

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Simulador OLED u8g2")
font = pygame.font.SysFont(None, 20)

# Estado de la aplicación
selected_tool = "Pixel"
drawing = False
start_pos = (0, 0)
end_pos = (0, 0)
drawn_shapes = []
undo_stack = []
redo_stack = []

# Estados para mover figura y vértices
selected_shape = None
shape_offset = (0, 0)
modo_editar = False
figura_idx = None
punto_idx = None

# Bucle principal
running = True
while running:
    screen.fill(BLACK)
    draw_toolbar(screen, font, selected_tool)

    # Redibujar figuras existentes
    for shape in drawn_shapes:
        if len(shape) == 2:
            tool, datos = shape
            if isinstance(datos, list):
                draw_shape(screen, tool, datos, datos, preview=False, save=False, drawn_shapes=[])
            else:
                draw_shape(screen, tool, *datos, preview=False, save=False, drawn_shapes=[])
        elif len(shape) == 3:
            tool, start, end = shape
            draw_shape(screen, tool, start, end, preview=False, save=False, drawn_shapes=[])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            herramienta = detectar_herramienta(x, y)

            if herramienta:
                selected_tool = herramienta
                if selected_tool == "Guardar":
                    guardar_comandos(drawn_shapes)
                elif selected_tool == "Cargar":
                    from cargar_dibujo import interpretar_comandos
                    contenido = cargar_comandos()
                    if contenido:
                        clear_commands()
                        drawn_shapes.clear()
                        interpretar_comandos(contenido, drawn_shapes)
                elif selected_tool == "Borrar":
                    clear_commands()
                    drawn_shapes.clear()
            else:
                if not dentro_area_oled(x, y):
                    continue

                if selected_tool == "Seleccionar":
                    selected_shape, shape_offset = seleccionar_figura(drawn_shapes, event.pos)
                elif selected_tool == "Editar vértice":
                    figura_idx, punto_idx = detectar_vertice_cercano(drawn_shapes, event.pos)
                    if figura_idx is not None:
                        modo_editar = True
                else:
                    drawing = True
                    start_pos = event.pos

        elif event.type == pygame.MOUSEMOTION:
            if selected_tool == "Seleccionar" and selected_shape is not None:
                mover_figura(drawn_shapes, selected_shape, event.pos, shape_offset)
            elif modo_editar and figura_idx is not None and punto_idx is not None:
                mover_vertice(drawn_shapes, figura_idx, punto_idx, event.pos)

        elif event.type == pygame.MOUSEBUTTONUP:
            if selected_tool == "Seleccionar":
                selected_shape = None
            elif modo_editar:
                modo_editar = False
                figura_idx = None
                punto_idx = None
            elif drawing:
                end_pos = pygame.mouse.get_pos()

                # Aseguramos que tanto inicio como fin estén en el área OLED
                if dentro_area_oled(*start_pos) and dentro_area_oled(*end_pos):
                    undo_stack.append((list(drawn_shapes), list(get_commands())))
                    redo_stack.clear()
                    draw_shape(screen, selected_tool, start_pos, end_pos, preview=False, save=True, drawn_shapes=drawn_shapes)
                drawing = False

        elif event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            if event.key == pygame.K_z and mods & pygame.KMOD_CTRL:
                if undo_stack:
                    redo_stack.append((list(drawn_shapes), list(get_commands())))
                    prev_shapes, prev_cmds = undo_stack.pop()
                    drawn_shapes.clear()
                    drawn_shapes.extend(prev_shapes)
                    clear_commands()
                    from comandos import u8g2_commands
                    u8g2_commands.clear()
                    u8g2_commands.extend(prev_cmds)
            elif event.key == pygame.K_y and mods & pygame.KMOD_CTRL:
                if redo_stack:
                    undo_stack.append((list(drawn_shapes), list(get_commands())))
                    next_shapes, next_cmds = redo_stack.pop()
                    drawn_shapes.clear()
                    drawn_shapes.extend(next_shapes)
                    clear_commands()
                    from comandos import u8g2_commands
                    u8g2_commands.clear()
                    u8g2_commands.extend(next_cmds)

    # Vista previa mientras se dibuja
    if drawing and selected_tool not in ["Guardar", "Cargar", "Borrar", "Seleccionar", "Editar vértice"]:
        end_pos = pygame.mouse.get_pos()
        if dentro_area_oled(*end_pos):
            draw_shape(screen, selected_tool, start_pos, end_pos, preview=True, save=False, drawn_shapes=[])

    pygame.display.flip()

pygame.quit()
