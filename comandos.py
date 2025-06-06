# comandos.py
u8g2_commands = []

def add_command(cmd):
    if cmd not in u8g2_commands:
        u8g2_commands.append(cmd)

def get_commands():
    return u8g2_commands

def clear_commands():
    u8g2_commands.clear()
