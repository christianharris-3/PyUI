import pygame,random,math,time,copy,ctypes
pygame.init()

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def rectscaler(rect,scale,offset=(0,0)):
    if not type(scale) in [float,int]:
        return pygame.Rect((rect.x-offset[0])*scale.dirscale[0],(rect.y-offset[1])*scale.dirscale[1],rect.w*scale.scale,rect.h*scale.scale)
    else:
        return pygame.Rect((rect.x-offset[0])*scale,(rect.y-offset[1])*scale,rect.w*scale,rect.h*scale)
def roundrect(x,y,width,height):
    return pygame.Rect(round(x),round(y),round(width),round(height))

def emptyfunction():
    pass

def normalizelist(lis,sumto=1):
    total = sum(lis)
    if total>0:
        newlis = []
        for a in lis:
            newlis.append(a*(sumto/total))
        return newlis
    else:
        return lis

def drawroundedline(surf,col,point1,point2,width):
    if point1[0]-point2[0] != 0:
        grad = (point1[1]-point2[1])/(point1[0]-point2[0])
        if grad != 0: invgrad = -1/grad
        else: invgrad = 100000
    else: invgrad = 0
    ang = math.atan(invgrad)
    points = [(point1[0]+math.cos(ang)*width,point1[1]+math.sin(ang)*width),
              (point1[0]-math.cos(ang)*width,point1[1]-math.sin(ang)*width),
              (point2[0]-math.cos(ang)*width,point2[1]-math.sin(ang)*width),
              (point2[0]+math.cos(ang)*width,point2[1]+math.sin(ang)*width)]
    pygame.draw.polygon(surf,col,points)
    pygame.draw.circle(surf,col,point1,width)
    pygame.draw.circle(surf,col,point2,width)

def colav(col1,col2,weight):
    return (col1[0]+(col2[0]-col1[0])*weight,col1[1]+(col2[1]-col1[1])*weight,col1[2]+(col2[2]-col1[2])*weight)
def shiftcolor(col,shift):
    return [max([min([255,a+shift]),0]) for a in col]
def autoshiftcol(col,default=(150,150,150),editamount=0):
    if type(col) == int:
        if col != -1:
            editamount = col
        col = default
        return shiftcolor(col,editamount)
    return col

def linecross(L1,L2):
    #print(L1,L2)
##    x1,x2,x3,x4,y1,y2,y3 ,y4 = L1[0][0],L1[1][0],L2[0][0],L2[1][0],L1[0][1],L1[1][1],L2[0][1],L2[1][1]
##    xcross = (x1*(x3*(-2*y1+y2+2*y3-y4)+x4*(2*y1-y2-y3))+x2*(x3*(y1-2*y3+y4)+x4*(y3-y1)))/(y3*(x1-x2)+y4*(x2-x1)+y1*(x4-x3)+y2*(x3-x4))
    a,b,c,d,e,f,g,h = L1[0][0],L1[1][0],L2[0][0],L2[1][0],L1[0][1],L1[1][1],L2[0][1],L2[1][1]
    try:
        xcross = (a*(c*(h-f)+d*(f-g))+b*(c*(e-h)+d*(g-e)))/((g*(b-a)+h*(a-b)+e*(c-d)+f*(d-c)))
        if abs(a-b) < 0.001:
            ycross = (xcross-c)*((g-h)/(c-d))+g
        else:
            ycross = ((e-f)*(xcross-a))/(a-b)+e

        distances = []
        for x in L1+L2:
            distances.append(((x[0]-xcross)**2+(x[1]-ycross)**2)**0.5)
##        print(distances,L1,L2,xcross,ycross)
        if min(distances)<0.1:
            return False,10
        else: 
            dis = 0
            if a<b:
                if xcross<a-dis or xcross>b+dis:
                    return False,1
            elif b<a:
                if xcross<b-dis or xcross>a+dis:
                    return False,2
            if c<d:
                if xcross<c-dis or xcross>d+dis:
                    return False,3
            elif d<c:
                if xcross<d-dis or xcross>c+dis:
                    return False,4
            if e<f:
                if ycross<e-dis or ycross>f+dis:
                    return False,5
            elif f<e:
                if ycross<f-dis or ycross>e+dis:
                    return False,6
            if g<h:
                if ycross<g-dis or ycross>h+dis:
                    return False,7
            elif h<g:
                if ycross<h-dis or ycross>g+dis:
                    return False,8

        return True,xcross,ycross
    except:
        return False,9

def linecirclecross(L1,L2):
    #print(L1,L2)
    a,b,c,d = -L1[0][0],-L1[1][0],-L1[0][1],-L1[1][1]
    p,q,r = L2[0][0],L2[0][1],L2[1]
    if c-d == 0:
        m = 0
        i = m*a-c
        A = (m**2+1)
        B = 2*(m*i-m*q-p)
    elif a-b == 0:
        m = 1000000000
        i = a
        A = 1
        B = 2*p
    else:
        m = (c-d)/(a-b)
        i = m*a-c
        A = (m**2+1)
        B = 2*(m*i-m*q-p)
    C = (q**2-r**2+p**2-2*i*q+i**2)
    if B**2-4*A*C<0:
        return False,2
##    ycross1 = (m*(((-B)+math.sqrt(B**2-4*A*C))/(2*A))+i)
##    ycross2 = (m*(((-B)-math.sqrt(B**2-4*A*C))/(2*A))+i)
    xcross1 = (((-B)+math.sqrt(B**2-4*A*C))/(2*A))
    xcross2 = (((-B)-math.sqrt(B**2-4*A*C))/(2*A))
    ycross1 = (m*xcross1+i)
    ycross2 = (m*xcross2+i)
    dis = 0
    passed = [True,True]
    a,b,c,d = -a,-b,-c,-d
    if a<b:
        if xcross1<a-dis or xcross1>b+dis:
            passed[0] = False
    elif b<a:
        if xcross1<b-dis or xcross1>a+dis:
            passed[0] = False
    if c<d:
        if ycross1<c-dis or ycross1>d+dis:
            passed[0] = False
    elif d<c:
        if ycross1<d-dis or ycross1>c+dis:
            passed[0] = False
    if a<b:
        if xcross2<a-dis or xcross2>b+dis:
            passed[1] = False
    elif b<a:
        if xcross2<b-dis or xcross2>a+dis:
            passed[1] = False
    if c<d:
        if ycross2<c-dis or ycross2>d+dis:
            passed[1] = False
    elif d<c:
        if ycross2<d-dis or ycross2>c+dis:
            passed[1] = False
    if passed[0] == True:
        return True,[xcross1,ycross1]
    if passed[1] == True:
        return True,[xcross2,ycross2]
    return False,0

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

