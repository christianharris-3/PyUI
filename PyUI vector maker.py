import pygame,math,random,json
import pygame.gfxdraw
import PyUI
pygame.init()
screenw = 1000
screenh = 600
screen = pygame.display.set_mode((screenw, screenh))
pygame.scrap.init()
ui = PyUI.UI()
done = False
clock = pygame.time.Clock()

ui.styleset(col=(220,220,220))

splines = []
global nodecount
nodecount = 4
global gridsize
gridsize = 10

class lambdafuncmaker:
    def __init__(self,inpu):
        self.inpu = inpu
    def realignfunc(self):
        self.func = lambda: realign(self.inpu)
def bezierpoints(roots,progress,detail):
    #print(roots)
    npoints = []
    for a in range(len(roots)-1):
        npoints.append((roots[a][0]+(roots[a+1][0]-roots[a][0])*(progress/detail),roots[a][1]+(roots[a+1][1]-roots[a][1])*(progress/detail)))
    if len(npoints)>0:
        point = bezierpoints(npoints,progress,detail)
    else:
        point = roots[0]
    return point
def bezierdrawer(points,width,commandpoints=True,detail=200):
    curvepoints = []
    for a in range(detail):
        #print(a)
        curvepoints.append(bezierpoints(points,a,detail))
    curvepoints.append(points[-1])
    if commandpoints:
        pygame.draw.aalines(screen,(0,0,0),False,curvepoints)
        if len(points) == 4:
            pygame.draw.line(screen,(100,100,100),points[0],points[1])
            pygame.draw.line(screen,(100,100,100),points[2],points[3])
        else:
            pygame.draw.lines(screen,(100,100,100),False,points)
    return curvepoints

def makespline(splines):
    splines.append([[]])
    for a in range(nodecount):
        ID = 'spline '+str(len(splines))+' segment '+str(len(splines[-1]))+' point '+str(a)
        funcer = lambdafuncmaker(ID)
        funcer.realignfunc()
        ui.makebutton(200+a*100,15*len(splines[-1])+40*(len(splines)-1),'',10,funcer.func,runcommandat=1,width=10,height=10,roundedcorners=5,border=1,clickdownsize=2,dragable=True,objanchor=('w','h'),ID=ID)
        splines[-1][-1].append(ID)
def extendspline(splines):
    if len(splines)>0 and splines[-1][-1][-1]!=splines[-1][0][0]:
        splines[-1].append([])
        for a in range(nodecount):
            ID = 'spline '+str(len(splines))+' segment '+str(len(splines[-1]))+' point '+str(a)
            funcer = lambdafuncmaker(ID)
            funcer.realignfunc()
            ui.makebutton(200+a*100,15*len(splines[-1])+40*(len(splines)-1),'',10,funcer.func,runcommandat=1,width=10,height=10,roundedcorners=5,border=1,clickdownsize=2,dragable=True,objanchor=('w','h'),ID=ID)
            splines[-1][-1].append(ID)
        ui.delete(splines[-1][-1][0])
        splines[-1][-1][0] = 'spline '+str(len(splines))+' segment '+str(len(splines[-1])-1)+' point '+str(len(splines[-1][-2])-1)
    else:
        makespline(splines)
def completespline(splines):
    if len(splines)>0 and splines[-1][-1][-1]!=splines[-1][0][0]:
        ui.delete(splines[-1][-1][-1])
        splines[-1][-1][-1] = splines[-1][0][0]
def delspline(splines):
    if len(splines)>0:
        for a in splines[-1]:
            for b in a:
                ui.delete(b)
        del splines[-1]
def delsplinesegment(splines):
    if len(splines)>0:
        if len(splines[-1])>1:
            for a in splines[-1][-1][1:]:
                ui.delete(a)
            del splines[-1][-1]
        else:
            delspline(splines)

def saveas(splines):
    ui.movemenu('main')
    save(splines,ui.IDs['saveas textbox'].text)
    
