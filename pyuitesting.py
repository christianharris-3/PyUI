import pygame,math,random
import PyUI
pygame.init()
screen = pygame.display.set_mode((1400, 1200),pygame.RESIZABLE)
pygame.scrap.init()
ui = PyUI.UI()
done = False
clock = pygame.time.Clock()
ui.defaultcol = (150,100,0)
ui.defaultbackingcol = (100,100,100)

ui.images = ['test thing', [[[(200, 100), (490, 220), (300, 40), (850, 340)], [(850, 340), (300, 200), (450, 350), (340, 430)], [(340, 430), (310, 250), (200, 310), (200, 100)]], [[(380, 440), (540, 360), (330, 240), (850, 370)], [(850, 370), (380, 440)]]]],


def stop():
    print('goodbye')
    ui.menuback()

def cheese():
    print('cheese')
    if ui.queuedmenumove[0]<0:
        for a in ui.onmenu('main'):
            cords = (random.randint(100,1300),random.randint(100,1000))
            returnto = (a.x,a.y)
            ui.makeanimation(a.ID,'current',cords,'sin',length=30,queued=False)#,command=lambda: ui.movemenu('tickmenu'),runcommandat=30)
            ui.makeanimation(a.ID,'current',returnto,'sin',length=30,queued=True)

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

ui.makebutton(600,600,'',800,ui.menuback,img='settings',layer=2,menu='tickmenu',runcommandat=2)
##ui.makebutton(700,600,'',100,ui.menuback,img=pygame.image.load('helm.png'),layer=2)
ui.makebutton(1050,600,'',100,cheese,img='arrow up stick=0.3 point=0.3',horizontalspacing=10,verticalspacing=10,clickdownsize=3,toggleable=True)
ui.makebutton(880,560,'',72,cheese,img='skip rounded=0.05 offset=-0.2 left',textcol=(173,216,230),col=(41,41,41),width=160,height=160,roundedcorners=80,horizontalspacing=10,verticalspacing=10,clickdownsize=3,border=6,bordercol=(173,216,230),ID='move menu around lol')
#ui.makebutton(

ui.makebutton(150,70,'go to a big tick',50,lambda: ui.movemenu('tickmenu'),width=150)
ui.makebutton(400,200,'Crash',100,stop,roundedcorners=10)
ui.makebutton(400,350,'Settings',50,lambda: ui.movemenu('settings','left'),ID='settingsbutton')
ui.makebutton(100,400,'back',50,ui.menuback,'settings')
ui.makebutton(600,400,'randomize screen scale',50,randomizescreenscale,'settings',font='helvetica',bold=True)
ui.makebutton(600,500,'reset screen scale',50,lambda: ui.scaleset(1),'settings',font='helvetica',bold=True)

##ui.maketextbox(700,150,'textbox',350,8,font='calibre',textcenter=False,roundedcorners=5,ID='textbox')
ui.maketextbox(80,150,'another textbox',250,3,font='calibre',textcenter=False,roundedcorners=5)

titles = ['Name','Grade','Grade Up','Grade Down']
data = [['James',7,ui.makebutton(0,0,'+1',35,lambda: increase(0)),ui.makebutton(0,0,'-1',35,lambda: decrease(0))],
        ['John',6,ui.makebutton(0,0,'+1',35,lambda: increase(1)),ui.makebutton(0,0,'-1',35,lambda: decrease(1))],
        ['Jim',9,ui.makebutton(0,0,'+1',35,lambda: increase(2)),ui.makebutton(0,0,'-1',35,lambda: decrease(2))],
        ['Jack',5,ui.makebutton(0,0,'+1',35,lambda: increase(3)),ui.makebutton(0,0,'-1',35,lambda: decrease(3))]]

ui.maketable(20,420,data,titles,roundedcorners=5,boxwidth=150,ID='editable table',textcenter=True,verticalspacing=4)
ui.maketext(500,40,'this is a long sentance designed to show how the thing can be on multiple lines',50,'settings',maxwidth=400,backingcol=(150,100,50),font='calibre',roundedcorners=10,border=20)

ui.maketable(20,740,[['{shuffle}',ui.maketextbox(0,0,'',100,1,textsize=40)],['{skip}',ui.makebutton(0,0,'button lol',30)]],[ui.maketext(0,0,'',200,img='settings'),'stuffs'],textsize=30)

ui.makeslider(700,700,200,20,maxp=1000,ID='testslider',command=cheese,runcommandat=2,increment=50)

ui.makewindowedmenu(400,100,500,500,'windowed','main',(150,150,150),False,10,0)
ui.makebutton(600,1000,'mini menu',100,lambda: ui.movemenu('windowed','down'))
ui.maketextbox(160,40,'hi',300,5,'windowed')
ui.makebutton(160,280,'buttony button',50,menu='windowed',dragable=True)

for a in range(5):
    ui.makecheckbox(930,40+a*80,ID='binded'+str(a),bindtoggle=['binded'+str(b) for b in range(5)],col=(100,100,100),center=True)
    ui.maketext(980,20+a*80,'Checkbox '+str(a),60,center=False,border=10,roundedcorners=5)
while not done:
    pygameeventget = ui.loadtickdata()
    for event in pygameeventget:
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pass
    screen.fill((100,100,100))
    ui.rendergui(screen)
    if not ui.IDs['testslider'].holding:
        ui.IDs['testslider'].slider+=1
        ui.IDs['testslider'].limitpos(ui)
    ui.write(screen,20,1180,str(int(clock.get_fps())),20)
    pygame.display.flip()
    clock.tick(60)                                               
pygame.quit()                                         
