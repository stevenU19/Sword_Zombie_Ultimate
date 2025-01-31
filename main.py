import random
import subprocess
import sys
import pygame
import constantes

from personaje import Personaje
from textos import DamageText
from items import Item
from enemigo import Enemigo

def restart():
    pygame.quit()
    subprocess.call([sys.executable] + sys.argv)
    sys.exit()

pygame.init()

# Se establecen las caracteristicas de la Ventana
ventana = pygame.display.set_mode((constantes.ANCHO_VENTANA,
                                   constantes.ALTO_VENTANA))

background = pygame.image.load("assets/images/background.jpg")

# Se define el titulo de la Ventana
pygame.display.set_caption("Sword Zombie Ultimate")

# Se importan las fuentes
font = pygame.font.Font("assets//fonts//m6.ttf", 30)
font_game_over = pygame.font.Font("assets//fonts//m6.ttf", 90)
font_reinicio = pygame.font.Font("assets//fonts//m6.ttf", 30)
font_inicio = pygame.font.Font("assets//fonts//m6.ttf", 30)
font_titulo = pygame.font.Font("assets//fonts//m6.ttf", 80)


# Botones de Inicio
btn_jugar = pygame.Rect(constantes.ANCHO_VENTANA/2 - 100,
                        constantes.ALTO_VENTANA/2 + 25, 160, 40)
btn_salir = pygame.Rect(constantes.ANCHO_VENTANA/2 - 100,
                        constantes.ALTO_VENTANA/2 + 100, 160, 40)

# Texto de botones
texto_btn_reinicio = font_reinicio.render("Reiniciar", True, constantes.COLOR_NEGRO)
texto_btn_jugar = font_reinicio.render("Jugar", True, constantes.COLOR_NEGRO)
texto_btn_salir = font_reinicio.render("Salir", True, constantes.COLOR_BLANCO)

# Pantalla de Inicio
def pantalla_inicio():
    ventana.fill(constantes.COLOR_AZUL)
    mostrar_texto("SWORD ZOMBIE ULTIMATE", font_titulo, constantes.COLOR_BLANCO,
                  constantes.ANCHO_VENTANA/20,
                  constantes.ALTO_VENTANA/2 - 100)
    pygame.draw.rect(ventana, constantes.COLOR_MONEDA, btn_jugar)
    pygame.draw.rect(ventana, constantes.COLOR_ROJO, btn_salir)
    ventana.blit(texto_btn_jugar, (btn_jugar.x+50, btn_jugar.y+10))
    ventana.blit(texto_btn_salir, (btn_salir.x + 50, btn_salir.y + 10))
    pygame.display.update()


# Escalado de la imagen del Personaje
def escalar_img(image, width, height):
    return pygame.transform.scale(image, (width*constantes.ESCALA_PERSONAJE,
                                          height*constantes.ESCALA_PERSONAJE))

# Cargar animaciones de movimiento
animaciones = []
for i in range(2):  # Número de frames de la animación de movimiento
    img = pygame.image.load(f"assets/images/characters/player/character_run_{i}.png")
    img = escalar_img(img, constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE)
    animaciones.append(img)

# Cargar animaciones de ataque
animaciones_ataque = []
for i in range(2):  # Número de frames de la animación de ataque
    img = pygame.image.load(f"assets/images/characters/player/character_attack_{i}.png")
    img = escalar_img(img, constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE)
    animaciones_ataque.append(img)


# Cargar animaciones de enemigos
animaciones_enemigos = []
for i in range(2):
    img = pygame.image.load(f"assets//images//characters//enemies//enemies_attack_{i}.png")
    img = escalar_img(img, constantes.ANCHO_PERSONAJE, constantes.ALTO_PERSONAJE)
    animaciones_enemigos.append(img)

# Cargar imagen de la posion
pocion_vida = pygame.image.load("assets//images//live.png")
pocion_vida = escalar_img(pocion_vida, 15,15)

# Cargar animaciones de las monedas
animaciones_monedas = []
for i in range(7):
    img = pygame.image.load(f"assets//images//coin//coin{i}.png")
    img = escalar_img(img, 10,10)
    animaciones_monedas.append(img)

# Se inicializar el personaje del juego
jugador = Personaje(50, 50, animaciones, animaciones_ataque, 100)