class UI:
    def __init__(self,scale=1):
        pygame.key.set_repeat(350,31)
        
        self.scale = scale
        self.dirscale = [1,1]
        self.mouseheld = [[0,0],[0,0],[0,0]]
        
        self.buttons = []
        self.tables = []
        self.textboxes = []
        self.texts = []
        self.scrollers = []
        self.sliders = []
        self.animations = []
        self.rects = []
        self.selectedtextbox = -1
        self.IDs = {}
        self.items = []

        self.images = []
        self.getscreen()

        self.activemenu = 'main'
        self.windowedmenus = []
        self.windowedmenunames = []
        self.backchain = []
        self.queuedmenumove = [0,[]]
        self.buttondowntimer = 9

        self.fullscreen = False
        self.exit = False
        
        self.loadtickdata()
        self.checkcaps()
        self.clipboard = pygame.scrap.get('str')

        self.defaultfont = 'calibre'
        self.defaultcol = (150,150,150)
        self.defaulttextcol = (0,0,0)
        self.defaultbackingcol = (255,255,255)
        self.defaultanimationspeed = 30
        self.escapeback = True
        self.backquits = True
        self.scrollwheelscrolls = True
        self.idmessages = False
        
        self.resizable = True
        self.fullscreenable = True
        self.autoscale = 'width'
        tempscreen = pygame.display.get_surface()
        self.basescreensize = [tempscreen.get_width(),tempscreen.get_height()]

    def checkcaps(self):
        hllDll = ctypes.WinDLL("User32.dll")
        self.capslock = bool(hllDll.GetKeyState(0x14))
        
    def scaleset(self,scale):
        self.scale = scale
        self.dirscale = [self.screenw/self.basescreensize[0],self.screenh/self.basescreensize[1]]
        #fix this later u lazy melt
        for a in self.items:
            if type(TABLE):
                a.refresh(self)
                a.resetcords(self)
            a.refresh(self)
            a.resetcords(self)
        
    def getscreen(self):
        sc = pygame.display.get_surface()
        self.screenw = sc.get_width()
        self.screenh = sc.get_height()
    def rendergui(self,screen):
        windowedmenubackings = [a.behindmenu for a in self.windowedmenus]
        self.breakrenderloop = False
        for i,a in enumerate(self.items):
            if (a.menu in windowedmenubackings or (a.menu == 'universal' and not(self.activemenu in a.menuexceptions))) and (self.activemenu in self.windowedmenunames) and type(a)!=WINDOWEDMENU:
                if a.menu == windowedmenubackings[self.windowedmenunames.index(self.activemenu)]:
                    window = self.windowedmenus[self.windowedmenunames.index(self.activemenu)]
                    if pygame.Rect(window.x,window.y,window.width,window.height).collidepoint(self.mpos):
                        self.drawguiobject(a,screen)
                    else:
                        if window.isolated:
                            self.drawguiobject(a,screen)
                            if self.mprs[0] and self.mouseheld[0][1] == self.buttondowntimer:
                                self.menuback()
                        else:
                            self.renderguiobject(a,screen)
            elif (a.menu == self.activemenu or (a.menu == 'universal' and not(self.activemenu in a.menuexceptions))) and not(self.activemenu in self.windowedmenunames):
                self.renderguiobject(a,screen)
            if self.breakrenderloop:
                break
        self.animate()
        if self.activemenu in self.windowedmenunames:
            window = self.windowedmenus[self.windowedmenunames.index(self.activemenu)]
            #window = [menu,behindmenu,x,y,width,height,col,rounedcorners,colorkey,isolated,darken]
            self.mpos[0]-=window.x
            self.mpos[1]-=window.y

            darkening = pygame.Surface((self.screenw,self.screenh),pygame.SRCALPHA)
            darkening.fill((0,0,0,window.darken))
            screen.blit(darkening,(0,0))

            windowsurf = pygame.Surface((window.width*self.scale,window.height*self.scale))
            windowsurf.fill(window.colorkey)
            pygame.draw.rect(windowsurf,window.col,pygame.Rect(0,0,window.width*self.scale,window.height*self.scale),border_radius=int(window.roundedcorners*self.scale))
            windowsurf.set_colorkey(window.colorkey)
            for i,a in enumerate(self.items):
                if (a.menu == self.activemenu or (a.menu == 'universal' and not(self.activemenu in a.menuexceptions)))and type(a)!=WINDOWEDMENU:
                    self.renderguiobject(a,windowsurf)
            screen.blit(windowsurf,(window.x*self.scale,window.y*self.scale))
    def renderguiobject(self,a,screen):
        a.render(screen,self)
    def drawguiobject(self,a,screen):
        a.draw(screen,self)
            
    def loadtickdata(self):
        mpos = pygame.mouse.get_pos()
        self.mpos = [mpos[0]/self.scale,mpos[1]/self.scale]
        self.mprs = pygame.mouse.get_pressed()
        self.kprs = pygame.key.get_pressed()
        for a in range(3):
            if self.mprs[a] and not self.mouseheld[a][0]: self.mouseheld[a] = [1,self.buttondowntimer]
            elif self.mprs[a]: self.mouseheld[a][1] -= 1
            if not self.mprs[a]: self.mouseheld[a][0] = 0
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_CAPSLOCK:
                    if self.capslock: self.capslock = False
                    else: self.capslock = True
                if event.key == pygame.K_ESCAPE and self.escapeback:
                    self.menuback()
                if event.key == pygame.K_F5:
                    self.scaleset(self.scale)
                if event.key == pygame.K_F11 and self.fullscreenable:
                    self.togglefullscreen(pygame.display.get_surface())
                if self.selectedtextbox!=-1:
                    if not self.textboxes[self.selectedtextbox].selected:
                        self.selectedtextbox = -1
                    else:
                        self.textboxes[self.selectedtextbox].inputkey(self.capslock,event,self.kprs,self)
            if event.type == pygame.VIDEORESIZE:
                self.screenw = event.w
                self.screenh = event.h
                self.resetscreen(pygame.display.get_surface())
            if event.type == pygame.MOUSEWHEEL:
                moved = False
                for a in self.textboxes:
                    if a.scrolleron and a.selected:
                        a.scroller.scroll-=(event.y*(a.scroller.maxp-a.scroller.minp)/20)
                        a.scroller.limitpos(self)
                        moved = True
                if not moved:
                    for a in self.scrollers:
                        if a.menu == self.activemenu and not a.ontextbox:
                            a.scroll-=(event.y*(a.maxp-a.minp)/20)
                            a.limitpos(self)
                            break
        if self.exit:
            events.append(pygame.event.Event(pygame.QUIT))
        return events
    def togglefullscreen(self,screen):
        if self.fullscreen: self.fullscreen = False
        else: self.fullscreen = True
        self.resetscreen(screen)
    def resetscreen(self,screen):
        if self.autoscale == 'width':
            self.scaleset(self.screenw/self.basescreensize[0])
        else:
            self.scaleset(self.screenh/self.basescreensize[1])
        if self.fullscreen: screen = pygame.display.set_mode((self.screenw,self.screenh),pygame.FULLSCREEN)
        else: screen = pygame.display.set_mode((self.screenw,self.screenh),pygame.RESIZABLE)       
        
    def write(self,screen,x,y,text,size,col='default',center=True,font='default',bold=False,antialiasing=True):
        if font=='default': font=self.defaultfont
        if col == 'default': col = self.defaulttextcol
        largetext = pygame.font.SysFont(font,int(size*self.scale),bold)
        textsurf = largetext.render(text, antialiasing, col)
        textrect = textsurf.get_rect()
        if center:
            textrect.center = (int(x)*self.dirscale[0],int(y)*self.dirscale[1])
            textrect.y = y*self.dirscale[1]
        else:
            textrect.x = int(x)*self.dirscale[0]
            textrect.y = int(y)*self.dirscale[1]
        screen.blit(textsurf, textrect)

    def rendertext(self,text,size,col='default',font='default',bold=False,antialiasing=True,backingcol=(150,150,150),imgin=False,img=''):
        if font=='default': font = self.defaultfont
        if col == 'default': col = self.defaulttextcol
        if imgin:
            if text == '' and img!='':
                text = '{'+img+'}'
            stext = text.split('{')
            texts = []
            imagenames = []
            texts.append(stext[0])
            del stext[0]
            for a in stext:
                split = a.split('}')
                texts.append(split[1])
                if split[0] == '':
                    imagenames.append(img)
                else:
                    imagenames.append(split[0])
        else:
            texts = [text]
        images = []
        largetext = pygame.font.SysFont(font,int(size),bold)
        images.append(largetext.render(texts[0], antialiasing, col))
        for a in range(len(texts)-1):
            images.append(self.rendershape(imagenames[a],size,col,False))
            images.append(largetext.render(texts[a+1], antialiasing, col))
        textsurf = pygame.Surface((sum([a.get_width() for a in images]),max([a.get_height() for a in images])))
        textsurf.fill(backingcol)
        xpos = 0
        h = textsurf.get_height()
        for a in images:
            textsurf.blit(a,(xpos,(h-a.get_height())/2))
            xpos+=a.get_width()
        textsurf.set_colorkey(backingcol)
        return textsurf

    def rendershape(self,name,size,col='default',failmessage=True):
        if col == 'default': col = self.defaulttextcol
        backcol = (255,255,255)
        if col == backcol: backcol = (0,0,0)
        if name[:4] == 'tick':
            surf = self.rendershapetick(name,size,col,backcol)
        elif name[:5] == 'arrow':
            surf = self.rendershapearrow(name,size,col,backcol)
        elif name[:5] == 'cross':
            surf = self.rendershapecross(name,size,col,backcol)
        elif name[:8] == 'settings':
            surf = self.rendershapesettings(name,size,col,backcol)
        elif name[:4] == 'play':
            surf = self.rendershapeplay(name,size,col,backcol)
        elif name[:5] == 'pause':
            surf = self.rendershapepause(name,size,col,backcol)
        elif name[:4] == 'skip':
            surf = self.rendershapeskip(name,size,col,backcol)
        elif name[:6] == 'circle':
            surf = self.rendershapecircle(name,size,col,backcol)
        elif name[:4] == 'rect':
            surf = self.rendershaperect(name,size,col,backcol)
        elif name[:5] == 'clock':
            surf = self.rendershapeclock(name,size,col,backcol)
        else:
            surf = self.rendershapebezier(name,size,col,backcol,failmessage)
        if 'left' in name:
            surf = pygame.transform.flip(surf,True,False)
        elif 'up' in name:
            surf = pygame.transform.rotate(surf,90)
        elif 'down' in name:
            surf = pygame.transform.rotate(surf,-90)
        surf.set_colorkey(backcol)
        return surf
    def rendershapetick(self,name,size,col,backcol):
        vals = self.getshapedata(name,['thickness'],[0.2])
        basethickness = vals[0]
        tsize = size
        size = 1000
        surf = pygame.Surface((size,size))
        surf.fill(backcol)
        thickness = size*basethickness
        points = [[size*0.12,size*0.6],[size*0.38,size*0.9],[size*0.88,size*0.1]]
        sc = 1-(thickness/size)
        for a in points:
            a[0] = (a[0]-size*0.5)*sc+size*0.5
            a[1] = (a[1]-size*0.5)*sc+size*0.5
        
        pygame.draw.lines(surf,col,False,points,int(thickness))
        thickness/=2
        dirc = [-1,1,-1]
        skew = [(-0.6,0),(0,-0.4),(0.6,0)]
        npoints = []
        detail = 100
        for i,a in enumerate(points):
            npoints.append([])
            for b in range(detail+1):
                npoints[-1].append([a[0]+(math.cos(b/detail*math.pi)+abs(math.sin(b/detail*math.pi))*skew[i][0])*thickness,a[1]+(math.sin(b/detail*math.pi)+abs(math.sin(b/detail*math.pi))*skew[i][1])*dirc[i]*thickness])
        for a in npoints[1]:
            a[1]-=size*0.015
        for a in npoints:
            pygame.draw.polygon(surf,col,a)
        surf = pygame.transform.scale(surf,(tsize,tsize))
        return surf
    def rendershapearrow(self,name,size,col,backcol):
        vals = self.getshapedata(name,['stick','point','smooth','width'],[0.95,0.45,0,0.2])
        sticklen = vals[0]
        pointlen = vals[1]
        smooth = bool(vals[2])
        width = vals[3]
        surf = pygame.Surface((size*(sticklen+pointlen+0.1),size*0.7))
        surf.fill(backcol)
        if smooth:
            drawroundedline(surf,col,(size*(width+0.05),size*0.35),(size*(sticklen+pointlen+0.05-width),size*0.35),width*size)
            drawroundedline(surf,col,(size*(sticklen+0.05),size*(0.05+width)),(size*(sticklen+pointlen+0.05-width),size*0.35),width*size)
            drawroundedline(surf,col,(size*(sticklen+0.05),size*(0.7-0.05-width)),(size*(sticklen+pointlen+0.05-width),size*0.35),width*size)
        else:
            pygame.draw.polygon(surf,col,((size*0.05,size*0.25),(size*(sticklen+0.05),size*0.25),(size*(sticklen+0.05),size*0.05),(size*(sticklen+pointlen+0.05),size*0.35),(size*(sticklen+0.05),size*0.65),(size*(sticklen+0.05),size*0.45),(size*0.05,size*0.45)))
        return surf
    def rendershapecross(self,name,size,col,backcol):
        vals = self.getshapedata(name,['width'],[0.1])
        width = vals[0]
        surf = pygame.Surface((size,size))
        surf.fill(backcol)
        drawroundedline(surf,col,(size*width,size*width),(size*(1-width),size*(1-width)),size*width)
        drawroundedline(surf,col,(size*(1-width),size*width),(size*width,size*(1-width)),size*width)
        return surf
    def rendershapesettings(self,name,size,col,backcol):
        surf = pygame.Surface((size,size))
        surf.fill(backcol)
        vals = self.getshapedata(name,['innercircle','outercircle','prongs','prongwidth','prongsteepness'],[0.15,0.35,6,0.2,1.1])
        innercircle = vals[0]
        outercircle = vals[1]
        prongs = int(vals[2])
        prongwidth = vals[3]
        prongsteepness = vals[4]
        pygame.draw.circle(surf,col,(size*0.5,size*0.5),size*outercircle)
        pygame.draw.circle(surf,backcol,(size*0.5,size*0.5),size*innercircle)
        width=prongwidth
        innerwidth=width+math.sin(width)*prongsteepness
        points = []
        outercircle-=0.01
        for a in range(prongs):
            ang = (math.pi*2)*a/prongs
            points.append([((math.sin(ang-width)*0.5*0.95+0.5)*size,(math.cos(ang-width)*0.5*0.95+0.5)*size),((math.sin(ang+width)*0.5*0.95+0.5)*size,(math.cos(ang+width)*0.5*0.95+0.5)*size),((math.sin(ang+innerwidth)*0.5*(outercircle*2)+0.5)*size,(math.cos(ang+innerwidth)*0.5*(outercircle*2)+0.5)*size),((math.sin(ang-innerwidth)*0.5*(outercircle*2)+0.5)*size,(math.cos(ang-innerwidth)*0.5*(outercircle*2)+0.5)*size)])
        for a in points:
            pygame.draw.polygon(surf,col,a)
        return surf
    def rendershapeplay(self,name,size,col,backcol):
        vals = self.getshapedata(name,['rounded'],[0.0])
        rounded = vals[0]
        points = [[size*rounded/2,size*rounded/2],[size*rounded/2+size*(1-rounded)*(3**0.5)/2,size*0.5],[size*rounded/2,size-size*(rounded)/2]]
        realign = ((((points[0][0]-points[-1][0])**2+(points[0][1]-points[-1][1])**2)**0.5)*(3**0.5)/3)-size/(2*(3**0.5))
        surf = pygame.Surface((size*(rounded+(1-rounded)*(3**0.5)/2)+realign,size))
        surf.fill(backcol)
        for a in range(len(points)):
            points[a][0]+=realign
        for a in range(len(points)):
            drawroundedline(surf,col,points[a],points[a-1],size*rounded/2)
        pygame.draw.polygon(surf,col,points)
        return surf
    def rendershapepause(self,name,size,col,backcol):
        surf = pygame.Surface((size*0.75,size))
        surf.fill(backcol)
        vals = self.getshapedata(name,['rounded'],[0.0])
        rounded = vals[0]
        pygame.draw.rect(surf,col,pygame.Rect(0,0,size*0.25,size),border_radius=int(size*rounded))
        pygame.draw.rect(surf,col,pygame.Rect(size*0.5,0,size*0.25,size),border_radius=int(size*rounded))
        return surf
    def rendershapeskip(self,name,size,col,backcol):
        vals = self.getshapedata(name,['rounded','thickness','offset'],[0,0.25,-0.35])
        rounded = vals[0]
        thickness = vals[1]
        offset = vals[2]
        points = [[size*rounded/2,size*rounded/2],[size*rounded/2,size-size*(rounded)/2]]
        realign = ((((points[0][0]-points[-1][0])**2+(points[0][1]-points[-1][1])**2)**0.5)*(3**0.5)/3)-size/(2*(3**0.5))
        surf = pygame.Surface((max([size*(rounded+(1-rounded)*(3**0.5)/2),size+(offset+thickness)*size]),size))
        surf.fill(backcol)
        surf.blit(self.rendershapeplay(name,size,col,backcol),(-realign,0))
        pygame.draw.rect(surf,col,pygame.Rect(size+size*offset,0,size*thickness,size),border_radius=int(size*rounded))
        return surf
    def rendershapecircle(self,name,size,col,backcol):
        vals = self.getshapedata(name,['width'],[1])
        width = vals[0]
        surf = pygame.Surface((size*width,size))
        surf.fill(backcol)
        pygame.draw.ellipse(surf,col,pygame.Rect(0,0,size*width,size))
        return surf
    def rendershaperect(self,name,size,col,backcol):
        vals = self.getshapedata(name,['rounded','width'],[0,size])
        rounded = vals[0]
        width = vals[1]*self.scale
        surf = pygame.Surface((width,size))
        surf.fill(backcol)
        pygame.draw.rect(surf,col,pygame.Rect(0,0,width,size),border_radius=int(size*rounded))
        return surf
    def rendershapeclock(self,name,size,col,backcol):
        vals = self.getshapedata(name,['hour','minute','border','handwidth','circlewidth'],[0,20,0.05,0.05,0.05])
        hour = vals[0]
        minute = vals[1]
        border = vals[2]
        handwidth = vals[3]
        circlewidth = vals[4]
        surf = pygame.Surface((size,size))
        surf.fill(backcol)
        pygame.draw.circle(surf,col,(size/2,size/2),size/2)
        pygame.draw.circle(surf,backcol,(size/2,size/2),size/2-size*circlewidth)
        drawroundedline(surf,col,(size/2,size/2),(size/2+size*0.4*math.cos(math.pi*2*(minute/60)-math.pi/2),size/2+size*0.4*math.sin(math.pi*2*(minute/60)-math.pi/2)),size*handwidth)
        drawroundedline(surf,col,(size/2,size/2),(size/2+size*0.25*math.cos(math.pi*2*(hour/12)-math.pi/2),size/2+size*0.25*math.sin(math.pi*2*(hour/12)-math.pi/2)),size*handwidth)
        return surf
    def rendershapebezier(self,name,size,col,backcol,failmessage):
        data = [['test thing', [[[(200, 100), (490, 220), (300, 40), (850, 340)], [(850, 340), (300, 200), (450, 350), (340, 430)], [(340, 430), (310, 250), (200, 310), (200, 100)]], [[(380, 440), (540, 360), (330, 240), (850, 370)], [(850, 370), (380, 440)]]]],
                ['search', [[[(300, 350), (150, 200), (350, 0), (500, 150)], [(500, 150), (560, 210), (520, 280), (485, 315)], [(485, 315), (585, 415)], [(585, 415), (625, 455), (595, 485), (555, 445)], [(555, 445), (455, 345)], [(455, 345), (420, 380), (350, 400), (300, 350)], [(300, 350), (325, 325)], [(325, 325), (205, 205), (365, 65), (475, 175)], [(475, 175), (555, 255), (395, 395), (325, 325)], [(325, 325), (300, 350)]]]],
                ['shuffle', [[[(275, 200), (450, 200), (450, 400), (600, 400)], [(600, 400), (600, 350)], [(600, 350), (675, 425)], [(675, 425), (600, 500)], [(600, 500), (600, 450)], [(600, 450), (425, 450), (425, 250), (275, 250)], [(275, 250), (275, 200)]], [[(275, 400), (275, 450)], [(275, 450), (360, 450), (420, 390)], [(420, 390), (385, 345)], [(385, 345), (350, 390), (275, 400)]], [[(600, 250), (600, 300)], [(600, 300), (675, 225)], [(675, 225), (600, 150)], [(600, 150), (600, 200)], [(600, 200), (500, 200), (455, 260)], [(455, 260), (490, 300)], [(490, 300), (530, 255), (600, 250)]]]],
                ['penis', [[[(560, 540), (670, 440), (690, 320), (690, 200)], [(690, 200), (680, -10), (620, 60), (610, 190)], [(610, 190), (600, 310), (570, 410), (510, 470)], [(510, 470), (440, 520), (480, 570), (560, 540)]], [[(490, 500), (370, 560), (280, 420), (440, 300), (570, 420), (540, 460)], [(540, 460), (490, 500)]], [[(560, 500), (650, 430), (810, 470), (610, 730), (470, 650), (530, 540)], [(530, 540), (560, 500)]]]],
                ['pfp', [[[(340, 430), (710, 430)], [(710, 430), (650, 280), (380, 280), (340, 430)]], [[(510, 280), (400, 280), (400, 50), (630, 50), (630, 280), (510, 280)]]]],
                ['face', [[[(560, 460), (310, 460), (310, 40), (810, 40), (810, 460), (560, 460)], [(560, 460), (560, 430)], [(560, 430), (380, 430), (380, 120), (740, 120), (740, 430), (560, 430)], [(560, 430), (560, 460)]], [[(630, 350), (560, 470), (500, 350)], [(500, 350), (560, 420), (630, 350)]], [[(490, 290), (520, 340), (550, 290)], [(550, 290), (520, 280), (490, 290)]], [[(570, 290), (600, 340), (630, 290)], [(630, 290), (600, 280), (570, 290)]]]],
                ['face2', [[[(560, 460), (310, 460), (310, 40), (810, 40), (810, 460), (560, 460)], [(560, 460), (560, 430)], [(560, 430), (380, 430), (380, 120), (740, 120), (740, 430), (560, 430)], [(560, 430), (560, 460)]], [[(590, 350), (560, 470), (530, 350)], [(530, 350), (570, 360), (590, 350)]], [[(490, 290), (520, 340), (550, 290)], [(550, 290), (520, 280), (490, 290)]], [[(570, 290), (600, 340), (630, 290)], [(630, 290), (600, 280), (570, 290)]]]],
                ['heart', [[[(549, 526), (528, 483), (444, 462), (444, 399)], [(444, 399), (444, 357), (486, 315), (549, 357)], [(549, 357), (612, 315), (654, 357), (654, 399)], [(654, 399), (654, 462), (570, 483), (549, 526)]]]],
                ]
        for a in self.images:
            data.append(a)
        names = [a[0] for a in data]
        splines = []
        for a in names:
            if name[:len(a)] == a:
                splines = data[names.index(a)][1]
        if splines == [] and failmessage:
            print('incorrect image name "'+name+'"')
        boundingbox = [1000,1000,0,0]
        for a in splines:
            for b in a:
                for c in b:
                    if c[0]<boundingbox[0]: boundingbox[0] = c[0]
                    if c[1]<boundingbox[1]: boundingbox[1] = c[1]
                    if c[0]>boundingbox[2]: boundingbox[2] = c[0]
                    if c[1]>boundingbox[3]: boundingbox[3] = c[1]
        minus1 = [boundingbox[0],boundingbox[1]]
        mul1 = size/(boundingbox[3]-boundingbox[1])
        polys = []
        for b in splines:
            points = []
            for a in b:
                points+=bezierdrawer([((a[c][0]-minus1[0])*mul1,(a[c][1]-minus1[1])*mul1) for c in range(len(a))],0,False)
            polys.append(points)
        boundingbox = [1000,1000,0,0]   
        for a in polys:
            for c in a:
                if c[0]<boundingbox[0]: boundingbox[0] = c[0]
                if c[1]<boundingbox[1]: boundingbox[1] = c[1]
                if c[0]>boundingbox[2]: boundingbox[2] = c[0]
                if c[1]>boundingbox[3]: boundingbox[3] = c[1]
        minus = [boundingbox[0],boundingbox[1]]
        mul = size/(boundingbox[3]-boundingbox[1])
        surf = pygame.Surface((size*((boundingbox[2]-boundingbox[0])/(boundingbox[3]-boundingbox[1])),size))
        surf.fill(backcol)
        for b in splines:
            points = []
            for a in b:
                points+=bezierdrawer([(((a[c][0]-minus1[0])*mul1-minus[0])*mul,((a[c][1]-minus1[1])*mul1-minus[1])*mul) for c in range(len(a))],0,False)
            pygame.draw.polygon(surf,col,points)

        return surf
                        
    def getshapedata(self,name,var,defaults):
        vals = defaults
        if sum([a in name for a in var])>0:
            namesplit = name.split()
            for a in namesplit:
                for i,b in enumerate(var):
                    if b in a:
                        vals[i] = float(a.split('=')[1])     
        return vals
        
    def rendertextlined(self,text,size,col='default',backingcol=(150,150,150),font='default',width=-1,bold=False,antialiasing=True,center=False,spacing=0,imgin=False,img='',scale='default',linelimit=10000,getcords=False):
        if font=='default': font=self.defaultfont
        if col == 'default': col = self.defaulttextcol
        if width==-1 and center: center = False
        if scale == 'default': scale = self.scale
        size*=scale
        if width!=-1: width*=scale
        if text == '' and (img == '' or img == 'none'):
            if getcords:
                return pygame.Surface((0,0)),[]
            return pygame.Surface((0,0))
        imgchr = '@'
        imgnames = []
        imgwidthid = 0
        if imgin:
            ntext = ''
            stext = text.split('{')
            ntext+=stext[0]
            del stext[0]
            if len(stext) == 0:
                imgnames = ['']
            for a in stext:
                split = a.split('}')
                ntext+=imgchr
                ntext+=split[1]
                imgnames.append(split[0])
        else:
            ntext = text
            
        lines = ntext.split('\n')
        textgen = pygame.font.SysFont(font,int(size),bold)
        
        textimages = []
        imagesize = [0,0]
        addedlines = 0
        processedlines = []
        while len(lines)>0 and addedlines < linelimit:
            newline = ''
            if width!=-1:
                if textgen.size(lines[0])[0] != imgchr :
                    chrwidth = textgen.size(lines[0])[0]
                else:
                    chrwidth = self.rendershape(imgnames[imgwidthid],size,col).get_width()
                while chrwidth>width:
                    split = lines[0].rsplit(' ',1)
                    if len(split)>1:
                        slide = split[1]
                        replace = split[0]+' '
                        if split[1] == '':
                            slide = ' '
                            replace = split[0]
                    else:
                        replace = split[0][:len(split[0])-1]
                        if split[0] != '':
                            slide = split[0][-1]
                        else:
                            slide = ''
                    lines[0] = replace
                    newline = slide+newline
                    if textgen.size(lines[0])[0] != imgchr :
                        chrwidth = textgen.size(lines[0])[0]
                    else:
                        chrwidth = self.rendershape(imgnames[imgwidthid],size,col).get_width()
            if imgin:
                while lines[0].count(imgchr) != 0:
                    lines[0] = lines[0].replace(imgchr,'{'+imgnames[imgwidthid]+'}',1)
                    if imgwidthid!=len(imgnames)-1:
                        imgwidthid+=1
            if lines[0] == '':
                lines[0] = newline
                newline = ''
            textimages.append(self.rendertext(lines[0],int(size),col,font,bold,antialiasing,backingcol,imgin,img))
            tempsize = (textimages[-1].get_width(),textimages[-1].get_height())
            if tempsize[0]>imagesize[0]: imagesize[0] = tempsize[0]
            imagesize[1]+=tempsize[1]+spacing
            processedlines.append(lines[0])
            del lines[0]
            if newline!='':
                lines.insert(0,newline)
            else:
                break
            addedlines+=1
        surf = pygame.Surface(imagesize)
        surf.fill(backingcol)
        yinc = 0
        if not center:
            for a in textimages:
                surf.blit(a,(0,yinc))
                yinc+=a.get_height()+spacing
        else:
            for a in textimages:
                surf.blit(a,(int(surf.get_width()/2)-int(a.get_width()/2),yinc))
                yinc+=a.get_height()+spacing
        surf.set_colorkey(backingcol)
        if getcords:
            cords = self.textlinedcordgetter(center,imagesize,textimages,processedlines,textgen,spacing,width)
            return surf,cords
        return surf
    
    def textlinedcordgetter(self,center,imagesize,textimages,processedlines,textgen,spacing,width):#text,size,font='default',width=-1,bold=False,center=False,spacing=0):
        rowstart = []
        if center:
            for a in processedlines:
                rowstart.append(int(width/2)-int(textgen.size(a)[0]/2))
        else: rowstart = [0 for a in range(len(processedlines))]
        yinc = 0
        corddata = []
        noffset = 0
        nsize = textgen.size('\n')[0]
        for i,a in enumerate(processedlines):
            if a[:1] == '\n': noffset = nsize
            else: noffset = 0
            corddata.append([])
            for b in range(len(a)):
                lettersize = textgen.size(a[b])
                linesize = textgen.size(a[:b+1])
                corddata[-1].append([a[b],(rowstart[i]+linesize[0]-lettersize[0]/2-noffset,yinc+lettersize[1]/2),lettersize])
            yinc+=textgen.size(a)[1]+spacing
        return corddata
    def gettextsize(self,text,font,size,bold=False):
        largetext = pygame.font.SysFont(font,int(size),bold)
        size = largetext.size(text)
        return size

    def addid(self,ID,obj):
        if ID in self.IDs:
            adder = 1
            ID+=str(adder)
            while ID in self.IDs:
                ID = ID.removesuffix(str(adder))
                adder+=1
                ID+=str(adder)
        if self.idmessages: print('adding:',ID)
        self.IDs[ID] = obj
        obj.ID = ID
        if type(obj) == BUTTON: self.buttons.append(obj)
        elif type(obj) == TEXTBOX: self.textboxes.append(obj)
        elif type(obj) == TABLE: self.tables.append(obj)
        elif type(obj) == TEXT: self.texts.append(obj)
        elif type(obj) == SCROLLER: self.scrollers.append(obj)
        elif type(obj) == SLIDER: self.sliders.append(obj)
        elif type(obj) == WINDOWEDMENU: self.windowedmenus.append(obj)
        elif type(obj) == ANIMATION: self.animations.append(obj)
        elif type(obj) == RECT: self.rects.append(obj)
        self.refreshitems()
    def refreshitems(self):
        self.items = self.buttons+self.textboxes+self.tables+self.texts+self.scrollers+self.sliders+self.windowedmenus+self.rects
        self.items.sort(key=lambda x: x.layer,reverse=False)
        
    def makebutton(self,x,y,text,textsize=50,command=emptyfunction,menu='main',ID='button',layer=1,roundedcorners=0,menuexceptions=[],width=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,img='none',font='default',bold=False,antialiasing=True,pregenerated=True,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=True,scalex=True,scaley=True,
                 runcommandat=0,col=-1,textcol=-1,backingcol=-1,bordercol=-1,hovercol=-1,clickdownsize=4,clicktype=0,textoffsetx=0,textoffsety=0,maxwidth=-1,
                 dragable=False,colorkey=(255,255,255),toggle=True,toggleable=False,toggletext=-1,toggleimg='none',togglecol=-1,togglehovercol=-1,bindtoggle=[],spacing=-1,verticalspacing=0,horizontalspacing=8,
                 backingdraw=True,borderdraw=True,animationspeed=5,linelimit=1000):
        if maxwidth == -1: maxwidth = width
        if backingcol == -1: backingcol = bordercol
        obj = BUTTON(self,x,y,width,height,menu,ID,layer,roundedcorners,menuexceptions,
                 anchor,objanchor,center,centery,text,textsize,img,font,bold,antialiasing,pregenerated,
                 border,upperborder,lowerborder,rightborder,leftborder,scalesize,scalex,scaley,
                 command,runcommandat,col,textcol,backingcol,hovercol,clickdownsize,clicktype,textoffsetx,textoffsety,maxwidth,
                 dragable,colorkey,toggle,toggleable,toggletext,toggleimg,togglecol,togglehovercol,bindtoggle,spacing,verticalspacing,horizontalspacing,animationspeed=animationspeed,backingdraw=backingdraw,borderdraw=borderdraw,linelimit=linelimit)
        return obj
