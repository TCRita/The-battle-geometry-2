import pygame
import random
import sys
from config import *
from utils import load_image, render_text
from generator import generate_geometric_char
from castle import Castle
from game_character import GameCharacter
from button import Button

pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("幾何学戦争")

print(f"リソース読み込み場所: {BASE_DIR}")

bg_image = load_image('image/bg_optimized.png', (SCREEN_WIDTH, SCREEN_HEIGHT))

p_castle_img = load_image('image/castle.png', (100, 100))
e_castle_img = load_image('image/castle_enemy.png', (100, 100))
e_castle_img_top = load_image('image/castle_enemy1.png', (100, 100))

unit_images = []
unit_attack_anims = []

# 味方12種類の生成
for i in range(12):
    img, anim = generate_geometric_char(seed_val=i, is_enemy=False)
    unit_images.append(img)
    unit_attack_anims.append(anim)

# ステータス設定（ユーザー指定の特徴を反映）
UNIT_STATS = [
    # 1. Triangle: 最速、紙装甲、安価
    {"name": "トライアングル", "atk": 30,  "hp": 80,  "cost": 50,   "cd": 30,   "speed": 5, "range": 5},
    # 2. Square: 基本、バランス
    {"name": "スクエア",     "atk": 50,  "hp": 250, "cost": 200,  "cd": 100,  "speed": 2, "range": 5},
    # 3. Pentagon: タンク、守り堅い
    {"name": "ペンタゴン",   "atk": 40,  "hp": 600, "cost": 400,  "cd": 150,  "speed": 1, "range": 5},
    # 4. Hexagon: 範囲、バリア持ちイメージ（HP高め）
    {"name": "ヘキサゴン",   "atk": 60,  "hp": 450, "cost": 500,  "cd": 180,  "speed": 2, "range": 40},
    # 5. Circle: バウンサー（速い、特殊な動きイメージ）
    {"name": "サークル",     "atk": 40,  "hp": 200, "cost": 250,  "cd": 60,   "speed": 4, "range": 5},
    # 6. Star: 高火力アタッカー
    {"name": "スター",       "atk": 150, "hp": 150, "cost": 600,  "cd": 200,  "speed": 3, "range": 5},
    # 7. Cross: 支援（低コスト、中衛）
    {"name": "クロス",       "atk": 20,  "hp": 300, "cost": 300,  "cd": 120,  "speed": 2, "range": 100},
    # 8. Rhombus: 貫通（長射程イメージ）
    {"name": "ロンバス",     "atk": 80,  "hp": 120, "cost": 450,  "cd": 250,  "speed": 3, "range": 150},
    # 9. Crescent: ブーメラン（特殊軌道イメージ、中距離）
    {"name": "クレセント",   "atk": 70,  "hp": 180, "cost": 350,  "cd": 100,  "speed": 4, "range": 60},
    # 10. Trapezoid: 重戦車（超鈍足、高HP）
    {"name": "トラペゾイド", "atk": 100, "hp": 1000,"cost": 900,  "cd": 400,  "speed": 1, "range": 5},
    # 11. Hexagram: 魔法使い（遠距離、高コスト）
    {"name": "ヘキサグラム", "atk": 200, "hp": 150, "cost": 800,  "cd": 300,  "speed": 2, "range": 200},
    # 12. Fractal: ボス級（最強）
    {"name": "フラクタル",   "atk": 250, "hp": 1500,"cost": 2000, "cd": 600,  "speed": 2, "range": 30},
]

PLAYER_DECK = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

enemy_images_cache = {}
enemy_anims_cache = {}

e_idx_list = [100, 101, 102, 104, 105] 
for idx in e_idx_list:
    m, a = generate_geometric_char(seed_val=idx, is_enemy=True)
    enemy_images_cache[idx] = m
    enemy_anims_cache[idx] = a

boss_list = [200, 201, 202]
for idx in boss_list:
    m, a = generate_geometric_char(seed_val=idx, is_enemy=True)
    enemy_images_cache[idx] = m
    enemy_anims_cache[idx] = a

