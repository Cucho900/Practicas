import pygame
pygame.init()

#Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
player_width = 15
player_height = 90

screen_size = (800, 600)
screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()

fondo = pygame.image.load('3273-800x600.jpg').convert()

#Coordenadas jugadores
player1_x_coord = 50
player1_y_coord = 255
player1_y_speed = 0

player2_x_coord = 750 - player_width
player2_y_coord = 255
player2_y_speed = 0

#Coordenada de la pelota
pelota_x_coord = 400
pelota_y_coord = 300
pelota_x_speed = 3
pelota_y_speed = 3

game_over = False

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        if event.type == pygame.KEYDOWN:
            #jugador 1
            if event.key == pygame.K_w:
                player1_y_speed = -3
            if event.key == pygame.K_s:
                player1_y_speed = 3
            #jugador 2
            if event.key == pygame.K_UP:
                player2_y_speed = -3
            if event.key == pygame.K_DOWN:
                player2_y_speed = 3
        if event.type == pygame.KEYUP:
            #jugador 1
            if event.key == pygame.K_w:
                player1_y_speed = 0
            if event.key == pygame.K_s:
                player1_y_speed = 0
            #jugador 2
            if event.key == pygame.K_UP:
                player2_y_speed = 0
            if event.key == pygame.K_DOWN:
                player2_y_speed = 0 

    #Hacemos que la pelota rebote
    if pelota_y_coord < 10 or pelota_y_coord > 590:
        pelota_y_speed *= -1
    #Revisar si la pelota sale de los lados
    if pelota_x_coord < 0 or pelota_x_coord > 800:
        pelota_x_coord = 400
        pelota_y_coord = 300
        pelota_x_speed *= -1
        pelota_y_speed *= -1

    #Modificar coordenadas jugadores y pelota
    player1_y_coord += player1_y_speed
    player2_y_coord += player2_y_speed
    pelota_x_coord += pelota_x_speed
    pelota_y_coord += pelota_y_speed

    screen.blit(fondo, [0, 0]) 
    #Zona de dibujo
    player1 = pygame.draw.rect(screen, WHITE, (player1_x_coord, player1_y_coord, player_width, player_height))
    player2 = pygame.draw.rect(screen, WHITE, (player2_x_coord, player2_y_coord, player_width, player_height))
    pelota = pygame.draw.circle(screen, WHITE, (pelota_x_coord, pelota_y_coord), 10)

    #Colisiones
    if pelota.colliderect(player1) or pelota.colliderect(player2):
        pelota_x_speed *= -1


    pygame.display.flip()
    clock.tick(60) 

pygame.quit()       