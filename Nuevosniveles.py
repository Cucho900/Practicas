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

class Game():
    def __init__(self, screen, clock, score):
        self.screen = screen
        self.clock = clock
        self.score = score
        self.all_sprites = pygame.sprite.Group()
        self.pepinillo_list = pygame.sprite.Group()
        self.laser_list = pygame.sprite.Group()
        self.player = Player(self.all_sprites, self.laser_list)
        self.all_sprites.add(self.player)
        self.nivel = 0
        self.running = True
        self.game_over = True
        self.pepinillo_speedx = 7
        self.pepinillo_speedy = 7

    def init_game(self):
        self.screen.blit(fondo, [0, 0])
        self.text(self.screen, "Rick vs PickleRick", 65, size[0] // 2, size[1] // 4)
        self.text(self.screen, "Mata a todos los pickle Rick que puedas, mata a 50 y sube de nivel, si recibes 5 golpes pierdes", 18, size[0] // 2, size[1] // 2)
        self.text(self.screen, f"Preparado para el nivel {self.nivel} ?", 18, size[0] // 2, size[1] * 2//3 )
        self.text(self.screen, "Presiona r para jugar", 20, size[0] // 2, size[1] * 3//4)
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        waiting = False
        #Creamos pepinillos
        for _ in range(10):
            pepinillo = Pepinillo(self.pepinillo_speedy + self.nivel, self.pepinillo_speedx + self.nivel, self.nivel)
            self.all_sprites.add(pepinillo)
            self.pepinillo_list.add(pepinillo)
    
    def victory(self):
        self.nivel = 0
        self.score = 0
        self.screen.blit(fondo, [0, 0])
        self.text(self.screen, "Ganaste!", 65, size[0] // 2, size[1] // 4)
        self.text(self.screen, "Presiona r para jugar de nuevo", 20, size[0] // 2, size[1] * 3//4)
        pygame.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_r:
                        waiting = False

    def text(self, surface, text, size, x, y):
        font = pygame.font.SysFont("serif", size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surface.blit(text_surface, text_rect)

    def player_hp(self, surface, x, y, percentage):
        bar_lenght = 100
        bar_height = 10
        fill = (percentage/100) * bar_lenght
        border = pygame.Rect(x, y, bar_lenght, bar_height)
        fill = pygame.Rect(x, y, fill, bar_height)
        pygame.draw.rect(surface, GREEN, fill)
        pygame.draw.rect(surface, WHITE, border, 2)

    def controlador_nivel(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()

        self.all_sprites.update()

        #Colisiones del laser contra los pepinillos y cuando chocan creamos uno nuevo
        collide_list = pygame.sprite.groupcollide(self.laser_list, self.pepinillo_list, True, True)
        for _ in collide_list:
            self.score += 1
            if self.score % 10 == 0:
                self.nivel += 1
                self.player.shield = 100
                if self.nivel == len(enemy_pictures):
                    self.victory()                    

                self.pepinillo_list.remove()
                self.all_sprites.remove(self.pepinillo_list)
                self.init_game()

            explosion_sound.play()
            pepinillo = Pepinillo(self.pepinillo_speedy + self.nivel, self.pepinillo_speedx + self.nivel, self.nivel)
            self.all_sprites.add(pepinillo)
            self.pepinillo_list.add(pepinillo)

        #Colisiones contra Rick
        collide_list = pygame.sprite.spritecollide(self.player, self.pepinillo_list, True)
        for _ in collide_list:
            self.player.shield -= 20
            choque_sound.play()
            pepinillo = Pepinillo(self.pepinillo_speedy + self.nivel, self.pepinillo_speedx + self.nivel, self.nivel)
            self.all_sprites.add(pepinillo)
            self.pepinillo_list.add(pepinillo)
            if self.player.shield <= 0:
                self.defeat()

        screen.blit(fondo, [0, 0])

        game.text(screen, str(self.score), 25, size[0] - 20, 10)

        game.player_hp(screen, 5, 5, self.player.shield)

        self.all_sprites.draw(screen)
        pygame.display.flip()

    def defeat(self):        
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.pepinillo_list = pygame.sprite.Group()
        self.laser_list = pygame.sprite.Group()
        self.player = Player(self.all_sprites, self.laser_list)
        self.all_sprites.add(self.player)
        self.nivel = 0
        self.running = True
        self.game_over = True
        self.pepinillo_speedx = 7
        self.pepinillo_speedy = 7

class Player(pygame.sprite.Sprite):
    def __init__(self, all_sprites, laser_list):
        super().__init__()
        self.image = pygame.image.load("assets/Rick_frontal.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = size[0] // 2
        self.rect.bottom = size[1] - 10
        self.speed_x = 0
        self.shield = 100
        self.all_sprites = all_sprites
        self.laser_list = laser_list

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
        self.all_sprites.add(laser)
        self.laser_list.add(laser)
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
    def __init__(self, speedy, speedx, nivel):
        super().__init__()
        self.imagen_de_nivel = nivel
        self.image = enemy_pictures[self.imagen_de_nivel]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(size[0] - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.new_speedy = speedy
        self.new_speedx = speedx
        self.speedy = random.randrange(self.new_speedy - 6, self.new_speedy)
        self.speedx = random.randrange(self.new_speedx - 12, self.new_speedx)
    
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        #Vemos si los pepinillos salen de la pantalla y los devolvemos hacia arriba
        if self.rect.top > size[1] or self.rect.left > size[0] or self.rect.right < 0:
            self.rect.x = random.randrange(size[0] - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(self.new_speedy -6, self.new_speedy)
            self.speedx = random.randrange(self.new_speedx -12, self.new_speedx)

#Sonidos
laser_sound = pygame.mixer.Sound("assets/Sonido_Laser.mp3")
pygame.mixer.Sound.set_volume(laser_sound, 0.1)
explosion_sound = pygame.mixer.Sound("assets/Explosion.mp3")
choque_sound = pygame.mixer.Sound("assets/Choque.mp3")
# pygame.mixer.music.load("assets/Music.mp3")
# pygame.mixer.music.set_volume(0.05)

#Imagenes Rick
right_pictures = []
right = ["assets/Rick_derecha1.png", "assets/Rick_derecha2.png", "assets/Rick_derecha3.png", "assets/Rick_derecha4.png"]
for image in right:
    right_pictures.append(pygame.image.load(image).convert())

left_pictures = []
left = ["assets/Rick_izquierda1.png", "assets/Rick_izquierda2.png", "assets/Rick_izquierda3.png", "assets/Rick_izquierda4.png"]
for rick in left:
    left_pictures.append(pygame.image.load(rick).convert())

#Imagenes de enemigos
enemy_pictures = []
pictures = ["assets/Pepinillo.png", "assets/Limon.png", "assets/Bola_de_nieve.png", "assets/Popo.png", "assets/Meeseeks.png", "assets/Frijol.png"]
for picture in pictures:
    enemy_pictures.append(pygame.image.load(picture).convert())

game = Game(screen, clock, 0)

# pygame.mixer.music.play(loops=-1)

while game.running:
    if game.game_over:

        game.init_game()

        game.game_over = False

    clock.tick(60)

    game.controlador_nivel()

pygame.quit()