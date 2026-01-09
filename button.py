import pygame
from config import WHITE, BLACK, RED, GRAY
from utils import render_text

class Button:
    def __init__(self, x, y, width, height, color, stats, unit_img, index):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.stats = stats
        self.unit_img = pygame.transform.scale(unit_img, (30, 30))
        self.index = index
        self.cost = stats["cost"]
        self.cooldown_time = stats["cd"] 
        self.current_cooldown = 0

    def update(self):
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

    def draw(self, screen, money):
        pygame.draw.rect(screen, WHITE, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 2)
        screen.blit(self.unit_img, (self.rect.x + 5, self.rect.y + 15))
        
        name_text = render_text(self.stats["name"], BLACK, "name")
        screen.blit(name_text, (self.rect.x + 40, self.rect.y + 5))
        
        cost_color = BLACK if money >= self.cost else RED
        cost_str = f"{self.cost}円"
        cost_text = render_text(cost_str, cost_color, "ui")
        screen.blit(cost_text, (self.rect.x + 40, self.rect.y + 35))

        if money < self.cost or self.current_cooldown > 0:
            s = pygame.Surface((self.rect.width, self.rect.height))
            s.set_alpha(100)
            s.fill(GRAY)
            screen.blit(s, (self.rect.x, self.rect.y))
        
        if self.current_cooldown > 0:
            ratio = self.current_cooldown / self.cooldown_time
            overlay_h = self.rect.height * ratio
            overlay = pygame.Surface((self.rect.width, overlay_h))
            overlay.set_alpha(150) 
            overlay.fill(RED)
            screen.blit(overlay, (self.rect.x, self.rect.y + (self.rect.height - overlay_h)))

    def is_clicked(self, pos, money):
        if self.rect.collidepoint(pos) and self.current_cooldown == 0 and money >= self.cost:
            self.current_cooldown = self.cooldown_time 
            return True
        return False