##    def makecheckbox(self,x,y,textsize=80,command=emptyfunction,menu='main',menuexceptions=[],edgebound=(1,0,0,1),text='',col=(255,255,255),bordercol='default',hovercol=-1,textcol='default',img='tick',colorkey=(255,255,255),runcommandat=0,width=-1,height=-1,border=4,clickdownsize=1,verticalspacing=-15,horizontalspacing=-15,roundedcorners=0,clicktype=0,textoffsetx=0,textoffsety=0,toggle=True,togglecol=-1,togglehovercol=-1,toggleable=True,drawifoff=False,bindtoggle=[],dragable=False,center=True,font='default',bold=False,layer=1,ID='tickbox',returnobj=False):
    def makecheckbox(self,x,y,textsize=80,command=emptyfunction,menu='main',ID='checkbox',text='',layer=1,roundedcorners=0,menuexceptions=[],width=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,img='tick',font='default',bold=False,antialiasing=True,pregenerated=True,
                 border=4,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=True,scalex=True,scaley=True,
                 runcommandat=0,col=-1,textcol=-1,backingcol=-1,bordercol=-1,hovercol=-1,clickdownsize=4,clicktype=0,textoffsetx=0,textoffsety=0,maxwidth=-1,
                 dragable=False,colorkey=(255,255,255),toggle=True,toggleable=True,toggletext='',toggleimg='none',togglecol=-1,togglehovercol=-1,bindtoggle=[],spacing=-15,verticalspacing=-15,horizontalspacing=-15,
                 backingdraw=False,borderdraw=True,animationspeed=5,linelimit=1000):
        if width == -1: width = textsize+spacing*2
        if height == -1: height = textsize+spacing*2
        obj = BUTTON(self,x,y,width,height,menu,ID,layer,roundedcorners,menuexceptions,
                 anchor,objanchor,center,centery,text,textsize,img,font,bold,antialiasing,pregenerated,
                 border,upperborder,lowerborder,rightborder,leftborder,scalesize,scalex,scaley,
                 command,runcommandat,col,textcol,backingcol,hovercol,clickdownsize,clicktype,textoffsetx,textoffsety,maxwidth,
                 dragable,colorkey,toggle,toggleable,toggletext,toggleimg,togglecol,togglehovercol,bindtoggle,spacing,verticalspacing,horizontalspacing,animationspeed=animationspeed,backingdraw=backingdraw,borderdraw=borderdraw,linelimit=linelimit)
        return obj
    def maketextbox(self,x,y,text='',width=200,lines=1,menu='main',command=emptyfunction,ID='textbox',layer=1,roundedcorners=0,menuexceptions=[],height=-1,
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,img='none',textsize=50,font='default',bold=False,antialiasing=True,pregenerated=True,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=True,scalex=True,scaley=True,
                 runcommandat=0,col=-1,textcol=-1,backingcol=-1,hovercol=-1,clickdownsize=4,clicktype=0,textoffsetx=0,textoffsety=0,
                 colorkey=(255,255,255),spacing=-1,verticalspacing=0,horizontalspacing=8,
                 linelimit=100,selectcol=-1,selectbordersize=2,selectshrinksize=0,cursorsize=-1,textcenter=False,chrlimit=10000,numsonly=False,enterreturns=False,commandifenter=True,commandifkey=False,
                 backingdraw=True,borderdraw=True):
        if col == -1: col = self.defaultcol
        if backingcol == -1: backingcol = shiftcolor(col,-20)   
        obj = TEXTBOX(self,x,y,width,height,menu,ID,layer,roundedcorners,menuexceptions,
                 anchor,objanchor,center,centery,text,textsize,img,font,bold,antialiasing,pregenerated,
                 border,upperborder,lowerborder,rightborder,leftborder,scalesize,scalex,scaley,
                 command,runcommandat,col,textcol,backingcol,hovercol,clickdownsize,clicktype,textoffsetx,textoffsety,
                 colorkey=colorkey,spacing=spacing,verticalspacing=verticalspacing,horizontalspacing=horizontalspacing,
                 lines=lines,linelimit=linelimit,selectcol=selectcol,selectbordersize=selectbordersize,selectshrinksize=selectshrinksize,cursorsize=cursorsize,textcenter=textcenter,chrlimit=chrlimit,numsonly=numsonly,enterreturns=enterreturns,commandifenter=commandifenter,commandifkey=commandifkey,
                 backingdraw=backingdraw,borderdraw=borderdraw)
        return obj
            
            
