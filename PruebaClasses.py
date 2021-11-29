import pygame, random
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen_size = (900, 700)

class Moneda(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Moneda.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.y += 1

        if self.rect.y > screen_size[1]:
            self.rect.y = -10
            self.rect.x = random.randrange(screen_size[0])

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        player.rect.x = mouse_pos[0]
        player.rect.y = mouse_pos[1]

class Laser(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/laser.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
    def update(self):
        self.rect.y -= 8

screen = pygame.display.set_mode(screen_size)
clock = pygame.time.Clock()
game_over = False

score = 0

moneda_list = pygame.sprite.Group()
all_sprite_list = pygame.sprite.Group()
laser_list = pygame.sprite.Group()

#Dandole posicion a las monedas
for i in range(50):
    moneda = Moneda()
    moneda.rect.x = random.randrange(screen_size[0])
    moneda.rect.y = random.randrange(screen_size[1])

    moneda_list.add(moneda)
    all_sprite_list.add(moneda)

player = Player()
all_sprite_list.add(player)

pygame.mouse.set_visible(0)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            laser = Laser()
            laser.rect.x = player.rect.x + 70
            laser.rect.y = player.rect.y - 20

            all_sprite_list.add(laser)
            laser_list.add(laser)

    all_sprite_list.update()

    for laser in laser_list:
        moneda_hit_list = pygame.sprite.spritecollide(laser, moneda_list, True)
        for moneda in moneda_hit_list:
             all_sprite_list.remove(laser)
             laser_list.remove(laser)
             score += 1
             print(score)
        if laser.rect.y < -10:
            all_sprite_list.remove(laser)
            laser_list.remove(laser)

    screen.fill(BLACK)

    #Mostrando elementos en pantalla
    all_sprite_list.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()