import pygame
import os

# coordinate system is top left which is (0,0)
class Bird:
    BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird1.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird2.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images", "bird3.png")))]
    #BIRD_IMAGES = [pygame.transform.scale2x(pygame.image.load(os.path.join("images", "thug_life.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images", "thug_life.png"))), pygame.transform.scale2x(pygame.image.load(os.path.join("images", "thug_life.png")))]

    MAX_ROTATION = 25
    ROTATION_VELOCITY = 20
    TERMINAL_VELOCITY = 16
    ENDURANCE_VELOCITY = 2
    ANIMATION_TIME = 5


    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.velocity = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.BIRD_IMAGES[0]

    def jump(self):
        self.velocity = -9
        #self.velocity = -10.5
        self.tick_count = 0
        self.height = self.y

    def move(self):
        self.tick_count += 1
        displacement = self.velocity * self.tick_count + 1.5 * self.tick_count ** 2

        if displacement >= self.TERMINAL_VELOCITY:
            displacement = (displacement/abs(displacement)) * self.TERMINAL_VELOCITY

        if displacement < 0:
            displacement -= self.ENDURANCE_VELOCITY

        self.y += displacement

        # tilt up
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        else:
            if self.tilt > -90:
                self.tilt -= self.ROTATION_VELOCITY

    def draw(self, win):
        self.img_count += 1
        if self.img_count < self.ANIMATION_TIME:
            self.img = self.BIRD_IMAGES[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            self.img = self.BIRD_IMAGES[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            self.img = self.BIRD_IMAGES[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            self.img = self.BIRD_IMAGES[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            self.img = self.BIRD_IMAGES[0]
            self.img_count = 0

        if self.tilt <= -80:
            self.img = self.BIRD_IMAGES[1]
            self.img_count = self.ANIMATION_TIME * 2
        
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)
        win.blit(rotated_image, new_rect.topleft)
        
    def blitRotateCenter(self, surf, image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)

        surf.blit(rotated_image, new_rect.topleft)
    
    def get_mask(self):
        return pygame.mask.from_surface(self.img)