def save(splines,name):
    data = []
    for a in splines:
        data.append([])
        for b in a:
            data[-1].append([])
            for c in b:
                data[-1][-1].append((ui.IDs[c].x,ui.IDs[c].y))
    with open(name+'.json','w') as fl:
        json.dump(data,fl)
        
def load(splines):
    ui.movemenu('main')
    try:
        with open(ui.IDs['load textbox'].text+'.json','r') as fl:
            data = json.load(fl)
        data = [[[(275, 200), (450, 200), (450, 400), (600, 400)], [(600, 400), (600, 350)], [(600, 350), (675, 425)], [(675, 425), (600, 500)], [(600, 500), (600, 450)], [(600, 450), (425, 450), (425, 250), (275, 250)], [(275, 250), (275, 200)]], [[(275, 400), (275, 450)], [(275, 450), (360, 450), (420, 390)], [(420, 390), (385, 345)], [(385, 345), (350, 390), (275, 400)]], [[(600, 250), (600, 300)], [(600, 300), (675, 225)], [(675, 225), (600, 150)], [(600, 150), (600, 200)], [(600, 200), (500, 200), (455, 260)], [(455, 260), (490, 300)], [(490, 300), (530, 255), (600, 250)]]]
        global nodecount
        for a in data:
            for b in a:
                nodecount = len(b)
                extendspline(splines)
                for i,c in enumerate(splines[-1][-1]):
                    ui.IDs[c].x = float(b[i][0])
                    ui.IDs[c].y = float(b[i][1])
            if a[0][0] == a[-1][-1]:
                completespline(splines)
    except Exception as ex:
        print(ex)
        print('failed to load file: '+ui.IDs['load textbox'].text+'.txt')

def PyUIify(splines):
    data = []
    for a in splines:
        data.append([])
        for b in a:
            data[-1].append([])
            for c in b:
                data[-1][-1].append((ui.IDs[c].x,ui.IDs[c].y))
    print(['name here',data])
def realign(ID):
    global gridsize
    if ui.IDs[ID].x<150:
        ui.IDs[ID].x=150
    else:
        ui.IDs[ID].x = round((ui.IDs[ID].x-150)/gridsize)*gridsize+150-ui.IDs[ID].width/2
    ui.IDs[ID].y = round(ui.IDs[ID].y/gridsize)*gridsize-ui.IDs[ID].height/2
    
        
def updatenodecount():
    global nodecount
    nodecount = ui.IDs['nodecount'].slider
    ui.IDs['node count display'].settext(str(nodecount))

def updategridsize():
    global gridsize
    gridsize = ui.IDs['gridsize'].slider
    ui.IDs['grid size display'].settext(str(gridsize))

ui.maketext(0,0,'',screenh,img='rect width=150',textcol=(235,235,235),layer=-1,spacing=0)

######
splinesy = 0
ui.maketext(75,splinesy,'-Splines-',25,center=True,centery=False)

ui.makebutton(0,splinesy+20,'Make Spline',25,lambda: makespline(splines),width=150,center=False,clickdownsize=1,border=1)
ui.makebutton(0,splinesy+40,'Extend Spline',25,lambda: extendspline(splines),width=150,center=False,clickdownsize=1,border=1)
ui.makebutton(0,splinesy+60,'Complete Spline',25,lambda: completespline(splines),width=150,center=False,clickdownsize=1,border=1)
ui.makebutton(0,splinesy+80,'Delete Spline',25,lambda: delspline(splines),width=150,center=False,clickdownsize=1,border=1)
ui.makebutton(0,splinesy+100,'Delete Segment',25,lambda: delsplinesegment(splines),width=150,center=False,clickdownsize=1,border=1)

ui.makeslider(28,splinesy+130,116,10,6,increment=1,minp=2,startp=4,command=updatenodecount,ID='nodecount')
ui.maketext(4,splinesy+124,'4',25,center=False,ID='node count display')

######
gridy = 146
ui.maketext(75,gridy,'-Grid-',25,center=True,centery=False)

