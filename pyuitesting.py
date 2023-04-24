import pygame,math,random
import PyUI
pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.scrap.init()
ui = PyUI.UI(1)
done = False
clock = pygame.time.Clock()


def stop():
    print('goodbye')
    pygame.quit()

def cheese():
    print('cheese')

def randomizescreenscale():
    ui.scaleset(0.5)

def increase(row):
    if ui.tables[0].data[row][1] == 'U':
            ui.tables[0].data[row][1] = 1
    elif ui.tables[0].data[row][1]<9:
        ui.tables[0].data[row][1]+=1
    ui.tables[0].refresh(ui)

def decrease(row):
    if ui.tables[0].data[row][1]!='U':
        ui.tables[0].data[row][1]-=1
        if ui.tables[0].data[row][1] == 0:
            ui.tables[0].data[row][1] = 'U'
        ui.tables[0].refresh(ui)


ui.makebutton(400,200,'Crash',100,stop,roundedcorners=10)
ui.makebutton(400,350,'Settings',50,lambda: ui.movemenu('settings'))
ui.makebutton(100,400,'back',50,ui.menuback,'settings')
ui.makebutton(800,700,'cheese',100,cheese,'settings',roundedcorners=200)
ui.makebutton(600,400,'randomize screen scale',50,randomizescreenscale,'settings',font='helvetica',bold=True)
ui.makebutton(600,500,'reset screen scale',50,lambda: ui.scaleset(1),'settings',font='helvetica',bold=True)

ui.maketextbox(700,150,'textbox',350,300,font='calibre',titlefont='impact',textcenter=False,roundedcorners=5)

titles = ['Name','Grade','Grade Up','Grade Down']
data = [['James',7,ui.makebutton(0,0,'+1',35,lambda: increase(0),returnobj=True),ui.makebutton(0,0,'-1',35,lambda: decrease(0),returnobj=True)],
        ['John',6,ui.makebutton(0,0,'+1',35,lambda: increase(1),returnobj=True),ui.makebutton(0,0,'-1',35,lambda: decrease(1),returnobj=True)],
        ['Jim',9,ui.makebutton(0,0,'+1',35,lambda: increase(2),returnobj=True),ui.makebutton(0,0,'-1',35,lambda: decrease(2),returnobj=True)],
        ['Jack',5,ui.makebutton(0,0,'+1',35,lambda: increase(3),returnobj=True),ui.makebutton(0,0,'-1',35,lambda: decrease(3),returnobj=True)]]

ui.maketable(20,440,data,titles,roundedcorners=5)
ui.maketext(500,40,'this is a long sentance designed to show how the thing can be on multiple lines',50,'settings',maxwidth=400,backingcol=(150,100,50),font='calibre',roundedcorners=10,backingborder=20)

while not done:
    ui.loadtickdata()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
    screen.fill((255,255,255))
    ui.rendergui(screen)
    ui.write(screen,20,780,str(int(clock.get_fps())),20)
    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit()                                         
