import pygame, random, sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
size = (1209, 680)


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Rick vs PepinilloRick")
clock = pygame.time.Clock()
fondo = pygame.image.load("assets/Fondo.jpg").convert()


def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_hp(surface, x, y, percentage):
    bar_lenght = 100
    bar_height = 10
    fill = (percentage/100) * bar_lenght
    border = pygame.Rect(x, y, bar_lenght, bar_height)
    fill = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = size[0] // 2
        self.rect.bottom = size[1] - 10
        self.speed_x = 0
        self.shield = 100

    def update(self):
        self.speed_x = 0
        #Leemos si se presiona una tecla en el teclado para mover a rick
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        #No permitimos que rick salga de la pantalla
        if self.rect.right > size[0]:
            self.rect.right = size[0]
        if self.rect.left < 0:
            self.rect.left = 0
    
    def shoot(self):
        laser = Laser(self.rect.right, self.rect.top)
        all_sprites.add(laser)
        laser_list.add(laser)
        laser_sound.play()

class Laser(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x - self.rect.width
        self.speedy = -8
    
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Pepinillo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/Pepinillo.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(size[0] - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 6)
        self.speedx = random.randrange(-6, 6)
    
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #Vemos si los pepinillos salen de la pantalla y los devolvemos hacia arriba
        if self.rect.top > size[1] or self.rect.left > size[0] or self.rect.right < 0:
            self.rect.x = random.randrange(size[0] - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 6)
            self.speedx = random.randrange(-6, 6)

def game_over_screen():
    screen.blit(fondo, [0, 0])
    draw_text(screen, "Rick vs PickleRick", 65, size[0] // 2, size[1] // 4)
    draw_text(screen, "Mata a todos los pickle Rick que puedas, si recibes 5 golpes pierdes", 18, size[0] // 2, size[1] // 2)
    draw_text(screen, "Presiona una tecla para jugar", 20, size[0] // 2, size[1] * 3//4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                waiting = False

#Sonidos
laser_sound = pygame.mixer.Sound("assets/Sonido_Laser.mp3")
pygame.mixer.Sound.set_volume(laser_sound, 0.1)
explosion_sound = pygame.mixer.Sound("assets/Explosion.mp3")
choque_sound = pygame.mixer.Sound("assets/Choque.mp3")

game_over = True
running = True

while running:
    if game_over:

        game_over_screen()

        game_over = False
        all_sprites = pygame.sprite.Group()
        pepinillo_list = pygame.sprite.Group()
        laser_list = pygame.sprite.Group()

        player = Player()
        all_sprites.add(player)

        #Creamos pepinillos
        for i in range(30):
            pepinillo = Pepinillo()
            all_sprites.add(pepinillo)
            pepinillo_list.add(pepinillo)
        score = 0

    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    #Colisiones del laser contra los pepinillos y cuando chocan creamos uno nuevo
    collide_list = pygame.sprite.groupcollide(laser_list, pepinillo_list, True, True)
    for collide in collide_list:
        score += 1
        explosion_sound.play()
        pepinillo = Pepinillo()
        all_sprites.add(pepinillo)
        pepinillo_list.add(pepinillo)

    #Colisiones contra Rick
    collide_list = pygame.sprite.spritecollide(player, pepinillo_list, True)
    for collide in collide_list:
        player.shield -= 20
        choque_sound.play()
        pepinillo = Pepinillo()
        all_sprites.add(pepinillo)
        pepinillo_list.add(pepinillo)
        if player.shield <= 0:
            game_over = True

    screen.blit(fondo, [0, 0])

    draw_text(screen, str(score), 25, size[0] - 20, 10)

    draw_hp(screen, 5, 5, player.shield)

    all_sprites.draw(screen)
    pygame.display.flip()

pygame.quit()