##    def maketable(self,x,y,data='empty',titles=[],menu='main',menuexceptions=[],edgebound=(1,0,0,1),rows=5,colomns=3,boxwidth=-1,boxheight=-1,spacing=10,col='default',boxtextcol='default',boxtextsize=40,boxcenter=True,font='default',bold=False,titlefont=-1,titlebold=-1,titleboxcol=-1,titletextcol='default',titletextsize=-1,titlecenter=True,linesize=2,linecol=-1,roundedcorners=0,layer=1,ID='default',returnobj=False):

    def maketable(self,x,y,data='empty',titles=[],menu='main',ID='table',layer=1,roundedcorners=0,menuexceptions=[],width=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,text='',textsize=50,img='none',font='default',bold=False,antialiasing=True,pregenerated=True,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=True,scalex=True,scaley=True,
                 command=emptyfunction,runcommandat=0,col=-1,textcol=-1,backingcol=-1,hovercol=-1,clickdownsize=4,clicktype=0,textoffsetx=0,textoffsety=0,
                 dragable=False,colorkey=(255,255,255),spacing=-1,verticalspacing=0,horizontalspacing=8,
                 boxwidth=-1,boxheight=-1,linesize=2,textcenter=True,
                 backingdraw=True,borderdraw=True):

        if col == -1: col = self.defaultcol
        if backingcol == -1: backingcol = shiftcolor(col,-20)
        
        #obj = TABLE(x,y,rows,colomns,data,titles,boxwidth,boxheight,spacing,menu,menuexceptions,boxcol,boxtextcol,boxtextsize,boxcenter,font,bold,titlefont,titlebold,titleboxcol,titletextcol,titletextsize,titlecenter,linesize,linecol,roundedcorners,layer,ID,self)
        obj = TABLE(self,x,y,width,height,menu,ID,layer,roundedcorners,menuexceptions,
                 anchor,objanchor,center,centery,text,textsize,img,font,bold,antialiasing,pregenerated,
                 border,upperborder,lowerborder,rightborder,leftborder,scalesize,scalex,scaley,
                 command,runcommandat,col,textcol,backingcol,hovercol,clickdownsize,clicktype,textoffsetx,textoffsety,
                 colorkey=colorkey,spacing=spacing,verticalspacing=verticalspacing,horizontalspacing=horizontalspacing,
                 data=data,titles=titles,boxwidth=boxwidth,boxheight=boxheight,linesize=linesize,textcenter=textcenter,
                 backingdraw=backingdraw,borderdraw=borderdraw)
        return obj
            
##    def maketext(self,x,y,text,size,menu='main',menuexceptions=[],edgebound=(1,0,0,1),col='default',center=True,font='default',bold=False,maxwidth=-1,border=4,backingcol='default',backingdraw=0,backingwidth=-1,backingheight=-1,img='none',colorkey=(255,255,255),roundedcorners=0,layer=1,ID='default',antialiasing=True,pregenerated=True,returnobj=False):
    def maketext(self,x,y,text,textsize=50,menu='main',ID='text',layer=1,roundedcorners=0,menuexceptions=[],width=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,img='none',font='default',bold=False,antialiasing=True,pregenerated=True,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=True,scalex=True,scaley=True,
                 command=emptyfunction,runcommandat=0,col=-1,textcol=-1,clicktype=0,backingcol=-1,bordercol=-1,textoffsetx=0,textoffsety=0,
                 dragable=False,colorkey=(255,255,255),spacing=-1,verticalspacing=3,horizontalspacing=3,maxwidth=-1,animationspeed=5,
                 textcenter=False,backingdraw=False,borderdraw=False):
        if col == -1: col = backingcol
        backingcol = bordercol
        
        obj = TEXT(self,x,y,width,height,menu,ID,layer,roundedcorners,menuexceptions,
                 anchor,objanchor,center,centery,text,textsize,img,font,bold,antialiasing,pregenerated,
                 border,upperborder,lowerborder,rightborder,leftborder,scalesize,scalex,scaley,
                 command,runcommandat,col,textcol,backingcol,clicktype=clicktype,textoffsetx=textoffsetx,textoffsety=textoffsety,maxwidth=maxwidth,
                 dragable=dragable,colorkey=colorkey,spacing=spacing,verticalspacing=verticalspacing,horizontalspacing=horizontalspacing,
                 textcenter=textcenter,backingdraw=backingdraw,borderdraw=borderdraw,animationspeed=animationspeed)
        return obj

##    def makescroller(self,x,y,height,command=emptyfunction,width=15,minh=0,maxh=-1,pageh=100,starth=0,menu='main',menuexceptions=[],edgebound=(1,0,0,1),col='default',scrollercol=-1,hovercol=-1,clickcol=-1,scrollerwidth=11,runcommandat=1,clicktype=0,layer=1,ID='default',returnobj=False):
    def makescroller(self,x,y,height,command=emptyfunction,width=15,minp=0,maxp=100,pageheight=15,menu='main',ID='scroller',layer=1,roundedcorners=0,menuexceptions=[],
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=True,scalex=True,scaley=True,
                 runcommandat=0,col=-1,backingcol=-1,clicktype=0,
                 dragable=True,backingdraw=True,borderdraw=True,scrollercol=-1,scrollerwidth=-1,increment=0,startp=0):

        if maxp == -1:
            maxp = height
        obj = SCROLLER(self,x,y,width,height,menu,ID,layer,roundedcorners,menuexceptions,
                 anchor,objanchor,center,centery,
                 border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,
                 command=command,runcommandat=runcommandat,col=col,backingcol=backingcol,clicktype=clicktype,
                 dragable=dragable,backingdraw=backingdraw,borderdraw=borderdraw,
                 increment=increment,minp=minp,maxp=maxp,startp=startp,pageheight=pageheight)
        return obj

##    def makeslider(self,x,y,width,height,maxp=100,menu='main',command=emptyfunction,menuexceptions=[],edgebound=(1,0,0,1),col='default',slidercol=-1,sliderbordercol=-1,hovercol=-1,clickcol=-1,clickdownsize=2,bordercol=-1,border=2,slidersize=-1,increment=0,img='none',colorkey=(255,255,255),minp=0,startp=0,style='square',roundedcorners=0,barroundedcorners=-1,dragable=True,runcommandat=1,clicktype=0,layer=1,ID='default',returnobj=False):
    def makeslider(self,x,y,width,height,maxp=100,menu='main',command=emptyfunction,ID='slider',layer=1,roundedcorners=0,menuexceptions=[],
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=True,scalex=True,scaley=True,
                 runcommandat=1,col=-1,backingcol=-1,button='default',
                 dragable=True,colorkey=(255,255,255),backingdraw=True,borderdraw=True,
                 slidersize=-1,increment=0,sliderroundedcorners=-1,minp=0,startp=0,direction='horizontal',containedslider=False):

        obj = SLIDER(self,x,y,width,height,menu,ID,layer,roundedcorners,menuexceptions,
                 anchor,objanchor,center,centery,
                 border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,
                 command=command,runcommandat=runcommandat,col=col,backingcol=backingcol,
                 dragable=dragable,colorkey=colorkey,backingdraw=backingdraw,borderdraw=borderdraw,
                 slidersize=slidersize,increment=increment,sliderroundedcorners=sliderroundedcorners,minp=minp,maxp=maxp,startp=startp,direction=direction,containedslider=containedslider,data=button)

        return obj

##    def makewindowedmenu(self,x,y,width,height,menu,behindmenu,edgebound=(1,0,0,1),col='default',isolated=True,roundedcorners=0,darken=60,colourkey=(243,244,242),ID='default'):
    def makewindowedmenu(self,x,y,width,height,menu,behindmenu='main',col=-1,
                 dragable=False,colorkey=(255,255,255),isolated=True,darken=60,ID='windowedmenu',layer=1,roundedcorners=0,
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,
                 scalesize=True,scalex=True,scaley=True,command=emptyfunction,runcommandat=0):

        if col == -1: col = [max([0,a-35]) for a in self.defaultcol]

        obj = WINDOWEDMENU(self,x,y,width,height,menu,ID,layer,roundedcorners,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,
                 scalesize=scalesize,scalex=scalex,scaley=scaley,
                 command=emptyfunction,runcommandat=runcommandat,col=col,
                 dragable=dragable,colorkey=colorkey,
                 behindmenu=behindmenu,isolated=isolated,darken=darken)
        self.windowedmenunames = [a.menu for a in self.windowedmenus]
    def makerect(self,x,y,width,height,command=emptyfunction,menu='main',ID='button',layer=1,roundedcorners=0,menuexceptions=[],
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,
                 border=-1,scalesize=True,scalex=True,scaley=True,
                 runcommandat=0,col=-1,dragable=False):
        obj = RECT(self,x,y,command=emptyfunction,menu=menu,ID=ID ,layer=layer,roundedcorners=roundedcorners,menuexceptions=menuexceptions,width=width,height=height,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,
                 border=border,scalesize=scalesize,scalex=scalex,scaley=scaley,
                 runcommandat=runcommandat,col=col,dragable=dragable)
        return obj
    def makecircle(self,x,y,radius,command=emptyfunction,menu='main',ID='button',layer=1,roundedcorners=-1,menuexceptions=[],
                 anchor=(0,0),objanchor=(0,0),center=True,centery=-1,
                 border=-1,scalesize=True,scalex=True,scaley=True,
                 runcommandat=0,col=-1,dragable=False):
        if roundedcorners==-1: roundedcorners=radius
        self.makerect(x,y,radius*2,radius*2,command,menu,ID ,layer,roundedcorners,menuexceptions,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,
                 border=border,scalesize=scalesize,scalex=scalex,scaley=scaley,
                 runcommandat=runcommandat,col=col,dragable=dragable)
    def animate(self):
        self.queuedmenumove[0]-=1
        if self.queuedmenumove[0]<0 and self.queuedmenumove[1] != []:
            if self.queuedmenumove[1][0] == 'move': self.movemenu(self.queuedmenumove[1][1],self.queuedmenumove[1][2],self.queuedmenumove[1][3])
            else: self.menuback(self.queuedmenumove[1][1],self.queuedmenumove[1][2])
            self.queuedmenumove[1] = []
        delete = []
        for a in self.animations:
            if a.animate(self):
                delete.append(a.ID)
        for a in delete:
            self.delete(a)
    def makeanimation(self,animateID,startpos,endpos,movetype='linear',length='default',command=emptyfunction,runcommandat=-1,queued=True,menu=False,relativemove=False,skiptoscreen=False,acceleration=1,ID='default'):
        if length == 'default':
            length = self.defaultanimationspeed
        if menu:
            for a in self.items:
                if ((a.menu == animateID) or (type(a) == WINDOWEDMENU and a.behindmenu == animateID)):
                    if not(a.ontable or a.ontextbox or a.onslider):
                        self.makeanimation(a.ID,startpos,endpos,movetype,length,command,runcommandat,queued,False,relativemove,skiptoscreen,acceleration)
                        runcommandat = -1
        else:
            if ID == 'default':
                ID = 'animation '+animateID
            wait = 1
            if not queued:
                tofinish = []
                for a in self.animations:
                    if a.animateID == animateID:
                        tofinish.append([a.ID,a.wait])
                tofinish.sort(key=lambda x: x[0],reverse=False)
                for a in tofinish:
                    self.IDs[a[0]].finish(self,True)
                    self.delete(a[0])
            else:
                for a in self.animations:
                    if a.animateID == animateID:
                        wait = max([a.wait+a.length,wait])
            obj = ANIMATION(animateID,startpos,endpos,movetype,length,wait,relativemove,command,runcommandat,skiptoscreen,acceleration,ID)
            self.addid(ID,obj)
        
                
    def movemenu(self,moveto,slide='none',length='default',backchainadd=True):
        if length == 'default':
            length = self.defaultanimationspeed
        if self.queuedmenumove[0]<0 or slide=='none':
            if (self.activemenu in self.windowedmenunames) and (moveto == self.activemenu) and (self.queuedmenumove[0]<0):
                self.menuback(slide+' flip',length)
            else:
                if backchainadd:
                    self.backchain.append([self.activemenu,slide])
                if slide=='none':
                    self.activemenu = moveto
                else:
                    self.slidemenu(self.activemenu,moveto,slide,length)
            for a in self.mouseheld:
                a[1]-=1
        else:
            self.queuedmenumove[1] = ['move',moveto,slide,length]
    def menuback(self,slide='none',length='default'):
        if length == 'default':
            length = self.defaultanimationspeed
        if self.queuedmenumove[0]<0 or slide=='none':
            if len(self.backchain)>0:
                if slide=='none' and self.backchain[-1][1] != 'none':
                    slide = self.backchain[-1][1]+' flip'
                if slide=='none':
                    self.activemenu = self.backchain[-1][0]
                else:
                    self.slidemenu(self.activemenu,self.backchain[-1][0],slide,length) 
                del self.backchain[-1]
            elif self.backquits and self.queuedmenumove[0]<0:
                self.exit = True
            for a in self.mouseheld:
                a[1]-=1
        else:
            self.queuedmenumove[1] = ['back',slide,length]
    def slidemenu(self,menufrom,menuto,slide,length):
        self.queuedmenumove[0] = length*30
        dirr = [0,0]
        if 'left' in slide: dirr[0]-=self.screenw/self.scale
        if 'right' in slide: dirr[0]+=self.screenw/self.scale
        if 'up' in slide: dirr[1]-=self.screenh/self.scale
        if 'down' in slide: dirr[1]+=self.screenh/self.scale
        if 'flip' in slide: dirr = [dirr[0]*-1,dirr[1]*-1]
        if menufrom in self.windowedmenunames:
            if menuto == self.windowedmenus[self.windowedmenunames.index(menufrom)].behindmenu:
                self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].ID,'current',dirr,'sinout',length,command=lambda: self.movemenu(menuto,backchainadd=False),runcommandat=length,queued=False,relativemove=True,skiptoscreen=True)
                self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].ID,'current',[dirr[0]*-1,dirr[1]*-1],'linear',1,command=self.finishmenumove,runcommandat=1,queued=True,relativemove=True)
            else:
                self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].behindmenu,'current',dirr,'sinout',length,command=lambda: self.slidemenuin(menuto,length,dirr),runcommandat=length,queued=False,menu=True,relativemove=True)
                self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].behindmenu,'current',[dirr[0]*-1,dirr[1]*-1],'linear',1,menu=True,relativemove=True)
        elif menuto in self.windowedmenunames:
            if menufrom == self.windowedmenus[self.windowedmenunames.index(menuto)].behindmenu:
                self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menuto)].ID,[dirr[0]*-1,dirr[1]*-1],'current','sinin',length,command=self.finishmenumove,runcommandat=length,queued=True,relativemove=True,skiptoscreen=True)
                self.movemenu(menuto,backchainadd=False)
            else:
                self.makeanimation(menufrom,'current',dirr,'sinout',length,command=lambda: self.slidemenuin(self.windowedmenus[self.windowedmenunames.index(menuto)].behindmenu,length,dirr,menuto),runcommandat=length,queued=False,menu=True,relativemove=True)
                self.makeanimation(menufrom,'current',[dirr[0]*-1,dirr[1]*-1],'linear',1,menu=True,relativemove=True)   
        else:
            self.makeanimation(menufrom,'current',dirr,'sinout',length,command=lambda: self.slidemenuin(menuto,length,dirr),runcommandat=length,queued=False,menu=True,relativemove=True)
            self.makeanimation(menufrom,'current',[dirr[0]*-1,dirr[1]*-1],'linear',1,menu=True,relativemove=True)
    def slidemenuin(self,moveto,length,dirr,realmenuto=0):
        self.makeanimation(moveto,[dirr[0]*-1,dirr[1]*-1],'current','sinin',length,command=self.finishmenumove,runcommandat=length,queued=True,menu=True,relativemove=True)
        if realmenuto != 0: moveto=realmenuto
        self.movemenu(moveto,backchainadd=False)
    def finishmenumove(self):
        self.queuedmenumove[0] = -1

    def delete(self,ID,failmessage=True):
        try:
            if type(self.IDs[ID]) == BUTTON: self.buttons.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == TEXTBOX:
                self.delete(self.IDs[ID].scroller.ID)
                self.textboxes.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == TABLE:
                for a in self.IDs[ID].tableimages:
                    for b in a:
                        self.delete(b[1].ID)
                self.tables.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == TEXT: self.texts.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == SCROLLER: self.scrollers.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == SLIDER:
                self.delete(self.IDs[ID].button.ID)
                self.sliders.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == ANIMATION: self.animations.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == RECT: self.rects.append(self.IDs[ID])
            del self.IDs[ID]
            self.refreshitems()
            return True
        except:
            if failmessage: print('failed to delete object:',ID)
            return False
    def onmenu(self,menu):
        lis = []
        for b in self.items:
            if b.menu == menu:
                lis.append(b)
        return lis

                 
