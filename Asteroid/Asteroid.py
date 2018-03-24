# Pygame Asteroid
import pygame
import random
import math
from os import path

img_dir = path.join(path.dirname(__file__), 'images')
snd_dir = path.join(path.dirname(__file__), 'sounds')

WIDTH = 1200
HEIGHT = 800
FPS = 60

# define colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)

# Initialize pygame and Create our Window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asteroid")
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)

def newenemy():
    em = Enemy()
    all_sprites.add(em)
    enemies.add(em)

def draw_lives(surf, x, y, lives, img):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 60 - 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)
        
def show_go_screen():
    screen.blit(background, background_rect)
    draw_text(screen, "ASTEROID BLASTER", 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, "Arrow keys move, Space to fire", 22,WIDTH / 2, HEIGHT / 2)
    draw_text(screen, "M and N keys are for volume", 22, WIDTH / 2, HEIGHT * 53/100)
    draw_text(screen, "Press a key to begin", 18, WIDTH / 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

    
# Defining all the sprites
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 22
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT / 2
        self.speedx = 0
        self.speedy = 0
        angle = 0
        self.angle = angle
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()

    def update(self):
        self.speedx = 0
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_UP]:
            self.speedy = -8
            self.angle -= 2
            self.rotate_image()
        if keystate[pygame.K_DOWN]:
            self.speedy = 8
            self.angle += 2
            self.rotate_image()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.left = 0
        if self.rect.left < 0:
            self.rect.right = WIDTH
        if self.rect.top > HEIGHT:
            self.rect.top = 0
        if self.rect.bottom < 0 :
            self.rect.bottom = HEIGHT

    def rotate_image(self):#rotating player image
        self.image = pygame.transform.rotozoom(player_img, self.angle , 0.29 )
        self.rect = self.image.get_rect(center=self.rect.center)
        self.image.set_colorkey(BLACK)
        
    def shoot(self):
        missile = Missile(self.rect.center, self.angle)
        all_sprites.add(missile)
        missiles.add(missile)
        shoot_sound.play()

class Missile(pygame.sprite.Sprite):
    def __init__(self, pos, angle):
        super().__init__()
        # Rotate the image.
        self.image = pygame.transform.rotozoom(missile_img, angle , 0.3)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        speed = 5  
        self.velocity_x = math.cos(math.radians(-angle)+30) * speed
        self.velocity_y = math.sin(math.radians(-angle)+30) * speed
        self.pos = list(pos)
        
    def update(self):
        self.pos[0] = self.velocity_x + self.pos[0] 
        self.pos[1] = self.velocity_y + self.pos[1] 
        self.rect.center = self.pos
        # transport to other location
        if self.rect.bottom < 0 or self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH :
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        tx = random.randint(0,1)
        ty = random.randint(0,1)
        if tx == 0:
           self.rect.x = random.randrange(600,800)
           self.speedx = random.randrange(-5, -1)
        elif tx == 1:
           self.rect.x = random.randrange(0,200)
           self.speedx = random.randrange(1, 5)
        if ty == 0:
           self.rect.y = random.randrange(1000,1200)
           self.speedy = random.randrange(-5, -1)
        elif ty == 1:
           self.rect.y = random.randrange(0,200)
           self.speedy = random.randrange(1, 5)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        if self.rect.top > HEIGHT + 10  or self.rect.left < -100 or self.rect.right > WIDTH + 100 :
           tx = random.randint(0,1)
           ty = random.randint(0,1)
           if tx == 0:
               self.rect.x = random.randrange(600,800)
               self.speedx = random.randrange(-5, -1)
           elif tx == 1:
               self.rect.x = random.randrange(0,200)
               self.speedx = random.randrange(1, 5)
           if ty == 0:
               self.rect.y = random.randrange(1000,1200)
               self.speedy = random.randrange(-5, -1)
           elif ty == 1:
               self.rect.y = random.randrange(0,200)
               self.speedy = random.randrange(1, 5)
        self.rect.x += self.speedx
        self.rect.y += self.speedx
                            
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 75

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Load all game graphics
background = pygame.image.load(path.join(img_dir, "preview-1.jpg")).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "spaceShips_007.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
missile_img = pygame.image.load(path.join(img_dir, "laserRed12.png")).convert()
meteor_images = []
meteor_list = ['meteorBrown_big1.png', 'meteorBrown_med1.png','meteorBrown_med3.png',
               'meteorBrown_small1.png', 'meteorBrown_small2.png','meteorBrown_tiny1.png']
for img in meteor_list:
    meteor_images.append(pygame.image.load(path.join(img_dir, img)).convert())
explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []

for i in range(8):
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)

# Load all game sounds
vol=0.3
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, 'pew.wav'))
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
pygame.mixer.music.load(path.join(snd_dir, 'through space.ogg'))
pygame.mixer.music.set_volume(vol)
expl_sounds = []
for snd in ['expl3.wav', 'expl6.wav']:
    expl_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))
player_die_sound = pygame.mixer.Sound(path.join(snd_dir, 'rumble1.ogg'))
pygame.mixer.music.play(loops=-1)

#All the sprites used
all_sprites = pygame.sprite.Group()
player = Player()
enemies = pygame.sprite.Group()
missiles = pygame.sprite.Group()
all_sprites.add(player)

#Game Loop
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        enemies = pygame.sprite.Group()
        missiles = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newenemy()
        score = 0
        
    # keep loop running at the right speed
    clock.tick(FPS)
    # process input(events)
    for event in pygame.event.get():
        #check for closing window
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                missile = Missile(player.rect.center, player.angle)
                player.shoot()
            if event.key == pygame.K_n:
                vol+=0.1
                pygame.mixer.music.set_volume(vol)
            elif event.key == pygame.K_b:
                vol-=0.1
                if vol <=0:
                    vol = 0
                    pygame.mixer.music.set_volume(vol)
            elif event.key == pygame.K_m:
                vol=0
                pygame.mixer.music.set_volume(vol)
                
    # Update
    all_sprites.update()

    # check to see if a bullet hit a enemy
    hits = pygame.sprite.groupcollide(enemies, missiles, True, True)
    for hit in hits:
        score += (hit.radius * 2) 
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        newenemy()

    # check to see if a enemy hit the player
    hits = pygame.sprite.spritecollide(player, enemies, True, pygame.sprite.collide_circle)
    for hit in hits:
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newenemy()
        player_die_sound.play()
        death_explosion = Explosion(player.rect.center, 'player')
        player.rect.centerx = WIDTH / 2
        player.rect.bottom = HEIGHT / 2
        all_sprites.add(death_explosion)
        player.lives -= 1
        
    # if the player died and the explosion has finished playing
    if player.lives <= 0 and not death_explosion.alive():
        game_over = True

    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    draw_text(screen, str(score), 18, WIDTH / 2, 10)
    draw_lives(screen, 0 , 5, player.lives, player_mini_img)
    # *after* drawing everything, flip the display
    pygame.display.flip()
    
pygame.quit()
