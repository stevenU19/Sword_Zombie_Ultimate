import pygame.sprite

class DamageText(pygame.sprite.Sprite):
    def __init__ (self, x, y, damage, font, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = font.render(damage, True, color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.cont = 0



    def update(self):
        self.rect.y -= 2
        self.cont += 1
        if self.cont > 50:
            self.kill()
