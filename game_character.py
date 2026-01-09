import pygame
from config import RED, GREEN, SCREEN_WIDTH

class GameCharacter:
    def __init__(self, name, attack, health, speed, attack_range, image, attack_images, x, y, lane, is_enemy=False):
        self.name = name
        self.attack_power = attack
        self.health = health
        self.max_health = health
        self.speed = speed
        self.attack_range = attack_range
        self.image = image
        self.attack_images = attack_images
        self.x = x
        self.y = y
        self.lane = lane 
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.is_enemy = is_enemy
        self.is_alive = True
        self.state = "MOVE"
        self.target = None
        self.anim_index = 0
        self.anim_timer = 0
        self.attack_cooldown = 60 
        self.current_cooldown = 0

    def update(self, targets, castle_list):
        if not self.is_alive: return
        closest = None
        min_dist = float('inf')
        
        my_lane_castle = castle_list[self.lane]
        
        search_list = []
        for t in targets:
            if t.is_alive and t.lane == self.lane:
                search_list.append(t)
        
        if my_lane_castle.is_alive:
            search_list.append(my_lane_castle)
        
        for t in search_list:
            if self.is_enemy:
                real_dist = t.rect.left - self.rect.right
            else:
                real_dist = self.rect.left - t.rect.right

            if real_dist <= self.attack_range:
                # 距離の絶対値で比較しないと、背後の敵(マイナス距離)を優先してしまう
                dist_abs = abs(real_dist)
                if dist_abs < min_dist:
                    min_dist = dist_abs
                    closest = t
        
        if closest:
            self.state = "ATTACK"
            self.target = closest
        else:
            self.state = "MOVE"
            self.target = None

        if self.state == "MOVE":
            if self.is_enemy: self.x += self.speed
            else: self.x -= self.speed
            self.current_cooldown = 0
            
            # 画面枠から出ないように制御 (Clamp)
            if self.x < 0: self.x = 0
            if self.x > SCREEN_WIDTH - self.rect.width: self.x = SCREEN_WIDTH - self.rect.width

        elif self.state == "ATTACK":
            if self.current_cooldown > 0:
                self.current_cooldown -= 1
            else:
                self.anim_timer += 1
                if self.anim_timer >= 10:
                    self.anim_timer = 0
                    self.anim_index += 1
                    if self.anim_index == 1 and self.target and self.target.is_alive:
                        self.target.take_damage(self.attack_power)
                    if self.anim_index >= len(self.attack_images):
                        self.anim_index = 0
                        self.current_cooldown = self.attack_cooldown 

        self.rect.topleft = (self.x, self.y)

    def draw(self, screen):
        if not self.is_alive: return
        img = self.image
        if self.state == "ATTACK" and self.current_cooldown == 0 and self.anim_index < len(self.attack_images):
            img = self.attack_images[self.anim_index]
        
        draw_pos = (self.x, self.y)
        if self.state == "ATTACK" and self.current_cooldown == 0:
            draw_pos = (self.x - 5, self.y - 5)
        
        screen.blit(img, draw_pos)
        
        bar_x = self.x + 10
        pygame.draw.rect(screen, RED, (bar_x, self.y-10, 40, 4))
        fill = (self.health / self.max_health) * 40
        pygame.draw.rect(screen, GREEN, (bar_x, self.y-10, fill, 4))

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.is_alive = False
