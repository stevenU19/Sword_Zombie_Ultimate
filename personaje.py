import pygame
import constantes


class Personaje():
    def __init__(self, x, y, animaciones, animaciones_ataque, energia):
        self.flip = False # Voltear el personaje
        self.cant_monedas = 0
        self.energia = energia
        self.vida = True
        self.animaciones = animaciones
        self.animaciones_enemigo = animaciones
        self.animaciones_ataque = animaciones_ataque
        self.atacando = False

        # Imagen de la animacion que se muestra actualmente
        self.frame_index = 0

        # Se almacena la hora actual en milisegundos
        self.update_time = pygame.time.get_ticks()
        self.image = animaciones[self.frame_index]
        self.shape = self.image.get_rect()

        self.shape = pygame.Rect(0, 0,
                                 constantes.ANCHO_PERSONAJE,
                                 constantes.ALTO_PERSONAJE)
        self.shape.center = (x, y)

    def update(self):
        cooldown_animation = 250  # Tiempo entre frames

        # Comprobar si el personaje esta muerto
        if self.energia <= 0:
            self.energia = 0
            self.vida = False

        # Determinar la animación actual
        if self.atacando:
            animacion = self.animaciones_ataque
        else:
            animacion = self.animaciones

        # Actualizar la imagen
        if pygame.time.get_ticks() - self.update_time >= cooldown_animation:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()

            # Si la animación de ataque termina, volver a la animación normal
            if self.frame_index >= len(animacion):
                if self.atacando:
                    self.atacando = False  # Detener el estado de ataque
                self.frame_index = 0

        self.image = animacion[self.frame_index]

    # Evita que los personajes salgan de la ventana
    def limitar_movimiento(self):
        if self.shape.x < 0:
            self.shape.x = 0
        if self.shape.x + self.shape.width > constantes.ANCHO_VENTANA:
            self.shape.x = constantes.ANCHO_VENTANA - self.shape.width
        if self.shape.y < 0:
            self.shape.y = 0
        if self.shape.y + self.shape.height > constantes.ALTO_VENTANA:
            self.shape.y = constantes.ALTO_VENTANA - self.shape.height

    def movimiento(self, delta_X, delta_Y):

        if not self.atacando:  # No moverse si está atacando
            if delta_X < 0:
                self.flip = True
            if delta_X > 0:
                self.flip = False

        self.shape.x = self.shape.x + delta_X
        self.shape.y = self.shape.y + delta_Y

        self.limitar_movimiento()

    def atacar(self):
        if not self.atacando:  # Evita interrumpir un ataque en curso
            self.atacando = True
            self.frame_index = 0  # Reiniciar la animación de ataque
            #self.update_time = pygame.time.get_ticks()

    def mostrar(self, interfaz):
        imagen_flip = pygame.transform.flip(self.image, self.flip, False)
        interfaz.blit(imagen_flip, self.shape)
        #pygame.draw.rect(interfaz, constants.COLOR_PERSONAJE, self.shape, 1)

    def recibir_daño(self, dano):
        self.energia -= dano
        if self.energia < 0:
            self.energia = 0





