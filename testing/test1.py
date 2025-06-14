import numpy as np
import pygame
# import UIpygame as pyui

pygame.init()
screenw = 1200
screenh = 900
screen = pygame.display.set_mode((screenw, screenh), pygame.RESIZABLE)

done = False
clock = pygame.time.Clock()

# ui.makeButton(10, 10, 'test', clicktype=pyui.ClickType.LEFT_CLICK)

while not done:
    for event in []:
        if event.type == pygame.QUIT:
            done = True
    screen.fill((255,255,255))

    pygame.draw.circle(screen, (255,0,0), np.array([100.54,25.6]),30)

    pygame.display.flip()
    clock.tick(60)
pygame.quit()
