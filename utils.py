import pygame
import os
import math
from config import BASE_DIR, GRAY

pygame.init()

font_path = 'font/Corporate-Logo-Rounded-Bold-ver3.otf'
debug_font = pygame.font.SysFont(None, 24)

def render_text(text, color, size="main"):
    try:
        if size == "big": s = 50
        elif size == "ui": s = 20
        elif size == "name": s = 14
        else: s = 24
        return pygame.font.Font(font_path, s).render(text, True, color)
    except:
        return debug_font.render(text, True, color)

def load_image(path, scale=None):
    path = path.replace('/', os.sep)
    full_path = os.path.join(BASE_DIR, path)
    if not os.path.exists(full_path):
        filename = os.path.basename(path)
        full_path = os.path.join(BASE_DIR, 'image', filename)

    try:
        img = pygame.image.load(full_path).convert_alpha()
        if scale:
            img = pygame.transform.scale(img, scale)
        return img
    except:
        surf = pygame.Surface(scale if scale else (60, 60))
        surf.fill(GRAY)
        return surf

def get_polygon_points(n, radius, cx, cy, angle_offset=0):
    points = []
    for i in range(n):
        angle = math.radians(360 / n * i - 90 + angle_offset)
        x = cx + radius * math.cos(angle)
        y = cy + radius * math.sin(angle)
        points.append((x, y))
    return points

def get_star_points(n, r_outer, r_inner, cx, cy, angle_offset=0):
    points = []
    for i in range(n * 2):
        angle = math.radians(360 / (n * 2) * i - 90 + angle_offset)
        r = r_outer if i % 2 == 0 else r_inner
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        points.append((x, y))
    return points