def team_select_screen():
    running = True
    cols = 4
    margin = 20
    icon_w, icon_h = 140, 80
    start_x = (SCREEN_WIDTH - (icon_w * cols + margin * (cols-1))) // 2
    start_y = 120
    
    while running:
        screen.fill(LIGHT_BLUE)
        
        title = render_text(f"出撃メンバー選択 ({len(PLAYER_DECK)}/10)", BLACK, "big")
        screen.blit(title, title.get_rect(center=(SCREEN_WIDTH//2, 50)))
        
        desc = render_text("クリックで選択/解除・最大10体まで", BLACK, "ui")
        screen.blit(desc, desc.get_rect(center=(SCREEN_WIDTH//2, 90)))
        
        mouse_pos = pygame.mouse.get_pos()
        clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                clicked = True
        
        back_rect = pygame.Rect(SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT - 80, 200, 60)
        pygame.draw.rect(screen, WHITE, back_rect)
        pygame.draw.rect(screen, BLACK, back_rect, 3)
        back_text = render_text("決 定", BLACK)
        screen.blit(back_text, back_text.get_rect(center=back_rect.center))
        
        if clicked and back_rect.collidepoint(mouse_pos):
            running = False
            
        for i, stats in enumerate(UNIT_STATS):
            row = i // cols
            col = i % cols
            x = start_x + col * (icon_w + margin)
            y = start_y + row * (icon_h + margin)
            rect = pygame.Rect(x, y, icon_w, icon_h)
            
            is_selected = i in PLAYER_DECK
            bg_color = (150, 255, 150) if is_selected else (220, 220, 220)
            pygame.draw.rect(screen, bg_color, rect)
            pygame.draw.rect(screen, BLACK, rect, 2)
            
            img = pygame.transform.scale(unit_images[i], (40, 40))
            screen.blit(img, (rect.x + 10, rect.y + 20))
            name = render_text(stats["name"], BLACK, "name")
            screen.blit(name, (rect.x + 60, rect.y + 30))
            
            if clicked and rect.collidepoint(mouse_pos):
                if is_selected:
                    if len(PLAYER_DECK) > 1:
                        PLAYER_DECK.remove(i)
                else:
                    if len(PLAYER_DECK) < 10:
                        PLAYER_DECK.append(i)
                        PLAYER_DECK.sort()

        pygame.display.flip()
        pygame.time.Clock().tick(60)

def stage_select_screen():
    running = True
    selected_stage = None
    
    btn_w, btn_h = 240, 70
    center_x = SCREEN_WIDTH // 2
    
    buttons = [
        {"rect": pygame.Rect(center_x - btn_w // 2, 130, btn_w, btn_h), "label": "ステージ 1", "action": "stage", "id": 1},
        {"rect": pygame.Rect(center_x - btn_w // 2, 220, btn_w, btn_h), "label": "ステージ 2", "action": "stage", "id": 2},
        {"rect": pygame.Rect(center_x - btn_w // 2, 310, btn_w, btn_h), "label": "ステージ 3", "action": "stage", "id": 3},
        {"rect": pygame.Rect(center_x - btn_w // 2, 420, btn_w, btn_h), "label": "チーム編成", "action": "team", "id": 0}
    ]

    while running:
        screen.fill(LIGHT_BLUE)
        title = render_text("ステージを選択してください", BLACK, "big")
        screen.blit(title, title.get_rect(center=(center_x, 60)))
        
        mouse_pos = pygame.mouse.get_pos()
        
        for btn in buttons:
            color = WHITE if btn["rect"].collidepoint(mouse_pos) else (230, 230, 230)
            if btn["action"] == "team": color = (255, 255, 200) if btn["rect"].collidepoint(mouse_pos) else (240, 240, 150)
            
            pygame.draw.rect(screen, color, btn["rect"])
            pygame.draw.rect(screen, BLACK, btn["rect"], 3)
            
            text = render_text(btn["label"], BLACK)
            screen.blit(text, text.get_rect(center=btn["rect"].center))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for btn in buttons:
                    if btn["rect"].collidepoint(event.pos):
                        if btn["action"] == "stage":
                            selected_stage = btn["id"]
                            running = False
                        elif btn["action"] == "team":
                            team_select_screen()

        pygame.display.flip()
        pygame.time.Clock().tick(60)
        
    return selected_stage

def run_game(stage_id):
    clock = pygame.time.Clock()
    running = True
    game_over = False

    spawn_interval = 3000
    castle_hp = 3000
    if stage_id == 1:
        spawn_interval = 3000
        castle_hp = 3000
    elif stage_id == 2:
        spawn_interval = 2500
        castle_hp = 5000
    elif stage_id == 3:
        spawn_interval = 1500
        castle_hp = 15000
    
    player_units = []
    enemies = []
    buttons = []

    money = 500
    max_money = 10000 
    money_timer = 0
    spawn_timer = 0
    
    LANE_Y_COORDS = [170, 370] 

    enemy_castles = []
    ec1 = Castle(e_castle_img_top, 80, LANE_Y_COORDS[0], castle_hp, True)
    enemy_castles.append(ec1)
    ec2 = Castle(e_castle_img, 80, LANE_Y_COORDS[1], castle_hp, True)
    enemy_castles.append(ec2)
    
    player_castles = []
    pc1 = Castle(p_castle_img, SCREEN_WIDTH - 80, LANE_Y_COORDS[0], 3000, False)
    player_castles.append(pc1)
    pc2 = Castle(p_castle_img, SCREEN_WIDTH - 80, LANE_Y_COORDS[1], 3000, False)
    player_castles.append(pc2)
    
    current_spawn_lane = 0 

    btn_w, btn_h = 130, 60 
    margin_x = 10
    margin_y = 10
    cols_in_row = 5
    total_width = cols_in_row * btn_w + (cols_in_row - 1) * margin_x
    start_x = (SCREEN_WIDTH - total_width) // 2
    
    for i, unit_idx in enumerate(PLAYER_DECK):
        stats = UNIT_STATS[unit_idx]
        row = i // cols_in_row
        col = i % cols_in_row
        bx = start_x + col * (btn_w + margin_x)
        by = SCREEN_HEIGHT - ((row + 1) * btn_h) - ((row + 1) * margin_y)
        u_img = unit_images[unit_idx]
        btn = Button(bx, by, btn_w, btn_h, WHITE, stats, u_img, unit_idx)
        buttons.append(btn)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    current_spawn_lane = 1 - current_spawn_lane
            
            elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if event.button == 1:
                    for btn in buttons:
                        if btn.is_clicked(event.pos, money):
                            money -= btn.cost
                            target_y = LANE_Y_COORDS[current_spawn_lane]
                            spawn_x = player_castles[current_spawn_lane].rect.centerx - 30
                            
                            idx = btn.index
                            stats = UNIT_STATS[idx]
                            
                            # キャラクター生成 (IDに応じたステータスを使用)
                            unit = GameCharacter(
                                stats["name"], 
                                stats["atk"], 
                                stats["hp"], 
                                stats["speed"], 
                                stats["range"], 
                                unit_images[idx], 
                                unit_attack_anims[idx], 
                                spawn_x, 
                                target_y - 30, 
                                current_spawn_lane, 
                                False
                            )
                            player_units.append(unit)

        if not game_over:
            money_timer += clock.get_time()
            if money_timer >= 100:
                money += 20 
                if money > max_money: money = max_money
                money_timer = 0
            
            for btn in buttons: btn.update()

            spawn_timer += clock.get_time()
            if spawn_timer >= spawn_interval:
                enemy_lane = random.choice([0, 1])
                target_y = LANE_Y_COORDS[enemy_lane]
                spawn_x = enemy_castles[enemy_lane].rect.centerx - 30

                if enemy_castles[enemy_lane].is_alive:
                    e_idx = 0
                    r = random.randint(0, 100)
                    
                    if stage_id == 1:
                        if r < 50: e_idx = 100
                        elif r < 90: e_idx = 101
                        else: e_idx = 200
                    elif stage_id == 2:
                        if r < 40: e_idx = 102
                        elif r < 80: e_idx = 105
                        else: e_idx = 201
                    elif stage_id == 3:
                        if r < 40: e_idx = 100
                        elif r < 80: e_idx = 104
                        else: e_idx = 202

                    enemy = None
                    if e_idx == 100:
                        enemy = GameCharacter("敵ボール", 20, 100, 1, 5, enemy_images_cache[100], enemy_anims_cache[100], spawn_x, target_y-30, enemy_lane, True)
                    elif e_idx == 101:
                        enemy = GameCharacter("敵タンク", 10, 300, 1, 5, enemy_images_cache[101], enemy_anims_cache[101], spawn_x, target_y-30, enemy_lane, True)
                    elif e_idx == 200:
                        enemy = GameCharacter("スターボス", 50, 1000, 1, 20, enemy_images_cache[200], enemy_anims_cache[200], spawn_x, target_y-30, enemy_lane, True)
                    elif e_idx == 102:
                        enemy = GameCharacter("敵リング", 40, 300, 1, 5, enemy_images_cache[102], enemy_anims_cache[102], spawn_x, target_y-30, enemy_lane, True)
                    elif e_idx == 105:
                        enemy = GameCharacter("敵忍者", 30, 150, 3, 5, enemy_images_cache[105], enemy_anims_cache[105], spawn_x, target_y-30, enemy_lane, True)
                    elif e_idx == 201:
                        enemy = GameCharacter("ヘキサボス", 100, 2500, 1, 30, enemy_images_cache[201], enemy_anims_cache[201], spawn_x, target_y-30, enemy_lane, True)
                    elif e_idx == 104:
                        enemy = GameCharacter("敵ビースト", 100, 1000, 3, 5, enemy_images_cache[104], enemy_anims_cache[104], spawn_x, target_y-30, enemy_lane, True)
                    elif e_idx == 202:
                        enemy = GameCharacter("立体魔王", 300, 5000, 1, 40, enemy_images_cache[202], enemy_anims_cache[202], spawn_x, target_y-30, enemy_lane, True)
                    
                    if enemy:
                        enemies.append(enemy)

                spawn_timer = 0

            for u in player_units: u.update(enemies, enemy_castles)
            for e in enemies: e.update(player_units, player_castles)

            player_units = [u for u in player_units if u.is_alive]
            killed = [e for e in enemies if not e.is_alive]
            if killed: 
                money += 100
                if money > max_money: money = max_money
            enemies = [e for e in enemies if e.is_alive]

            lose_cond = (not player_castles[0].is_alive) or (not player_castles[1].is_alive)
            win_cond = (not enemy_castles[0].is_alive) and (not enemy_castles[1].is_alive)

            if lose_cond or win_cond:
                game_over = True
                if lose_cond:
                    result_text = "GAME OVER..."
                    result_color = RED
                else:
                    result_text = "VICTORY!"
                    result_color = BLUE

        screen.blit(bg_image, (0, -130))
        
        for c in player_castles: c.draw(screen)
        for c in enemy_castles: c.draw(screen)
        
        for u in player_units: u.draw(screen)
        for e in enemies: e.draw(screen)
        for btn in buttons: btn.draw(screen, money)
        
        stage_name = render_text(f"STAGE {stage_id}", BLACK, "ui")
        screen.blit(stage_name, (10, 10))
        
        money_text = render_text(f"所持金: {money}/{max_money}", BLACK)
        screen.blit(money_text, (SCREEN_WIDTH - 250, 20))

        lane_str = "出撃レーン: [ 上 ]" if current_spawn_lane == 0 else "出撃レーン: [ 下 ]"
        lane_color = RED if current_spawn_lane == 0 else BLUE
        lane_text = render_text(lane_str, lane_color)
        screen.blit(lane_text, (SCREEN_WIDTH // 2 - 100, 20))
        
        hint_text = render_text("Spaceキーで切替", BLACK, "ui")
        screen.blit(hint_text, (SCREEN_WIDTH // 2 - 80, 50))

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(150)
            overlay.fill(BLACK)
            screen.blit(overlay, (0,0))
            text = render_text(result_text, result_color, "big")
            screen.blit(text, text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2)))
            
            sub_text = render_text("Click to Return Title", WHITE)
            screen.blit(sub_text, sub_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60)))
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    return

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    try:
        while True:
            selected_stage_id = stage_select_screen()
            if selected_stage_id:
                run_game(selected_stage_id)
    except KeyboardInterrupt:
        print("\nゲームを終了します")
        pygame.quit()
        sys.exit()
    except Exception as e:
        import traceback
        with open("error.log", "w") as f:
            f.write(traceback.format_exc())
        print("エラーが発生しました。error.logを確認してください。")
        pygame.quit()
        sys.exit()
