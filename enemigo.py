import random
import constantes
from personaje import Personaje

class Enemigo(Personaje):
    def __init__(self, x, y, animaciones, animaciones_ataque, energia):
        super().__init__(x, y, animaciones, animaciones_ataque, energia)
        self.direccion_x = random.choice([-1, 1])  # Movimiento aleatorio en x
        self.direccion_y = random.choice([-1, 1])  # Movimiento aleatorio en y
        self.velocidad = constantes.VELOCIDAD_ENEMIGO

    def mover(self):
        self.shape.x += self.direccion_x * self.velocidad
        self.shape.y += self.direccion_y * self.velocidad

        # Cambiar dirección aleatoriamente
        if random.randint(1, 100) > 98:
            self.direccion_x *= -1
        if random.randint(1, 100) > 98:
            self.direccion_y *= -1

        self.limitar_movimiento()  # Evitar que desaparezca de la pantalla
