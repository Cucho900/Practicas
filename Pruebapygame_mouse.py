import pygame, sys
pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

size = (800, 500)

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

pygame.mouse.set_visible(0)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    mouse_pos = pygame.mouse.get_pos()
    x = mouse_pos[0]
    y = mouse_pos[1]

    screen.fill(WHITE)

    pygame.draw.rect(screen, RED, (x, y, 100, 100))

    pygame.display.flip()
    clock.tick(60)