class GUI_ITEM:
    def __init__(self,ui,x,y,width,height,menu='main',ID='',layer=1,roundedcorners=0,menuexceptions=[],
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,text='',textsize=50,img='none',font='default',bold=False,antialiasing=True,pregenerated=True,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=True,scalex=True,scaley=True,
                 command=emptyfunction,runcommandat=0,col=-1,textcol=-1,backingcol=-1,hovercol=-1,clickdownsize=4,clicktype=0,textoffsetx=0,textoffsety=0,maxwidth=-1,
                 dragable=False,colorkey=(255,255,255),toggle=True,toggleable=False,toggletext=-1,toggleimg='none',togglecol=-1,togglehovercol=-1,bindtoggle=[],spacing=-1,verticalspacing=0,horizontalspacing=8,
                 lines=1,linelimit=100,selectcol=-1,selectbordersize=2,selectshrinksize=0,cursorsize=-1,textcenter=True,chrlimit=10000,numsonly=False,enterreturns=False,commandifenter=True,commandifkey=False,
                 data='empty',titles=[],boxwidth=-1,boxheight=-1,linesize=2,datatable=[],
                 backingdraw=True,borderdraw=True,animationspeed=5,scrollercol=-1,scrollerwidth=-1,pageheight=15,
                 slidercol=-1,sliderbordercol=-1,slidersize=-1,increment=0,sliderroundedcorners=-1,minp=0,maxp=100,startp=0,direction='horizontal',containedslider=False,
                 behindmenu='main',isolated=True,darken=60):
        self.center = center
        if centery == -1: centery = center
        self.centery = centery
        self.x = x
        self.y = y
        self.startx = x
        self.starty = y
        self.startanchor = list(anchor)
        self.startobjanchor = list(objanchor)
        if self.center and self.startobjanchor[0] == 0: self.startobjanchor[0]='w/2'
        if self.centery and self.startobjanchor[1] == 0: self.startobjanchor[1]='h/2'

        self.width = width
        self.height = height
        self.roundedcorners = roundedcorners
        self.scalesize = scalesize
        self.scalex = scalex
        self.scaley = scaley

        self.border = border
        if upperborder == -1: upperborder = border
        if lowerborder == -1: lowerborder = border
        if leftborder == -1: leftborder = border
        if rightborder == -1: rightborder = border
        self.upperborder = upperborder
        self.lowerborder = lowerborder
        self.leftborder = leftborder
        self.rightborder = rightborder

        self.menu = menu
        self.menuexceptions = menuexceptions
        self.layer = layer
        if ID == '': ID = text
        ui.addid(ID,self)

        self.text = text
        self.textsize = textsize
        self.img = img
        if font == 'default': font = ui.defaultfont
        self.font = font
        self.bold = bold
        self.antialiasing = antialiasing
        self.pregenerated = pregenerated
        self.textcenter = textcenter
        self.maxwidth = maxwidth

        self.col = autoshiftcol(col,ui.defaultcol)
        self.textcol = autoshiftcol(textcol,ui.defaulttextcol)
        self.backingcol = autoshiftcol(backingcol,self.col,20)
        self.bordercol = self.backingcol
        self.hovercol = autoshiftcol(hovercol,self.col,-20)
        self.togglecol = autoshiftcol(togglecol,self.col,-50)
        self.togglehovercol = autoshiftcol(togglehovercol,self.togglecol,-20)
        self.selectcol = autoshiftcol(selectcol,self.col,20)
        self.scrollercol = autoshiftcol(scrollercol,self.col,-30)
        self.slidercol = autoshiftcol(slidercol,self.col,-30)
        self.sliderbordercol = autoshiftcol(sliderbordercol,self.col,-10)
        self.colorkey = colorkey
        
        self.clickdownsize = clickdownsize
        self.textoffsetx = textoffsetx
        self.textoffsety = textoffsety
        self.dragable = dragable
        self.spacing = spacing
        self.verticalspacing = verticalspacing
        self.horizontalspacing = horizontalspacing
        if spacing!=-1:
            if verticalspacing == 0:self.verticalspacing = spacing
            if horizontalspacing == 8:self.horizontalspacing = spacing

        self.toggle = toggle
        self.toggleable = toggleable
        if toggletext == -1: toggletext = text
        self.toggletext = toggletext
        if toggleimg == -1: toggleimg = img
        self.toggleimg = toggleimg
        self.bindtoggle = bindtoggle
        
        self.clicktype = clicktype
        self.holding = False
        self.hovering = False
        self.animating = False
        self.animationspeed = animationspeed
        self.animate = 0
        self.currentframe = 0
        self.command = command
        self.runcommandat = runcommandat

        self.lines = lines
        self.linelimit = linelimit
        self.selectbordersize = selectbordersize
        self.selectshrinksize = selectshrinksize
        self.cursorsize = cursorsize
        self.chrlimit = chrlimit
        self.numsonly = numsonly
        self.enterreturns = enterreturns
        self.commandifenter = commandifenter
        self.commandifkey = commandifkey

        self.data = data
        self.titles = titles
        self.datatable = datatable
        self.linesize = linesize
        self.boxwidth = boxwidth
        self.boxheight = boxheight
        self.ontable = False
        self.onslider = False
        self.ontextbox = False

        self.backingdraw = backingdraw
        self.borderdraw = borderdraw
        self.scrollerwidth = scrollerwidth
        self.pageheight = pageheight

        self.minp = minp
        self.maxp = maxp
        self.startp = startp
        self.increment = increment
        self.containedslider = containedslider
        if slidersize == -1:
            self.slidersize = self.height*2
            if self.containedslider: self.slidersize = self.height-self.upperborder-self.lowerborder
            if direction == 'vertical':
                self.slidersize = self.width*2
                if self.containedslider: self.slidersize = self.width-self.leftborder-self.rightborder
        else:
            self.slidersize = slidersize
        if sliderroundedcorners == -1: sliderroundedcorners = roundedcorners
        self.sliderroundedcorners = sliderroundedcorners
        self.direction = direction
        self.containedslider = containedslider

        self.behindmenu = behindmenu
        self.isolated = isolated
        self.darken = darken
        
        self.reset(ui)
        
    def reset(self,ui):
        self.refreshscale(ui)
        self.autoscale(ui)
        self.refreshcords(ui)
        self.resetcords(ui)
        self.refresh(ui)
        
    def refresh(self,ui):
        self.refreshscale(ui)
        self.gentext(ui)
        self.refreshcords(ui)
    def gentext(self,ui):
        if type(self.img) != list: imgs = [self.img]
        else: imgs = self.img

        self.textimages = []
        for img in imgs:
            if type(img) == str:
                if len(imgs)!=1: txt = img
                else: txt = self.text
                self.textimages.append(ui.rendertextlined(txt,self.textsize,self.textcol,self.col,self.font,self.maxwidth,self.bold,self.antialiasing,True,imgin=True,img=img,scale=self.scale,linelimit=self.linelimit))
            else:
                self.textimages.append(pygame.transform.scale(img,(img.get_width()*(self.textsize/img.get_height())*self.scale,img.get_height()*(self.textsize/img.get_height())*self.scale)))
                self.textimages[-1].set_colorkey(self.colorkey)
        self.textimage = self.textimages[0]
        if len(self.textimages) != 1:
            self.animating = True
        self.child_gentext(ui)
    def animatetext(self,ui):
        if self.animating:
            self.animate+=1
            if self.animate%self.animationspeed == 0:
                self.currentframe+=1
                if self.currentframe == len(self.textimages):
                    self.currentframe = 0
                self.textimage = self.textimages[self.currentframe]
    def resetcords(self,ui,scalereset=True):
        if scalereset: self.refreshscale(ui)
        self.anchor = self.startanchor[:]
        global returnedexecvalue
        if type(self.anchor[0]) == str:
            exec('returnedexecvalue='+self.anchor[0].replace('w',str(ui.screenw)),globals())
            self.anchor[0] = returnedexecvalue
        if type(self.anchor[1]) == str:
            exec('returnedexecvalue='+self.anchor[1].replace('h',str(ui.screenh)),globals())
            self.anchor[1] = returnedexecvalue
            
        self.objanchor = self.startobjanchor[:]
        if type(self.objanchor[0]) == str:
            exec('returnedexecvalue='+self.objanchor[0].replace('w',str(self.width)),globals())
            self.objanchor[0] = returnedexecvalue
        if type(self.objanchor[1]) == str:
            exec('returnedexecvalue='+self.objanchor[1].replace('h',str(self.height)),globals())
            self.objanchor[1] = returnedexecvalue
        self.x = int(self.anchor[0]+self.startx*self.scale-self.objanchor[0]*self.scale)/self.dirscale[0]
        self.y = int(self.anchor[1]+self.starty*self.scale-self.objanchor[1]*self.scale)/self.dirscale[1]
        self.refreshcords(ui)

    def refreshcords(self,ui):
        self.refreshscale(ui)
        self.child_refreshcords(ui)
        self.centerx = self.x+self.width/2
        self.centery = self.y+self.height/2
        
    def refreshscale(self,ui):
        self.scale = ui.scale
        self.dirscale = ui.dirscale[:]
        if not self.scalesize: self.scale = 1
        if not self.scalex: self.dirscale[0] = 1
        if not self.scaley: self.dirscale[1] = 1
    def autoscale(self,_):
        pass
    def child_gentext(self,_):
        pass
    def child_refreshcords(self,_):
        pass
    def getclickedon(self,ui,rect='default',runcom=True,drag=True):
        if rect == 'default':
            rect = pygame.Rect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale)
        self.clickedon = -1
        self.hovering = False
        mpos = [ui.mpos[0]*ui.scale,ui.mpos[1]*ui.scale]
        if rect.collidepoint(mpos):
            if ui.mprs[self.clicktype] and (ui.mouseheld[self.clicktype][1]>0 or self.holding):
                if ui.mouseheld[self.clicktype][1] == ui.buttondowntimer:
                    self.clickedon = 0
                    self.holding = True
                    self.holdingcords = [(mpos[0])-rect.x,(mpos[1])-rect.y]
                    if self.runcommandat<2 and runcom:
                        if self.toggleable:
                            if self.toggle: self.toggle = False
                            else: self.toggle = True
                        self.command()
            else:
                self.hovering = True
        if ui.mprs[self.clicktype] and self.holding:
            if self.clickedon!=0:
                self.clickedon = 1
            if self.dragable and drag:
                self.x = (mpos[0]-self.holdingcords[0])/self.dirscale[0]
                self.y = (mpos[1]-self.holdingcords[1])/self.dirscale[1]
                self.centerx = self.x+self.width/2
                self.centery = self.y+self.height/2
            if self.runcommandat == 1 and runcom:
                self.command()
        elif not ui.mprs[self.clicktype]:
            if self.holding:
                self.clickedon = 2
                if rect.collidepoint(mpos) and self.runcommandat>0 and runcom:
                    if self.toggleable and self.runcommandat!=1:
                        if self.toggle: self.toggle = False
                        else: self.toggle = True
                    self.command()
            self.holding = False
        return False


##x,y,width,height,menu,menuexceptions,pointbound,center,centery,col,textcol,backingcol,layer,ID
##
##
##button = x,y,text,textsize,command,menu,menuexceptions,edgebound,col,bordercol,hovercol,textcol,img,colorkey,runcommandat,width,height,border,clickdownsize,roundedcorners,clicktype,textoffsetx,textoffsety,toggle,togglecol,togglehovercol,toggleable,bindtoggle,drawifoff,dragable,font,bold,layer,ID,ui
##textbox = ,x,y,width,height,border,titleheight,roundedcorners,title,titlecenter,titlesize,titlecol,titlefont,titlebold,backingcol,textcenter,textsize,textcol,textbackingcol,upperborder,lowerborder,rightborder,leftborder,chrlimit,numsonly,enterreturns,command,commandifenter,commandifkey,selectcol,selectbordersize,selectshrinksize,cursorsize,menu,menuexceptions,edgebound,clicktype,titleimage,textoffsetx,textoffsety,font,bold,layer,ID,ui
##table = x,y,rows,colomns,data,titles,boxwidths,boxheight,spacing,menu,menuexceptions,edgebound,boxcol,boxtextcol,boxtextsize,boxcenter,boxfont,boxbold,titlefont,titlebold,titleboxcol,titletextcol,titletextsize,titlecenter,linesize,linecol,roundedcorners,layer,ID,ui
##text = x,y,text,size,menu,menuexceptions,edgebound,col,center,font,bold,maxwidth,backingborder,backingcol,backingdraw,backingwidth,backingheight,img,colorkey,roundedcorners,antialiasing,pregenerated,layer,ID,ui
##scroller = x,y,menu,menuexceptions,edgebound,command,width,height,col,scrollercol,hovercol,clickcol,scrollerwidth,minh,maxh,pageh,starth,runcommandat,clicktype,layer,ID,ui
##slider = x,y,width,height,menu,menuexceptions,edgebound,command,col,bordercol,slidercol,sliderbordercol,hovercol,clickdownsize,border,slidersize,increment,roundedcorners,barroundedcorners,img,colorkey,minp,maxp,startp,dragable,runcommandat,clicktype,layer,ID,ui
##windowedmenu = menu,behindmenu,x,y,width,height,col,roundedcorners,colorkey,isolated,darken,edgebound,ID
    
