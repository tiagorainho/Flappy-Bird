import pygame
import os

class Base:
    IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("images", "base.png")))
    WIDTH = IMG.get_width()
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self, vel):
        self.x1 -= vel
        self.x2 -= vel

        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))

