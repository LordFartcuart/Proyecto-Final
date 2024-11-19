import pygame
import random
import time
pygame.init()

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AZUL = (0, 0, 255)

ANCHO, ALTO = 600, 400
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Juego de la Serpiente con Enemigos Estáticos y Potenciador")

tamaño_celda = 20
velocidad_serpiente = 10

def juego():
    game_over = False
    game_close = False

    x_snake = ANCHO // 2
    y_snake = ALTO // 2

    x_cambio = 0
    y_cambio = 0

    snake_list = []
    longitud_serpiente = 1

    comida_x = round(random.randrange(0, ANCHO - tamaño_celda) / tamaño_celda) * tamaño_celda
    comida_y = round(random.randrange(0, ALTO - tamaño_celda) / tamaño_celda) * tamaño_celda

    enemigo_x = round(random.randrange(0, ANCHO - tamaño_celda) / tamaño_celda) * tamaño_celda
    enemigo_y = round(random.randrange(0, ALTO - tamaño_celda) / tamaño_celda) * tamaño_celda
    potenciador_derr_enemigos_x = round(random.randrange(0, ANCHO - tamaño_celda) / tamaño_celda) * tamaño_celda
    potenciador_derr_enemigos_y = round(random.randrange(0, ALTO - tamaño_celda) / tamaño_celda) * tamaño_celda

    derr_enemigos = False
    tiempo_derr_enemigos = 0

    reloj = pygame.time.Clock()

    while not game_over:
        while game_close:
            pantalla.fill(BLANCO)
            fuente = pygame.font.SysFont("bahnschrift", 25)
            mensaje = fuente.render("Presiona C para jugar de nuevo o Q para salir", True, ROJO)
            pantalla.blit(mensaje, [ANCHO / 6, ALTO / 3])
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        juego()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_cambio = -tamaño_celda
                    y_cambio = 0
                elif event.key == pygame.K_RIGHT:
                    x_cambio = tamaño_celda
                    y_cambio = 0
                elif event.key == pygame.K_UP:
                    y_cambio = -tamaño_celda
                    x_cambio = 0
                elif event.key == pygame.K_DOWN:
                    y_cambio = tamaño_celda
                    x_cambio = 0

        if x_snake >= ANCHO or x_snake < 0 or y_snake >= ALTO or y_snake < 0:
            game_close = True

        x_snake += x_cambio
        y_snake += y_cambio
        pantalla.fill(NEGRO)

        pygame.draw.rect(pantalla, VERDE, [comida_x, comida_y, tamaño_celda, tamaño_celda])

        pygame.draw.rect(pantalla, ROJO, [enemigo_x, enemigo_y, tamaño_celda, tamaño_celda])
        pygame.draw.rect(pantalla, AZUL, [potenciador_derr_enemigos_x, potenciador_derr_enemigos_y, tamaño_celda, tamaño_celda])

        snake_head = [x_snake, y_snake]
        snake_list.append(snake_head)

        if len(snake_list) > longitud_serpiente:
            del snake_list[0]

        for segmento in snake_list[:-1]:
            if segmento == snake_head:
                game_close = True

        for segmento in snake_list:
            pygame.draw.rect(pantalla, BLANCO, [segmento[0], segmento[1], tamaño_celda, tamaño_celda])

        pygame.display.update()

        if x_snake == comida_x and y_snake == comida_y:
            comida_x = round(random.randrange(0, ANCHO - tamaño_celda) / tamaño_celda) * tamaño_celda
            comida_y = round(random.randrange(0, ALTO - tamaño_celda) / tamaño_celda) * tamaño_celda
            longitud_serpiente += 1

        if x_snake == enemigo_x and y_snake == enemigo_y:
            if derr_enemigos:
                enemigo_x = round(random.randrange(0, ANCHO - tamaño_celda) / tamaño_celda) * tamaño_celda
                enemigo_y = round(random.randrange(0, ALTO - tamaño_celda) / tamaño_celda) * tamaño_celda
            else:
                game_close = True

        if x_snake == potenciador_derr_enemigos_x and y_snake == potenciador_derr_enemigos_y:
            derr_enemigos = True
            tiempo_derr_enemigos = time.time()
            potenciador_derr_enemigos_x, potenciador_derr_enemigos_y = -tamaño_celda, -tamaño_celda

        # Verificar si el potenciador ha expirado
        if derr_enemigos and time.time() - tiempo_derr_enemigos > 10:
            derr_enemigos = False
            # Hacer que el potenciador reaparezca en una posición aleatoria
            while True:
                potenciador_derr_enemigos_x = round(random.randrange(0, ANCHO - tamaño_celda) / tamaño_celda) * tamaño_celda
                potenciador_derr_enemigos_y = round(random.randrange(0, ALTO - tamaño_celda) / tamaño_celda) * tamaño_celda
                # Asegurarse de que el potenciador no reaparezca dentro de la serpiente o en un enemigo
                if [potenciador_derr_enemigos_x, potenciador_derr_enemigos_y] not in snake_list and \
                    (potenciador_derr_enemigos_x, potenciador_derr_enemigos_y) != (enemigo_x, enemigo_y):
                    break


                        
        reloj.tick(velocidad_serpiente)

    pygame.quit()
    quit()

# Ejecutar el juego
juego()
