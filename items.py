import pygame.sprite

class Item(pygame.sprite.Sprite):
    def __init__ (self, x, y, item_type, lista_animacion):
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type #0 indica monedas, 1 indica posion de vida
        self.lista_animacion = lista_animacion
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        self.image = self.lista_animacion[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


    def update(self, personaje):

        # Colision entre personaje y los items
        if self.rect.colliderect(personaje.shape):
            # Para las monedas
            if self.item_type == 0:
                personaje.cant_monedas += 1

            # Para las pociones
            elif self.item_type == 1:
                personaje.energia += 50
                if personaje.energia > 100:
                    personaje.energia = 100
            self.kill()



        cooldown_animation = 100
        self.image = self.lista_animacion[self.frame_index]

        if pygame.time.get_ticks() - self.update_time > cooldown_animation:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.lista_animacion):
            self.frame_index = 0