# Se inicializan los enemigos
enemigo1 = Enemigo(400, 300, animaciones_enemigos, animaciones_enemigos, 100)
enemigo2 = Enemigo(100, 250, animaciones_enemigos, animaciones_enemigos, 100)
enemigo3 = Enemigo(350, 500, animaciones_enemigos, animaciones_enemigos, 100)
enemigo4 = Enemigo(500, 100, animaciones_enemigos, animaciones_enemigos, 100)
enemigo5 = Enemigo(600, 500, animaciones_enemigos, animaciones_enemigos, 100)

# Crear lista de enemigos
lista_enemigos = []
lista_enemigos.append(enemigo1)
lista_enemigos.append(enemigo2)
lista_enemigos.append(enemigo3)
lista_enemigos.append(enemigo4)
lista_enemigos.append(enemigo5)

# Se definen las variables de movimiento del personaje
mover_arriba = False
mover_abajo = False
mover_izq = False
mover_der = False

# Se definen los Items, moneda y pocion
moneda1 = Item(200,300, 0, animaciones_monedas)
moneda2 = Item(400,300, 0, animaciones_monedas)
moneda3 = Item(600,300, 0, animaciones_monedas)
moneda4 = Item(400,100, 0, animaciones_monedas)
moneda5 = Item(400,500, 0, animaciones_monedas)
pocion = Item(400, 55, 1, [pocion_vida])
pocion2 = Item(400, 555, 1, [pocion_vida])

# Grupo de sprites
grupo_damage_text = pygame.sprite.Group()
grupo_items = pygame.sprite.Group()

damage_text = DamageText(100, 240, " ", font, constantes.COLOR_TEXTO_DAMAGE)
grupo_damage_text.add(damage_text)

grupo_items.add(moneda1)
grupo_items.add(moneda2)
grupo_items.add(moneda3)
grupo_items.add(moneda4)
grupo_items.add(moneda5)
grupo_items.add(pocion)
grupo_items.add(pocion2)

# Controlar el frame rate
reloj = pygame.time.Clock()

run = True
dano = 0
pos_dano = None

def mostrar_texto(texto, fuente, color, x, y):
    img = fuente.render(texto, True, color)
    ventana.blit(img, (x,y))

# Barra de la Vida del personaje
def barra_vida(ventana, x, y, vida_actual, vida_maxima):
    largo = 200  # Ancho de la barra
    alto = 20  # Alto de la barra
    vida = max(vida_actual, 0)  # Evitar valores negativos

    # Calcular el porcentaje de vida
    porcentaje_vida = vida / vida_maxima
    vida_ancho = int(largo * porcentaje_vida)

    # Fondo de la barra (rojo)
    pygame.draw.rect(ventana, (255, 0, 0), (x, y, largo, alto))

    # Vida restante (verde)
    pygame.draw.rect(ventana, (0, 255, 0), (x, y, vida_ancho, alto))

    # Borde negro alrededor de la barra
    pygame.draw.rect(ventana, (255, 255, 255), (x, y, largo, alto), 2)

