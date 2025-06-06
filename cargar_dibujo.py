# cargar_dibujo.py
import re
from configuracion import *
from comandos import add_command

def interpretar_comandos(lineas, drawn_shapes):
    pattern = re.compile(r"-?\d+")
    for cmd in lineas:
        cmd = cmd.strip()
        if not cmd:
            continue

        paren_content = re.search(r'\((.*?)\)', cmd)
        if not paren_content:
            continue

        nums = list(map(int, pattern.findall(paren_content.group(1))))

        def sx(x): return x * SCALE + TOOLBAR_WIDTH
        def sy(y): return y * SCALE

        # --- Pixel
        if cmd.startswith("u8g2.drawPixel") and len(nums) >= 2:
            x, y = nums[:2]
            drawn_shapes.append(("Pixel", (sx(x), sy(y)), (sx(x), sy(y))))
            add_command(cmd)

        # --- Línea (editable)
        elif cmd.startswith("u8g2.drawLine") and len(nums) >= 4:
            x0, y0, x1, y1 = nums[:4]
            drawn_shapes.append(("Línea", [(sx(x0), sy(y0)), (sx(x1), sy(y1))]))
            add_command(cmd)

        # --- Rectángulo
        elif cmd.startswith("u8g2.drawFrame") and len(nums) >= 4:
            x, y, w, h = nums[:4]
            drawn_shapes.append(("Rectangulo", (sx(x), sy(y)), (sx(x + w), sy(y + h))))
            add_command(cmd)

        elif cmd.startswith("u8g2.drawBox") and len(nums) >= 4:
            x, y, w, h = nums[:4]
            drawn_shapes.append(("Rectangulo lleno", (sx(x), sy(y)), (sx(x + w), sy(y + h))))
            add_command(cmd)

        # --- Círculo
        elif cmd.startswith("u8g2.drawCircle") and len(nums) >= 3:
            cx, cy, r = nums[:3]
            drawn_shapes.append(("Círculo", (sx(cx - r), sy(cy - r)), (sx(cx + r), sy(cy + r))))
            add_command(cmd)

        elif cmd.startswith("u8g2.drawDisc") and len(nums) >= 3:
            cx, cy, r = nums[:3]
            drawn_shapes.append(("Círculo lleno", (sx(cx - r), sy(cy - r)), (sx(cx + r), sy(cy + r))))
            add_command(cmd)

        # --- Elipses
        elif cmd.startswith("u8g2.drawEllipse") and len(nums) >= 4:
            x, y, rx, ry = nums[:4]
            drawn_shapes.append(("Elipse", (sx(x), sy(y)), (sx(x + 2*rx), sy(y + 2*ry))))
            add_command(cmd)

        elif cmd.startswith("u8g2.drawFilledEllipse") and len(nums) >= 4:
            x, y, rx, ry = nums[:4]
            drawn_shapes.append(("Elipse llena", (sx(x), sy(y)), (sx(x + 2*rx), sy(y + 2*ry))))
            add_command(cmd)

        # --- Triángulo (editable)
        elif cmd.startswith("u8g2.drawTriangle") and len(nums) >= 6:
            x0, y0, x1, y1, x2, y2 = nums[:6]
            puntos = [(sx(x0), sy(y0)), (sx(x1), sy(y1)), (sx(x2), sy(y2))]
            drawn_shapes.append(("Triángulo", puntos))
            add_command(cmd)

        elif cmd.startswith("u8g2.drawFilledTriangle") and len(nums) >= 6:
            x0, y0, x1, y1, x2, y2 = nums[:6]
            puntos = [(sx(x0), sy(y0)), (sx(x1), sy(y1)), (sx(x2), sy(y2))]
            drawn_shapes.append(("Triángulo lleno", puntos))
            add_command(cmd)

        # --- Marcos redondeados
        elif cmd.startswith("u8g2.drawRBox") and len(nums) >= 5:
            x, y, w, h, r = nums[:5]
            drawn_shapes.append(("Caja redonda llena", (sx(x), sy(y)), (sx(x + w), sy(y + h))))
            add_command(cmd)

        elif cmd.startswith("u8g2.drawRFrame") and len(nums) >= 5:
            x, y, w, h, r = nums[:5]
            drawn_shapes.append(("Marco redondo", (sx(x), sy(y)), (sx(x + w), sy(y + h))))
            add_command(cmd)