class BUTTON(GUI_ITEM):
    def refresh(self,ui):
        if not self.ontable:
            self.refreshcords(ui)
        self.gentext(ui)
    def child_gentext(self,ui):
        if (self.img != self.toggleimg) or (self.text != self.toggletext):
            if type(self.img) != list: imgs = [self.toggleimg]
            else: imgs = self.toggleimg
            
            self.toggletextimages = []
            for img in imgs:
                if type(img) == str:
                    if len(imgs)!=1: txt = img
                    else: txt = self.toggletext
                    self.toggletextimages.append(ui.rendertextlined(self.toggletext,self.textsize,self.textcol,self.togglecol,self.font,self.maxwidth,self.bold,True,imgin=True,img=self.toggleimg,scale=self.scale,linelimit=self.linelimit))
                else:
                    self.toggletextimages.append(pygame.transform.scale(img,(self.textsize,img.get_width()*self.textsize/img.get_height())))
                    self.toggletextimages[-1].set_colorkey(self.colorkey)
            self.toggletextimage = self.toggletextimages[0]
            if len(self.toggletextimages) != 1:
                self.animating = True
        else:
            self.toggletextimages = self.textimages
            self.toggletextimage = self.toggletextimages[0]
        
    def autoscale(self,ui):
        self.gentext(ui)
        imgsizes = [a.get_size() for a in self.textimages]+[a.get_size() for a in self.toggletextimages]
        if self.width == -1:
            self.width = max([a[0] for a in imgsizes])/ui.scale+self.horizontalspacing*2+self.leftborder+self.rightborder
        if self.height == -1:
            self.height = max([a[1] for a in imgsizes])/ui.scale+self.verticalspacing*2+self.upperborder+self.lowerborder
    def child_refreshcords(self,ui):
        self.colliderect = pygame.Rect(self.x+self.leftborder,self.y+self.upperborder,self.width-self.leftborder-self.rightborder,self.height-self.upperborder-self.lowerborder)
    def render(self,screen,ui):
        self.animatetext(ui)
        self.innerrect = pygame.Rect(self.x*self.dirscale[0]+(self.leftborder+self.clickdownsize*self.holding)*self.scale,self.y*self.dirscale[1]+(self.upperborder+self.clickdownsize*self.holding)*self.scale,(self.width-self.leftborder-self.rightborder-self.clickdownsize*self.holding*2)*self.scale,(self.height-self.upperborder-self.lowerborder-self.clickdownsize*self.holding*2)*self.scale)
        self.getclickedon(ui,self.innerrect)
        if self.clickedon > -1:
            if self.clickedon == 0: ui.mouseheld[self.clicktype][1]-=1
            for a in self.bindtoggle:
                if a!=self.ID:
                    ui.IDs[a].toggle = False
        if not self.onslider:
            self.draw(screen,ui)
    def draw(self,screen,ui):
        col = self.col
        if not self.toggle: col = self.togglecol
        innerrect = roundrect(self.x*self.dirscale[0]+(self.leftborder+self.clickdownsize*self.holding)*self.scale,self.y*self.dirscale[1]+(self.upperborder+self.clickdownsize*self.holding)*self.scale,(self.width-self.leftborder-self.rightborder-self.clickdownsize*self.holding*2)*self.scale,(self.height-self.upperborder-self.lowerborder-self.clickdownsize*self.holding*2)*self.scale)
        if self.holding or self.hovering:
            if not self.toggle: col = self.togglehovercol
            else: col = self.hovercol
        if self.borderdraw:
            if self.backingdraw: pygame.draw.rect(screen,self.backingcol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
            else: pygame.draw.rect(screen,self.backingcol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),int((self.border+self.clickdownsize*self.holding)*self.scale),border_radius=int(self.roundedcorners*self.scale))
        if self.backingdraw: pygame.draw.rect(screen,col,innerrect,border_radius=int((self.roundedcorners-self.border)*self.scale))
        if self.toggle:
            screen.blit(self.textimage,(self.x*self.dirscale[0]+((self.width-self.leftborder-self.rightborder)/2+self.leftborder+self.textoffsetx)*self.scale-self.textimage.get_width()/2,self.y*self.dirscale[1]+((self.height-self.upperborder-self.lowerborder)/2+self.upperborder+self.textoffsety)*self.scale-self.textimage.get_height()/2))
        else:
            screen.blit(self.toggletextimage,(self.x*self.dirscale[0]+((self.width-self.leftborder-self.rightborder)/2+self.leftborder+self.textoffsetx)*self.scale-self.toggletextimage.get_width()/2,self.y*self.dirscale[1]+((self.height-self.upperborder-self.lowerborder)/2+self.upperborder+self.textoffsety)*self.scale-self.toggletextimage.get_height()/2))

