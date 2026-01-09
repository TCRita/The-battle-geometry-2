import pygame
from config import BLACK, RED, GREEN

class Castle:
    def __init__(self, image, x, y, health, is_enemy=False):
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.health = health
        self.max_health = health
        self.is_enemy = is_enemy
        self.is_alive = True

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if not self.is_alive: return
        bar_w, bar_h = 80, 8
        fill = (self.health / self.max_health) * bar_w
        bar_x = self.rect.centerx - bar_w//2
        bar_y = self.rect.top - 15
        pygame.draw.rect(screen, RED, (bar_x, bar_y, bar_w, bar_h))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, fill, bar_h))
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, bar_w, bar_h), 1)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0 and self.is_alive:
            self.health = 0
            self.is_alive = False
