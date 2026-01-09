import pygame
import random
import math
from config import *
from utils import get_polygon_points, get_star_points

def generate_geometric_char(seed_val, is_enemy=False):
    random.seed(seed_val)
    
    w, h = 100, 100
    
    # デフォルトの色設定
    if is_enemy:
        base_color = (random.randint(150, 255), random.randint(0, 100), random.randint(0, 100))
        sub_color = (random.randint(50, 150), 0, 0)
        shape_id = -1 # 敵用のランダム生成フラグ
    else:
        # 味方はID(seed_val)によって色と形を固定
        shape_id = seed_val
        colors = [
            RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA, 
            WHITE, ORANGE, PURPLE, GRAY, (0, 0, 128), (100, 200, 255)
        ]
        base_color = colors[seed_val % len(colors)]
        sub_color = (min(255, base_color[0]+50), min(255, base_color[1]+50), min(255, base_color[2]+50))

    # 敵キャラの特殊生成（既存のロジック維持）
    if is_enemy:
        shape_type = random.choice(["circle", "rect", "triangle", "diamond"])
        if seed_val == 200: shape_type = "star"; base_color = (255, 215, 0)
        elif seed_val == 201: shape_type = "hexagram"; base_color = (138, 43, 226)
        elif seed_val == 202: shape_type = "3d_cube"; base_color = (0, 191, 255)

    def draw_body(surf, color, scale=1.0, offset_x=0):
        cx, cy = w//2 + offset_x, h//2
        size = 30 * scale

        # --- 味方キャラクターの描画 (12種) ---
        if not is_enemy and 0 <= shape_id <= 11:
            if shape_id == 0: # 1. 正三角形 (Triangle)
                points = get_polygon_points(3, size, cx, cy)
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)
            
            elif shape_id == 1: # 2. 正方形 (Square)
                # 45度回転させて正方形らしく（ひし形と差別化のため0度でもよいが今回は45度）
                rect = pygame.Rect(0, 0, size*1.5, size*1.5)
                rect.center = (cx, cy)
                pygame.draw.rect(surf, color, rect)
                pygame.draw.rect(surf, BLACK, rect, 2)

            elif shape_id == 2: # 3. 正五角形 (Pentagon)
                points = get_polygon_points(5, size, cx, cy)
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)

            elif shape_id == 3: # 4. 正六角形 (Hexagon)
                points = get_polygon_points(6, size, cx, cy)
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)

            elif shape_id == 4: # 5. 円 (Circle)
                pygame.draw.circle(surf, color, (cx, cy), size)
                pygame.draw.circle(surf, BLACK, (cx, cy), size, 2)

            elif shape_id == 5: # 6. 星型 (Star)
                points = get_star_points(5, size, size*0.4, cx, cy)
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)

            elif shape_id == 6: # 7. 十字 (Cross)
                w_bar = size * 0.35
                points = [
                    (cx - w_bar, cy - size), (cx + w_bar, cy - size),
                    (cx + w_bar, cy - w_bar), (cx + size, cy - w_bar),
                    (cx + size, cy + w_bar), (cx + w_bar, cy + w_bar),
                    (cx + w_bar, cy + size), (cx - w_bar, cy + size),
                    (cx - w_bar, cy + w_bar), (cx - size, cy + w_bar),
                    (cx - size, cy - w_bar), (cx - w_bar, cy - w_bar)
                ]
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)

            elif shape_id == 7: # 8. ひし形 (Rhombus) - 鋭利
                points = [
                    (cx, cy - size*1.2), (cx + size*0.6, cy),
                    (cx, cy + size*1.2), (cx - size*0.6, cy)
                ]
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)

            elif shape_id == 8: # 9. 三日月 (Crescent)
                # ポリゴンで近似
                points = []
                for i in range(30, 331, 15):
                    rad = math.radians(i)
                    points.append((cx + size * math.cos(rad), cy + size * math.sin(rad)))
                offset = size * 0.4
                for i in range(330, 29, -15):
                    rad = math.radians(i)
                    points.append((cx + offset + size * 0.8 * math.cos(rad), cy + size * 0.8 * math.sin(rad)))
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)

            elif shape_id == 9: # 10. 台形 (Trapezoid)
                points = [
                    (cx - size*0.5, cy - size*0.5), (cx + size*0.5, cy - size*0.5),
                    (cx + size, cy + size*0.6), (cx - size, cy + size*0.6)
                ]
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)

            elif shape_id == 10: # 11. 六芒星 (Hexagram)
                points = get_star_points(6, size, size*0.5, cx, cy)
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)

            elif shape_id == 11: # 12. 雪の結晶 (Fractal/Snowflake)
                points = get_star_points(12, size, size*0.2, cx, cy)
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)
                pygame.draw.circle(surf, WHITE, (cx, cy), size*0.3)

        # --- 敵キャラクターの描画 (既存ロジック) ---
        else:
            if shape_type == "circle":
                pygame.draw.circle(surf, color, (cx, cy), size)
                pygame.draw.circle(surf, BLACK, (cx, cy), size, 2)
            elif shape_type == "rect":
                pygame.draw.rect(surf, color, (cx-size, cy-size, size*2, size*2))
                pygame.draw.rect(surf, BLACK, (cx-size, cy-size, size*2, size*2), 2)
            elif shape_type == "triangle":
                points = get_polygon_points(3, size, cx, cy)
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)
            elif shape_type == "diamond":
                points = get_polygon_points(4, size, cx, cy)
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)
            elif shape_type == "star":
                points = get_star_points(5, size*1.2, size*0.5, cx, cy)
                pygame.draw.polygon(surf, color, points)
                pygame.draw.polygon(surf, BLACK, points, 2)
            elif shape_type == "hexagram":
                points1 = get_polygon_points(3, size, cx, cy)
                points2 = get_polygon_points(3, size, cx, cy, 180)
                pygame.draw.polygon(surf, color, points1)
                pygame.draw.polygon(surf, BLACK, points1, 2)
                pygame.draw.polygon(surf, color, points2)
                pygame.draw.polygon(surf, BLACK, points2, 2)
            elif shape_type == "3d_cube":
                # 簡易的な3Dキューブ
                s = size * 0.8
                rect = pygame.Rect(cx-s, cy-s, s*2, s*2)
                pygame.draw.rect(surf, color, rect)
                pygame.draw.rect(surf, BLACK, rect, 2)

        # 目の描画
        eye_color = YELLOW if is_enemy else BLACK
        if not is_enemy and shape_id == 0: # Triangleは目が一つ（単眼）
            pygame.draw.circle(surf, eye_color, (cx, cy), 4)
        else:
            pygame.draw.circle(surf, eye_color, (cx - 8, cy - 2), 4)
            pygame.draw.circle(surf, eye_color, (cx + 8, cy - 2), 4)

    move_surf = pygame.Surface((w, h), pygame.SRCALPHA)
    draw_body(move_surf, base_color, scale=1.0)

    attack_frames = []
    f1 = pygame.Surface((w, h), pygame.SRCALPHA)
    draw_body(f1, sub_color, scale=0.9, offset_x=5)
    attack_frames.append(f1)
    
    f2 = pygame.Surface((w, h), pygame.SRCALPHA)
    draw_body(f2, base_color, scale=1.1, offset_x=10)
    # 攻撃エフェクト
    pygame.draw.circle(f2, WHITE, (w//2+30, h//2), 10) 
    attack_frames.append(f2)
    
    return move_surf, attack_frames
