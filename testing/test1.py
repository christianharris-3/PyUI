import pygame
import src as pyui

print(pyui.ColEdit.shiftcolor((100,120,130),10))

pygame.init()
screenw = 1200
screenh = 900
screen = pygame.display.set_mode((screenw, screenh), pygame.RESIZABLE)
ui = pyui.UI()
done = False
clock = pygame.time.Clock()

ui.makebutton(10,10,'test')

while not done:
    for event in ui.loadtickdata():
        if event.type == pygame.QUIT:
            done = True
    screen.fill(pyui.Style.wallpapercol)

    ui.rendergui(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit()
