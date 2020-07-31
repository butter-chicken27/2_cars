import pygame, time
from pygame.locals import *
import random, math, sys

pygame.init()

WHITE = (128, 128, 128)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

FPS = 32

FramesPerSec = pygame.time.Clock()
SCREEN_WIDTH = 512
SCREEN_HEIGHT = 256

#x_speed = 5
#y_speed = 5

#font = pygame.font.SysFont("Verdana", 60)

DIS = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
DIS.fill(BLACK)
pygame.display.set_caption("PONG")

class Paddle_1(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 28))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(3, SCREEN_HEIGHT / 2))
    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_w]:
            if self.rect.top > 4:
                self.rect.move_ip(0, -4)
        if pressed_key[K_s]:
            if self.rect.bottom < SCREEN_HEIGHT - 4:
                self.rect.move_ip(0, 4)

class Paddle_2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((2, 28))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH - 3, SCREEN_HEIGHT / 2))
    def move(self):
        pressed_key = pygame.key.get_pressed()
        if pressed_key[K_UP]:
            if self.rect.top > 4:
                self.rect.move_ip(0, -4)
        if pressed_key[K_DOWN]:
            if self.rect.bottom < SCREEN_HEIGHT - 4:
                self.rect.move_ip(0, 4)

class Ball(pygame.sprite.Sprite):
    speed = 4
    x_speed = 0
    y_speed = 0
    angle = 0
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        self.angle = random.uniform(0, 2 * 3.14529)
    def set_speed(self):
        self.speed = 5
        self.x_speed = 0
        while(abs(self.x_speed) < 1.5):
            self.angle = random.uniform(0, 2 * 3.14529)
            self.x_speed = self.speed * math.cos(self.angle)
            self.y_speed = self.speed * math.sin(self.angle)
    def move(self):
        if self.y_speed > 0:
            if self.rect.bottom > SCREEN_HEIGHT:
                self.y_speed = self.y_speed * -1
        elif self.y_speed < 0:
            if self.rect.top < 0:
                self.y_speed = self.y_speed * -1
        self.rect.move_ip(self.x_speed, self.y_speed)

P1 = Paddle_1()
P2 = Paddle_2()
B1 = Ball()
B1.set_speed()
players = pygame.sprite.Group()
players.add(P1)
players.add(P2)
s_a = 0
s_b = 0
font = pygame.font.SysFont("robotoslab", 30)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 3000)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == INC_SPEED:
            B1.speed = B1.speed + 0.5
            B1.x_speed = B1.x_speed * (B1.speed) / (B1.speed - 0.5)
            B1.y_speed = B1.y_speed * (B1.speed) / (B1.speed - 0.5)
    DIS.fill(BLACK)
    for entity in players:
        entity.move()
        DIS.blit(entity.image, entity.rect)
    B1.move()
    DIS.blit(B1.image, B1.rect)
    score_a = font.render(str(s_a), True, WHITE)
    score_b = font.render(str(s_b), True, WHITE)
    DIS.blit(score_a, (0, SCREEN_HEIGHT - 40))
    DIS.blit(score_b, (SCREEN_WIDTH - 15, SCREEN_HEIGHT - 40))
    if pygame.sprite.spritecollideany(B1, players):
        B1.x_speed = B1.x_speed * -1
    if B1.rect.left < 0:
        s_b += 1
        if(s_b == 5):
            DIS.fill(RED)
            message = font.render("Player 2 wins", True, BLACK)
            DIS.blit(message, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            pygame.display.update()
            for entity in players:
                entity.kill()
                time.sleep(1)
            pygame.quit()
            sys.exit()
        else:
            P1.rect.x = 3
            P1.rect.y = SCREEN_HEIGHT / 2
            P2.rect.x = SCREEN_WIDTH - 3
            P2.rect.y = SCREEN_HEIGHT / 2
            B1.rect.x = SCREEN_WIDTH / 2
            B1.rect.y = SCREEN_HEIGHT / 2
            B1.set_speed()
            time.sleep(2)
    elif B1.rect.right > SCREEN_WIDTH:
        s_a += 1
        if(s_a == 5):
            DIS.fill(RED)
            message = font.render("Player 1 wins", True, BLACK)
            DIS.blit(message, (SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
            pygame.display.update()
            for entity in players:
                entity.kill()
                time.sleep(1)
            pygame.quit()
            sys.exit()
        else:
            P1.rect.x = 3
            P1.rect.y = SCREEN_HEIGHT / 2
            P2.rect.x = SCREEN_WIDTH - 3
            P2.rect.y = SCREEN_HEIGHT / 2
            B1.rect.x = SCREEN_WIDTH / 2
            B1.rect.y = SCREEN_HEIGHT / 2
            B1.set_speed()
            time.sleep(2)
    pygame.display.update()
    FramesPerSec.tick(FPS)
