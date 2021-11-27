import pygame, sys, random
pygame.init()

#Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

size = (800, 500)

#Crear ventana
screen = pygame.display.set_mode(size)

#Reloj
clock = pygame.time.Clock()

#Coordenadas del cuadrado
coord_x = 400
coord_y = 250

#Velocidad del cuadrado
speed_x = 3
speed_y = 3

#Lista de puntos
coord_list = []

for i in range(60):
     x = random.randint(0, 800)
     y = random.randint(0, 800)
     coord_list.append([x,y])

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
    
    if (coord_x > 750 or coord_x < 0):
        speed_x *= -1
    if (coord_y > 450 or coord_y < 0):
        speed_y *= -1

    coord_x += speed_x
    coord_y += speed_y
    
    #Color de fondo
    screen.fill(WHITE)

    for coord in coord_list:
        pygame.draw.circle(screen, BLACK, coord, 2)
        coord[1] += 1
        if coord[1] > 500:
            coord[1] = 0 
   
    pygame.draw.rect(screen, BLUE, (coord_x, coord_y, 50, 50))

    #Actualizar pantalla
    pygame.display.flip()
    clock.tick(60)