import pygame,math,random,sys,os
import PyUI
pygame.init()
screenw = 1200
screenh = 900
screen = pygame.display.set_mode((screenw, screenh),pygame.RESIZABLE)
pygame.scrap.init()
ui = PyUI.UI()
done = False
clock = pygame.time.Clock()
ui.defaultcol = (50,150,200)

def test():
    ui.maketext(20,-20,'Please do not press this button again',100,maxwidth=600,anchor=('w/2','h/2'),
                dragable=True,borderdraw=True,roundedcorners=10,spacing=15,center=True,
                col=(0,255,255),bordercol=(50,150,150),scalesize=True)
    
ui.makebutton(0,0,'{cross}',command=test,anchor=('w/2','h'),objanchor=('w/2','h+20'),scalesize=True,toggleable=True,toggletext='',togglecol=ui.defaultcol,clickdownsize=1,spacing=-10,border=3,roundedcorners=10,leftborder=100)
ui.maketextbox(300,100,'no',200,lines=2,linelimit=3,roundedcorners=10,scalesize=True,textcenter=True)
##ui.maketable(100,200,[['{heart}',2],[ui.makebutton(0,0,'hello',command=test,roundedcorners=5),ui.maketext(0,0,'',50,img=pygame.image.load('helm.png'),textcenter=True)],[ui.maketextbox(0,0,'yes',200,height=100),'1']],scalesize=True,boxwidth=-1,textcenter=True,spacing=5,roundedcorners=5,textcol=(255,0,0))

ui.makeslider(100,400,15,200,button=ui.makebutton(0,0,'{heart}',30,clickdownsize=1,spacing=3,roundedcorners=5,col=PyUI.shiftcolor(ui.defaultcol,10),textcol=(255,0,0)),roundedcorners=10,direction='vertical')
ui.makebutton(100,100,'{face2}',command=lambda: ui.movemenu('menu2','left'))
ui.makebutton(10,10,'{face}',command=ui.menuback,menu='menu2')
ui.makewindowedmenu(200,100,300,300,'menu2',roundedcorners=10,isolated=True)
ui.makescroller(20,20,200,roundedcorners=3)
ui.makecheckbox(300,300)

while not done:
    pygameeventget = ui.loadtickdata()
    for event in pygameeventget:
        if event.type == pygame.QUIT:
            done = True
    screen.fill((0,255,255))
    
    ui.rendergui(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit() 
