# configuracion.py
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

TOOLS = [
    "Pixel", "Línea", "Rectangulo", "Rectangulo lleno", "Círculo", "Círculo lleno",
    "Elipse", "Elipse llena", "Triángulo", "Triángulo lleno", "Caja redonda llena",
    "Marco redondo", "Borrar", "Guardar", "Cargar", "Seleccionar", "Editar vértice"
]