class TEXTBOX(GUI_ITEM):
    def reset(self,ui):
        self.setvars()
        self.autoscale(ui)
        self.resetcords(ui)
        self.resetscroller(ui)
        self.refreshscale(ui)
        self.gentext(ui,False)
        self.refreshcursor()
        self.refreshscroller(ui)
        self.refreshcords(ui)
        self.resetcords(ui)
    def setvars(self):
        self.scroller=0
        self.selected = False
        self.textselected = [False,0,0]
        self.clickstartedinbound = False
        self.typingcursor=0
        self.typeline=0
        self.scrolleron=False
    def autoscale(self,ui):
        heightgetter = ui.rendertext('Tg',self.textsize,self.textcol,self.font,self.bold)
        if self.height == -1:
            self.height = self.upperborder+self.lowerborder+heightgetter.get_height()*self.lines
        if self.cursorsize == -1:
            self.cursorsize = ui.gettextsize('Tg',self.font,self.textsize,self.bold)[1]-2
    def inputkey(self,caps,event,kprs,ui):
        if kprs[pygame.K_LSHIFT] or kprs[pygame.K_RSHIFT]:
            if caps: caps = False
            else: caps = True
        if kprs[pygame.K_LCTRL] or kprs[pygame.K_RCTRL]: ctrl = True
        else: ctrl = False
        if self.textselected[1]>self.textselected[2]:
            temp = self.textselected[1]
            self.textselected[1] = self.textselected[2]
            self.textselected[2] = temp
        item = ''
        backspace = False
        delete = False
        esc = False
        enter = False
        unicodechrs = '''#',-./0123456789;=[\]`'''
        shiftunicodechrs = '''~@<_>?)!"£$%^&*(:+{|}¬'''
        if event.key>32 and event.key<127:
            if ctrl:
                if chr(event.key) == 'a':
                    self.textselected = [True,0,len(self.chrcorddata)]
                elif chr(event.key) == 'c':
                    pygame.scrap.put(pygame.SCRAP_TEXT,self.text.encode())
                    ui.clipboard = self.text[self.textselected[1]:self.textselected[2]]
                elif chr(event.key) == 'v':
                    self.clipboard = str(pygame.scrap.get(pygame.SCRAP_TEXT).decode('utf-8'))
                    self.clipboard = self.clipboard.strip('\x00')
                    item = ui.clipboard
                    if item == None: item = ''
            else:
                if (event.key>96 and event.key<123):
                    if caps: item = chr(event.key-32)
                    else: item = chr(event.key)
                elif chr(event.key) in unicodechrs:
                    if not (kprs[pygame.K_LSHIFT] or kprs[pygame.K_RSHIFT]): item = chr(event.key)
                    else: item = shiftunicodechrs[list(unicodechrs).index(chr(event.key))]
        elif event.key == pygame.K_BACKSPACE: backspace = True
        elif event.key == pygame.K_DELETE: delete = True
        elif event.key == pygame.K_ESCAPE: self.selected = False
        elif event.key == pygame.K_RETURN:
            if self.enterreturns: item = '\n'
            if self.commandifenter: self.command()
        elif event.key == pygame.K_SPACE: item = ' '
        elif event.key == pygame.K_LEFT:
            if self.typingcursor>-1: self.typingcursor-=1
        elif event.key == pygame.K_RIGHT:
            if self.typingcursor<len(self.chrcorddata)-1: self.typingcursor+=1
        elif event.key == pygame.K_UP:
            self.typingcursor = self.findclickloc(relativempos=[self.linecenter[0],self.linecenter[1]-self.cursorsize])
        elif event.key == pygame.K_DOWN:
            self.typingcursor = self.findclickloc(relativempos=[self.linecenter[0],self.linecenter[1]+self.cursorsize])
        
        if not(self.textselected[0] and self.textselected[1]!=self.textselected[2]):
            if item != '':
                try:
                    temp = int(item)
                    num=True
                except:
                    num=False
                if (not(self.numsonly) or num):
                    self.text = self.text[:self.typingcursor+1]+item+self.text[self.typingcursor+1:]
                    self.typingcursor+=len(item)
            if backspace:
                if self.typingcursor>-1:
                    self.typingcursor-=1
                if self.text[self.typingcursor:self.typingcursor+2] == '\n':
                    self.text = self.text[:self.typingcursor]+self.text[self.typingcursor+2:]
                    self.typingcursor-=1
                else: self.text = self.text[:self.typingcursor+1]+self.text[self.typingcursor+2:]
            elif delete:
                if self.text[self.typingcursor:self.typingcursor+2] == '\n':
                    self.text = self.text[:self.typingcursor]+self.text[self.typingcursor+2:]
                else: self.text = self.text[:self.typingcursor+1]+self.text[self.typingcursor+2:]
            if self.commandifkey and (item != '' or backspace or delete):
                self.command()
        else:
            if backspace or delete or item != '':
                self.text = self.text[:self.textselected[1]]+item+self.text[self.textselected[2]:]
                self.typingcursor = self.textselected[1]-1+len(item)
                self.textselected = [False,0,0]
        if self.text[self.chrlimit-1:self.chrlimit+1] == '\n':
            self.text = self.text[:self.chrlimit-1]
        else:
            self.text = self.text[:self.chrlimit]
        self.refresh(ui)
    def resetscroller(self,ui):
        self.scroll = 0
        if self.scroller != 0:
            ui.delete(self.scroller.ID,False)
        self.scroller = ui.makescroller(self.x+self.width-15-self.rightborder/2,self.y+self.upperborder,self.height-self.upperborder-self.lowerborder,emptyfunction,15,0,self.height-self.upperborder-self.lowerborder,self.height,menu=self.menu,roundedcorners=self.roundedcorners,col=self.col)
        self.scroller.ontextbox = True
        self.scroller.layer = self.layer+0.01
        self.scrolleron = False
        
    def refresh(self,ui):
        self.refreshscale(ui)
        self.gentext(ui)
        self.refreshcursor()
        self.refreshscroller(ui)
        
        self.scroller.maxp = self.textimage.get_height()/self.scale+self.upperborder+self.lowerborder
        self.scroller.refresh(ui)
        if (self.scroller.maxp-self.scroller.minp)>self.scroller.pageheight:
            self.scrolleron = True
            if self.scroller.scroll>self.scroller.maxp-self.scroller.pageheight:
                self.scroller.scroll = self.scroller.maxp-self.scroller.pageheight
        else:
            self.scrolleron = False
        self.scroller.refresh(ui)
        self.refreshcords(ui)
           
    def gentext(self,ui,refcurse=True):
        self.textimage,self.chrcorddatalined = ui.rendertextlined(self.text,self.textsize,self.textcol,self.col,self.font,self.width-self.horizontalspacing*2-self.leftborder-self.rightborder-self.scrolleron*self.scroller.width,self.bold,center=self.textcenter,scale=self.scale,linelimit=self.linelimit,getcords=True)
        for l in self.chrcorddatalined:
            for a in l:
                a[1] = (a[1][0]/self.scale,a[1][1]/self.scale)
                a[2] = (a[2][0]/self.scale,a[2][1]/self.scale)
        self.chrcorddata = []
        for a in self.chrcorddatalined:
            self.chrcorddata+=a
        self.textimagerect = self.textimage.get_rect()
        self.textimagerect.width/=ui.scale
        self.textimagerect.height/=ui.scale
        if refcurse: self.refreshcursor()
      
    def refreshcursor(self):
        if self.typingcursor>len(self.chrcorddata)-1: self.typingcursor=len(self.chrcorddata)-1
        elif self.typingcursor<-1: self.typingcursor = -1
        if self.typingcursor != -1: self.linecenter = [self.chrcorddata[self.typingcursor][1][0]+self.chrcorddata[self.typingcursor][2][0]/2+self.horizontalspacing,self.chrcorddata[self.typingcursor][1][1]]
        elif len(self.chrcorddata)>0: self.linecenter = [self.chrcorddata[self.typingcursor+1][1][0]-self.chrcorddata[self.typingcursor+1][2][0]/2+self.horizontalspacing,self.chrcorddata[self.typingcursor+1][1][1]]
        else:
            if self.textcenter: self.linecenter = [self.width/2-self.leftborder,self.textsize*0.3]
            else: self.linecenter = [self.horizontalspacing,self.textsize*0.3]
    def refreshscroller(self,ui):
        inc = 0
        if self.linecenter[1]-self.scroller.scroll>self.height-self.upperborder-self.lowerborder:
            inc = self.textsize
        if self.linecenter[1]-self.scroller.scroll<0:
            inc = -self.textsize
        count = 0
        while inc!=0:
            self.scroller.scroll+=inc
            count+=1
            if not(self.linecenter[1]-self.scroller.scroll<0 or self.linecenter[1]-self.scroller.scroll>self.height-self.upperborder-self.lowerborder):
                inc = 0
            if count>20:
                break
        if self.scrolleron:
            self.scroller.limitpos(ui)
        else:
            self.scroller.scroll = self.scroller.minp
    def child_refreshcords(self,ui):
        if self.scroller != 0:
            self.rect = roundrect(self.x,self.y,self.width,self.height)
            self.innerrect = roundrect(self.x+self.leftborder,self.y+self.upperborder,self.width-self.rightborder-self.leftborder-self.scrolleron*self.scroller.width,self.height-self.upperborder-self.lowerborder)
            self.textimagerect = self.textimage.get_rect()     
            if self.textcenter:
                self.textimagerect.x = (self.width-self.horizontalspacing*2-self.scrolleron*self.scroller.width-self.leftborder-self.rightborder)/2+self.textoffsetx+self.horizontalspacing-self.textimagerect.width/2/self.scale
                self.textimagerect.y = self.verticalspacing+self.textimagerect.height/2+self.textoffsety-self.textimagerect.height/2
            else:
                self.textimagerect.x = self.textoffsetx+self.horizontalspacing
                self.textimagerect.y = self.textoffsety+self.verticalspacing
            
    def render(self,screen,ui):
        self.typeline+=1
        self.selectrect = roundrect(self.x*self.dirscale[0]+(self.leftborder-self.selectbordersize)*self.scale,self.y*self.dirscale[1]+(self.upperborder-self.selectbordersize)*self.scale,(self.width-(self.leftborder+self.rightborder)+self.selectbordersize*2-self.scrolleron*self.scroller.width)*self.scale,(self.height-(self.upperborder+self.lowerborder)+self.selectbordersize*2)*self.scale)
        if self.typeline == 80:
            self.typeline = 0 
        self.getclickedon(ui,self.selectrect,False,False)
        self.draw(screen,ui)
        mpos = [ui.mpos[0]*ui.scale,ui.mpos[1]*ui.scale]
        if self.clickedon == 0:
            self.typingcursor = min([max([self.findclickloc(mpos)+1,0]),len(self.chrcorddata)])-1
            self.textselected[2] = self.typingcursor+1
            if len(self.chrcorddata)!=0: self.textselected[0] = True
            self.textselected[1] = self.typingcursor+1
            self.refreshcursor()
            self.selected = True
            self.clickstartedinbound = True
            ui.selectedtextbox = ui.textboxes.index(self)
        elif self.selected:
            if ui.mprs[self.clicktype] and ui.mouseheld[self.clicktype][1] == ui.buttondowntimer:
                self.clickstartedinbound = False
                self.selected = False
            if not self.selectrect.collidepoint(mpos) and ui.mprs[self.clicktype] and not ui.mouseheld[self.clicktype]:
                self.selected = False
                self.textselected = [False,0,0]

        if ui.mprs[self.clicktype] and ui.mouseheld[self.clicktype][1] != ui.buttondowntimer and self.clickstartedinbound:
            self.textselected[2] = min([max([self.findclickloc(mpos)+1,0]),len(self.chrcorddata)])
            if self.scrolleron:
                if mpos[1]<self.y*self.dirscale[1]+self.upperborder*self.scale:
                    self.scroller.scroll+=(mpos[1]-(self.y*self.dirscale[1]+self.upperborder*self.scale))/10
                    self.scroller.limitpos(ui)
                elif mpos[1]>self.y*self.dirscale[1]+(self.height-self.lowerborder)*self.scale:
                    self.scroller.scroll+=(mpos[1]-(self.y*self.dirscale[1]+(self.height-self.lowerborder)*self.scale))/10
                    self.scroller.limitpos(ui)
        if not ui.mprs[self.clicktype]:
            self.clickstartedinbound = False
        return False
    
    def findclickloc(self,mpos=-1,relativempos=-1):
        if len(self.chrcorddata)==0:
            return -1
        else:
            if relativempos == -1: self.relativempos = ((mpos[0]-(self.x*self.dirscale[0]+(self.leftborder+self.horizontalspacing)*self.scale))/self.scale,(mpos[1]-(self.y*self.dirscale[1]+(self.upperborder+self.verticalspacing-self.scroller.scroll)*self.scale))/self.scale)
            else: self.relativempos = relativempos
            dis = [0,10000]
            for i,a in enumerate(self.chrcorddatalined):
                if len(a) != 0 and abs(a[0][1][1]-self.relativempos[1])<dis[1]:
                    dis[1] = abs(a[0][1][1]-self.relativempos[1])
                    dis[0] = i
            hdis = [0,10000]
            for i,a in enumerate(self.chrcorddatalined[dis[0]]):
                if abs(a[1][0]-self.relativempos[0])<hdis[1]:
                    hdis[1] = abs(a[1][0]-self.relativempos[0])
                    hdis[0] = i
            if hdis[0]>len(self.chrcorddatalined[dis[0]])-1:
                hdis[0] = len(self.chrcorddatalined[dis[0]])-1
                
            strpos = hdis[0]+sum([len(a) for a in self.chrcorddatalined[:max([dis[0],0])]]) 
            if self.relativempos[0]<self.chrcorddatalined[dis[0]][hdis[0]][1][0]:
                strpos-=1
            return strpos
    def draw(self,screen,ui):
        if self.borderdraw:
            pygame.draw.rect(screen,self.backingcol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
        if self.selected: pygame.draw.rect(screen,self.selectcol,self.selectrect,int(self.selectbordersize*self.scale),border_radius=int((self.roundedcorners+self.selectbordersize)*self.scale))

        surf = pygame.Surface(((self.width-self.leftborder-self.rightborder-self.scrolleron*self.scroller.width)*self.scale,(self.height-self.upperborder-self.lowerborder)*self.scale))
        surf.fill((199,77,166))
        pygame.draw.rect(surf,self.col,(0,0,surf.get_width(),surf.get_height()),border_radius=int(self.roundedcorners*self.scale))
        surf.set_colorkey((199,77,166))

        offset = (0,self.scroller.scroll)
        surf.blit(self.textimage,(self.textimagerect.x*self.scale,(self.textimagerect.y-self.scroller.scroll)*self.scale))
        if self.typeline>20 and self.selected:
            pygame.draw.line(surf,self.textcol,((self.linecenter[0])*self.scale,(self.linecenter[1]-self.cursorsize/2+self.verticalspacing-self.scroller.scroll)*self.scale),((self.linecenter[0])*self.scale,(self.linecenter[1]+self.cursorsize/2+self.verticalspacing-self.scroller.scroll)*self.scale),2)
        if self.textselected[0] and self.textselected[1]!=self.textselected[2]:
            trect = [1000000,0,0,0]
            for a in range(min([self.textselected[1],self.textselected[2]]),max([self.textselected[1],self.textselected[2]])):
                if self.chrcorddata[a][0] != '\n':
                    trect[0] = (self.horizontalspacing+self.chrcorddata[a][1][0]-self.chrcorddata[a][2][0]/2)*self.scale
                    trect[1] = (self.verticalspacing+self.chrcorddata[a][1][1]-self.chrcorddata[a][2][1]/2-self.scroller.scroll)*self.scale
                    trect[2] = self.chrcorddata[a][2][0]*self.scale
                    trect[3] = self.chrcorddata[a][2][1]*self.scale
                highlight = pygame.Surface((trect[2],trect[3]))
                highlight.set_alpha(180)
                highlight.fill((51,144,255))
                surf.blit(highlight,(trect[0],trect[1]))
            
        screen.blit(surf,(self.x*self.dirscale[0]+(self.leftborder)*self.scale,self.y*self.dirscale[1]+(self.upperborder)*self.scale))
        
        
                



class TABLE(GUI_ITEM):
    def reset(self,ui):
        self.tableimages=0
        self.refreshscale(ui)
        self.resetcords(ui)
        self.refresh(ui)
        self.resetcords(ui)
    def refresh(self,ui):
        self.refreshscale(ui)
        self.labeldata(ui)
        self.initheightwidth()
        self.gentext(ui)
        self.gettablewidths(ui)
        self.gettableheights(ui)          
        self.refreshcords(ui)

    def labeldata(self,ui):
        self.labeleddata = []
        temp = copy.copy(self.data)
        if len(self.titles)!=0:
            temp.insert(0,copy.copy(self.titles))
        self.rows = len(temp)
        self.columns = max([len(a) for a in temp])
        
        for a in range(len(temp)):
            while len(temp[a])<self.columns:
                temp[a].append('')
        
        for a in temp:
            self.labeleddata.append([])
            for b in a:
                if type(b) == str: self.labeleddata[-1].append(['text',b])
                elif type(b) == int: self.labeleddata[-1].append(['text',str(b)])
                elif type(b) == list: self.labeleddata[-1].append(['text',str(b)])
                elif type(b) == BUTTON: self.labeleddata[-1].append(['button',b])
                elif type(b) == TEXTBOX: self.labeleddata[-1].append(['textbox',b])
                elif type(b) == TEXT: self.labeleddata[-1].append(['textobj',b])
                elif type(b) == pygame.Surface:self.labeleddata[-1].append(['image',b])
                else: print('unrecognised data type in table:',b)
                
    def gentext(self,ui):
        self.tableimages = []
        for a in range(len(self.labeleddata)):
            self.tableimages.append([])
            for i,b in enumerate(self.labeleddata[a]):
                if b[0] == 'text':
                    ui.delete('tabletext'+self.ID+str(a)+str(i),False)
                    obj = ui.maketext(0,0,b[1],self.textsize,self.menu,'tabletext'+self.ID+str(a)+str(i),self.layer+0.01,self.roundedcorners,self.menuexceptions,textcenter=self.textcenter,textcol=self.textcol,font=self.font,bold=self.bold,antialiasing=self.antialiasing,pregenerated=self.pregenerated,maxwidth=self.boxwidth[i],scalesize=self.scalesize,horizontalspacing=self.horizontalspacing,verticalspacing=self.verticalspacing)
                    self.tableimages[-1].append(['textobj',obj])
                elif b[0] == 'button':
                    b[1].scale = self.scale
                    b[1].gentext(ui)
                    self.tableimages[-1].append(['button',b[1]])
                elif b[0] == 'textbox':
                    self.tableimages[-1].append(['textbox',b[1]])
                elif b[0] == 'textobj':
                    self.tableimages[-1].append(['textobj',b[1]])
                elif b[0] == 'image':
                    ui.delete('tabletext'+self.ID+str(a)+str(i),False)
                    obj = ui.maketext(0,0,'',self.textsize,self.menu,'tabletext'+self.ID+str(a)+str(i),self.layer+0.01,self.roundedcorners,self.menuexceptions,textcenter=self.textcenter,img=b[1],maxwidth=self.boxwidth[i],scalesize=self.scalesize,horizontalspacing=self.horizontalspacing,verticalspacing=self.verticalspacing)
                    self.tableimages[-1].append(['textobj',obj]) 
                else:
                    print(b[0])
                    
    def child_refreshcords(self,ui):
        if self.tableimages!=0:
            for a in range(len(self.tableimages)):
                for i,b in enumerate(self.tableimages[a]):
                    b[1].startanchor = [self.x*self.dirscale[0],self.y*self.dirscale[1]]
                    b[1].startobjanchor = [0,0]
                    b[1].startx = (self.linesize*(i+1)+self.boxwidthsinc[i])
                    b[1].starty = (self.linesize*(a+1)+self.boxheightsinc[a])
                    b[1].width = self.boxwidths[i]
                    b[1].height = self.boxheights[a]
                    b[1].backingdraw = self.backingdraw
                    b[1].scalex = self.scalesize
                    b[1].scaley = self.scalesize
                    b[1].scalesize = self.scalesize
                    b[1].resetcords(ui,False)
                    b[1].layer = self.layer+0.1
                    b[1].ontable = True
                    if b[0] == 'button':
                        b[1].gentext(ui)
                        b[1].refreshcords(ui)
                    elif b[0] == 'textbox':
                        b[1].refreshcords(ui)
                        b[1].resetscroller(ui)
                    else:
                        b[1].gentext(ui)
                        b[1].refreshcords(ui)
            ui.refreshitems()

    def initheightwidth(self):
        if type(self.boxwidth) == int:
            self.boxwidth = [self.boxwidth for a in range(self.columns)]
        else:
            while len(self.boxwidth)<self.columns:
                self.boxwidth.append(-1)
        if type(self.boxheight) == int:
            self.boxheight = [self.boxheight for a in range(self.rows)]
        else:
            while len(self.boxheight)<self.rows:
                self.boxheight.append(-1)
                
    def gettablewidths(self,ui):
        self.boxwidthsinc = []
        self.boxwidths = []
        for a in range(len(self.boxwidth)):
            if self.boxwidth[a] == -1:
                minn = 0
                for b in [self.tableimages[c][a] for c in range(len(self.tableimages))]:
                    if b[0] == 'button' or b[0] == 'textobj':
                        if minn<b[1].textimage.get_width()+b[1].horizontalspacing*2*self.scale:
                            minn = b[1].textimage.get_width()+b[1].horizontalspacing*2*self.scale
                self.boxwidthsinc.append(sum(self.boxwidths))
                self.boxwidths.append(minn/self.scale)
            else:
                self.boxwidthsinc.append(sum(self.boxwidths))
                self.boxwidths.append(self.boxwidth[a])
        self.boxwidthtotal = sum(self.boxwidths)
        self.width = self.boxwidthtotal+self.linesize*(self.columns+1)
##        print('get widths',self.width,self.boxwidths,b[1].textimage.get_rect())
        
    def gettableheights(self,ui):
        self.boxheightsinc = [] 
        self.boxheights = []
        for a in range(len(self.boxheight)):
            if self.boxheight[a] == -1:
                minn = 0
                for b in [self.tableimages[a][c] for c in range(len(self.tableimages[0]))]:
                    if b[0] == 'button' or b[0] == 'textobj':
                        if minn<b[1].textimage.get_height()+b[1].verticalspacing*2*self.scale:
                            minn = b[1].textimage.get_height()+b[1].verticalspacing*2*self.scale
                self.boxheightsinc.append(sum(self.boxheights))
                self.boxheights.append(minn/self.scale)
            else:
                self.boxheightsinc.append(sum(self.boxheights))
                self.boxheights.append(self.boxheight[a])
        self.boxheighttotal = sum(self.boxheights)
        self.height = self.boxheighttotal+self.linesize*(self.rows+1)
                    
                    
    def render(self,screen,ui):
        self.draw(screen,ui)
        
    def draw(self,screen,ui):
        if self.borderdraw:
            pygame.draw.rect(screen,self.bordercol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
        for y in range(self.rows):
            for x in range(self.columns):
                #pygame.draw.rect(screen,self.col,pygame.Rect(self.x*self.dirscale[0]+(self.linesize*(x+1)+self.boxwidthsinc[x])*self.scale,self.y*self.dirscale[1]+(self.linesize*(y+1)+self.boxheightsinc[y])*self.scale,self.boxwidths[x]*self.scale,self.boxheights[y]*self.scale),border_radius=int(self.roundedcorners*scale))
                if self.tableimages[y][x][0] == 'text':
                    screen.blit(self.tableimages[y][x][1],self.tableimages[y][x][2])
                            

class TEXT(GUI_ITEM):
    def reset(self,ui):
        self.refreshscale(ui)
        self.autoscale(ui)
        self.resetcords(ui)
        self.refreshcords(ui)
    def autoscale(self,ui):
        self.gentext(ui)
        if self.width == -1:
            self.width = self.textimage.get_width()/self.scale+self.horizontalspacing*2
        if self.height == -1:
            self.height = self.textimage.get_height()/self.scale+self.verticalspacing*2
    def render(self,screen,ui):
        self.animatetext(ui)
        self.getclickedon(ui)
        self.draw(screen,ui)
    def draw(self,screen,ui):
        if self.backingdraw:
            pygame.draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
        if self.borderdraw:
            pygame.draw.rect(screen,self.bordercol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),self.border,border_radius=int(self.roundedcorners*self.scale))
        if self.pregenerated:
            if self.textcenter:
                screen.blit(self.textimage,(self.x*self.dirscale[0]+self.width/2*self.scale-self.textimage.get_width()/2,self.y*self.dirscale[1]+self.height/2*self.scale-self.textimage.get_height()/2))
            else:
                screen.blit(self.textimage,(self.x*self.dirscale[0]+self.horizontalspacing*self.scale,self.y*self.dirscale[1]+self.verticalspacing*self.scale))
        else:
            ui.write(screen,self.x,self.y,self.text,self.textsize,self.textcol,self.textcenter,self.font,self.bold,self.antialiasing)
    def refresh(self,ui):
        if not self.ontable:
            self.refreshscale(ui)
        self.gentext(ui)
        
        if not self.ontable:
            self.refreshcords(ui)

class SCROLLER(GUI_ITEM):
    def reset(self,ui):
        self.scroll = self.startp
        self.scheight = self.height-self.border*2
        self.prevholding = self.holding
        self.refreshscale(ui)
        self.refresh(ui)
        self.resetcords(ui)
    def render(self,screen,ui):

        temp = (self.x,self.y)
        self.getclickedon(ui,pygame.Rect(self.x*self.dirscale[0]+self.leftborder*self.scale,self.y*self.dirscale[1]+(self.border+self.scroll*(self.scheight/(self.maxp-self.minp)))*self.scale,self.scrollerwidth*self.scale,self.scrollerheight*self.scale))
        if self.holding:
            self.scroll = (self.y-temp[1])/self.scale/(self.scheight/(self.maxp-self.minp))
            
            self.limitpos(ui)
        self.x,self.y = temp
        self.draw(screen,ui)
            
    def limitpos(self,ui):
        if self.scroll<self.minp:
            self.scroll = self.minp
        elif self.scroll>self.maxp-self.pageheight:
            self.scroll = self.maxp-self.pageheight
##        self.refreshcords(ui)
    def refresh(self,ui):
        self.refreshcords(ui)
    def child_refreshcords(self,ui):
        self.scrollerheight = (self.pageheight/(self.maxp-self.minp))*self.scheight
        self.scrollerwidth = self.width-self.leftborder-self.rightborder
        
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.sliderrect = pygame.Rect(self.x+self.border,self.y+self.border+self.scroll*(self.scheight/(self.maxp-self.minp)),self.scrollerwidth,self.scrollerheight)
    def draw(self,screen,ui):
        if (self.maxp-self.minp)>self.pageheight:
            pygame.draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
            pygame.draw.rect(screen,self.scrollercol,roundrect(self.x*self.dirscale[0]+self.leftborder*self.scale,self.y*self.dirscale[1]+(self.border+self.scroll*(self.scheight/(self.maxp-self.minp)))*self.scale,self.scrollerwidth*self.scale,self.scrollerheight*self.scale),border_radius=int(self.roundedcorners*self.scale))

class SLIDER(GUI_ITEM):
    def reset(self,ui):
        self.slider = self.startp
        self.holding = False
        self.prevholding = False
        self.holdingcords = [self.x,self.y]
        self.refreshscale(ui)
        self.resetbutton(ui)
        self.resetcords(ui)
    def refresh(self,ui):
        self.refreshcords(ui)
        self.refreshbutton(ui)
    def child_refreshcords(self,ui):
        self.slidercenter = (self.x+self.border+(self.width-self.border*2)*(self.slider/(self.maxp-self.minp)),self.y+self.height/2)
        self.innerrect = pygame.Rect(self.slidercenter[0]-self.slidersize/2+self.border,self.slidercenter[1]-self.slidersize/2+self.border,self.slidersize-self.border*2,self.slidersize-self.border*2)
        self.refreshbutton(ui)
    def resetbutton(self,ui):
        try:
            ui.delete(self.button.ID,False)
        except:
            pass
        if type(self.data) == BUTTON: self.button = self.data
        else:
            self.button = ui.makebutton(self.x,self.y,self.text,self.textsize,self.command,self.menu,self.ID+'button',self.layer+0.01,self.roundedcorners,self.menuexceptions,width=self.slidersize,height=self.slidersize,img=self.img,dragable=self.dragable,clickdownsize=int(self.slidersize/15),col=shiftcolor(self.col,-30),runcommandat=self.runcommandat)
        if self.direction == 'vertical': self.button.startobjanchor = [self.button.width/2,self.button.height/2]
        else: self.button.startobjanchor = ['w/2','h/2']
        self.button.onsliderbox = True
        self.button.layer = self.layer+0.1
        self.refreshbutton(ui)
    def refreshbuttoncords(self,ui):
        offset = 0
        if self.containedslider: offset = self.button.width/2
        self.slidercenter = (self.x+self.leftborder+offset+(self.width-self.leftborder-self.rightborder-offset*2)*((self.slider-self.minp)/(self.maxp-self.minp)),self.y+self.height/2)
        self.button.startx = self.slidercenter[0]-self.x
        self.button.starty = 0
        if self.direction == 'vertical':
            if self.containedslider: offset = self.button.height/2
            self.slidercenter = (self.x+self.width/2,self.y+self.upperborder+offset+(self.height-self.upperborder-self.lowerborder-offset*2)*((self.slider-self.minp)/(self.maxp-self.minp)))
            self.button.startx = 0
            self.button.starty = self.slidercenter[1]-self.y

        self.button.scalex = self.scalesize
        self.button.scaley = self.scalesize
        self.button.scalesize = self.scalesize
        self.button.resetcords(ui,False)
        self.button.refreshcords(ui)
        self.button.onslider=True
    def refreshbutton(self,ui):
        self.refreshscale(ui)
        self.button.startanchor = [self.x*self.dirscale[0],self.y*self.dirscale[1]+self.height/2*self.scale]
        if self.direction == 'vertical':
            self.button.startanchor = [self.x*self.dirscale[0]+self.width/2*self.scale,self.y*self.dirscale[1]]

        self.button.gentext(ui)
        self.refreshbuttoncords(ui)
        
    def render(self,screen,ui):
        self.draw(screen,ui)
        if self.button.holding: self.movetomouse(ui)
        self.button.draw(screen,ui)
    def movetomouse(self,ui):
        self.slider = (ui.mpos[0]*ui.scale-self.x*self.dirscale[0]-self.leftborder*self.scale)/((self.width-self.leftborder-self.rightborder)*self.scale/(self.maxp-self.minp))+self.minp
        if self.direction == 'vertical':
            self.slider = (ui.mpos[1]*ui.scale-self.y*self.dirscale[1]-self.upperborder*self.scale)/((self.height-self.upperborder-self.lowerborder)*self.scale/(self.maxp-self.minp))+self.minp
        if self.increment!=0: self.slider = round(self.slider/self.increment)*self.increment
        self.limitpos(ui)
    def limitpos(self,ui):
        if self.slider>self.maxp:
            self.slider = self.maxp
        elif self.slider<self.minp:
            self.slider = self.minp
        self.refreshbuttoncords(ui)

    def draw(self,screen,ui):
        pygame.draw.rect(screen,self.bordercol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
        if self.direction == 'vertical':
            pygame.draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0]+self.leftborder*self.scale,self.y*self.dirscale[1]+self.upperborder*self.scale,(self.width-self.leftborder-self.rightborder)*self.scale,((self.height-self.upperborder-self.lowerborder-self.button.height*self.containedslider)*((self.slider-self.minp)/(self.maxp-self.minp))+self.button.height*self.containedslider)*self.scale),border_radius=int(self.roundedcorners*self.scale))
        else:
            pygame.draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0]+self.leftborder*self.scale,self.y*self.dirscale[1]+self.upperborder*self.scale,((self.width-self.leftborder-self.rightborder-self.button.width*self.containedslider)*((self.slider-self.minp)/(self.maxp-self.minp))+self.button.width*self.containedslider)*self.scale,(self.height-self.upperborder-self.lowerborder)*self.scale),border_radius=int(self.roundedcorners*self.scale))