ui.makebutton(0,gridy+20,'Toggle Lines',25,width=150,center=False,clickdownsize=1,border=1,toggle=True,toggleable=True,ID='gridline toggle')

ui.makeslider(28,gridy+50,116,10,50,increment=1,minp=1,startp=10,command=updategridsize,runcommandat=1,ID='gridsize')
ui.maketext(4,gridy+44,'10',25,center=False,ID='grid size display')

######
savey = 210
ui.maketext(75,savey-1,'-Saving-',25,center=True,centery=False)
ui.makebutton(0,savey+20,'Save',25,lambda: save(splines,'image'),width=150,center=False,clickdownsize=1,border=1)
ui.makebutton(0,savey+40,'Save As',25,lambda: ui.movemenu('savescreen','right'),width=150,center=False,clickdownsize=1,border=1)
ui.makebutton(0,savey+60,'Load',25,lambda: ui.movemenu('loadscreen','right'),width=150,center=False,clickdownsize=1,border=1)
ui.makebutton(0,savey+80,'PyUI',25,lambda: PyUIify(splines),width=150,center=False,clickdownsize=1,border=1)

######
ui.makebutton(0,screenh-20,'Hide points',25,lambda: ui.movemenu('show points'),width=150,center=False,clickdownsize=1,border=1)
ui.makebutton(0,screenh-20,'Show points',25,ui.menuback,'show points',width=150,center=False,clickdownsize=1,border=1)

######
ui.makewindowedmenu(200,200,400,300,'savescreen','main',col=(240,240,240),roundedcorners=5)
ui.makewindowedmenu(200,200,400,300,'loadscreen','main',col=(240,240,240),roundedcorners=5)
ui.maketext(10,10,'Save As',50,'savescreen',center=False)
ui.maketext(10,10,'Load',50,'loadscreen',center=False)
ui.maketextbox(200,50,'',380,5,'savescreen',command=lambda: saveas(splines),center=True,centery=False,ID='saveas textbox')
ui.maketextbox(200,50,'',380,5,'loadscreen',command=lambda: load(splines),center=True,centery=False,ID='load textbox')
ui.makebutton(10,260,'Enter',40,lambda: saveas(splines),'savescreen',center=False)
ui.makebutton(10,260,'Enter',40,lambda: load(splines),'loadscreen',center=False)

##
##ui.maketext(200,200,'',400,dragable=True,img=pygame.image.load('backingimage2.png'),colorkey=(226,227,232))


while not done:
    pygameeventget = ui.loadtickdata()
    for event in pygameeventget:
        if event.type == pygame.QUIT:
            done = True
##        if event.type == pygame.KEYDOWN:
##            if event.key == pygame.K_ESCAPE:
##                done = True
    screen.fill((255,255,255))
    if ui.activemenu == 'main' or ui.activemenu == 'savescreen' or ui.activemenu == 'loadscreen': drawpoints = True
    else: drawpoints = False
    if ui.IDs['gridline toggle'].toggle and drawpoints:
        for a in range((screenw-150)//gridsize+1):
            pygame.draw.line(screen,(235,235,235),(a*gridsize+150,0),(a*gridsize+150,screenh))
        for a in range(screenh//gridsize+1):
            pygame.draw.line(screen,(235,235,235),(150,a*gridsize),(screenw,a*gridsize))
    for b in splines:
        points = []
        for a in b:
            points+=bezierdrawer([(ui.IDs[a[b]].x+ui.IDs[a[b]].width/2,ui.IDs[a[b]].y+ui.IDs[a[b]].height/2) for b in range(len(a))],0,drawpoints)
        if not drawpoints:
            if points[0] == points[-1]:
                pygame.gfxdraw.aapolygon(screen,points,(0,0,0))
                pygame.gfxdraw.filled_polygon(screen,points,(0,0,0))
##                pygame.draw.polygon(screen,(0,0,0),points)
            else:
                pygame.draw.aalines(screen,(0,0,0),False,points)
    ui.rendergui(screen)
    pygame.display.flip()
    clock.tick(60)
pygame.quit() 