# ---------------------------------------
# -------------- EJECUCIÓN --------------
# ---------------------------------------
mostrar_inicio = True
run = True
while run:
    if mostrar_inicio:
        pantalla_inicio()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if btn_jugar.collidepoint(event.pos):
                    mostrar_inicio = False
                if btn_salir.collidepoint(event.pos):
                    run = False
                    pygame.quit()
    else:
        reloj.tick(constantes.FPS)

        # Dibujar el fondo
        ventana.blit(background, (0, 0))

        # Calcular el movimiento del personaje
        delta_X = 0
        delta_Y = 0

        if mover_der == True:
            delta_X = constantes.VELOCIDAD

        if mover_izq == True:
            delta_X = -constantes.VELOCIDAD

        if mover_arriba == True:
            delta_Y = -constantes.VELOCIDAD

        if mover_abajo == True:
            delta_Y = constantes.VELOCIDAD

        # Mover al Personaje
        jugador.movimiento(delta_X, delta_Y)

        # Actualiza los estados del jugador
        jugador.update()

        # Actualiza los estados de los enemigos y los hace moverse
        for enemigo in lista_enemigos:
            enemigo.mover()
            enemigo.update()

            # Verificar colisión con el jugador
            if jugador.shape.colliderect(enemigo.shape):
                jugador.energia -= 1  # Reducir vida del jugador
                if jugador.energia < 0:
                    jugador.energia = 0  # Evitar valores negativos

        # Actualizar dano
        grupo_damage_text.update()

        # Actualizar Items
        grupo_items.update(jugador)

        # Se muestra el dano
        grupo_damage_text.draw(ventana)

        # Mostrar textos
        mostrar_texto(f"Monedas: {jugador.cant_monedas}", font, constantes.COLOR_MONEDA, 650, 20)

        # Se muestran los items
        grupo_items.draw(ventana)

        # Se muestra el jugador
        jugador.mostrar(ventana)

        # Se muestran los enemigos
        for a in lista_enemigos:
            a.mostrar(ventana)

        for event in pygame.event.get():

            # Cerrar el Programa
            if event.type == pygame.QUIT:
                run = False

            # Movimiento del Personaje
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    mover_izq = True
                if event.key == pygame.K_d:
                    mover_der = True
                if event.key == pygame.K_w:
                    mover_arriba = True
                if event.key == pygame.K_s:
                    mover_abajo = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    mover_izq = False
                if event.key == pygame.K_d:
                    mover_der = False
                if event.key == pygame.K_w:
                    mover_arriba = False
                if event.key == pygame.K_s:
                    mover_abajo = False

            # Detectar clic del mouse para atacar
            if event.type == pygame.MOUSEBUTTONDOWN:

                jugador.atacar()

                # Verificar colisión con los enemigos
                for enemigo in lista_enemigos:
                    if jugador.shape.colliderect(enemigo.shape):

                        # Reducir la vida del enemigo
                        dano = 95 + random.randint(0, 5)

                        pos_dano = enemigo.shape
                        enemigo.recibir_daño(dano)

                        damage_text = DamageText(pos_dano.centerx, pos_dano.centery, str(dano), font, constantes.COLOR_TEXTO_DAMAGE)
                        grupo_damage_text.add(damage_text)

                        # Verificar si la vida del enemigo llegó a 0 o menos
                        if enemigo.vida <= 0:
                            lista_enemigos.remove(enemigo)


        # Barra de vida del jugador
        barra_vida(ventana, 20, 20, jugador.energia, 100)

        # -------- VENTANA DE GAME OVER --------
        if jugador.energia == 0:
            #jugador.vida = False
            ventana.fill(constantes.COLOR_GAME_OVER)
            mostrar_texto(f"GAME OVER", font_game_over,
                          constantes.COLOR_BLANCO,
                          constantes.ANCHO_VENTANA/2 - 180,
                          constantes.ALTO_VENTANA/2)

            # Boton de Reinicio
            btn_reinicio = pygame.Rect(constantes.ANCHO_VENTANA/2 - 100, 400, 200, 40)

            pygame.draw.rect(ventana, constantes.COLOR_MONEDA, btn_reinicio)
            ventana.blit(texto_btn_reinicio,
                         (btn_reinicio.x + 50, btn_reinicio.y + 10))

            # Detectar clic del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Boton de reinicio
                if btn_reinicio.collidepoint(event.pos):
                    restart()

        # -------- VENTANA DE VICTORIA --------
        if lista_enemigos == [] and jugador.cant_monedas == 5:
            ventana.fill(constantes.COLOR_AZUL)
            mostrar_texto(f"¡HAS GANADO!", font_game_over,
                          constantes.COLOR_BLANCO,
                          constantes.ANCHO_VENTANA / 2 - 200,
                          constantes.ALTO_VENTANA / 2)

            btn_reinicio = pygame.Rect(constantes.ANCHO_VENTANA / 2 - 100, 400, 200, 40)

            pygame.draw.rect(ventana, constantes.COLOR_MONEDA, btn_reinicio)
            ventana.blit(texto_btn_reinicio,
                         (btn_reinicio.x + 50, btn_reinicio.y + 10))
            # Detectar clic del mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Boton de reinicio
                if btn_reinicio.collidepoint(event.pos):
                    restart()

        # Actualizar la pantalla
        pygame.display.update()

pygame.quit()