class WINDOWEDMENU(GUI_ITEM):
    def reset(self,ui):
        self.truedarken = self.darken
        self.refreshscale(ui)
    def refresh(self,ui):
        pass 


class ANIMATION:
    def __init__(self,animateID,startpos,endpos,movetype,length,wait,relativemove,command,runcommandat,skiptoscreen,acceleration,ID):
        self.startpos = startpos
        self.endpos = endpos
        self.trueendpos = 0
        self.movetype = movetype
        self.length = length
        self.acceleration = acceleration
        self.relativemove = relativemove

        self.command = command
        self.runcommandat = runcommandat
        
        self.ID = ID
        self.animateID = animateID
        
        self.progress = 0
        self.wait = wait
        self.skip = skiptoscreen
        self.fadeout = False
    def gencordlist(self,ui):
        self.speedlist = [1 for a in range(self.length)]
        speed = 0
        pos = 0
        if self.movetype == 'sin':
            self.speedlist = []
            for p in range(self.length+1):
                self.speedlist.append(1-math.cos(math.pi*2*((p+1)/self.length)))
        elif self.movetype == 'sinin':
            self.speedlist = []
            for p in range(self.length+1):
                self.speedlist.append(1-math.cos(math.pi*((p+1)/self.length)+math.pi))
        elif self.movetype == 'sinout':
            self.speedlist = []
            for p in range(self.length+1):
                self.speedlist.append(1-math.cos(math.pi*((p+1)/self.length)))
            
        for a in range(len(self.speedlist)):
            self.speedlist[a] = (self.speedlist[a]/2)**self.acceleration
        self.speedlist = normalizelist(self.speedlist)
        self.cordlist = []
        for a in range(self.length):
            self.cordlist.append((self.startpos[0]+(self.endpos[0]-self.startpos[0])*(sum(self.speedlist[:a+1])),self.startpos[1]+(self.endpos[1]-self.startpos[1])*(sum(self.speedlist[:a+1]))))
        if self.skip:
            self.findonscreen(ui)
    def findonscreen(self,ui):
        tcords = list(self.cordlist[0])
        scale = ui.IDs[self.animateID].scale
        dirscale = ui.IDs[self.animateID].dirscale
        prog = 0
        prev = pygame.Rect(0,0,ui.screenw,ui.screenh).colliderect(pygame.Rect(tcords[0]*dirscale[0],tcords[1]*dirscale[1],ui.IDs[self.animateID].width*scale,ui.IDs[self.animateID].height*scale))
        while 1:
            if not((pygame.Rect(0,0,ui.screenw,ui.screenh).colliderect(pygame.Rect(tcords[0]*dirscale[0],tcords[1]*dirscale[1],ui.IDs[self.animateID].width*scale,ui.IDs[self.animateID].height*scale)) != prev) or prog>self.length-2):
                prog+=1
                prev = pygame.Rect(0,0,ui.screenw,ui.screenh).colliderect(pygame.Rect(tcords[0]*dirscale[0],tcords[1]*dirscale[1],ui.IDs[self.animateID].width*scale,ui.IDs[self.animateID].height*scale))
                tcords[0] = self.cordlist[prog][0]
                tcords[1] = self.cordlist[prog][1]
            else:
                break
        if pygame.Rect(0,0,ui.screenw,ui.screenh).colliderect(pygame.Rect(tcords[0]*dirscale[0],tcords[1]*dirscale[1],ui.IDs[self.animateID].width*scale,ui.IDs[self.animateID].height*scale)):
            self.cordlist = self.cordlist[prog:]
            self.fadeout = False
        else:
            self.cordlist = self.cordlist[:prog]
            self.fadeout = True
        self.skip = False
        self.startpos = self.cordlist[0]
        self.endpos = self.cordlist[-1]
        self.gencordlist(ui)
    
        
    def animate(self,ui):
        self.wait-=1
        if self.wait == 0:
            sp,ep = False,False
            if self.startpos == 'current':
                sp = True
                self.startpos = (ui.IDs[self.animateID].x,ui.IDs[self.animateID].y)
            if self.endpos == 'current':
                ep = True
                self.endpos = (ui.IDs[self.animateID].x,ui.IDs[self.animateID].y)
            if self.relativemove:
                if (sp and not ep):
                    self.endpos = (self.startpos[0]+self.endpos[0],self.startpos[1]+self.endpos[1])
                elif (ep and not sp):
                    self.startpos = (self.startpos[0]+self.endpos[0],self.startpos[1]+self.endpos[1])
            self.trueendpos = self.endpos[:]
            self.gencordlist(ui)
        if self.wait<1:
            if self.progress<self.length:
                ui.IDs[self.animateID].x = self.cordlist[self.progress][0]
                ui.IDs[self.animateID].y = self.cordlist[self.progress][1]
                if type(ui.IDs[self.animateID]) in [TABLE,TEXTBOX,TEXT,SCROLLER,SLIDER,WINDOWEDMENU]:
                    ui.IDs[self.animateID].refreshcords(ui)
                if type(ui.IDs[self.animateID]) == WINDOWEDMENU:
                    ui.IDs[self.animateID].darken = ui.IDs[self.animateID].truedarken*(self.progress/self.length)
                    if self.fadeout: ui.IDs[self.animateID].darken = ui.IDs[self.animateID].truedarken-ui.IDs[self.animateID].darken

            if self.progress == self.runcommandat or (type(self.runcommandat)==list and self.progress in self.runcommandat):
                self.command()
            self.progress+=1
            if self.progress >= self.length:
                self.finish(ui)
                return True
        return False
    def finish(self,ui,forcefinish=False):
        if forcefinish:
            while not self.animate(ui):
                pass
        if self.progress == self.runcommandat or (type(self.runcommandat)==list and self.progress in self.runcommandat):
            self.command()
        if self.relativemove and self.wait>0 and self.endpos!='current':
            if self.startpos == 'current':
                self.startpos = (ui.IDs[self.animateID].x,ui.IDs[self.animateID].y)
            self.endpos = (self.startpos[0]+self.endpos[0],self.startpos[1]+self.endpos[1])
        ui.IDs[self.animateID].x = self.trueendpos[0]
        ui.IDs[self.animateID].y = self.trueendpos[1]
        if type(ui.IDs[self.animateID]) in [TABLE,TEXTBOX,TEXT,SCROLLER,SLIDER,WINDOWEDMENU]:
            ui.IDs[self.animateID].refreshcords(ui)
        if type(ui.IDs[self.animateID]) == WINDOWEDMENU:
            ui.IDs[self.animateID].darken = ui.IDs[self.animateID].truedarken

class RECT(GUI_ITEM):
    def render(self,screen,ui):
        self.getclickedon(ui)
        self.draw(screen,ui)
    def draw(self,screen,ui):
        pygame.draw.rect(screen,self.backingcol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
        
        
    























    
        

        
        
                          




