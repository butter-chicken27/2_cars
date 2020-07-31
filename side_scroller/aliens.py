import pygame, random, time
from pygame.locals import *
import sys

pygame.init()

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

FPS = 55
FramesPerSec = pygame.time.Clock()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

DIS = pygame.display.set_mode((400, 600))
DIS.fill(WHITE)

pygame.display.set_caption("Game")

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.surface = pygame.Surface((50, 80))
        self.rect = self.surface.get_rect(center=(random.randint(40, SCREEN_WIDTH - 40), 0))
    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.bottom > 600:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(30, 370), 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.surface = pygame.Surface((50, 100))
        self.rect = self.surface.get_rect(center=(200, 500))
        self.rect.bottom = 600
    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_LEFT]:
            if self.rect.left > 0:
                self.rect.move_ip(-8, 0)
        if pressed_key[K_RIGHT]:
            if self.rect.right < SCREEN_WIDTH:
                self.rect.move_ip(8, 0)


E1 = Enemy()
P1 = Player()
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemies.add(E1)
all_sprites.add(P1)
all_sprites.add(E1)
bg = pygame.image.load("AnimatedStreet.png")

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == INC_SPEED:
            SPEED += 0.5
    DIS.fill(WHITE)
    DIS.blit(bg, [0, 0])
    score = font_small.render(str(SCORE), True, BLACK)
    DIS.blit(score, (10, 10))
    for entity in all_sprites:
        entity.move()
        DIS.blit(entity.image, entity.rect)
    
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound("crash.wav").play()
        time.sleep(0.5)
        DIS.fill(RED)
        DIS.blit(game_over, (40, 250))
        pygame.display.update()
        for entity in all_sprites:
            entity.kill()
            time.sleep(2)
            pygame.quit()
            sys.exit()
    pygame.display.update()
    FramesPerSec.tick(FPS)
