import GameObject
from GameObject import *
import pygame
import sys
from pygame.locals import *

pygame.init()
s = pygame.display.set_mode([800,600])

Clock = pygame.time.Clock()
man = pygame.image.load('miaomiao.png').convert_alpha()
back = pygame.image.load('sixing.jpg').convert()
right_mouse = pygame.image.load('right_mouse.png').convert_alpha()
occupied = pygame.image.load('occupied.png').convert()
W = World(s,back)
A = Gameobj(W,'steve',man,2,4,3,2,1.2);
A.location = Vector(100,50)
A.destination = Vector(800,200)
A.speed = 10
W.object.append(A)
location = Vector(200,50)
mouse_count = [0,0,0]
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        pygame.quit()
        break

    W.update(right_mouse,occupied)
    

    Clock.tick(30);
    pygame.display.update()
    
    
