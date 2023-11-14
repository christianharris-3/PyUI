import pygame,random,math,time,copy,ctypes,os,threading
import pygame.gfxdraw 
pygame.init()

def resourcepath(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def loadinganimation(points=12):
    img = []
    for a in range(points):
        img.append('{loading largest='+str(a)+'}')
    return img

def rectscaler(rect,scale,offset=(0,0)):
    if not type(scale) in [float,int]:
        return pygame.Rect((rect.x-offset[0])*scale.dirscale[0],(rect.y-offset[1])*scale.dirscale[1],rect.w*scale.scale,rect.h*scale.scale)
    else:
        return pygame.Rect((rect.x-offset[0])*scale,(rect.y-offset[1])*scale,rect.w*scale,rect.h*scale)
def roundrect(x,y,width,height):
    return pygame.Rect(round(x),round(y),round(width),round(height))

def emptyfunction():
    pass
class emptyobject:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.scale = 1
        self.dirscale = [1,1]
        self.empty = True
        self.active = False
    def getenabled(self):
        return True
class funcer:
    def __init__(self,func,**args):
        self.func = lambda: func(**args)

def normalizelist(lis,sumto=1):
    total = sum(lis)
    if total>0:
        newlis = []
        for a in lis:
            newlis.append(a*(sumto/total))
        return newlis
    else:
        return lis

def colav(col1,col2,weight):
    if len(col1) == 3: return (col1[0]+(col2[0]-col1[0])*weight,col1[1]+(col2[1]-col1[1])*weight,col1[2]+(col2[2]-col1[2])*weight)
    else: return (col1[0]+(col2[0]-col1[0])*weight,col1[1]+(col2[1]-col1[1])*weight,col1[2]+(col2[2]-col1[2])*weight,col1[3]+(col2[3]-col1[3])*weight)

def genfade(colourlist,sizeperfade):
    cols = []
    for a in range(len(colourlist)-1):
        for b in range(sizeperfade):
            cols.append(colav(colourlist[a],colourlist[a+1],b/sizeperfade))
    return cols

def RGBtoHSV(rgb):
    rp = rgb[0]/255
    gp = rgb[1]/255
    bp = rgb[2]/255
    cmax = max(rp,gp,bp)
    cmin = min(rp,gp,bp)
    delta = cmax-cmin
    if cmax-cmin == 0:
        H = 0
    else:
        if cmax == rp: H = (60*(0+(gp-bp)/(cmax-cmin)))%360
        elif cmax == gp: H = (60*(2+(bp-rp)/(cmax-cmin)))%360
        elif cmax == bp: H = (60*(4+(rp-gp)/(cmax-cmin)))%360
    
    if cmax == 0: S = 0
    else: S = delta/cmax
    V = cmax    
    return (H,S,V)

    
def shiftcolor_hsva(col,shift):
    col = pygame.color.Color(col)
    col.hsva = (col.hsva[0],col.hsva[1],max([min([100,col.hsva[2]+shift/2.55]),0]),col.hsva[3])
    return col

def shiftcolor_rgb(col,shift):
    return [max([min([255,a+shift]),0]) for a in col]

def shiftcolor(col,shift):
    if Style.defaults['hsvashift']:
        return shiftcolor_hsva(col,shift)
    else:
        return shiftcolor_rgb(col,shift)

def autoshiftcol(col,default=(150,150,150),editamount=0):
    if type(col) == int:
        if col != -1:
            editamount = col
        col = default
        return shiftcolor(col,editamount)
    return col

def menuin(objmenu,menulist):
    for a in objmenu:
        if a in menulist:
            return True
    return False

def relativetoval(st,w,h,ui):
    global returnedexecvalue
    if type(st) == str:
        st = smartreplace(smartreplace(st,'w',w),'h',h)
        tlocals = {'ui':ui}
        execstring = 'returnedexecvalue='+st
        exec(execstring,tlocals,globals())
        return returnedexecvalue
    else:
        return st
def collidepointrects(point,rects):
    for a in rects:
        if a.collidepoint(point):
            return True
    return False

def smartreplace(st,char,replace):
    # Only replaces when no characters on either side
    lis = list(st)
    alphabet = [chr(a) for a in range(97,123)]
    nstring = ''
    for i,a in enumerate(lis):
        if a == char and (i==0 or not(lis[i-1] in alphabet)) and (i == len(lis)-1 or not(lis[i+1] in alphabet)):
            nstring+=str(replace)
        else:
            nstring+=a
    return nstring

def losslesssplit(text,splitter):
    splitted = text.split(splitter)
    for a in range(len(splitted)-1):
        splitted[a+1]=splitter+splitted[a+1]
    if text[-2:] == splitter:
        splitted.append(splitter)
    return splitted

def distance(point1,point2):
    return ((point1[0]-point2[0])**2+(point1[1]-point2[1])**2)**0.5

def distancetorect(point,rect):
    x,y,w,h = rect
    if pygame.Rect(x,y,w,h).collidepoint(point): return 0
    if point[0]<x:
        if point[1]>y:
            if point[1]<y+h: return x-point[0]
            else: return distance(point,(x,y+h))
        else: return distance(point,(x,y))
    elif point[0]>x+w:
        if point[1]>y:
            if point[1]<y+h: return point[0]-(x+w)
            else: return distance(point,(x+w,y+h))
        else: return distance(point,(x+w,y))
    else:
        if point[1]>y: return y-point[1]
        else: return point[1]-(y-h)
        

##def stress(num=10000):
####    items = [[[(random.gauss(0,1000),random.gauss(0,1000)),(random.gauss(0,1000),random.gauss(0,1000))],[(random.gauss(0,1000),random.gauss(0,1000)),(random.gauss(0,1000),random.gauss(0,1000))]] for a in range(num)]
##    items = [(random.gauss(0,1000),random.gauss(0,1000)) for a in range(num)]
##    poly = [[6121.418823168169, 2540.4649881431005], [5902.418823100715, 2551.4649881504115], [5773.418823092922, 2553.464988151256], [5620.418823088219, 2550.4649881517657], [5490.418823085731, 2545.4649881520363], [5378.418823084146, 2527.464988152208], [5286.418823083264, 2489.4649881523032], [5091.924628306851, 2332.387747678128], [5036.921068889245, 2246.1805067546848], [4992.968283297781, 2160.3846598957725], [4960.878762510003, 2066.520712568027], [4927.625408027907, 1969.9715330965237], [4902.238222271764, 1874.3132243192679], [4832.185483354941, 1596.2392434177348], [4746.037533214347, 1294.3999832223974], [4668.196053825487, 1123.9184982530383], [4388.045581531835, 852.6694429143116], [4234.770978869179, 742.7471765057273], [4023.5661500620718, 657.4162418848409], [3881.367373533748, 619.2805369612004], [3362.504158675401, 560.7525398940218], [3012.495293479294, 518.6831357669186], [2663.48521220508, 473.7023164851081], [1921.305458538932, 440.7934343278041], [1206.2112352050306, 441.18459194927823], [163.12564768061986, 487.04410206501905], [303.07450108395574, 1400.8082649197895], [3428.1258279353483, 1750.02606706993], [4628.002315536618, 3522.9779499727438], [6105.462208231702, 3263.3031797131207]]
##    print('starting')
##    start = time.time()
##    for a in items:
##        polyescape(a,poly)
##    total = time.time()-start
##    print('total:',total,'per:',total/num)
##
##def stress2(num=100000):
##    items = [[[(random.gauss(0,1000),random.gauss(0,1000)),(random.gauss(0,1000),random.gauss(0,1000))],[(random.gauss(0,1000),random.gauss(0,1000)),(random.gauss(0,1000),random.gauss(0,1000))]] for a in range(num)]
##    print('starting')
##    start = time.time()
##    for a in items:
##        linecross(a[0],a[1])
##    total = time.time()-start
##    print('total:',total,'per:',total/num)
    
def polycollide(point,poly,angle=0.5):
    center = point
    crosses = 0
    dis = 100000
    for a in range(len(poly)):
        awayline = [center,[center[0]+(dis*math.cos(angle/180*math.pi)),center[1]+(dis*math.sin(angle/180*math.pi))]]
        collide = linecross(awayline,[poly[a],poly[a-1]])
        if collide[0]:
            crosses+=1
    if crosses%2:
        return True
    return False

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

##        if xcross<min([a,b]) or xcross>max([a,b]) or ycross<min([e,f]) or ycross>max([e,f]) or xcross<min([c,d]) or xcross>max([c,d]) or ycross<min([g,h]) or ycross>max([g,h]):
##            return False,1

        dis = 0.1
        if a<b:
            if xcross<a-dis or xcross>b+dis: return False,1
        else:
            if xcross<b-dis or xcross>a+dis: return False,2
        if c<d:
            if xcross<c-dis or xcross>d+dis: return False,3
        else:
            if xcross<d-dis or xcross>c+dis: return False,4
        if e<f:
            if ycross<e-dis or ycross>f+dis: return False,5
        else:
            if ycross<f-dis or ycross>e+dis: return False,6
        if g<h:
            if ycross<g-dis or ycross>h+dis: return False,7
        else:
            if ycross<h-dis or ycross>g+dis: return False,8

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

class draw:
    def bezierpoints(roots,progress,detail):
        #print(roots)
        npoints = []
        for a in range(len(roots)-1):
            npoints.append((roots[a][0]+(roots[a+1][0]-roots[a][0])*(progress/detail),roots[a][1]+(roots[a+1][1]-roots[a][1])*(progress/detail)))
        if len(npoints)>0:
            point = draw.bezierpoints(npoints,progress,detail)
        else:
            point = roots[0]
        return point
    def bezierdrawer(points,width,commandpoints=True,detail=200,rounded=True):
        curvepoints = []
        for a in range(detail):
            curvepoints.append(draw.bezierpoints(points,a,detail))
        curvepoints.append(points[-1])
        if commandpoints:
            pygame.draw.aalines(screen,(0,0,0),False,curvepoints)
            if len(points) == 4:
                pygame.draw.line(screen,(100,100,100),points[0],points[1])
                pygame.draw.line(screen,(100,100,100),points[2],points[3])
            else:
                pygame.draw.lines(screen,(100,100,100),False,points)
        if rounded:
            final = []
            prev = 0
            for a in curvepoints:
                if (round(a[0]),round(a[1])) != prev:
                    final.append((round(a[0]),round(a[1])))
                    prev = (round(a[0]),round(a[1]))
            return final
        return curvepoints
    def roundedline(surf,col,point1,point2,width):
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
        pygame.gfxdraw.aapolygon(surf,points,col)
        pygame.gfxdraw.filled_polygon(surf,points,col)
        draw.circle(surf,col,point1,width)
        draw.circle(surf,col,point2,width)
    def rect(surf,col,rect,width=0,border_radius=0):
        x,y,w,h = rect
        radius = abs(int(min([border_radius,rect[2]/2,rect[3]/2])))
        if border_radius != 0 and (radius*(1+(2**0.5)/2)<width or width==0):
            try:
                pygame.gfxdraw.aacircle(surf,x+radius,y+radius,radius,col)
                pygame.gfxdraw.aacircle(surf,x+w-radius-1,y+radius,radius,col)
                pygame.gfxdraw.aacircle(surf,x+w-radius-1,y+h-radius-1,radius,col)
                pygame.gfxdraw.aacircle(surf,x+radius,y+h-radius-1,radius,col)
            except:
                ## catches error with integer overflow when drawn at large coordinates
                pass
        pygame.draw.rect(surf,col,roundrect(x,y,w,h),int(width),int(border_radius))
    def circle(surf,col,center,radius):
        try:
            pygame.gfxdraw.aacircle(surf,int(center[0]),int(center[1]),int(radius),col)
            pygame.gfxdraw.filled_circle(surf,int(center[0]),int(center[1]),int(radius),col)
        except:
            ## catches error with integer overflow when drawn at large coordinates
            pass
    def polygon(surf,col,points):
        pygame.gfxdraw.aapolygon(surf,points,col)
        pygame.gfxdraw.filled_polygon(surf,points,col)
    def glow(surf,rect,distances,col,scale=1,detail=-1,shade=100,roundedcorners=-1):
        if distances!=0:
            if type(distances) == int: distances = [distances for a in range(4)]
            if roundedcorners == -1: roundedcorners=max(distances)
            if detail == -1: detail=int(max(distances))
            colorkey = (255,255,255)
            if col == colorkey: colorkey = (0,0,0)
            if len(col) == 3: col = [col[0],col[1],col[2],shade/detail]
            else: shade = col[3]
            for a in range(detail,0,-1):
                w = rect.width+(a/detail)*(distances[1]+distances[3])
                h = rect.height+(a/detail)*(distances[0]+distances[2])
                rec = pygame.Surface((w,h),pygame.SRCALPHA)
                pygame.draw.rect(rec,col,pygame.Rect(0,0,w,h),0,int(roundedcorners-(1-a/detail)*distances[0]))
                surf.blit(rec,(rect.x-(a/detail)*distances[3],rect.y-(a/detail)*distances[0]))
    def pichart(surf,center,radius,col,ang1,ang2=0,innercol=-1,border=2):
        draw.circle(surf,col,[center[0],center[1]],radius)
        if ang1!=ang2:
            innercol = autoshiftcol(innercol,col,-20)
            rad = radius-border
            draw.circle(surf,innercol,[center[0],center[1]],rad)
            temp = ang1
            ang1 = ang2
            ang2 = temp
            diff = (ang1-ang2)%(math.pi*2)
            poly = [[center[0],center[1]]]
            segments = max(int(radius*diff),1)
            rad+=1
            for a in range(segments+1):
                poly.append([center[0]-rad*math.sin(ang2+diff*a/segments),center[1]-rad*math.cos(ang2+diff*a/segments)])
            draw.polygon(surf,col,poly)
    def blitroundedcorners(surf,surfto,x,y,roundedcorners,area=None):
        if area == None: area = surf.get_rect()
        area.normalize()
        mask = pygame.Surface(area.size,pygame.SRCALPHA)
        draw.rect(mask,(255,255,255),(0,0,area.width,area.height),border_radius=roundedcorners)
        nsurf = pygame.Surface(surf.get_size(),pygame.SRCALPHA)
        nsurf.blit(surf,(0,0))
        nsurf.blit(mask,(area.x,area.y),special_flags=pygame.BLEND_RGBA_MIN)
        surfto.blit(nsurf,(x,y),area)
        
        
        
        

        


    
class UI:
    def __init__(self,scale=1,PyUItitle=True):
        pygame.key.set_repeat(350,31)
        pygame.scrap.init()
        pygame.scrap.set_mode(pygame.SCRAP_CLIPBOARD)
        
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
        self.dropdowns = []
        self.windows = []
        self.noclickrects = []
        self.selectedtextbox = -1
        self.IDs = {}
        self.items = []

        self.images = []
        self.getscreen()
        self.inbuiltimages = {}

        self.activemenu = 'main'
        self.framemenu = 'main'
        self.windowedmenus = []
        self.automenus = []
        self.windowedmenunames = []
        self.backchain = []
        self.queuedmenumove = [0,[]]
        self.prevmenumove = []
        self.buttondowntimer = 9

        self.fullscreen = False
        self.exit = False
        self.blockf11 = 0
        
        self.clipboard = pygame.scrap.get('str')

        self.timetracker = time.perf_counter()
        
        self.scrolllimit = 100
        self.escapeback = True
        self.backquits = True
        self.scrollwheelscrolls = True
        self.idmessages = False
        self.queuemenumove = True
        self.roundedbezier = True
        self.rendershapefunctions = {'tick':self.rendershapetick,'cross':self.rendershapecross,'arrow':self.rendershapearrow,'settings':self.rendershapesettings,
                                     'play':self.rendershapeplay,'pause':self.rendershapepause,'skip':self.rendershapeskip,'circle':self.rendershapecircle,
                                     'rect':self.rendershaperect,'clock':self.rendershapeclock,'loading':self.rendershapeloading,'dots':self.rendershapedots,
                                     'logo':self.rendershapelogo}
        self.renderedshapes = {}
        
        self.resizable = True
        self.fullscreenable = True
        self.autoscale = 'width'
        tempscreen = pygame.display.get_surface()
        self.basescreensize = [tempscreen.get_width(),tempscreen.get_height()]
        self.checkcaps()
        if self.scale!=1: self.setscale(self.scale)
        self.styleload_default()
        
        self.PyUItitle = PyUItitle
        if PyUItitle:
            self.logo = self.rendershapelogo('logo',50,(0,0,0),(255,255,255),False)
            self.logo.set_colorkey((255,255,255))
            pygame.display.set_icon(self.logo)
            pygame.display.set_caption('PyUI Application')
        self.loadtickdata()
        
    def checkcaps(self):
        hllDll = ctypes.WinDLL("User32.dll")
        self.capslock = bool(hllDll.GetKeyState(0x14))

    def styleset(self,**args):
        marked = {}
        for a in args:
            if (a in Style.defaults):
                Style.defaults[a] = args[a]
                for b in Style.objectdefaults:
                    Style.objectdefaults[b][a] = args[a]
            elif a == 'wallpapercol':
                exec(f'Style.{a} = {args[a]}')
            else:
                marked[a] = args[a]
           
        for a in marked:
            if a.split('_')[0] in UI.objectkey:
                Style.objectdefaults[UI.objectkey[a.split('_')[0]]][a.split('_',1)[1]] = args[a]
        
                    
    def styleload_soundium(self): self.styleset(col=(16,163,127),textcol=(255,255,255),wallpapercol=(62,63,75),textsize=24,roundedcorners=5,spacing=5,clickdownsize=2,scalesize=False)
    def styleload_default(self): self.styleset(roundedcorners=0,center=False,textsize=50,font='calibre',bold=False,antialiasing=True,border=3,scalesize=True,glow=0,col=(150,150,150),
                                               clickdownsize=4,clicktype=0,textoffsetx=0,textoffsety=0,clickableborder=0,lines=1,textcenter=False,linesize=2,backingdraw=True,borderdraw=True,
                                               animationspeed=30,containedslider=False,movetoclick=True,isolated=True,darken=60,textcol=(0,0,0),verticalspacing=2,horizontalspacing=8,
                                               text_animationspeed=5,text_backingdraw=False,text_borderdraw=False,text_verticalspacing=3,text_horizontalspacing=3,dropdown_animationspeed=15,
                                               textbox_verticalspacing=2,textbox_horizontalspacing=6,table_textcenter=True,button_textcenter=True,guesswidth=100,guessheight=100)
    def styleload_black(self): self.styleset(textcol=(0,0,0),backingcol=(0,0,0),hovercol=(255,255,255),bordercol=(0,0,0),verticalspacing=3,textsize=30,col=(255,255,255),clickdownsize=1)
    def styleload_blue(self): self.styleset(col=(35,0,156),textcol=(230,246,219),wallpapercol=(0,39,254),textsize=30,verticalspacing=2,horizontalspacing=5,clickdownsize=2,roundedcorners=4)
    def styleload_green(self): self.styleset(col=(87,112,86),textcol=(240,239,174),wallpapercol=(59,80,61),textsize=30,verticalspacing=2,horizontalspacing=5,clickdownsize=2,roundedcorners=4)
    def styleload_lightblue(self): self.styleset(col=(82,121,214),textcol=(56,1,103),wallpapercol=(228,242,253),textsize=30,verticalspacing=2,horizontalspacing=5,clickdownsize=2,roundedcorners=4)
    def styleload_teal(self): self.styleset(col=(109,123,152),textcol=(176,243,174),wallpapercol=(69,65,88),textsize=30,verticalspacing=2,horizontalspacing=5,clickdownsize=2,roundedcorners=4)
    def styleload_brown(self): self.styleset(col=(39,75,91),textcol=(235,217,115),wallpapercol=(40,41,35),textsize=30,verticalspacing=2,horizontalspacing=5,clickdownsize=2,roundedcorners=4)
    def styleload_red(self): self.styleset(col=(152,18,20),textcol=(234,230,133),wallpapercol=(171,19,18),spacing=3,clickdownsize=2,textsize=40,horizontalspacing=8,roundedcorners=5)
        
    def __scaleset__(self,scale):
        self.scale = scale
        self.dirscale = [self.screenw/self.basescreensize[0],self.screenh/self.basescreensize[1]]
        for a in self.automenus+self.windowedmenus:
            a.refresh()
            a.resetcords()
        for a in self.items:
            checker = (a.width,a.height)
            a.autoscale()
            if type(a) in [TABLE,SCROLLERTABLE]:
                a.small_refresh()
            if (a.width,a.height) != checker or a.scalesize:
                a.refresh()
            if a.clickablerect != -1:
                a.refreshclickablerect()
                
    def setscale(self,scale):
        pygame.event.post(pygame.event.Event(pygame.VIDEORESIZE,w=self.basescreensize[0]*scale,h=self.basescreensize[1]*scale))
    def quit(self):
        pygame.event.post(pygame.event.Event(pygame.QUIT))
    def refreshall(self):
        for a in self.automenus+self.windowedmenus:
            a.enabled = False
            self.refreshbound(a)
    def refreshbound(self,obj):
        obj.refresh()
        obj.enabled = True
        for b in obj.bounditems:
            b.enabled = False
            self.refreshbound(b)
        
    def getscreen(self):
        sc = pygame.display.get_surface()
        self.screenw = sc.get_width()
        self.screenh = sc.get_height()
    def rendergui(self,screen):
        windowedmenubackings = [a.behindmenu for a in self.windowedmenus]
        self.breakrenderloop = False
        self.animate()
        self.framemenu = self.activemenu
        for i,a in enumerate(self.automenus):
            if self.framemenu in a.truemenu:
                a.render(screen)
        for a in self.windowedmenus:
            if self.framemenu in a.truemenu:
                if pygame.Rect(a.x*a.dirscale[0],a.y*a.dirscale[1],a.width*a.scale,a.height*a.scale).collidepoint(self.mpos):
                    self.drawmenu(a.behindmenu,screen)
                else:
                    if a.isolated:
                        self.drawmenu(a.behindmenu,screen)
                        if self.mprs[0] and self.mouseheld[0][1] == self.buttondowntimer:
                            self.menuback()
                    else:
                        self.rendermenu(a.behindmenu,screen)
                a.render(screen)

    def rendermenu(self,menu,screen):
        if f'auto_generate_menu:{menu}' in self.IDs:
            self.IDs[f'auto_generate_menu:{menu}'].render(screen)
    def drawmenu(self,menu,screen):
        if f'auto_generate_menu:{menu}' in self.IDs:
            self.IDs[f'auto_generate_menu:{menu}'].drawallmenu(screen)
            
    def loadtickdata(self):
        t = time.perf_counter()
        self.deltatime = 60*(t-self.timetracker)
        self.timetracker = t
        self.blockf11-=1
        self.mpos = list(pygame.mouse.get_pos())
        self.mprs = pygame.mouse.get_pressed()
        self.kprs = pygame.key.get_pressed()
        self.time = time.time()
        for a in range(3):
            if self.mprs[a] and not self.mouseheld[a][0]: self.mouseheld[a] = [1,self.buttondowntimer]
            elif self.mprs[a]: self.mouseheld[a][1] -= 1
            if not self.mprs[a]: self.mouseheld[a][0] = 0
        events = pygame.event.get()
        repeatchecker = []
        for event in events:
            if not(event in repeatchecker):
                repeatchecker.append(event)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_CAPSLOCK:
                        if self.capslock: self.capslock = False
                        else: self.capslock = True
                    if event.key == pygame.K_ESCAPE and self.escapeback:
                        self.menuback()
                    if event.key == pygame.K_F5:
                        thread = threading.Thread(target=self.refreshall)
                        thread.start()
                    if event.key == pygame.K_F11 and self.fullscreenable and self.blockf11<0:
                        self.togglefullscreen(pygame.display.get_surface())
                    if self.selectedtextbox!=-1:
                        if not self.textboxes[self.selectedtextbox].selected:
                            self.selectedtextbox = -1
                        else:
                            self.textboxes[self.selectedtextbox].inputkey(self.capslock,event,self.kprs)
                elif event.type == pygame.VIDEORESIZE:
                    self.screenw = event.w
                    self.screenh = event.h
                    self.resetscreen(pygame.display.get_surface())
                elif event.type == pygame.MOUSEWHEEL:
                    moved = False
                    for a in self.textboxes:
                        if a.scrolleron and a.selected and self.activemenu == a.getmenu():
                            if a.pageheight<(a.maxp-a.minp):
                                a.scroller.scroll-=(event.y*min((a.scroller.maxp-a.scroller.minp)/20,self.scrolllimit))
                                a.scroller.limitpos()
                                a.scroller.command()
                                moved = True
                    if not moved:
                        scrollable = []
                        for a in self.scrollers:
                            if self.activemenu == a.getmenu() and type(a.master[0]) != TEXTBOX:
                                if a.pageheight<(a.maxp-a.minp) and a.getenabled():
                                    scrollable.append(a)
                        for x in scrollable:
                            x.tempdistancetomouse = distancetorect([self.mpos[0]/x.dirscale[0],self.mpos[1]/x.dirscale[1]],(x.x,x.y,x.width,x.height))
                            if type(x.master[0]) == SCROLLERTABLE:
                                x.tempdistancetomouse = distancetorect([self.mpos[0]/x.dirscale[0],self.mpos[1]/x.dirscale[1]],(x.master[0].x,x.master[0].y,x.master[0].width,x.master[0].height))
                        scrollable.sort(key= lambda x: x.tempdistancetomouse)
                        for a in scrollable:
                            a.scroll-=(event.y*min((a.maxp-a.minp)/20,self.scrolllimit))
                            a.limitpos()
                            a.command()
                            break
        return repeatchecker
    def togglefullscreen(self,screen):
        if self.fullscreen: self.fullscreen = False
        else: self.fullscreen = True
        self.resetscreen(screen)
    def resetscreen(self,screen):
        if self.autoscale == 'width':
            self.__scaleset__(self.screenw/self.basescreensize[0])
        else:
            self.__scaleset__(self.screenh/self.basescreensize[1])
        if self.fullscreen: screen = pygame.display.set_mode((self.screenw,self.screenh),pygame.FULLSCREEN)
        else: screen = pygame.display.set_mode((self.screenw,self.screenh),pygame.RESIZABLE)
        if self.PyUItitle:
            pygame.display.set_icon(self.logo)
        self.blockf11 = 10
        
    def write(self,screen,x,y,text,size,col=-1,center=True,font=-1,bold=False,antialiasing=True,scale=False,centery=-1):
        if font == -1: font = Style.defaults['font']
        if col == -1: col = Style.defaults['textcol']
        if size == -1: size = Style.defaults['textsize']
        if centery == -1: centery = center
        if scale:
            dirscale = self.dirscale
            scale = self.scale
        else:
            dirscale = [1,1]
            scale = 1
        largetext = pygame.font.SysFont(font,int(size*scale),bold)
        textsurf = largetext.render(text, antialiasing, col)
        textrect = textsurf.get_rect()
        if center:
            textrect.center = (int(x)*dirscale[0],int(y)*dirscale[1])
            if not centery: textrect.y = y*dirscale[1]
        else:
            textrect.y = int(y)*dirscale[1]
            if centery: textrect.center = (int(x)*dirscale[0],int(y)*dirscale[1])
            textrect.x = int(x)*dirscale[0]
        screen.blit(textsurf, textrect)
    
    def rendertext(self,text,size,col=-1,font=-1,bold=False,antialiasing=True,backingcol=(150,150,150),imgin=False,img=''):
        if font == -1: font = Style.defaults['font']
        if col == -1: col = Style.defaults['textcol']
        if size == -1: size = Style.defaults['textsize']
        if imgin:
            texts,imagenames = self.seperatestring(text) 
        else:
            texts = [text]
            imagenames = ['']
        images = []
        textgen = pygame.font.SysFont(font,int(size),bold)
        for a in range(len(texts)):
            if texts[a] != '': images.append(textgen.render(texts[a], antialiasing, col))
            if imagenames[a] != '': images.append(self.rendershape(imagenames[a],size,col,False,backcol=backingcol))
        if len(images) == 0:
            return pygame.Surface((0,textgen.size('\n')[1]))
        else:
            textsurf = pygame.Surface((sum([a.get_width() for a in images]),max([a.get_height() for a in images])))
            
        textsurf.fill(backingcol)
        xpos = 0
        h = textsurf.get_height()
        for a in images:
            textsurf.blit(a,(xpos,(h-a.get_height())/2))
            xpos+=a.get_width()
        textsurf.set_colorkey(backingcol)
        return textsurf
    
    def seperatestring(self,text):
        texts = ['']
        imagenames = ['']
        openn = 0
        for a in text:
            if a == '{':
                if openn == 0:
                    texts.append('')
                openn+=1
            if openn>0:
                imagenames[-1]+=a
            else:
                texts[-1]+=a

            if a == '}':
                if openn == 1:
                    imagenames.append('')
                openn-=1
                if openn<0: openn = 0
        if len([i for i in imagenames[-1] if i == '{']) != len([i for i in imagenames[-1] if i == '}']):
            texts[-2]+=imagenames.pop(-1)
            imagenames.append('')
            del texts[-1]
        for i,a in enumerate(imagenames):
            imagenames[i] = a.removeprefix('{').removesuffix('}')
        return texts,imagenames
    
    def rendershape(self,name,size,col='default',failmessage=True,backcol=(255,255,255)):
        name = name.strip()
        if col == 'default': col = Style.defaults['col']
        if col == backcol: backcol = (0,0,0)
        if 'col=' in name:
            try:
                c = name.split('col=')[1].split('(')[1].split(')')[0].split(',')
                col = (int(c[0]),int(c[1]),int(c[2]))
            except:
                pass
        if 'scale=' in name:
            size*=float(name.split('scale=')[1].split(' ')[0])
            
        if str([name,size,col,backcol]) in self.renderedshapes:
            return self.renderedshapes[str([name,size,col,backcol])]
        if len(name)>0 and name[0] == '"':
            surf = self.rendershapetext(name,size,col,backcol)
        elif name.split(' ')[0] in self.rendershapefunctions:
            surf = self.rendershapefunctions[name.split(' ')[0]](name,size,col,backcol)
        else:
            surf,worked,backcol = self.rendershapebezier(name,size,col,backcol,failmessage)
            if not worked:
                surf = self.rendershapetext(name,size,col,backcol)
        keywords = name.split('"')[-1].split()
        if 'left' in keywords:
            surf = pygame.transform.flip(surf,True,False)
        elif 'up' in keywords:
            surf = pygame.transform.rotate(surf,90)
        elif 'down' in keywords:
            surf = pygame.transform.rotate(surf,-90)
        surf.set_colorkey(backcol)
        self.renderedshapes[str([name,size,col,backcol])] = surf
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
            draw.polygon(surf,col,a)
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
            draw.roundedline(surf,col,(size*(width+0.05),size*0.35),(size*(sticklen+pointlen+0.05-width),size*0.35),width*size)
            draw.roundedline(surf,col,(size*(sticklen+0.05),size*(0.05+width)),(size*(sticklen+pointlen+0.05-width),size*0.35),width*size)
            draw.roundedline(surf,col,(size*(sticklen+0.05),size*(0.7-0.05-width)),(size*(sticklen+pointlen+0.05-width),size*0.35),width*size)
        else:
            draw.polygon(surf,col,((size*0.05,size*0.25),(size*(sticklen+0.05),size*0.25),(size*(sticklen+0.05),size*0.05),(size*(sticklen+pointlen+0.05),size*0.35),(size*(sticklen+0.05),size*0.65),(size*(sticklen+0.05),size*0.45),(size*0.05,size*0.45)))
        return surf
    def rendershapecross(self,name,size,col,backcol):
        vals = self.getshapedata(name,['width'],[0.1])
        width = vals[0]
        surf = pygame.Surface((size+1,size+1))
        surf.fill(backcol)
        draw.roundedline(surf,col,(size*width,size*width),(size*(1-width),size*(1-width)),size*width)
        draw.roundedline(surf,col,(size*(1-width),size*width),(size*width,size*(1-width)),size*width)
        return surf
    def rendershapesettings(self,name,size,col,backcol,antialiasing=True):
        surf = pygame.Surface((size,size)) 
        surf.fill(backcol)
        vals = self.getshapedata(name,['innercircle','outercircle','prongs','prongwidth','prongsteepness'],[0.15,0.35,6,0.2,1.1])
        innercircle = vals[0]
        outercircle = vals[1]
        prongs = int(vals[2])
        prongwidth = vals[3]
        prongsteepness = vals[4]
        if antialiasing: draw.circle(surf,col,(size*0.5,size*0.5),size*outercircle)
        else: pygame.draw.circle(surf,col,(size*0.5,size*0.5),size*outercircle)
        width=prongwidth
        innerwidth=width+math.sin(width)*prongsteepness
        points = []
        outercircle-=0.01
        for a in range(prongs):
            ang = (math.pi*2)*a/prongs
            points.append([((math.sin(ang-width)*0.5*0.95+0.5)*size,(math.cos(ang-width)*0.5*0.95+0.5)*size),((math.sin(ang+width)*0.5*0.95+0.5)*size,(math.cos(ang+width)*0.5*0.95+0.5)*size),((math.sin(ang+innerwidth)*0.5*(outercircle*2)+0.5)*size,(math.cos(ang+innerwidth)*0.5*(outercircle*2)+0.5)*size),((math.sin(ang-innerwidth)*0.5*(outercircle*2)+0.5)*size,(math.cos(ang-innerwidth)*0.5*(outercircle*2)+0.5)*size)])
        if antialiasing:
            for a in points:
                draw.polygon(surf,col,a)
            draw.circle(surf,backcol,(size*0.5,size*0.5),size*innercircle)
        else:
            for a in points:
                pygame.draw.polygon(surf,col,a)
            pygame.draw.circle(surf,backcol,(size*0.5,size*0.5),size*innercircle)
        return surf
    def rendershapelogo(self,name,size,col,backcol,antialiasing=True):
        surf = pygame.Surface((size,size))
        surf.fill(backcol)
        surf = self.rendershapesettings(name,size,(66,129,180),backcol,antialiasing)
        self.write(surf,size*0.5,size*0.5,'PyUI',size*(360/600),(62,63,75),True,antialiasing=antialiasing)
        self.write(surf,size*0.5,size*0.5,'PyUI',size*(380/600),(253,226,93),True,antialiasing=antialiasing)
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
            draw.roundedline(surf,col,points[a],points[a-1],size*rounded/2)
        draw.polygon(surf,col,points)
        return surf
    def rendershapepause(self,name,size,col,backcol):
        surf = pygame.Surface((size*0.75,size))
        surf.fill(backcol)
        vals = self.getshapedata(name,['rounded'],[0.0])
        rounded = vals[0]
        draw.rect(surf,col,pygame.Rect(0,0,size*0.25,size),border_radius=int(size*rounded))
        draw.rect(surf,col,pygame.Rect(size*0.5,0,size*0.25,size),border_radius=int(size*rounded))
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
        draw.rect(surf,col,pygame.Rect(size+size*offset,0,size*thickness,size),border_radius=int(size*rounded))
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
        draw.rect(surf,col,pygame.Rect(0,0,width,size),border_radius=int(size*rounded))
        return surf
    def rendershapeclock(self,name,size,col,backcol):
        vals = self.getshapedata(name,['hour','minute','minutehandwidth','hourhandwidth','circlewidth'],[0,20,0.05,0.05,0.05])
        hour = vals[0]
        minute = vals[1]
        minutehandwidth = vals[2]
        hourhandwidth = vals[3]
        circlewidth = vals[4]
        surf = pygame.Surface((size+1,size+1))
        surf.fill(backcol)
        draw.circle(surf,col,(size/2,size/2),size/2)
        draw.circle(surf,backcol,(size/2,size/2),size/2-size*circlewidth)
        draw.roundedline(surf,col,(size/2,size/2),(size/2+size*0.4*math.cos(math.pi*2*(minute/60)-math.pi/2),size/2+size*0.4*math.sin(math.pi*2*(minute/60)-math.pi/2)),size*minutehandwidth)
        draw.roundedline(surf,col,(size/2,size/2),(size/2+size*0.25*math.cos(math.pi*2*(hour/12)-math.pi/2),size/2+size*0.25*math.sin(math.pi*2*(hour/12)-math.pi/2)),size*hourhandwidth)
        return surf
    def rendershapeloading(self,name,size,col,backcol):
        vals = self.getshapedata(name,['points','largest','traildrop','spotsize'],[12,0,0.015,0.1])
        points = vals[0]
        largest = vals[1]
        traildrop = vals[2]
        spotsize = vals[3]
        surf = pygame.Surface((size+2,size+2))
        surf.fill(backcol)
        rad = (size/2-spotsize*size)
        for a in range(points):
            draw.circle(surf,col,(size/2+rad*math.sin(math.pi*2*(a-largest)/points)+1,size/2+rad*math.cos(math.pi*2*(a-largest)/points)+1),spotsize*size)
            spotsize-=traildrop
            if spotsize<0:
                break
        return surf
    def rendershapedots(self,name,size,col,backcol):
        vals = self.getshapedata(name,['num','seperation','radius'],[3,0.3,0.1])
        dots = vals[0]
        seperation = vals[1]
        radius = vals[2]
        surf = pygame.Surface(((radius*2+seperation*(dots-1))*size+2,size+2))
        surf.fill(backcol)
        x = radius
        for a in range(dots):
            draw.circle(surf,col,(x*size+1,size/2+1),radius*size)
            x+=seperation
        return surf
    def rendershapetext(self,name,size,col,backcol):
        vals = self.getshapedata(name,['font','bold','italic','strikethrough','underlined','antialias'],
                                 [Style.defaults['font'],False,False,False,False,True])
        font = vals[0]
        bold = vals[1]
        italic = vals[2]
        strikethrough = vals[3]
        underlined = vals[4]
        antialias = vals[5]
        textgen = pygame.font.SysFont(font,int(size),bold,italic)
        try:
            textgen.set_strikethrough(strikethrough)
            textgen.set_underline(underlined)
        except:
            pass
        text = name
        if len([i for i in text if i=='"']) == 2:
            text = name.split('"')[1]
        else:
            text = name.split(' ')[0]
        return textgen.render(text,antialias,col,backcol)
        
        
    def rendershapebezier(self,name,size,col,backcol,failmessage):
        data = [['test thing', [[[(200, 100), (490, 220), (300, 40), (850, 340)], [(850, 340), (300, 200), (450, 350), (340, 430)], [(340, 430), (310, 250), (200, 310), (200, 100)]], [[(380, 440), (540, 360), (330, 240), (850, 370)], [(850, 370), (380, 440)]]]],
                ['search', [[[(300, 350), (150, 200), (350, 0), (500, 150)], [(500, 150), (560, 210), (520, 280), (485, 315)], [(485, 315), (585, 415)], [(585, 415), (625, 455), (595, 485), (555, 445)], [(555, 445), (455, 345)], [(455, 345), (420, 380), (350, 400), (300, 350)], [(300, 350), (325, 325)], [(325, 325), (205, 205), (365, 65), (475, 175)], [(475, 175), (555, 255), (395, 395), (325, 325)], [(325, 325), (300, 350)]]]],
                ['shuffle', [[[(275, 200), (450, 200), (450, 400), (600, 400)], [(600, 400), (600, 350)], [(600, 350), (675, 425)], [(675, 425), (600, 500)], [(600, 500), (600, 450)], [(600, 450), (425, 450), (425, 250), (275, 250)], [(275, 250), (275, 200)]], [[(275, 400), (275, 450)], [(275, 450), (360, 450), (420, 390)], [(420, 390), (385, 345)], [(385, 345), (350, 390), (275, 400)]], [[(600, 250), (600, 300)], [(600, 300), (675, 225)], [(675, 225), (600, 150)], [(600, 150), (600, 200)], [(600, 200), (500, 200), (455, 260)], [(455, 260), (490, 300)], [(490, 300), (530, 255), (600, 250)]]]],
                ['pfp', [[[(340, 430), (710, 430)], [(710, 430), (650, 280), (380, 280), (340, 430)]], [[(510, 280), (400, 280), (400, 50), (630, 50), (630, 280), (510, 280)]]]],
                ['smiley', [[[(560, 460), (310, 460), (310, 40), (810, 40), (810, 460), (560, 460)], [(560, 460), (560, 430)], [(560, 430), (380, 430), (380, 120), (740, 120), (740, 430), (560, 430)], [(560, 430), (560, 460)]], [[(630, 350), (560, 470), (500, 350)], [(500, 350), (560, 420), (630, 350)]], [[(490, 290), (520, 340), (550, 290)], [(550, 290), (520, 280), (490, 290)]], [[(570, 290), (600, 340), (630, 290)], [(630, 290), (600, 280), (570, 290)]]]],
                ['happy face', [[[(560, 460), (310, 460), (310, 40), (810, 40), (810, 460), (560, 460)], [(560, 460), (560, 430)], [(560, 430), (380, 430), (380, 120), (740, 120), (740, 430), (560, 430)], [(560, 430), (560, 460)]], [[(590, 350), (560, 470), (530, 350)], [(530, 350), (570, 360), (590, 350)]], [[(490, 290), (520, 340), (550, 290)], [(550, 290), (520, 280), (490, 290)]], [[(570, 290), (600, 340), (630, 290)], [(630, 290), (600, 280), (570, 290)]]]],
                ['heart', [[[(549, 526), (528, 483), (444, 462), (444, 399)], [(444, 399), (444, 357), (486, 315), (549, 357)], [(549, 357), (612, 315), (654, 357), (654, 399)], [(654, 399), (654, 462), (570, 483), (549, 526)]]]],
                ['mute', [[[(325, 215), (325, 315)], [(325, 315), (325, 325), (335, 325)], [(335, 325), (435, 325)], [(435, 325), (445, 325), (455, 335)], [(455, 335), (535, 415)], [(535, 415), (565, 445), (565, 415)], [(565, 415), (565, 115)], [(565, 115), (565, 85), (535, 115)], [(535, 115), (455, 195)], [(455, 195), (445, 205), (435, 205)], [(435, 205), (335, 205)], [(335, 205), (325, 205), (325, 215)]], [[(705.0, 240.0), (735.0, 210.0), (715.0, 190.0), (685.0, 220.0)], [(685.0, 220.0), (615.0, 290.0)], [(615.0, 290.0), (585.0, 320.0), (605.0, 340.0), (635.0, 310.0)], [(635.0, 310.0), (705.0, 240.0)]], [[(615.0, 240.0), (585.0, 210.0), (605.0, 190.0), (635.0, 220.0)], [(635.0, 220.0), (705.0, 290.0)], [(705.0, 290.0), (735.0, 320.0), (715.0, 340.0), (685.0, 310.0)], [(685.0, 310.0), (615.0, 240.0)]]]],
                ['speaker', [[[(325, 215), (325, 315)], [(325, 315), (325, 325), (335, 325)], [(335, 325), (435, 325)], [(435, 325), (445, 325), (455, 335)], [(455, 335), (535, 415)], [(535, 415), (565, 445), (565, 415)], [(565, 415), (565, 115)], [(565, 115), (565, 85), (535, 115)], [(535, 115), (455, 195)], [(455, 195), (445, 205), (435, 205)], [(435, 205), (335, 205)], [(335, 205), (325, 205), (325, 215)]], [[(665.0, 145.0), (655.0, 135.0), (635.0, 155.0), (645.0, 165.0)], [(645.0, 165.0), (705.0, 235.0), (705.0, 285.0), (645.0, 365.0)], [(645.0, 365.0), (635.0, 375.0), (655.0, 395.0), (665.0, 385.0)], [(665.0, 385.0), (735.0, 305.0), (735.0, 215.0), (665.0, 145.0)]], [[(605.0, 205.0), (595.0, 195.0), (615.0, 175.0), (625.0, 185.0)], [(625.0, 185.0), (665.0, 225.0), (665.0, 305.0), (625.0, 345.0)], [(625.0, 345.0), (615.0, 355.0), (595.0, 335.0), (605.0, 325.0)], [(605.0, 325.0), (635.0, 285.0), (635.0, 245.0), (605.0, 205.0)]]]],
                ['3dots', [[[(385.0, 325.0), (325.0, 325.0), (325.0, 205.0), (445.0, 205.0), (445.0, 325.0), (385.0, 325.0)]], [[(505.0, 325.0), (445.0, 325.0), (445.0, 205.0), (565.0, 205.0), (565.0, 325.0), (505.0, 325.0)]], [[(625.0, 325.0), (565.0, 325.0), (565.0, 205.0), (685.0, 205.0), (685.0, 325.0), (625.0, 325.0)]]]],
                ['pencil', [[[(325, 365), (345, 305)], [(345, 305), (515, 135)], [(515, 135), (555, 175)], [(555, 175), (385, 345)], [(385, 345), (325, 365)], [(325, 365), (345, 345)], [(345, 345), (355, 315)], [(355, 315), (515, 155)], [(515, 155), (535, 175)], [(535, 175), (385, 325)], [(385, 325), (365, 305)], [(365, 305), (355, 315)], [(355, 315), (375, 335)], [(375, 335), (345, 345)], [(345, 345), (325, 365)]]]],
                ['youtube', [[[(295.0, 215.0), (295.0, 185.0), (305.0, 175.0), (345.0, 175.0)], [(345.0, 175.0), (445.0, 175.0)], [(445.0, 175.0), (485.0, 175.0), (495.0, 185.0), (495.0, 215.0)], [(495.0, 215.0), (495.0, 255.0)], [(495.0, 255.0), (495.0, 285.0), (485.0, 295.0), (445.0, 295.0)], [(445.0, 295.0), (345.0, 295.0)], [(345.0, 295.0), (305.0, 295.0), (295.0, 285.0), (295.0, 255.0)], [(295.0, 255.0), (295.0, 235.0)], [(295.0, 235.0), (375.0, 235.0)], [(375.0, 235.0), (375.0, 265.0)], [(375.0, 265.0), (425.0, 235.0)], [(425.0, 235.0), (375.0, 205.0)], [(375.0, 205.0), (375.0, 235.0)], [(375.0, 235.0), (295.0, 235.0)], [(295.0, 235.0), (295.0, 215.0)]]]],
                ['queue', [[[(295.0, 215.0), (295.0, 185.0), (305.0, 175.0), (345.0, 175.0)], [(345.0, 175.0), (445.0, 175.0)], [(445.0, 175.0), (485.0, 175.0), (495.0, 185.0), (495.0, 215.0)], [(495.0, 215.0), (495.0, 255.0)], [(495.0, 255.0), (495.0, 285.0), (485.0, 295.0), (445.0, 295.0)], [(445.0, 295.0), (345.0, 295.0)], [(345.0, 295.0), (305.0, 295.0), (295.0, 285.0), (295.0, 255.0)], [(295.0, 255.0), (295.0, 235.0)], [(295.0, 235.0), (375.0, 235.0)], [(375.0, 235.0), (375.0, 265.0)], [(375.0, 265.0), (425.0, 235.0)], [(425.0, 235.0), (375.0, 205.0)], [(375.0, 205.0), (375.0, 235.0)], [(375.0, 235.0), (295.0, 235.0)], [(295.0, 235.0), (295.0, 215.0)]], [[(345.0, 155.0), (475.0, 155.0)], [(475.0, 155.0), (505.0, 155.0), (515.0, 165.0), (515.0, 195.0)], [(515.0, 195.0), (515.0, 245.0)], [(515.0, 245.0), (515.0, 275.0), (535.0, 275.0), (535.0, 245.0)], [(535.0, 245.0), (535.0, 185.0)], [(535.0, 185.0), (535.0, 155.0), (515.0, 135.0), (485.0, 135.0)], [(485.0, 135.0), (345.0, 135.0)], [(345.0, 135.0), (315.0, 135.0), (315.0, 155.0), (345.0, 155.0)]], [[(515.0, 115.0), (375.0, 115.0)], [(375.0, 115.0), (345.0, 115.0), (345.0, 95.0), (375.0, 95.0)], [(375.0, 95.0), (525.0, 95.0)], [(525.0, 95.0), (555.0, 95.0), (575.0, 115.0), (575.0, 145.0)], [(575.0, 145.0), (575.0, 215.0)], [(575.0, 215.0), (575.0, 245.0), (555.0, 245.0), (555.0, 215.0)], [(555.0, 215.0), (555.0, 155.0)], [(555.0, 155.0), (555.0, 135.0), (545.0, 115.0), (515.0, 115.0)]]]],
                ['star', [[[(425.0, 225.0), (705.0, 225.0)], [(705.0, 225.0), (565.0, 315.0)], [(565.0, 315.0), (425.0, 225.0)]], [[(565.0, 135.0), (475.0, 375.0)], [(475.0, 375.0), (565.0, 315.0)], [(565.0, 315.0), (655.0, 375.0)], [(655.0, 375.0), (565.0, 135.0)]]]],
                ['on', [[[(485.0, 275.0), (445.0, 285.0), (425.0, 345.0), (425.0, 375.0)], [(425.0, 375.0), (425.0, 435.0), (465.0, 485.0), (535.0, 485.0)], [(535.0, 485.0), (605.0, 485.0), (645.0, 435.0), (645.0, 375.0)], [(645.0, 375.0), (645.0, 345.0), (625.0, 285.0), (585.0, 275.0)], [(585.0, 275.0), (565.0, 275.0), (575.0, 295.0)], [(575.0, 295.0), (645.0, 375.0), (645.0, 505.0), (425.0, 505.0), (425.0, 375.0), (495.0, 295.0)], [(495.0, 295.0), (505.0, 275.0), (485.0, 275.0)]], [[(520.0, 315.0), (520.0, 355.0), (550.0, 355.0), (550.0, 315.0)], [(550.0, 315.0), (550.0, 265.0)], [(550.0, 265.0), (550.0, 225.0), (520.0, 225.0), (520.0, 265.0)], [(520.0, 265.0), (520.0, 315.0)]]]],
                ['lock', [[[(285.0, 205.0), (285.0, 115.0), (385.0, 115.0), (385, 205)], [(385, 205), (365.0, 205.0)], [(365.0, 205.0), (365.0, 145.0), (305, 145), (305.0, 205.0)], [(305.0, 205.0), (285.0, 205.0)]], [[(275.0, 205.0), (395, 205)], [(395, 205), (415, 205), (415, 225)], [(415, 225), (415, 305)], [(415, 305), (415, 325), (395, 325)], [(395, 325), (275, 325)], [(275, 325), (255, 325), (255, 305)], [(255, 305), (255, 225)], [(255, 225), (255, 205), (275, 205)], [(275, 205), (335, 225)], [(335, 225), (355, 225), (355, 245)], [(355, 245), (355, 265), (345, 265)], [(345, 265), (355.0, 305.0)], [(355.0, 305.0), (315.0, 305.0)], [(315.0, 305.0), (325, 265)], [(325, 265), (315, 265), (315.0, 245.0)], [(315.0, 245.0), (315.0, 225.0), (335.0, 225.0)], [(335.0, 225.0), (275.0, 205.0)]]]],
                ['splat',[[[[385.0, 265.0], [250.0, 85.0], [475.0, 145.0]], [[475.0, 145.0], [670.0, 115.0], [610.0, 190.0]], [[610.0, 190.0], [730.0, 325.0], [580.0, 340.0]], [[580.0, 340.0], [505.0, 475.0], [475.0, 370.0]], [[475.0, 370.0], [295.0, 490.0], [385.0, 265.0]]]]],
                ['more', [[[(225.0, 175.0), (355.0, 305.0)], [(355.0, 305.0), (415.0, 365.0), (475.0, 305.0)], [(475.0, 305.0), (605.0, 175.0)], [(605.0, 175.0), (625.0, 155.0), (605.0, 135.0)], [(605.0, 135.0), (585.0, 115.0), (565.0, 135.0)], [(565.0, 135.0), (445.0, 255.0)], [(445.0, 255.0), (415.0, 285.0), (385.0, 255.0)], [(385.0, 255.0), (265.0, 135.0)], [(265.0, 135.0), (245.0, 115.0), (225.0, 135.0)], [(225.0, 135.0), (205.0, 155.0), (225.0, 175.0)]]]],
                ['dropdown', [[[(275.0, 125.0), (435.0, 285.0)], [(435.0, 285.0), (595.0, 125.0)], [(595.0, 125.0), (565.0, 95.0)], [(565.0, 95.0), (435.0, 225.0)], [(435.0, 225.0), (305.0, 95.0)], [(305.0, 95.0), (275.0, 125.0)]]]],
                ]
        for a in self.images:
            data.append(a)
        names = [a[0] for a in data]
        splines = []
        for a in names:
            if len(name)>0 and name.split()[0] == a:
                splines = data[names.index(a)][1]
        if splines == []:
            for a in list(self.inbuiltimages):
                if len(name)>0 and name.split()[0] == a:
                    img = self.inbuiltimages[a]
                    sc = size/img.get_height()
                    return pygame.transform.scale(img,(img.get_width()*sc,size)),True,img.get_colorkey()
            return 0,False,backcol
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
                points+=draw.bezierdrawer([((a[c][0]-minus1[0])*mul1,(a[c][1]-minus1[1])*mul1) for c in range(len(a))],0,False,rounded=False)
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
        surf = pygame.Surface((size*((boundingbox[2]-boundingbox[0])/(boundingbox[3]-boundingbox[1]))+2,size+2))
        surf.fill(backcol)
        for b in splines:
            points = []
            for a in b:
                if len(a) == 2: detail = 1
                else: detail = 200
                points+=draw.bezierdrawer([(((a[c][0]-minus1[0])*mul1-minus[0])*mul+1,((a[c][1]-minus1[1])*mul1-minus[1])*mul+1) for c in range(len(a))],0,False,detail=detail,rounded=self.roundedbezier)
            pygame.draw.polygon(surf,col,points)
        return surf,True,backcol
    def addinbuiltimage(self,name,surface):
        self.inbuiltimages[name] = surface
                        
    def getshapedata(self,name,var,defaults):
        vals = defaults
        if sum([a in name for a in var])>0:
            namesplit = name.split()
            for a in namesplit:
                for i,b in enumerate(var):
                    if b == a.split('=')[0]:
                        try:
                            vals[i] = float(a.split('=')[1])
                        except:
                            if str(a.split('=')[1]).lower() == 'true':
                                vals[i] = True
                            elif str(a.split('=')[1]).lower() == 'false':
                                vals[i] = False
                            else:
                                vals[i] = str(a.split('=')[1])
        return vals
    
    def drawtosurf(self,screen,IDlist,surfcol,x,y,displayrect=None,displaymode='render',roundedcorners=0):
        surf = pygame.Surface((self.screenw,self.screenh))
        surf.fill(surfcol)
        surf.set_colorkey(surfcol)
        for a in IDlist:
            if a in self.IDs:
                if displaymode == 'render':
                    self.IDs[a].render(surf)
                else:
                    self.IDs[a].draw(surf)

        draw.blitroundedcorners(surf,screen,x,y,roundedcorners,pygame.Rect(displayrect))
        
    def rendertextlined(self,text,size,col='default',backingcol=(150,150,150),font='default',width=-1,bold=False,antialiasing=True,center=False,spacing=0,imgin=False,img='',scale='default',linelimit=10000,getcords=False,cutstartspaces=False):
        if font=='default': font = Style.defaults['font']
        if col == 'default': col = Style.defaults['textcol']
        if width==-1 and center: center = False
        if scale == 'default': scale = self.scale
        size*=scale
        if width!=-1: width*=scale
        if text == '' and (img == '' or img == 'none'):
            if getcords:
                return pygame.Surface((0,0)),[]
            return pygame.Surface((0,0))
        imgchr = 'ξ'
        imgtracker = 0
        if imgin: texts,imgnames = self.seperatestring(text)
        else:
            texts = [text]
            imgnames = ['']
        ntext = ''
        for i,a in enumerate(texts):
            ntext+=a
            if imgnames[i] != '':
                ntext+=imgchr
                

        imgsurfs = [self.rendershape(imgnames[i],size,col,backcol=backingcol) for i in range(len(imgnames))]
        
        linesimgchr = losslesssplit(ntext,'\n')
        linesimgchrstored = []
        linesrealtext = losslesssplit(text,'\n')
        linesrealtextstored = []
        textgen = pygame.font.SysFont(font,int(size),bold)
        
        textimages = []
        imagesize = [0,0]
        addedlines = 0
        while len(linesimgchr)>0 and addedlines < linelimit:
            newline = ''
            if width!=-1:
                chrwidth = self.gettextsize(linesrealtext[0],font,size,bold,imgin)[0]
                imgtrackeroffset = 0
                while chrwidth>width:
                    split = linesimgchr[0].rsplit(' ',1)
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
                    linesimgchr[0] = replace
                    replace,imgtrackeroffset = self.replaceimgchr(replace,imgchr,imgtracker,imgnames)
                    linesrealtext[0] = replace
                    newline = slide+newline
                    chrwidth = self.gettextsize(linesrealtext[0],font,size,bold,imgin)[0]
                imgtracker+=imgtrackeroffset
            if linesimgchr[0] == '':
                linesimgchr[0] = newline
                newline,_ = self.replaceimgchr(newline,imgchr,imgtracker,imgnames)
                linesrealtext[0] = newline
                newline = ''
            if cutstartspaces and len(linesimgchr[0])>0 and linesimgchr[0][0] == ' ':
                linesimgchr[0] = linesimgchr[0].removeprefix(' ')
                linesrealtext[0] = linesrealtext[0].removeprefix(' ')
            textimages.append(self.rendertext(linesrealtext[0].replace('\n',''),int(size),col,font,bold,antialiasing,backingcol,imgin,img))
            tempsize = (textimages[-1].get_width(),textimages[-1].get_height())
            if tempsize[0]>imagesize[0]: imagesize[0] = tempsize[0]
            imagesize[1]+=tempsize[1]+spacing
            linesimgchrstored.append(linesimgchr[0])
            del linesimgchr[0]
            linesrealtextstored.append(linesrealtext[0][:])
            del linesrealtext[0]
            if newline!='':
                linesimgchr.insert(0,newline)
                newline,_ = self.replaceimgchr(newline,imgchr,imgtracker,imgnames)
                linesrealtext.insert(0,newline)
            elif not ('\n' in text):
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
            cords = self.textlinedcordgetter(center,imagesize,textimages,linesimgchrstored,textgen,spacing,width,imgsurfs,linesrealtextstored,imgchr,imgnames,size,font,bold)
            return surf,cords
        return surf
    
    def textlinedcordgetter(self,center,imagesize,textimages,linesimgchrstored,textgen,spacing,width,imgsurfs,linesrealtextstored,imgchr,imgnames,size,font,bold):
        rowstart = []
        if center:
            for a in linesrealtextstored:
                rowstart.append(int(width/2)-int(textgen.size(a)[0]/2))
        else: rowstart = [0 for a in range(len(linesrealtextstored))]
        yinc = 0
        corddata = []
        noffset = 0
        nsize = textgen.size('\n')[0]
        imgtracker = 0
        for i,a in enumerate(linesimgchrstored):
            if a[:1] == '\n': noffset = nsize
            else: noffset = 0
            corddata.append([])
            inc = 0
            for b in range(len(a)):
                b+=inc
                extend = False
                if a[b] == imgchr:
                    a = a.replace(imgchr,'{'+imgnames[imgtracker]+'}',1)
                    inc+=len(imgnames[imgtracker])+1
                    b+=len(imgnames[imgtracker])+1
                    lettersize = imgsurfs[imgtracker].get_size()
                    imgtracker+=1
                    extend = True
                else:
                    lettersize = textgen.size(a[b])
                if inc == 0:
                    linesize = textgen.size(a[:b+1])
                else:
                    swapped = a[:b+1]
                    linesize = self.gettextsize(swapped,font,size,bold)
                corddata[-1].append([a[b],[rowstart[i]+linesize[0]-lettersize[0]/2-noffset,yinc+lettersize[1]/2],lettersize])
                if extend:
                    del corddata[-1][-1]
                    for c in range(len(imgnames[imgtracker-1])+1,-1,-1):
                        corddata[-1].append([a[b-c],[rowstart[i]+linesize[0]-lettersize[0]/2-noffset,yinc+lettersize[1]/2],lettersize])
            if len(corddata[-1]) != 0:
                ypoint = max([c[1][1] for c in corddata[-1]])
                for c in corddata[-1]:
                    c[1][1] = ypoint
                    
                yinc+=linesize[1]+spacing
        return corddata
    def gettextsize(self,text,font,textsize,bold=False,imgin=True):
        textgen = pygame.font.SysFont(font,int(textsize),bold)
        if imgin:
            texts,imgnames = self.seperatestring(text)
        else:
            texts = [text]
            imgnames = ['']
        size = [0,0]
        for a in range(len(texts)):
            if texts[a] != '':
                addon = textgen.size(texts[a])
                size[0]+=addon[0]
                size[1] = max(size[1],addon[1])
            if imgnames[a] != '':
                addon = self.rendershape(imgnames[a],textsize,(150,150,150),False,(0,0,0)).get_size()
                size[0]+=addon[0]
                size[1] = max(size[1],addon[1])
            
        return size
    def replaceimgchr(self,line,imgchr,imgtracker,imgnames):
        count = 0
        while line.count(imgchr) != 0:
            line = line.replace(imgchr,'{'+imgnames[imgtracker+count]+'}',1)
            if imgtracker+count!=len(imgnames)-1:
                count+=1
        return line,count
        

    def addid(self,ID,obj,refitems=True):
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
        if type(obj) == MENU:
            self.automenus.append(obj)
        else:
            if type(obj) == BUTTON: self.buttons.append(obj)
            elif type(obj) == TEXTBOX: self.textboxes.append(obj)
            elif type(obj) in [TABLE,SCROLLERTABLE]: self.tables.append(obj)
            elif type(obj) == DROPDOWN: self.dropdowns.append(obj)
            elif type(obj) == TEXT: self.texts.append(obj)
            elif type(obj) == SCROLLER: self.scrollers.append(obj)
            elif type(obj) == SLIDER: self.sliders.append(obj)
            elif type(obj) == WINDOWEDMENU: self.windowedmenus.append(obj)
            elif type(obj) == WINDOW: self.windows.append(obj)
            elif type(obj) == ANIMATION: self.animations.append(obj)
            elif type(obj) == RECT: self.rects.append(obj)
            self.refreshitems()
        if not type(obj) in [ANIMATION,MENU] and menuin(obj.truemenu,self.windowedmenunames):
            for b in obj.truemenu:
                if b in self.windowedmenunames:
                    valid = True
                    for a in obj.master:
                        if type(a) in [BUTTON,TEXTBOX,TEXT,TABLE,SCROLLERTABLE,SCROLLER,SLIDER,RECT]:
                            valid = False
                    if valid:
                        self.windowedmenus[self.windowedmenunames.index(b)].binditem(obj,False,False)
    def reID(self,ID,obj):
        newid = ID
        if ID in self.IDs:
            adder = 1
            ID+=str(adder)
            while ID in self.IDs:
                ID = ID.removesuffix(str(adder))
                adder+=1
                ID+=str(adder)
        self.IDs[newid] = self.IDs.pop(obj.ID)
        obj.ID = newid
    def refreshitems(self):
        self.items = self.buttons+self.textboxes+self.tables+self.texts+self.scrollers+self.sliders+self.windowedmenus+self.rects+self.dropdowns+self.windows
        for a in self.items:
            if len(a.master)<len(a.truemenu) or not a.onitem:
                menu = a.truemenu
                for m in menu:
                    if not(m in self.windowedmenunames):
                        if not('auto_generate_menu:'+m in self.IDs):
                            obj = self.automakemenu(m)
                        else:
                            obj = self.IDs['auto_generate_menu:'+m]
                        obj.binditem(a,False,False)
        self.items+=self.automenus
        self.items.sort(key=lambda x: x.layer,reverse=False)
    def refreshnoclickrects(self):
        self.noclickrects = []
        for a in self.items:
            a.noclickrectsapplied = []
            self.noclickrects+=a.noclickrect
        # Rect,IDs,menu,whitelist (true=all objects in list blocked by noclickrect)
        for a in self.noclickrects:
            objs = self.onmenu(a[2])
            if a[3]:
                for b in objs:
                    if b.ID in a[1]:
                        b.noclickrectsapplied.append(a[0])
            else:
                for b in objs:
                    if not b.ID in a[1]:
                        b.noclickrectsapplied.append(a[0])
            
    def printtree(self,obj=False):
        if type(obj) == str: obj = self.IDs[obj]
        prefixes = ['<{-=-{=-[=]-=}-=-}>','#@'*5,'<=>'*3,'+='*3,'--','']
        if obj == False:
            depth = max([self.gettreedepth(a) for a in self.automenus+self.windowedmenus])
            prefixes = prefixes[(6-depth):]
            for a in self.automenus+self.windowedmenus:
                self.printbound(a,prefixes)
        else:
            prefixes = prefixes[(6-self.gettreedepth(obj)):]
            self.printbound(obj,prefixes)
    def printbound(self,obj,prefixes):
        if prefixes[0] == '': print(obj.ID)
        else: print(prefixes[0],obj.ID)
        for a in obj.bounditems:
            self.printbound(a,prefixes[1:])
    def gettreedepth(self,obj,depth=1):
        ndepths = [depth]
        if len(obj.bounditems)>0:
            depth+=1
            ndepths = []
            for a in obj.bounditems:
                ndepths.append(self.gettreedepth(a,depth))
        return max(ndepths)
    
        
    def makebutton(self,x,y,text,textsize=-1,command=emptyfunction,menu='main',ID='button',layer=1,roundedcorners=-1,bounditems=[],killtime=-1,width=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=-1,centery=-1,img='none',font=-1,bold=-1,antialiasing=-1,pregenerated=True,enabled=True,
                 border=-1,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=-1,glowcol=-1,
                 runcommandat=0,col=-1,textcol=-1,backingcol=-1,bordercol=-1,hovercol=-1,clickdownsize=-1,clicktype=-1,textoffsetx=-1,textoffsety=-1,maxwidth=-1,
                 dragable=False,colorkey=-1,toggle=True,toggleable=False,toggletext=-1,toggleimg='none',togglecol=-1,togglehovercol=-1,bindtoggle=[],spacing=-1,verticalspacing=-1,horizontalspacing=-1,clickablerect=-1,clickableborder=-1,
                 backingdraw=-1,borderdraw=-1,animationspeed=-1,linelimit=1000,refreshbind=[]):
        if maxwidth == -1: maxwidth = width
        if backingcol == -1: backingcol = bordercol
        obj = BUTTON(ui=self,x=x,y=y,width=width,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,killtime=killtime,
                     anchor=anchor,objanchor=objanchor,center=center,centery=centery,text=str(text),textsize=textsize,img=img,font=font,bold=bold,antialiasing=antialiasing,pregenerated=pregenerated,enabled=enabled,
                     border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                     command=command,runcommandat=runcommandat,col=col,textcol=textcol,backingcol=backingcol,hovercol=hovercol,clickdownsize=clickdownsize,clicktype=clicktype,textoffsetx=textoffsetx,textoffsety=textoffsety,maxwidth=maxwidth,
                     dragable=dragable,colorkey=colorkey,toggle=toggle,toggleable=toggleable,toggletext=toggletext,toggleimg=toggleimg,togglecol=togglecol,togglehovercol=togglehovercol,bindtoggle=bindtoggle,spacing=spacing,verticalspacing=verticalspacing,horizontalspacing=horizontalspacing,clickablerect=clickablerect,clickableborder=clickableborder,
                     animationspeed=animationspeed,backingdraw=backingdraw,borderdraw=borderdraw,linelimit=linelimit,refreshbind=refreshbind)
        return obj
    def makecheckbox(self,x,y,textsize=-1,command=emptyfunction,menu='main',ID='checkbox',text='{tick}',layer=1,roundedcorners=0,bounditems=[],killtime=-1,width=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,img='none',font=-1,bold=-1,antialiasing=-1,pregenerated=True,enabled=True,
                 border=4,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=-1,glowcol=-1,
                 runcommandat=0,col=-1,textcol=-1,backingcol=-1,bordercol=-1,hovercol=-1,clickdownsize=-1,clicktype=-1,textoffsetx=-1,textoffsety=-1,maxwidth=-1,
                 dragable=False,colorkey=-1,toggle=True,toggleable=True,toggletext='',toggleimg='none',togglecol=-1,togglehovercol=-1,bindtoggle=[],spacing=-1,verticalspacing=-1,horizontalspacing=-1,clickablerect=-1,clickableborder=10,
                 backingdraw=False,borderdraw=-1,animationspeed=-1,linelimit=1000,refreshbind=[]):
        if textsize == -1: textsize = Style.defaults['textsize']
        if spacing == -1: spacing = -int(textsize/5)
        if width == -1: width = textsize+spacing*2
        if height == -1: height = textsize+spacing*2
        obj = BUTTON(ui=self,x=x,y=y,width=width,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,killtime=killtime,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,text=text,textsize=textsize,img=img,font=font,bold=bold,antialiasing=antialiasing,pregenerated=pregenerated,enabled=enabled,
                 border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                 command=command,runcommandat=runcommandat,col=col,textcol=textcol,backingcol=backingcol,hovercol=hovercol,clickdownsize=clickdownsize,clicktype=clicktype,textoffsetx=textoffsetx,textoffsety=textoffsety,maxwidth=maxwidth,
                 dragable=dragable,colorkey=colorkey,toggle=toggle,toggleable=toggleable,toggletext=toggletext,toggleimg=toggleimg,togglecol=togglecol,togglehovercol=togglehovercol,bindtoggle=bindtoggle,
                 spacing=spacing,verticalspacing=verticalspacing,horizontalspacing=horizontalspacing,clickablerect=clickablerect,clickableborder=clickableborder,
                 animationspeed=animationspeed,backingdraw=backingdraw,borderdraw=borderdraw,linelimit=linelimit,refreshbind=refreshbind)
        return obj
    def maketextbox(self,x,y,text='',width=200,lines=-1,menu='main',command=emptyfunction,ID='textbox',layer=1,roundedcorners=-1,bounditems=[],killtime=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=-1,centery=-1,img='none',textsize=-1,font=-1,bold=-1,antialiasing=-1,pregenerated=True,enabled=True,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=-1,glowcol=-1,
                 runcommandat=0,col=-1,textcol=-1,backingcol=-1,hovercol=-1,clickdownsize=4,clicktype=0,textoffsetx=-1,textoffsety=-1,
                 colorkey=-1,spacing=-1,verticalspacing=-1,horizontalspacing=-1,clickablerect=-1,
                 linelimit=100,selectcol=-1,selectbordersize=2,selectshrinksize=0,cursorsize=-1,textcenter=-1,chrlimit=10000,numsonly=False,enterreturns=False,commandifenter=True,commandifkey=False,imgdisplay=False,
                 backingdraw=-1,borderdraw=-1,refreshbind=[]):
        
        if col == -1: col = Style.objectdefaults[TEXTBOX]['col']
        if backingcol == -1: backingcol = autoshiftcol(Style.objectdefaults[TEXTBOX]['backingcol'],col,-20)
        
        obj = TEXTBOX(ui=self,x=x,y=y,width=width,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,killtime=killtime,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,text=text,textsize=textsize,img=img,font=font,bold=bold,antialiasing=antialiasing,pregenerated=pregenerated,enabled=enabled,
                 border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                 command=command,runcommandat=runcommandat,col=col,textcol=textcol,backingcol=backingcol,hovercol=hovercol,clickdownsize=clickdownsize,clicktype=clicktype,textoffsetx=textoffsetx,textoffsety=textoffsety,
                 colorkey=colorkey,spacing=spacing,verticalspacing=verticalspacing,horizontalspacing=horizontalspacing,clickablerect=clickablerect,
                 lines=lines,linelimit=linelimit,selectcol=selectcol,selectbordersize=selectbordersize,selectshrinksize=selectshrinksize,cursorsize=cursorsize,textcenter=textcenter,chrlimit=chrlimit,numsonly=numsonly,enterreturns=enterreturns,commandifenter=commandifenter,commandifkey=commandifkey,imgdisplay=imgdisplay,
                 backingdraw=backingdraw,borderdraw=borderdraw,refreshbind=refreshbind)
        return obj
            
            
##    def maketable(self,x,y,data='empty',titles=[],menu='main',menuexceptions=[],edgebound=(1,0,0,1),rows=5,colomns=3,boxwidth=-1,boxheight=-1,spacing=10,col='default',boxtextcol='default',boxtextsize=40,boxcenter=True,font='default',bold=False,titlefont=-1,titlebold=-1,titleboxcol=-1,titletextcol='default',titletextsize=-1,titlecenter=True,linesize=2,linecol=-1,roundedcorners=0,layer=1,ID='default',returnobj=False):

    def maketable(self,x,y,data=[],titles=[],menu='main',ID='table',layer=1,roundedcorners=-1,bounditems=[],killtime=-1,width=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=-1,centery=-1,text='',textsize=-1,img='none',font=-1,bold=-1,antialiasing=-1,pregenerated=True,enabled=True,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=-1,glowcol=-1,
                 command=emptyfunction,runcommandat=0,col=-1,textcol=-1,backingcol=-1,hovercol=-1,clickdownsize=4,clicktype=0,textoffsetx=-1,textoffsety=-1,
                 dragable=False,colorkey=-1,spacing=-1,verticalspacing=-1,horizontalspacing=-1,clickablerect=-1,
                 boxwidth=-1,boxheight=-1,linesize=2,textcenter=-1,guesswidth=-1,guessheight=-1,
                 backingdraw=-1,borderdraw=-1,refreshbind=[]):

        if col == -1: col = Style.objectdefaults[TABLE]['col']
        if backingcol == -1: backingcol = autoshiftcol(Style.objectdefaults[TABLE]['backingcol'],col,-20)
        
        #obj = TABLE(x,y,rows,colomns,data,titles,boxwidth,boxheight,spacing,menu,menuexceptions,boxcol,boxtextcol,boxtextsize,boxcenter,font,bold,titlefont,titlebold,titleboxcol,titletextcol,titletextsize,titlecenter,linesize,linecol,roundedcorners,layer,ID,self)
        obj = TABLE(ui=self,x=x,y=y,width=width,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,killtime=killtime,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,text=text,textsize=textsize,img=img,font=font,bold=bold,antialiasing=antialiasing,pregenerated=pregenerated,enabled=enabled,
                 border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                 command=command,runcommandat=runcommandat,col=col,textcol=textcol,backingcol=backingcol,hovercol=hovercol,clickdownsize=clickdownsize,clicktype=clicktype,textoffsetx=textoffsetx,textoffsety=textoffsety,
                 colorkey=colorkey,spacing=spacing,verticalspacing=verticalspacing,horizontalspacing=horizontalspacing,clickablerect=clickablerect,
                 data=data,titles=titles,boxwidth=boxwidth,boxheight=boxheight,linesize=linesize,textcenter=textcenter,guesswidth=guesswidth,guessheight=guessheight,
                 backingdraw=backingdraw,borderdraw=borderdraw,refreshbind=refreshbind)
        return obj
            
##    def maketext(self,x,y,text,size,menu='main',menuexceptions=[],edgebound=(1,0,0,1),col='default',center=True,font='default',bold=False,maxwidth=-1,border=4,backingcol='default',backingdraw=0,backingwidth=-1,backingheight=-1,img='none',colorkey=(255,255,255),roundedcorners=0,layer=1,ID='default',antialiasing=True,pregenerated=True,returnobj=False):
    def maketext(self,x,y,text,textsize=-1,menu='main',ID='text',layer=1,roundedcorners=-1,bounditems=[],killtime=-1,width=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=-1,centery=-1,img='none',font=-1,bold=-1,antialiasing=-1,pregenerated=True,enabled=True,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=0,glowcol=-1,
                 command=emptyfunction,runcommandat=0,col=-1,textcol=-1,clicktype=0,backingcol=-1,bordercol=-1,textoffsetx=-1,textoffsety=-1,
                 dragable=False,colorkey=-1,spacing=-1,verticalspacing=-1,horizontalspacing=-1,maxwidth=-1,animationspeed=-1,clickablerect=-1,
                 textcenter=-1,backingdraw=-1,borderdraw=-1,refreshbind=[]):
        if col == -1: col = backingcol
        if col == -1: col = Style.wallpapercol
        backingcol = bordercol
        
        obj = TEXT(ui=self,x=x,y=y,width=width,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,killtime=killtime,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,text=str(text),textsize=textsize,img=img,font=font,bold=bold,antialiasing=antialiasing,pregenerated=pregenerated,enabled=enabled,
                 border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                 command=command,runcommandat=runcommandat,col=col,textcol=textcol,backingcol=backingcol,clicktype=clicktype,textoffsetx=textoffsetx,textoffsety=textoffsety,maxwidth=maxwidth,
                 dragable=dragable,colorkey=colorkey,spacing=spacing,verticalspacing=verticalspacing,horizontalspacing=horizontalspacing,clickablerect=clickablerect,
                 textcenter=textcenter,backingdraw=backingdraw,borderdraw=borderdraw,animationspeed=animationspeed,refreshbind=refreshbind)
        return obj

##    def makescroller(self,x,y,height,command=emptyfunction,width=15,minh=0,maxh=-1,pageh=100,starth=0,menu='main',menuexceptions=[],edgebound=(1,0,0,1),col='default',scrollercol=-1,hovercol=-1,clickcol=-1,scrollerwidth=11,runcommandat=1,clicktype=0,layer=1,ID='default',returnobj=False):
    def makescroller(self,x,y,height,command=emptyfunction,width=15,minp=0,maxp=100,pageheight=15,menu='main',ID='scroller',layer=1,roundedcorners=-1,bounditems=[],killtime=-1,
                 anchor=(0,0),objanchor=(0,0),center=-1,centery=-1,enabled=True,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=-1,glowcol=-1,
                 runcommandat=1,col=-1,backingcol=-1,clicktype=0,clickablerect=-1,scrollbind=[],
                 dragable=True,backingdraw=-1,borderdraw=-1,scrollercol=-1,increment=0,startp=0,refreshbind=[],screencompressed=False):

        if maxp == -1: maxp = height
        
        obj = SCROLLER(ui=self,x=x,y=y,width=width,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,killtime=killtime,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,enabled=enabled,
                 border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                 command=command,runcommandat=runcommandat,col=col,backingcol=backingcol,clicktype=clicktype,
                 dragable=dragable,backingdraw=backingdraw,borderdraw=borderdraw,clickablerect=clickablerect,scrollbind=scrollbind,
                 increment=increment,minp=minp,maxp=maxp,startp=startp,pageheight=pageheight,refreshbind=refreshbind,screencompressed=screencompressed)
        return obj

##    def makeslider(self,x,y,width,height,maxp=100,menu='main',command=emptyfunction,menuexceptions=[],edgebound=(1,0,0,1),col='default',slidercol=-1,sliderbordercol=-1,hovercol=-1,clickcol=-1,clickdownsize=2,bordercol=-1,border=2,slidersize=-1,increment=0,img='none',colorkey=(255,255,255),minp=0,startp=0,style='square',roundedcorners=0,barroundedcorners=-1,dragable=True,runcommandat=1,clicktype=0,layer=1,ID='default',returnobj=False):
    def makeslider(self,x,y,width,height,maxp=100,menu='main',command=emptyfunction,ID='slider',layer=1,roundedcorners=-1,bounditems=[],boundtext=-1,killtime=-1,
                 anchor=(0,0),objanchor=(0,0),center=-1,centery=-1,enabled=True,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=-1,glowcol=-1,
                 runcommandat=1,col=-1,backingcol=-1,button='default',clickablerect=-1,
                 dragable=True,colorkey=(255,255,255),backingdraw=-1,borderdraw=-1,
                 slidersize=-1,increment=0,sliderroundedcorners=-1,minp=0,startp=0,direction='horizontal',containedslider=-1,movetoclick=-1,refreshbind=[]):
        if boundtext!=-1:
            bounditems.append(boundtext)
        obj = SLIDER(ui=self,x=x,y=y,width=width,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,killtime=killtime,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,enabled=enabled,
                 border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                 command=command,runcommandat=runcommandat,col=col,backingcol=backingcol,clickablerect=clickablerect,
                 dragable=dragable,colorkey=colorkey,backingdraw=backingdraw,borderdraw=borderdraw,
                 slidersize=slidersize,increment=increment,sliderroundedcorners=sliderroundedcorners,minp=minp,maxp=maxp,startp=startp,direction=direction,containedslider=containedslider,data=button,movetoclick=movetoclick,refreshbind=refreshbind)
        obj.boundtext = boundtext
        if type(boundtext) == TEXTBOX:
            boundtext.slider = obj
        obj.updatetext()
        return obj
 
##    def makewindowedmenu(self,x,y,width,height,menu,behindmenu,edgebound=(1,0,0,1),col='default',isolated=True,roundedcorners=0,darken=60,colourkey=(243,244,242),ID='default'):
    def makewindowedmenu(self,x,y,width,height,menu,behindmenu='main',col=-1,bounditems=[],
                 dragable=False,colorkey=(255,255,255),isolated=True,darken=-1,ID='windowedmenu',layer=1,roundedcorners=-1,
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,enabled=True,glow=-1,glowcol=-1,
                 scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,command=emptyfunction,runcommandat=0,refreshbind=[]):

        if col == -1: col = shiftcolor(Style.objectdefaults[WINDOWEDMENU]['col'],-35)

        self.windowedmenunames = [a.menu for a in self.windowedmenus]
        self.windowedmenunames.append(menu)
        
        obj = WINDOWEDMENU(ui=self,x=x,y=y,width=width,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,
                 scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,
                 command=emptyfunction,runcommandat=runcommandat,col=col,
                 dragable=dragable,colorkey=colorkey,border=0,enabled=enabled,
                 behindmenu=behindmenu,isolated=isolated,darken=darken,refreshbind=refreshbind)
        return obj
    def makewindow(self,x,y,width,height,menu='main',col=-1,bounditems=[],colorkey=(255,255,255),
                   ID='window',layer=10,roundedcorners=-1,anchor=(0,0),objanchor=(0,0),isolated=True,darken=-1,
                   center=False,centery=-1,enabled=False,glow=-1,glowcol=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,
                   refreshbind=[],clickablerect=(0,0,'w','h'),animationspeed=-1,animationtype='moveup'):

        if col == -1: col = shiftcolor(Style.objectdefaults[WINDOW]['col'],-35)
        
        obj = WINDOW(ui=self,x=x,y=y,width=width,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,enabled=enabled,
                 scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,col=col,colorkey=colorkey,
                 refreshbind=refreshbind,isolated=isolated,darken=darken,clickablerect=clickablerect,animationspeed=animationspeed,animationtype=animationtype)
        return obj
    
    def makerect(self,x,y,width,height,command=emptyfunction,menu='main',ID='button',layer=1,roundedcorners=-1,bounditems=[],killtime=-1,
                 anchor=(0,0),objanchor=(0,0),center=-1,centery=-1,enabled=True,
                 border=0,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=-1,glowcol=-1,
                 runcommandat=0,col=-1,dragable=False,backingdraw=-1,refreshbind=[]):
        obj = RECT(ui=self,x=x,y=y,command=emptyfunction,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,killtime=killtime,width=width,height=height,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,enabled=enabled,
                 border=border,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                 runcommandat=runcommandat,col=col,dragable=dragable,backingdraw=backingdraw,refreshbind=refreshbind)
        return obj
    def makecircle(self,x,y,radius,command=emptyfunction,menu='main',ID='button',layer=1,roundedcorners=-1,bounditems=[],killtime=-1,
                 anchor=(0,0),objanchor=(0,0),center=-1,centery=-1,enabled=True,
                 border=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=-1,glowcol=-1,
                 runcommandat=0,col=-1,dragable=False,backingdraw=-1,refreshbind=[]):
        if roundedcorners==-1: roundedcorners=radius
        obj = self.makerect(x=x,y=y,width=radius*2,height=radius*2,command=command,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,killtime=killtime,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,enabled=enabled,
                 border=border,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                 runcommandat=runcommandat,col=col,dragable=dragable,backingdraw=backingdraw,refreshbind=refreshbind)
        return obj
        
    def makesearchbar(self,x,y,text='Search',width=400,lines=1,menu='main',command=emptyfunction,ID='searchbar',layer=1,roundedcorners=-1,bounditems=[],killtime=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=-1,centery=-1,img='none',textsize=-1,font=-1,bold=-1,antialiasing=-1,pregenerated=True,enabled=True,
                 border=3,upperborder=-1,lowerborder=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=0,glowcol=-1,
                 runcommandat=0,col=-1,textcol=-1,titletextcol=-1,backingcol=-1,hovercol=-1,clickdownsize=-1,clicktype=0,textoffsetx=-1,textoffsety=-1,
                 colorkey=-1,spacing=-1,verticalspacing=1,horizontalspacing=4,clickablerect=-1,
                 linelimit=100,selectcol=-1,selectbordersize=2,selectshrinksize=0,cursorsize=-1,textcenter=-1,chrlimit=10000,numsonly=False,enterreturns=False,commandifenter=True,commandifkey=False,imgdisplay=-1,
                 backingdraw=-1,borderdraw=-1,refreshbind=[]):

        if titletextcol == -1: titletextcol = textcol
        if upperborder == -1: upperborder = border
        if lowerborder == -1: lowerborder = border
        if textsize == -1: textsize = Style.defaults['textsize']
        if height == -1:
            heightgetter = self.rendertext('Tg',textsize,(255,255,255),font,bold)
            height = upperborder+lowerborder+heightgetter.get_height()*lines+verticalspacing*2
        col = autoshiftcol(col,Style.defaults['col'])
        if backingcol == -1: backingcol = autoshiftcol(Style.defaults['backingcol'],col,20)
        
        txt = self.maketext(int(border+horizontalspacing)/2,0,text,textsize,anchor=(0,'h/2'),objanchor=(0,'h/2'),img=img,font=font,bold=bold,antialiasing=antialiasing,pregenerated=pregenerated,enabled=enabled,textcol=titletextcol,col=autoshiftcol(backingcol,col,-20),animationspeed=5)
        
        bsize = height-upperborder-lowerborder
        search = self.makebutton(-border*2-bsize,0,'{search}',textsize*0.55,command=command,roundedcorners=roundedcorners,width=bsize,height=bsize,
                 anchor=('w','h/2'),objanchor=('w','h/2'),border=0,col=col,textcol=textcol,backingcol=backingcol,bordercol=col,
                 clickdownsize=1,textoffsetx=0,textoffsety=0,spacing=2,clickablerect=clickablerect,hovercol=autoshiftcol(hovercol,col,-6),borderdraw=False)
        cross = self.makebutton(-border,0,'{cross}',textsize*0.5,command=emptyfunction,roundedcorners=roundedcorners,width=bsize,height=bsize,
                 anchor=('w','h/2'),objanchor=('w','h/2'),border=0,col=col,textcol=textcol,backingcol=backingcol,bordercol=col,
                 clickdownsize=1,textoffsetx=1,textoffsety=1,spacing=2,clickablerect=clickablerect,hovercol=autoshiftcol(hovercol,col,-6),borderdraw=False)

        obj = self.maketextbox(x,y,'',width,lines,menu,command,ID,layer,roundedcorners,bounditems+[txt,search,cross],killtime,height,
                 anchor,objanchor,center,centery,img,textsize,font,bold,antialiasing,pregenerated,enabled,
                 border,upperborder,lowerborder,bsize*2+border*3,txt.textimage.get_width()+border+horizontalspacing*2,scalesize,scalex,scaley,scaleby,glow,glowcol,
                 runcommandat,col,textcol,backingcol,hovercol,clickdownsize,clicktype,textoffsetx,textoffsety,
                 colorkey,spacing,verticalspacing,horizontalspacing,clickablerect,
                 linelimit,selectcol,selectbordersize,selectshrinksize,cursorsize,textcenter,chrlimit,numsonly,enterreturns,commandifenter,commandifkey,imgdisplay,
                 backingdraw,borderdraw,refreshbind)

        cross.command = lambda: obj.settext('')
        return obj

    def makescrollertable(self,x,y,data=[],titles=[],menu='main',ID='scrollertable',layer=1,roundedcorners=-1,bounditems=[],killtime=-1,width=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=-1,centery=-1,text='',textsize=-1,img='none',font=-1,bold=-1,antialiasing=-1,pregenerated=True,enabled=True,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=-1,glowcol=-1,
                 command=emptyfunction,runcommandat=0,col=-1,textcol=-1,backingcol=-1,hovercol=-1,clickdownsize=4,clicktype=0,textoffsetx=-1,textoffsety=-1,
                 dragable=False,colorkey=-1,spacing=-1,verticalspacing=-1,horizontalspacing=-1,clickablerect=(0,0,'w','h'),
                 boxwidth=-1,boxheight=-1,linesize=2,textcenter=-1,guesswidth=-1,guessheight=-1,
                 backingdraw=-1,borderdraw=-1,pageheight=-1,refreshbind=[],compress=True,scrollerwidth=15,screencompressed=5):
        
        if col == -1: col = Style.objectdefaults[TABLE]['col']
        if backingcol == -1: backingcol = autoshiftcol(Style.objectdefaults[TABLE]['backingcol'],col,-20)
        
        obj = SCROLLERTABLE(ui=self,x=x,y=y,width=width,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,killtime=killtime,
                 anchor=anchor,objanchor=objanchor,center=center,centery=centery,text=text,textsize=textsize,img=img,font=font,bold=bold,antialiasing=antialiasing,pregenerated=pregenerated,enabled=enabled,
                 border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                 command=command,runcommandat=runcommandat,col=col,textcol=textcol,backingcol=backingcol,hovercol=hovercol,clickdownsize=clickdownsize,clicktype=clicktype,textoffsetx=textoffsetx,textoffsety=textoffsety,
                 colorkey=colorkey,spacing=spacing,verticalspacing=verticalspacing,horizontalspacing=horizontalspacing,clickablerect=clickablerect,
                 data=data,titles=titles,boxwidth=boxwidth,boxheight=boxheight,linesize=linesize,textcenter=textcenter,guesswidth=guesswidth,guessheight=guessheight,
                 backingdraw=backingdraw,borderdraw=borderdraw,refreshbind=refreshbind,scroller=emptyobject(0,0,15,15),compress=compress)
        if len(titles) != 0 and clickablerect == (0,0,'w','h'):
            obj.startclickablerect = (0,f'(ui.IDs["{obj.ID}"].boxheights[0]+ui.IDs["{obj.ID}"].linesize*2)*ui.IDs["{obj.ID}"].scale','w',f'h-(ui.IDs["{obj.ID}"].boxheights[0]-ui.IDs["{obj.ID}"].linesize*2)')
        if pageheight == -1:
            pageheight = self.IDs[obj.ID].height
        obj.startpageheight = pageheight
        obj.autoscale()
        scroller = self.makescroller(x=border,y=0,width=scrollerwidth,height=f'ui.IDs["{obj.ID}"].pageheight',menu=menu,ID=obj.ID+'scroller',layer=layer,roundedcorners=roundedcorners,bounditems=bounditems,killtime=killtime,
                 anchor=('w',0),objanchor=(0,0),enabled=enabled,
                 border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                 col=col,backingcol=backingcol,clicktype=clicktype,
                 backingdraw=backingdraw,borderdraw=borderdraw,clickablerect=-1,scrollbind=[],screencompressed=screencompressed,
                 increment=0,minp=0,maxp=f"ui.IDs['{obj.ID}'].height",startp=0,pageheight=f'ui.IDs["{obj.ID}"].pageheight')
        scroller.command = lambda: obj.scrollerblocks(scroller)
        obj.refreshbind.append(scroller.ID)
        obj.binditem(scroller)
        obj.scroller = scroller
        scroller.resetcords()
        return obj
    def makedropdown(self,x,y,options: list,textsize=-1,command=emptyfunction,menu='main',ID='dropdown',layer=1,roundedcorners=-1,bounditems=[],killtime=-1,width=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=-1,centery=-1,img='none',font=-1,bold=-1,antialiasing=-1,pregenerated=True,enabled=True,pageheight=300,
                 border=3,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=-1,glowcol=-1,
                 runcommandat=0,col=-1,textcol=-1,backingcol=-1,bordercol=-1,hovercol=-1,clickdownsize=-1,clicktype=-1,textoffsetx=-1,textoffsety=-1,maxwidth=-1,
                 dragable=False,colorkey=-1,toggle=True,toggleable=False,toggletext=-1,toggleimg='none',togglecol=-1,togglehovercol=-1,bindtoggle=[],spacing=-1,verticalspacing=1,horizontalspacing=4,clickablerect=-1,clickableborder=-1,
                 backingdraw=-1,borderdraw=-1,linelimit=1000,refreshbind=[],animationspeed=15,animationtype='compressleft',startoptionindex=0):

        if options == []: options = ['text']
        text = options[startoptionindex]
        if textsize == -1: textsize = Style.defaults['textsize']
        
        if upperborder == -1: upperborder = border
        if lowerborder == -1: lowerborder = border
        if height == -1:
            heightgetter = self.rendertext('Tg',textsize,(255,255,255),font,bold)
            height = upperborder+lowerborder+heightgetter.get_height()
        col = autoshiftcol(col,Style.defaults['col'])

        txt = self.maketext(int(border+horizontalspacing)/2,0,text,textsize,anchor=(0,'h/2'),objanchor=(0,'h/2'),
                             img=img,font=font,bold=bold,antialiasing=antialiasing,pregenerated=pregenerated,
                             enabled=enabled,textcol=textcol,col=autoshiftcol(backingcol,col,20),animationspeed=5,roundedcorners=roundedcorners)
        
        obj = DROPDOWN(ui=self,x=x,y=y,width=-1,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=[txt]+bounditems,killtime=killtime,
                       anchor=anchor,objanchor=objanchor,center=center,centery=centery,text='{more scale=0.3}',textsize=textsize,img=img,font=font,bold=bold,antialiasing=antialiasing,pregenerated=pregenerated,enabled=enabled,
                       border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=txt.textimage.get_width()+border+horizontalspacing*2,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                       command=command,runcommandat=runcommandat,col=col,textcol=textcol,backingcol=backingcol,hovercol=hovercol,clickdownsize=clickdownsize,clicktype=clicktype,textoffsetx=textoffsetx,textoffsety=textoffsety,maxwidth=maxwidth,
                       dragable=dragable,colorkey=colorkey,toggle=toggle,toggleable=toggleable,toggletext=toggletext,toggleimg=toggleimg,togglecol=togglecol,togglehovercol=togglehovercol,bindtoggle=bindtoggle,spacing=spacing,
                       verticalspacing=verticalspacing,horizontalspacing=horizontalspacing,clickablerect=clickablerect,clickableborder=clickableborder,
                       animationspeed=animationspeed,backingdraw=backingdraw,borderdraw=borderdraw,linelimit=linelimit,refreshbind=refreshbind,options=options,startoptionindex=startoptionindex)
        tablew = width
        if tablew != -1: tablew-=border*2
        data = []
        for i,a in enumerate(options):
            func = funcer(obj.optionclicked,index=i)
            data.append([self.makebutton(0,0,a,textsize,font=font,bold=bold,textcol=textcol,col=col,roundedcorners=roundedcorners,command=func.func)])
         
        table = self.makescrollertable(border,border,data,pageheight=pageheight,roundedcorners=roundedcorners,textsize=textsize,font=font,bold=bold,border=border,scalesize=scalesize,col=col,textcol=textcol,backingcol=backingcol,width=tablew)
        window = self.makewindow(0,obj.height,f'ui.IDs["{obj.ID}"].width',f'ui.IDs["{table.ID}"].getheight()+{border}*2',enabled=False,animationspeed=animationspeed,animationtype=animationtype)
        obj.binditem(window)
        window.binditem(table)
        nwidth = (max([a[0].textimage.get_width() for a in table.table])+(obj.width-obj.leftborder-obj.rightborder)+border*5)
        obj.leftborder+=nwidth-obj.width
        obj.refresh()
        table.startwidth = nwidth-border*2
        table.refresh()
        window.refresh()
        obj.table = table
        obj.window = window
        obj.titletext = txt
        obj.command = lambda: obj.mainbuttonclicked()
        obj.truecommand = command
        return obj

    def makelabeledcheckbox(self,x,y,text,textsize=-1,command=emptyfunction,menu='main',ID='checkbox',textpos='left',layer=1,roundedcorners=0,bounditems=[],killtime=-1,width=-1,height=-1,
                 anchor=(0,0),objanchor=(0,0),center=False,centery=-1,img='none',font=-1,bold=-1,antialiasing=-1,pregenerated=True,enabled=True,
                 border=4,upperborder=-1,lowerborder=-1,rightborder=-1,leftborder=-1,scalesize=-1,scalex=-1,scaley=-1,scaleby=-1,glow=-1,glowcol=-1,
                 runcommandat=0,col=-1,textcol=-1,backingcol=-1,bordercol=-1,hovercol=-1,clickdownsize=-1,clicktype=-1,textoffsetx=-1,textoffsety=-1,maxwidth=-1,
                 dragable=False,colorkey=-1,toggle=True,toggleable=True,toggleimg='none',togglecol=-1,togglehovercol=-1,bindtoggle=[],spacing=-1,horizontalspacing=5,clickablerect=-1,clickableborder=10,
                 backingdraw=False,borderdraw=-1,animationspeed=-1,linelimit=1000,refreshbind=[]):

        if textsize == -1: textsize = Style.defaults['textsize']
        
        if textpos == 'left':
            anch = (0,'h/2')
            objanch = ('w','h/2')
            tx = -horizontalspacing
        else:
            anch = ('w','h/2')
            objanch = (0,'h/2')
            tx = horizontalspacing
        text = self.maketext(tx,0,text,textsize,menu,ID=ID+'text',
                         anchor=anch,objanchor=objanch,font=font,bold=bold,antialiasing=antialiasing,pregenerated=pregenerated,enabled=enabled,
                         scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,
                         col=col,textcol=textcol,backingcol=backingcol,textoffsetx=textoffsetx,textoffsety=textoffsety,
                         colorkey=colorkey,maxwidth=maxwidth,animationspeed=animationspeed)
        
        obj = self.makecheckbox(x=x,y=y,width=width,height=height,menu=menu,ID=ID,layer=layer,roundedcorners=roundedcorners,bounditems=bounditems+[text],killtime=killtime,
                                anchor=anchor,objanchor=objanchor,center=center,centery=centery,textsize=textsize,img=img,font=font,bold=bold,antialiasing=antialiasing,pregenerated=pregenerated,enabled=enabled,
                                border=border,upperborder=upperborder,lowerborder=lowerborder,rightborder=rightborder,leftborder=leftborder,scalesize=scalesize,scalex=scalex,scaley=scaley,scaleby=scaleby,glow=glow,glowcol=glowcol,
                                command=command,runcommandat=runcommandat,col=col,textcol=textcol,backingcol=backingcol,hovercol=hovercol,clickdownsize=clickdownsize,clicktype=clicktype,textoffsetx=textoffsetx,textoffsety=textoffsety,maxwidth=maxwidth,
                                dragable=dragable,colorkey=colorkey,toggle=toggle,toggleable=toggleable,toggleimg=toggleimg,togglecol=togglecol,togglehovercol=togglehovercol,bindtoggle=bindtoggle,
                                spacing=spacing,clickablerect=clickablerect,clickableborder=clickableborder,
                                animationspeed=animationspeed,backingdraw=backingdraw,borderdraw=borderdraw,linelimit=linelimit,refreshbind=refreshbind)
        return obj
    
    def automakemenu(self,menu):
        obj = MENU(ui=self,x=0,y=0,width=self.screenw,height=self.screenh,menu=menu,ID='auto_generate_menu:'+menu)
        return obj

            
    
    def animate(self):
        self.queuedmenumove[0]-=1
        if self.queuedmenumove[0]<0 and self.queuedmenumove[1] != []:
            if self.queuedmenumove[1][0] == 'move': self.movemenu(self.queuedmenumove[1][1],self.queuedmenumove[1][2],self.queuedmenumove[1][3])
            else: self.menuback(self.queuedmenumove[1][1],self.queuedmenumove[1][2])
            self.queuedmenumove[1] = []
        delete = []
        for a in self.animations:
            if a.animate():
                delete.append(a.ID)
        for a in delete:
            self.delete(a)
    def makeanimation(self,animateID,startpos,endpos,movetype='linear',length='default',command=emptyfunction,runcommandat=-1,queued=True,menu=False,relativemove=False,skiptoscreen=False,acceleration=1,permamove=False,ID='default'):
        if length == 'default':
            length = Style.defaults['animationspeed']
        if menu:
            for a in self.automenus:
                if (animateID in a.truemenu):
                    if not a.onitem:
                        self.makeanimation(a.ID,startpos,endpos,movetype,length,command,runcommandat,queued,False,relativemove,skiptoscreen,acceleration,permamove)
                        runcommandat = -2
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
                    self.IDs[a[0]].finish(True)
                    self.delete(a[0])
            else:
                for a in self.animations:
                    if a.animateID == animateID:
                        wait = max([a.wait+a.length,wait])
            obj = ANIMATION(self,animateID,startpos,endpos,movetype,length,wait,relativemove,command,runcommandat,skiptoscreen,acceleration,permamove,ID)
            self.addid(ID,obj)
        
                
    def movemenu(self,moveto,slide='none',length='default',backchainadd=True):
        if length == 'default':
            length = Style.defaults['animationspeed']
        if self.queuedmenumove[0]<0 or slide=='none':
            if (self.activemenu in self.windowedmenunames) and (moveto == self.activemenu) and (self.queuedmenumove[0]<0):
                self.menuback(slide+' flip',length)
            else:
                if backchainadd:
                    self.backchain.append([self.activemenu,slide,length])
                if slide=='none':
                    self.activemenu = moveto
                else:
                    self.slidemenu(self.activemenu,moveto,slide,length)
            for a in self.mouseheld:
                a[1]-=1
        elif self.queuemenumove:
            if ['move',moveto,slide,length]!=self.prevmenumove:
                self.queuedmenumove[1] = ['move',moveto,slide,length]
            self.prevmenumove = self.queuedmenumove[1]
    def menuback(self,slide='none',length='default'):
        if len(self.backchain)>0:
            if slide =='none' and self.backchain[-1][1] != 'none':
                if not(self.activemenu in self.windowedmenunames and self.backchain[-1][0] in self.windowedmenunames):
                    slide = self.backchain[-1][1]+' flip'
                else:
                    slide = self.backchain[-1][1]
            length = self.backchain[-1][2]
        if length == 'default':
            length = Style.defaults['animationspeed']
        if self.queuedmenumove[0]<0 or slide=='none':
            if len(self.backchain)>0:
                if slide=='none':
                    self.activemenu = self.backchain[-1][0]
                else:
                    self.slidemenu(self.activemenu,self.backchain[-1][0],slide,length) 
                del self.backchain[-1]
            elif self.backquits and self.queuedmenumove[0]<0:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
            for a in self.mouseheld:
                a[1]-=1
        elif self.queuemenumove:
            if ['back',slide,length]!=self.prevmenumove:
                self.queuedmenumove[1] = ['back',slide,length]
            self.prevmenumove = self.queuedmenumove[1]
    def slidemenu(self,menufrom,menuto,slide,length):
        self.queuedmenumove[0] = length*30
        dirr = [0,0]
        if 'left' in slide: dirr[0]-=self.screenw
        if 'right' in slide: dirr[0]+=self.screenw
        if 'up' in slide: dirr[1]-=self.screenh
        if 'down' in slide: dirr[1]+=self.screenh
        if 'flip' in slide: dirr = [dirr[0]*-1,dirr[1]*-1]
            
        if menufrom in self.windowedmenunames:
            if menuto == self.windowedmenus[self.windowedmenunames.index(menufrom)].behindmenu:
                self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].ID,'current',dirr,'sinout',length,command=lambda: self.movemenu(menuto,backchainadd=False),runcommandat=length,queued=False,relativemove=True,skiptoscreen=True)
                self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].ID,'current',[dirr[0]*-1,dirr[1]*-1],'linear',1,command=self.finishmenumove,runcommandat=1,queued=True,relativemove=True)
            else:
                if menuto in self.windowedmenunames:
                    self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].ID,'current',dirr,'sinout',length,command=lambda: self.slidemenuin(self.windowedmenus[self.windowedmenunames.index(menuto)].ID,length,[dirr[0]*-1,dirr[1]*-1],menuto,False),runcommandat=length,queued=False,relativemove=True,skiptoscreen=True)
                    self.makeanimation(self.windowedmenus[self.windowedmenunames.index(menufrom)].ID,'current',[dirr[0]*-1,dirr[1]*-1],'linear',1,relativemove=True)
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
    def slidemenuin(self,moveto,length,dirr,realmenuto=0,menu=True):
        self.makeanimation(moveto,[dirr[0]*-1,dirr[1]*-1],'current','sinin',length,command=self.finishmenumove,runcommandat=length,queued=True,menu=menu,relativemove=True)
        if realmenuto != 0: moveto=realmenuto
        self.movemenu(moveto,backchainadd=False)
    def finishmenumove(self):
        self.queuedmenumove[0] = -1

    def delete(self,ID,failmessage=True):
        try:
            if self.IDs[ID].onitem:
                self.IDs[ID].master[0].bounditems.remove(self.IDs[ID])
            for a in self.IDs[ID].bounditems:
                self.delete(ID,failmessage)
            if type(self.IDs[ID]) == BUTTON: self.buttons.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == TEXTBOX: self.textboxes.remove(self.IDs[ID])
            elif type(self.IDs[ID]) in [TABLE,SCROLLERTABLE]: self.tables.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == DROPDOWN: self.dropdowns.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == TEXT: self.texts.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == SCROLLER: self.scrollers.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == SLIDER: self.sliders.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == ANIMATION: self.animations.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == RECT: self.rects.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == MENU: self.automenus.remove(self.IDs[ID])
            elif type(self.IDs[ID]) == WINDOW: self.windows.remove(self.IDs[ID])
            del self.IDs[ID]
            self.refreshitems()
            return True
        except Exception as e:
            if failmessage: print('Failed to delete object:',ID,'Error:',e)
            return False
    def onmenu(self,menu):
        lis = []
        for b in self.items:
            if b.menu == menu:
                lis.append(b)
        return lis

def todict(**args):
    return args
def filloutargs(args):
    newargs = todict(menu='main',ID='',layer=1,bounditems=[],refreshbind=[],killtime=-1,scaleby=-1,
                text='',img='none',pregenerated=True,enabled=True,command=emptyfunction,runcommandat=0,
                dragable=False,toggle=True,toggleable=False,toggletext=-1,toggleimg='none',bindtoggle=[],clickablerect=-1,
                linelimit=100,chrlimit=10000,numsonly=False,enterreturns=False,commandifenter=True,commandifkey=False,imgdisplay=False,
                data='empty',titles=[],boxwidth=-1,boxheight=-1,pageheight=15,scrollcords=(0,0),scrollbind=[],screencompressed=False,
                sliderroundedcorners=-1,minp=0,maxp=100,startp=0,direction='horizontal',behindmenu='main',scroller=0,compress=False,
                options=[],startoptionindex=0,animationtype='movedown')
    for a in newargs:
        if not(a in args):
            args[a] = newargs[a]
    return args
    



                 
class GUI_ITEM:
    def __init__(self,**args):
        execs = []
        defaulttype = type(self)
        if 'defaulttype' in args: defaulttype = args['defaulttype']
        for var in Style.objectdefaults[defaulttype]:
            if not (var in args):
                args[var] = Style.objectdefaults[type(self)][var]
            elif args[var] == Style.universaldefaults[var]:
                args[var] = Style.objectdefaults[type(self)][var]
            
                
        args = filloutargs(args)
        ui = args.pop('ui')
        self.ui = ui
  
        self.enabled = args['enabled']
        self.center = args['center']
        if args['centery'] == -1: self.centery = self.center
        else: self.centery = args['centery']
        self.x = args['x']
        self.y = args['y']
        self.startx = args['x']
        self.starty = args['y']
        self.startanchor = list(args['anchor'])
        self.startobjanchor = list(args['objanchor'])
        if self.center and self.startobjanchor[0] == 0: self.startobjanchor[0]='w/2'
        if self.centery and self.startobjanchor[1] == 0: self.startobjanchor[1]='h/2'
        self.scrollcords = args['scrollcords']
        self.refreshbind = args['refreshbind'][:]

        self.startwidth = args['width']
        self.startheight = args['height']
        self.width = relativetoval(args['width'],ui.screenw,ui.screenh,ui)
        self.height = relativetoval(args['height'],ui.screenw,ui.screenh,ui)
        self.roundedcorners = args['roundedcorners']
        self.scalesize = args['scalesize']
        if args['scalex'] == -1: self.scalex = self.scalesize
        else: self.scalex = args['scalex']
        if args['scaley'] == -1: self.scaley = self.scalesize
        else: self.scaley = args['scaley']
        self.scaleby = args['scaleby']
        self.glow = args['glow']
        self.refreshscale()
        self.border = args['border']
        if args['upperborder'] == -1: self.upperborder = self.border
        else: self.upperborder = args['upperborder']
        if args['lowerborder'] == -1: self.lowerborder = self.border
        else: self.lowerborder = args['lowerborder']
        if args['leftborder'] == -1: self.leftborder = self.border
        else: self.leftborder = args['leftborder']
        if args['rightborder'] == -1: self.rightborder = self.border
        else: self.rightborder = args['rightborder']
            
        self.menu = args['menu']
        self.truemenu = self.menu
        if type(self.truemenu) == str: self.truemenu = [self.truemenu]
        self.behindmenu = args['behindmenu']
        if args['killtime'] == -1: self.killtime = -1
        else: self.killtime = time.time()+args['killtime']
        self.layer = args['layer']
        if args['ID'] == '': args['ID'] = args['text']


        self.text = str(args['text'])
        self.textsize = args['textsize']
        self.img = args['img']
        self.font = args['font']
        self.bold = args['bold']
        self.antialiasing = args['antialiasing']
        self.pregenerated = args['pregenerated']
        self.textcenter = args['textcenter']
        self.startmaxwidth = args['maxwidth']
        self.maxwidth = args['maxwidth']
        self.textimages = []
        self.toggletextimages = []

        self.col = args['col']
        self.textcol = args['textcol']
        self.backingcol = autoshiftcol(args['backingcol'],self.col,20)
        self.bordercol = self.backingcol
        self.glowcol = autoshiftcol(args['glowcol'],self.col,-20)
        self.hovercol = autoshiftcol(args['hovercol'],self.col,-20)
        self.togglecol = autoshiftcol(args['togglecol'],self.col,-50)
        self.togglehovercol = autoshiftcol(args['togglehovercol'],self.togglecol,-20)
        self.selectcol = autoshiftcol(args['selectcol'],self.col,20)
        self.scrollercol = autoshiftcol(args['scrollercol'],self.col,-30)
        self.slidercol = autoshiftcol(args['slidercol'],self.col,-30)
        self.sliderbordercol = autoshiftcol(args['sliderbordercol'],self.col,-10)
        self.colorkey = args['colorkey']
        
        self.clickdownsize = args['clickdownsize']
        self.textoffsetx = args['textoffsetx']
        self.textoffsety = args['textoffsety']
        self.dragable = args['dragable']
        self.spacing = args['spacing']
        self.verticalspacing = args['verticalspacing']
        self.horizontalspacing = args['horizontalspacing']
        if args['spacing']!=-1:
            self.verticalspacing = self.spacing
            self.horizontalspacing = self.spacing

        self.toggle = args['toggle']
        self.toggleable = args['toggleable']
        if args['toggletext'] == -1: self.toggletext = args['text']
        else: self.toggletext = args['toggletext']
        if args['toggleimg'] == -1: toggleimg = args['img']
        else: self.toggleimg = args['toggleimg']
        self.bindtoggle = args['bindtoggle']
        
        self.clicktype = args['clicktype']
        self.startclickablerect = args['clickablerect']
        self.clickablerect = args['clickablerect']
        self.noclickrect = []
        self.noclickrectsapplied = []
        self.clickableborder = args['clickableborder']
        self.clickedon = -1
        self.holding = False
        self.hovering = False
        self.animating = False
        self.animationspeed = args['animationspeed']
        self.animate = 0
        self.currentframe = 0
        self.command = args['command']
        self.runcommandat = args['runcommandat']

        self.lines = args['lines']
        self.linelimit = args['linelimit']
        self.selectbordersize = args['selectbordersize']
        self.selectshrinksize = args['selectshrinksize']
        self.cursorsize = args['cursorsize']
        self.chrlimit = args['chrlimit']
        self.numsonly = args['numsonly']
        self.enterreturns = args['enterreturns']
        self.commandifenter = args['commandifenter']
        self.commandifkey = args['commandifkey']
        self.imgdisplay = args['imgdisplay']

        self.tableobject = False
        self.data = args['data']
        self.titles = args['titles']
        self.table = 0
        self.linesize = args['linesize']
        self.boxwidth = args['boxwidth']
        self.boxheight = args['boxheight']
        self.guessheight = args['guessheight']
        self.guesswidth = args['guesswidth']
        self.scroller = args['scroller']
        self.compress = args['compress']

        self.animationtype = args['animationtype']
        self.options = args['options']
        if len(self.options)>0: self.active = self.options[args['startoptionindex']]
        
        self.backingdraw = args['backingdraw']
        self.borderdraw = args['borderdraw']
        self.startpageheight = args['pageheight']
        self.pageheight = relativetoval(args['pageheight'],ui.screenw,ui.screenh,ui)
 
        self.startminp = args['minp']
        self.minp = relativetoval(args['minp'],ui.screenw,ui.screenh,ui)
        self.startmaxp = args['maxp']
        self.maxp = relativetoval(args['maxp'],ui.screenw,ui.screenh,ui)
        self.startp = args['startp']
        self.increment = args['increment']
        self.containedslider = args['containedslider']
        if args['slidersize'] == -1:
            self.slidersize = self.height*2
            if self.containedslider: self.slidersize = self.height-self.upperborder-self.lowerborder
            if args['direction'] == 'vertical':
                self.slidersize = self.width*2
                if self.containedslider: self.slidersize = self.width-self.leftborder-self.rightborder
        else:
            self.slidersize = args['slidersize']
        if args['sliderroundedcorners'] == -1: self.sliderroundedcorners = args['roundedcorners']
        else: self.sliderroundedcorners = args['sliderroundedcorners']
        self.direction = args['direction']
        self.containedslider = args['containedslider']
        self.movetoclick = args['movetoclick']
        self.scrollbind = args['scrollbind']
        self.screencompressed = args['screencompressed']

        self.onitem = False
        self.master = [emptyobject(0,0,ui.screenw,ui.screenh)]
        self.bounditems = args['bounditems'][:]
        ui.addid(args['ID'],self)
        for a in self.bounditems:
            self.binditem(a)
        self.empty = False

        
        self.isolated = args['isolated']
        self.darken = args['darken']
        for a in self.bounditems:
            self.binditem(a)
        self.reset()
        pygame.event.pump()
        
    def __str__(self):
        return  '<'+str(type(self)).split("'")[1]+f' ID:{self.ID}>'
    def __repr__(self):
        return  '<'+str(type(self)).split("'")[1]+f' ID:{self.ID}>'
    def reset(self):
        self.autoscale()
        self.refreshscale()
        self.gentext()
        self.autoscale()
        self.refreshcords()
        self.resetcords()
        self.refresh()


    def refresh(self):
        ui = self.ui
        tscale = self.scale
        self.refreshscale()
        self.gentext()
        self.autoscale()
        self.resetcords()
        self.refreshglow()
        self.refreshbound()
        self.refreshclickablerect()
    def gentext(self):
        ui = self.ui
        self.currentframe = 0
        if type(self.img) != list: imgs = [self.img]
        else:
            imgs = self.img
            if len(imgs)<1: imgs.append('')

        self.textimages = []
        for img in imgs:
            if type(img) == str:
                if len(imgs)!=1: txt = img
                else: txt = self.text
                self.textimages.append(ui.rendertextlined(txt,self.textsize,self.textcol,self.col,self.font,self.maxwidth,self.bold,self.antialiasing,self.textcenter,imgin=True,img=img,scale=self.scale,linelimit=self.linelimit,cutstartspaces=True))
            else:
                self.textimages.append(pygame.transform.scale(img,(img.get_width()*(self.textsize/img.get_height())*self.scale,img.get_height()*(self.textsize/img.get_height())*self.scale)))
            if self.colorkey != -1: self.textimages[-1].set_colorkey(self.colorkey)
        self.textimage = self.textimages[0]
        if len(self.textimages) != 1:
            self.animating = True
        self.child_gentext()
    def refreshglow(self):
        if self.glow!=0:
            self.glowimage = pygame.Surface(((self.glow*2+self.width)*self.scale,(self.glow*2+self.height)*self.scale),pygame.SRCALPHA)
            draw.glow(self.glowimage,roundrect(self.glow*self.scale,self.glow*self.scale,self.width*self.scale,self.height*self.scale),self.glow,self.glowcol)
    def refreshbound(self):
        for a in self.refreshbind:
            if a in self.ui.IDs:
                self.ui.IDs[a].refresh()
    def animatetext(self):
        if self.animating:
            self.animate+=1
            if self.animate%self.animationspeed == 0:
                self.currentframe+=1
                if self.currentframe == len(self.textimages):
                    self.currentframe = 0
                self.textimage = self.textimages[self.currentframe]
    def resetcords(self,scalereset=True):
        ui = self.ui
        if scalereset: self.refreshscale()
        self.anchor = self.startanchor[:]

        master = self.master[0]
        if len(self.master)>1:
            if 'animate' in self.truemenu:
                for a in self.master:
                    if ui.activemenu in a.truemenu:
                        master = a
            else:
                for a in self.master:
                    if not(ui.activemenu in a.truemenu):
                        master = a
                        break
                        
        w = self.getmasterwidth()
        h = self.getmasterheight()

        self.anchor[0] = relativetoval(self.anchor[0],w,h,ui)
        self.anchor[1] = relativetoval(self.anchor[1],w,h,ui)
        
        self.objanchor = self.startobjanchor[:]
        self.objanchor[0] = relativetoval(self.objanchor[0],self.width,self.height,ui)
        self.objanchor[1] = relativetoval(self.objanchor[1],self.width,self.height,ui)
        
        self.x = int(master.x*master.dirscale[0]+self.anchor[0]+(self.startx-self.objanchor[0]-self.scrollcords[0])*self.scale)/self.dirscale[0]
        self.y = int(master.y*master.dirscale[1]+self.anchor[1]+(self.starty-self.objanchor[1]-self.scrollcords[1])*self.scale)/self.dirscale[1]

        self.refreshcords()
        for a in self.bounditems:
            a.resetcords()
        self.refreshclickablerect()

    def refreshcords(self):
        self.refreshscale()
        self.child_refreshcords()

        
    def refreshscale(self):
        if self.scaleby == -1:
            self.scale = self.ui.scale
        elif self.scaleby == 'vertical':
            self.scale = self.ui.dirscale[1]
        else:
            self.scale = self.ui.dirscale[0]
            
        self.dirscale = self.ui.dirscale[:]
        if not self.scalesize: self.scale = 1
        if not self.scalex: self.dirscale[0] = 1
        if not self.scaley: self.dirscale[1] = 1
    def autoscale(self):
        w = self.getmasterwidth()/self.scale
        h = self.getmasterheight()/self.scale
        if self.startwidth != -1: self.width = relativetoval(self.startwidth,w,h,self.ui)
        if self.startmaxwidth != -1: self.maxwidth = relativetoval(self.startmaxwidth,w,h,self.ui)
        if self.startheight != -1: self.height = relativetoval(self.startheight,w,h,self.ui)
        self.refreshclickablerect()
        self.child_autoscale()
    def refreshclickablerect(self):
        w = self.getmasterwidth()/self.scale
        h = self.getmasterheight()/self.scale
        if self.startclickablerect != -1:
            rx,ry,rw,rh = self.startclickablerect
            xstart = self.master[0].x
            ystart = self.master[0].y
            ow = self.getmasterwidth()/self.scale
            oh = self.getmasterheight()/self.scale
            if type(self) == SCROLLERTABLE:
                self.pageheight = relativetoval(self.startpageheight,w,h,self.ui)
                oh = self.pageheight
            if type(self) in [SCROLLERTABLE,TABLE]:
                xstart = self.x*self.dirscale[0]
                ystart = self.y*self.dirscale[1]
                ow = self.width
                oh = self.height
            self.clickablerect = pygame.Rect(xstart+relativetoval(rx,w,h,self.ui),
                                             ystart+relativetoval(ry,w,h,self.ui),
                                             relativetoval(rw,ow,oh,self.ui)*self.scale,
                                             relativetoval(rh,ow,oh,self.ui)*self.scale)
        else: self.clickablerect = self.startclickablerect
        
    def render(self,screen):
        if self.killtime != -1 and self.killtime<self.ui.time:
            self.ui.delete(self.ID)
        elif self.enabled:
            self.child_render(screen)
            for a in [i.ID for i in self.bounditems][:]:
                if a in self.ui.IDs:
                    self.ui.IDs[a].render(screen)
    def smartcords(self,x='',y='',startset=True,accountscroll=False):
        scr = [0,0]
        if accountscroll:
            scr = self.scrollcords[:]
        
        if x!='':
            self.x = x
            if startset: self.startx = ((self.x+scr[0])*self.dirscale[0]+self.objanchor[0]*self.scale-self.anchor[0])/self.scale
        if y!='':
            self.y = y
            if startset: self.starty = ((self.y+scr[1])*self.dirscale[1]+self.objanchor[1]*self.scale-self.anchor[1])/self.scale
    def binditem(self,item,replace=True,resetcords=True):
        if item!=self:
            for a in item.master:
                if type(a) == emptyobject:
                    item.master.remove(a)
            if item.onitem and replace:
                for a in item.master:
                    if type(a) != emptyobject:
                        if item in a.bounditems:
                            a.bounditems.remove(item)
            if not(item in self.bounditems):
                self.bounditems.append(item)
            item.onitem = True
            if replace:
                item.master = [self]
            else:
                item.master.append(self)
            self.bounditems.sort(key=lambda x: x.layer,reverse=False)
            if resetcords: item.resetcords()
    def setmenu(self,menu):
        old = self.truemenu
        self.menu = menu
        self.truemenu = self.menu
        if type(self.truemenu) == str: self.truemenu = [self.truemenu]

        for a in self.master:
            if type(a) in [WINDOWEDMENU,MENU]:
                a.bounditems.remove(self)
        self.master = []
        for a in self.truemenu:
            if a in self.ui.windowedmenunames:
                self.ui.windowedmenus[self.ui.windowedmenunames.index(a)].binditem(self,False,False)
        self.ui.refreshitems()
        self.resetcords()
        
        
    def getmenu(self):
        if type(self.master[0]) in [WINDOWEDMENU,MENU]:
            return self.master[0].menu
        else:
            return self.master[0].getmenu()
    def getmasterwidth(self):
        w = self.ui.screenw
        if self.onitem:
            w = self.master[0].width*self.master[0].scale
        return w
    def getmasterheight(self):
        h = self.ui.screenh
        if self.onitem:
            h = self.master[0].height*self.master[0].scale
        return h
    def getchildIDs(self):
        lis = [self.ID]
        lis += sum([a.getchildIDs() for a in self.bounditems],[])
        return lis
    def getenabled(self):
        if not self.enabled:
            return False
        else:
            return self.master[0].getenabled()
    def settext(self,text):
        self.text = str(text)
        self.refresh()
    def setwidth(self,width):
        self.startwidth = width
        self.autoscale()
    def setheight(self,height):
        self.startheight = height
        self.autoscale()
    def enable(self):
        self.enabled = True
    def disable(self):
        self.enabled = False
    def enabledtoggle(self):
        if self.enabled: self.disable()
        else: self.enable()
    def getwidth(self):
        return self.width
    def getheight(self):
        return self.height
    def child_gentext(self):
        pass
    def child_refreshcords(self):
        pass
    def child_autoscale(self):
        pass
    def getclickedon(self,rect='default',runcom=True,drag=True,smartdrag=True):
        ui = self.ui
        if rect == 'default':
            rect = pygame.Rect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale)
        self.clickedon = -1
        self.hovering = False
        mpos = ui.mpos
        if rect.collidepoint(mpos) and (self.clickablerect == -1 or self.clickablerect.collidepoint(mpos)) and not(collidepointrects(mpos,self.noclickrectsapplied)):
            if ui.mprs[self.clicktype] and (ui.mouseheld[self.clicktype][1]>0 or self.holding):
                if ui.mouseheld[self.clicktype][1] == ui.buttondowntimer:
                    self.clickedon = 0
                    self.holding = True
                    self.holdingcords = [(mpos[0])-rect.x,(mpos[1])-rect.y]
                    if self.runcommandat<2 and runcom:
                        for a in self.bindtoggle:
                            if a!=self.ID:
                                ui.IDs[a].toggle = False
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
                if type(self) == SCROLLER: account = [0,-self.border]
                else: account = [-rect.x+self.x,-rect.y+self.y]
                if smartdrag: self.smartcords((mpos[0]-self.holdingcords[0]+account[0])/self.dirscale[0],(mpos[1]-self.holdingcords[1]+account[1])/self.dirscale[1])
                else:
                    self.x = (mpos[0]-self.holdingcords[0]+account[0])/self.dirscale[0]
                    self.y = (mpos[1]-self.holdingcords[1]+account[1])/self.dirscale[1]
                self.centerx = self.x+self.width/2
                self.centery = self.y+self.height/2
                for a in self.bounditems:
                    a.resetcords(ui)
            if self.runcommandat == 1 and runcom:
                self.command()
        elif not ui.mprs[self.clicktype]:
            if self.holding:
                self.clickedon = 2
                if rect.collidepoint(mpos) and self.runcommandat>0 and runcom:
                    for a in self.bindtoggle:
                        if a!=self.ID:
                            ui.IDs[a].toggle = False
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
    def child_gentext(self):
        if (self.img != self.toggleimg) or (self.text != self.toggletext):
            if type(self.img) != list: imgs = [self.toggleimg]
            else: imgs = self.toggleimg
            
            self.toggletextimages = []
            for img in imgs:
                if type(img) == str:
                    if len(imgs)!=1: txt = img
                    else: txt = self.toggletext
                    self.toggletextimages.append(self.ui.rendertextlined(self.toggletext,self.textsize,self.textcol,self.togglecol,self.font,self.maxwidth,self.bold,True,center=self.textcenter,imgin=True,img=self.toggleimg,scale=self.scale,linelimit=self.linelimit,cutstartspaces=True))
                else:
                    self.toggletextimages.append(pygame.transform.scale(img,(self.textsize,img.get_width()*self.textsize/img.get_height())))
                    if self.colorkey != -1: self.toggletextimages[-1].set_colorkey(self.colorkey)
            self.toggletextimage = self.toggletextimages[0]
            if len(self.toggletextimages) != 1:
                self.animating = True
        else:
            self.toggletextimages = self.textimages
            self.toggletextimage = self.toggletextimages[0]
        
    def child_autoscale(self):
        if len(self.textimages)>0:
            imgsizes = [a.get_size() for a in self.textimages]
            if self.toggleable: imgsizes+=[a.get_size() for a in self.toggletextimages]
            if self.startwidth == -1:
                self.width = max([a[0] for a in imgsizes])/self.scale+self.horizontalspacing*2+self.leftborder+self.rightborder
            if self.startheight == -1:
                self.height = max([a[1] for a in imgsizes])/self.scale+self.verticalspacing*2+self.upperborder+self.lowerborder
            
##    def child_refreshcords(self,ui):
##        self.colliderect = pygame.Rect(self.x+self.leftborder,self.y+self.upperborder,self.width-self.leftborder-self.rightborder,self.height-self.upperborder-self.lowerborder)
    def child_render(self,screen):
        self.innerrect = pygame.Rect(self.x*self.dirscale[0]+(self.leftborder+self.clickdownsize*self.holding)*self.scale,
                                     self.y*self.dirscale[1]+(self.upperborder+self.clickdownsize*self.holding)*self.scale,
                                     (self.width-self.leftborder-self.rightborder-self.clickdownsize*self.holding*2)*self.scale,
                                     (self.height-self.upperborder-self.lowerborder-self.clickdownsize*self.holding*2)*self.scale)
        self.clickrect = pygame.Rect(self.x*self.dirscale[0]+(self.leftborder-self.clickableborder)*self.scale,
                                     self.y*self.dirscale[1]+(self.upperborder-self.clickableborder)*self.scale,
                                     (self.width-self.leftborder-self.rightborder+self.clickableborder*2)*self.scale,
                                     (self.height-self.upperborder-self.lowerborder+self.clickableborder*2)*self.scale)
        self.getclickedon(self.clickrect)
        if self.clickedon > -1:
            if self.clickedon == 0: self.ui.mouseheld[self.clicktype][1]-=1
        self.draw(screen)
    def draw(self,screen):
        if self.enabled:
            self.animatetext()
            col = self.col
            if not self.toggle: col = self.togglecol
            innerrect = roundrect(self.x*self.dirscale[0]+(self.leftborder+self.clickdownsize*self.holding)*self.scale,self.y*self.dirscale[1]+(self.upperborder+self.clickdownsize*self.holding)*self.scale,(self.width-self.leftborder-self.rightborder-self.clickdownsize*self.holding*2)*self.scale,(self.height-self.upperborder-self.lowerborder-self.clickdownsize*self.holding*2)*self.scale)
            if self.holding or self.hovering:
                if not self.toggle: col = self.togglehovercol
                else: col = self.hovercol
            if self.glow!=0:
                screen.blit(self.glowimage,(self.x*self.dirscale[0]-self.glow*self.scale,self.y*self.dirscale[1]-self.glow*self.scale))
            if self.borderdraw:
                if self.backingdraw: draw.rect(screen,self.backingcol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
                else: draw.rect(screen,self.backingcol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),int((self.border+self.clickdownsize*self.holding)*self.scale),border_radius=int(self.roundedcorners*self.scale))
            if self.backingdraw: draw.rect(screen,col,innerrect,border_radius=int((self.roundedcorners-self.border)*self.scale))
            if self.toggle:
                screen.blit(self.textimage,(self.x*self.dirscale[0]+((self.width-self.leftborder-self.rightborder)/2+self.leftborder+self.textoffsetx)*self.scale-self.textimage.get_width()/2,self.y*self.dirscale[1]+((self.height-self.upperborder-self.lowerborder)/2+self.upperborder+self.textoffsety)*self.scale-self.textimage.get_height()/2))
            else:
                screen.blit(self.toggletextimage,(self.x*self.dirscale[0]+((self.width-self.leftborder-self.rightborder)/2+self.leftborder+self.textoffsetx)*self.scale-self.toggletextimage.get_width()/2,self.y*self.dirscale[1]+((self.height-self.upperborder-self.lowerborder)/2+self.upperborder+self.textoffsety)*self.scale-self.toggletextimage.get_height()/2))

class TEXTBOX(GUI_ITEM):
    def reset(self):
        self.setvars()
        self.autoscale()
        self.resetcords()
        self.resetscroller()
        self.refreshscale()
        self.gentext(False)
        self.refreshcursor()
        self.refreshscroller()
        self.refreshcords()
        self.refreshglow()
        self.resetcords()
    def setvars(self):
        self.scroller=0
        self.selected = False
        self.textselected = [False,0,0]
        self.clickstartedinbound = False
        self.typingcursor=0
        self.typeline=0
        self.scrolleron=False
        self.slider = -1
    def child_autoscale(self):
        heightgetter = self.ui.rendertext('Tg',self.textsize,self.textcol,self.font,self.bold)
        if self.height == -1:
            self.height = self.upperborder+self.lowerborder+heightgetter.get_height()*self.lines+self.verticalspacing*2
        if self.cursorsize == -1:
            self.cursorsize = self.ui.gettextsize('Tg',self.font,self.textsize,self.bold)[1]-2
    def select(self):
        for a in self.ui.textboxes:
            a.selected = False
        self.ui.selectedtextbox = self.ui.textboxes.index(self)
        self.selected = True
    def settext(self,text=''):
        self.text = text
        self.refresh()
    def inputkey(self,caps,event,kprs):
        starttext = self.text
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
                    pygame.scrap.put('text/plain;charset=utf-8',self.text.encode())
                elif chr(event.key) == 'v':
                    clipboard = pygame.scrap.get(pygame.SCRAP_TEXT)
                    if clipboard == None:
                        clipboard = pygame.scrap.get(pygame.scrap.get_types()[0])
                    clipboard = clipboard.decode().strip('\x00')
                    item = clipboard
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
            if self.typingcursor>-1:
                prev = self.chrcorddata[self.typingcursor][1]
                while self.chrcorddata[self.typingcursor][1]==prev:
                    if self.typingcursor>-1: self.typingcursor-=1
                    else: break
        elif event.key == pygame.K_RIGHT:
            if len(self.chrcorddata)>0:
                if self.typingcursor < len(self.chrcorddata)-1:
                    prev = self.chrcorddata[self.typingcursor+1][1]
                    start = self.typingcursor
                    while self.chrcorddata[self.typingcursor+1][1]==prev:
                        if self.typingcursor<len(self.chrcorddata)-1: self.typingcursor+=1
                        else: break
                        if self.typingcursor > len(self.chrcorddata)-3:
                            break
                    if self.typingcursor-start>1: self.typingcursor+=1
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
        if self.text!=starttext:
            self.refresh()
            self.updateslider()
        else:
            self.refreshcursor()
   
    def resetscroller(self):
        self.scroll = 0
        if self.scroller != 0:
            self.bounditems.remove(self.scroller)
            ui.delete(self.scroller.ID,False)
            
        self.scroller = self.ui.makescroller(-self.rightborder-15+self.border/2,self.upperborder,self.height-self.upperborder-self.lowerborder,emptyfunction,15,0,self.height-self.upperborder-self.lowerborder,self.height,anchor=('w',0),
                                             menu=self.menu,roundedcorners=self.roundedcorners,col=self.col,scalesize=self.scalesize,scaley=self.scalesize,scalex=self.scalesize,scaleby=self.scaleby)
        self.binditem(self.scroller)
    def updateslider(self):
        if self.slider != -1:
            try:
                self.slider.slider = int(self.text)
                self.slider.limitpos()
                self.slider.updatetext()
            except:
                pass
    def refresh(self):
        self.refreshscale()
        self.gentext()
        self.refreshcursor()
        self.refreshscroller()
        
        self.scroller.setmaxp((self.textimage.get_height())/self.scale+self.verticalspacing*2-1)
        self.scroller.setheight(self.height-self.upperborder-self.lowerborder)
        self.scroller.setpageheight(self.height-self.upperborder-self.lowerborder)
        self.scroller.menu = self.menu
        self.scroller.scalesize = self.scalesize
        self.scroller.scalex = self.scalesize
        self.scroller.scaley = self.scalesize
        self.scroller.refresh()
        if (self.scroller.maxp-self.scroller.minp)>self.scroller.pageheight:
            self.scrolleron = True
            if self.scroller.scroll>self.scroller.maxp-self.scroller.pageheight:
                self.scroller.scroll = self.scroller.maxp-self.scroller.pageheight
        else:
            self.scrolleron = False
        self.scroller.refresh()
        self.resetcords()
        self.refreshglow()
        self.refreshbound()
           
    def gentext(self,refcurse=True):
        self.textimage,self.chrcorddatalined = self.ui.rendertextlined(self.text,self.textsize,self.textcol,self.col,self.font,self.width-self.horizontalspacing*2-self.leftborder-self.rightborder-self.scrolleron*self.scroller.width,self.bold,center=self.textcenter,scale=self.scale,linelimit=self.linelimit,getcords=True,imgin=self.imgdisplay)
        for l in self.chrcorddatalined:
            for a in l:
                a[1] = (a[1][0]/self.scale,a[1][1]/self.scale)
                a[2] = (a[2][0]/self.scale,a[2][1]/self.scale)
        self.chrcorddata = []
        for a in self.chrcorddatalined:
            self.chrcorddata+=a
        self.textimagerect = self.textimage.get_rect()
        self.textimagerect.width/=self.ui.scale
        self.textimagerect.height/=self.ui.scale
        if refcurse: self.refreshcursor()
      
    def refreshcursor(self):
        if self.typingcursor>len(self.chrcorddata)-1: self.typingcursor=len(self.chrcorddata)-1
        elif self.typingcursor<-1: self.typingcursor = -1
        if self.typingcursor != -1: self.linecenter = [self.chrcorddata[self.typingcursor][1][0]+self.chrcorddata[self.typingcursor][2][0]/2+self.horizontalspacing,self.chrcorddata[self.typingcursor][1][1]]
        elif len(self.chrcorddata)>0: self.linecenter = [self.chrcorddata[self.typingcursor+1][1][0]-self.chrcorddata[self.typingcursor+1][2][0]/2+self.horizontalspacing,self.chrcorddata[self.typingcursor+1][1][1]]
        else:
            if self.textcenter: self.linecenter = [self.width/2-self.leftborder,self.textsize*0.3]
            else: self.linecenter = [self.horizontalspacing,self.textsize*0.3]
        if self.textselected[1]>len(self.chrcorddata): self.textselected[1]=len(self.chrcorddata)
        elif self.textselected[1]<0: self.textselected[1] = 0
        if self.textselected[2]>len(self.chrcorddata): self.textselected[2]=len(self.chrcorddata)
        elif self.textselected[2]<0: self.textselected[2] = 0
    def refreshscroller(self):
        self.scroller.setheight(self.height-self.upperborder-self.lowerborder)
        self.scroller.setpageheight(self.height-self.upperborder-self.lowerborder)
        self.scroller.refresh()
        inc = 0
        if self.linecenter[1]-self.scroller.scroll>self.scroller.height:
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
            self.scroller.limitpos()
        else:
            self.scroller.scroll = self.scroller.minp
    def child_refreshcords(self):
        if self.scroller != 0:
            self.refreshscroller()
            self.rect = roundrect(self.x,self.y,self.width,self.height)
            self.innerrect = roundrect(self.x+self.leftborder,self.y+self.upperborder,self.width-self.rightborder-self.leftborder-self.scrolleron*self.scroller.width,self.height-self.upperborder-self.lowerborder)
            self.textimagerect = self.textimage.get_rect()     
            if self.textcenter:
                self.textimagerect.x = (self.width-self.horizontalspacing*2-self.scrolleron*self.scroller.width-self.leftborder-self.rightborder)/2+self.textoffsetx+self.horizontalspacing-self.textimagerect.width/2/self.scale
                self.textimagerect.y = self.verticalspacing+self.textimagerect.height/2+self.textoffsety-self.textimagerect.height/2
            else:
                self.textimagerect.x = self.textoffsetx+self.horizontalspacing
                self.textimagerect.y = self.textoffsety+self.verticalspacing
            
    def child_render(self,screen):
        self.typeline+=1
        self.selectrect = roundrect(self.x*self.dirscale[0]+(self.leftborder-self.selectbordersize)*self.scale,self.y*self.dirscale[1]+(self.upperborder-self.selectbordersize)*self.scale,(self.width-(self.leftborder+self.rightborder)+self.selectbordersize*2-self.scrolleron*self.scroller.width)*self.scale,(self.height-(self.upperborder+self.lowerborder)+self.selectbordersize*2)*self.scale)
        if self.typeline == 80:
            self.typeline = 0 
        self.getclickedon(self.selectrect,False,False)
        self.draw(screen)
        mpos = self.ui.mpos
        if self.clickedon == 0:
            self.typingcursor = min([max([self.findclickloc(mpos)+1,0]),len(self.chrcorddata)])-1
            self.textselected[2] = self.typingcursor+1
            if len(self.chrcorddata)!=0: self.textselected[0] = True
            self.textselected[1] = self.typingcursor+1
            self.refreshcursor()
            self.select()
            self.clickstartedinbound = True
        elif self.selected:
            if self.ui.mprs[self.clicktype] and self.ui.mouseheld[self.clicktype][1] == self.ui.buttondowntimer:
                self.clickstartedinbound = False
                self.selected = False
            if not self.selectrect.collidepoint(mpos) and self.ui.mprs[self.clicktype] and not self.ui.mouseheld[self.clicktype]:
                self.selected = False
                self.textselected = [False,0,0]

        if self.ui.mprs[self.clicktype] and self.ui.mouseheld[self.clicktype][1] != self.ui.buttondowntimer and self.clickstartedinbound:
            self.textselected[2] = min([max([self.findclickloc(mpos)+1,0]),len(self.chrcorddata)])
            if self.scrolleron:
                if mpos[1]<self.y*self.dirscale[1]+self.upperborder*self.scale:
                    self.scroller.scroll+=(mpos[1]-(self.y*self.dirscale[1]+self.upperborder*self.scale))/10
                    self.scroller.limitpos()
                elif mpos[1]>self.y*self.dirscale[1]+(self.height-self.lowerborder)*self.scale:
                    self.scroller.scroll+=(mpos[1]-(self.y*self.dirscale[1]+(self.height-self.lowerborder)*self.scale))/10
                    self.scroller.limitpos()
        if not self.ui.mprs[self.clicktype]:
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
    def draw(self,screen):
        if self.enabled:
            ui = self.ui
            if self.glow!=0:
                screen.blit(self.glowimage,(self.x*self.dirscale[0]-self.glow*self.scale,self.y*self.dirscale[1]-self.glow*self.scale))
            if self.borderdraw:
                draw.rect(screen,self.backingcol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
            if self.selected and self.selectbordersize!=0:
                draw.rect(screen,self.selectcol,pygame.Rect(self.selectrect.x+self.holding*self.selectshrinksize*self.scale,self.selectrect.y+self.holding*self.selectshrinksize*self.scale,self.selectrect.width-self.holding*self.selectshrinksize*self.scale*2,self.selectrect.height-self.holding*self.selectshrinksize*self.scale*2),int(self.selectbordersize*self.scale),border_radius=int((self.roundedcorners+self.selectbordersize)*self.scale))
            surf = pygame.Surface(((self.width-self.leftborder-self.rightborder-self.scrolleron*self.scroller.width)*self.scale,(self.height-self.upperborder-self.lowerborder)*self.scale))
            surf.fill(self.backingcol)
            if self.backingdraw: draw.rect(surf,self.col,(0,0,surf.get_width(),surf.get_height()),border_radius=int(self.roundedcorners*self.scale))
            surf.set_colorkey(self.backingcol)

            offset = (0,self.scroller.scroll)
            surf.blit(self.textimage,(self.textimagerect.x*self.scale,(self.textimagerect.y-self.scroller.scroll)*self.scale))
            if self.typeline>20 and self.selected:
                pygame.draw.line(surf,self.textcol,((self.linecenter[0])*self.scale,(self.linecenter[1]-self.cursorsize/2+self.verticalspacing-self.scroller.scroll)*self.scale),((self.linecenter[0])*self.scale,(self.linecenter[1]+self.cursorsize/2+self.verticalspacing-self.scroller.scroll)*self.scale),2)
            if self.textselected[0] and self.textselected[1]!=self.textselected[2]:
                trect = [1000000,0,0,0]
                prev = [0,0]
                for a in range(min([self.textselected[1],self.textselected[2]]),max([self.textselected[1],self.textselected[2]])):
                    if prev != self.chrcorddata[a][1]:
                        if self.chrcorddata[a][0] != '\n':
                            trect[0] = (self.horizontalspacing+self.chrcorddata[a][1][0]-self.chrcorddata[a][2][0]/2)*self.scale
                            trect[1] = (self.verticalspacing+self.chrcorddata[a][1][1]-self.chrcorddata[a][2][1]/2-self.scroller.scroll)*self.scale
                            trect[2] = self.chrcorddata[a][2][0]*self.scale
                            trect[3] = self.chrcorddata[a][2][1]*self.scale
                        highlight = pygame.Surface((trect[2],trect[3]))
                        highlight.set_alpha(180)
                        highlight.fill((51,144,255))
                        surf.blit(highlight,(trect[0],trect[1]))

                    prev = self.chrcorddata[a][1]
                
            screen.blit(surf,(self.x*self.dirscale[0]+(self.leftborder)*self.scale,self.y*self.dirscale[1]+(self.upperborder)*self.scale))
                
            
                



class TABLE(GUI_ITEM):
    def reset(self):
        self.startboxwidth = self.boxwidth
        self.startboxheight = self.boxheight
        self.tableitemID = str(random.randint(1000000,10000000))
        self.threadactive = False
        self.table = 0
        self.refreshscale()
        self.autoscale()
        self.resetcords()
        self.refreshscale()
        self.preprocess()
        self.initheightwidth()
        self.estimatewidths()
        self.gentext()
        self.gettablewidths()
        self.gettableheights()          
        self.refreshcords()
        self.resetcords()
        self.enable()
        
    def refresh(self):
        self.refreshscale()
        self.autoscale()
        self.preprocess()
        self.initheightwidth()
        self.estimatewidths()
        self.gentext()
        self.gettablewidths()
        self.gettableheights()        
        self.refreshcords()
        self.refreshglow()
        self.refreshclickablerect()
        self.enable()
        self.threadactive = False
    def threadrefresh(self):
        if not self.threadactive:
            self.threadactive = True
            thread =  threading.Thread(target=lambda: self.refresh())
            thread.start()
                
    def disable(self):
        self.enabled = False
        if self.table != 0:
            for a in self.table:
                for b in a:
                    b.enabled = False
        else:
            for a in self.data:
                for b in a:
                    if not (type(b) in [str,int,float,list]):
                        b.enabled = False
            
    def enable(self):
        self.enabled = True
        if self.table != 0:
            for a in self.table:
                for b in a:
                    b.enabled = True
    def preprocess(self):
        self.preprocessed = []
        for a in self.data:
            self.preprocessed.append(list(a))
        if len(self.titles)!=0:
            self.preprocessed.insert(0,copy.copy(list(self.titles)))
        self.rows = len(self.preprocessed)
        if self.rows == 0: self.columns = 0
        else:
            self.columns = max([len(a) for a in self.preprocessed])
            if type(self.startboxwidth) == list:
                self.columns = max(self.columns,len(self.startboxwidth))
        for a in range(len(self.preprocessed)):
            while len(self.preprocessed[a])<self.columns:
                self.preprocessed[a].append('')
                
    def gentext(self):
        self.enabled = True
        stillactive = []
        for a in self.preprocessed: stillactive+=a
        copy = [a.ID for a in self.bounditems][:]
        for a in copy:
            if self.ui.IDs[a].tableobject and not(self.ui.IDs[a] in stillactive):
                self.ui.delete(a)
        self.table = []
        for a in range(len(self.preprocessed)):
            self.table.append(self.row_gentext(a))
            
    def row_gentext(self,index):
        row = []
        a = index
        for i,b in enumerate(self.preprocessed[a]):
            ref = False
            if type(b) in [BUTTON,TEXTBOX,TEXT,TABLE,SCROLLERTABLE,SLIDER]:
                b.enabled = self.enabled
                ref = True
                obj = b
            elif type(b) == pygame.Surface:
                self.ui.delete('tabletext'+self.tableitemID+self.ID+str(a)+str(i),False)
                obj = self.ui.maketext(0,0,'',self.textsize,self.menu,'tabletext'+self.tableitemID+self.ID+str(a)+str(i),self.layer+0.01,self.roundedcorners,textcenter=self.textcenter,img=b,maxwidth=self.boxwidth[i],
                                       scalesize=self.scalesize,scaleby=self.scaleby,horizontalspacing=self.horizontalspacing,verticalspacing=self.verticalspacing,colorkey=self.colorkey,enabled=False)
            else:
                b = str(b)
                self.ui.delete('tabletext'+self.tableitemID+self.ID+str(a)+str(i),False)
                obj = self.ui.maketext(0,0,b,self.textsize,self.menu,'tabletext'+self.tableitemID+self.ID+str(a)+str(i),self.layer,self.roundedcorners,textcenter=self.textcenter,textcol=self.textcol,
                                       font=self.font,bold=self.bold,antialiasing=self.antialiasing,pregenerated=self.pregenerated,maxwidth=max([self.boxwidth[i]-self.horizontalspacing*2,-1]),
                                       scalesize=self.scalesize,scaleby=self.scaleby,horizontalspacing=self.horizontalspacing,verticalspacing=self.verticalspacing,backingcol=self.col,enabled=False)
            row.append(obj)
            self.itemintotable(obj,i,a)
            if ref:
                obj.refresh()
        return row
    def child_refreshcords(self):
        if self.table!=0:
            for a in range(len(self.table)):
                for i,b in enumerate(self.table[a]):
                    self.itemrefreshcords(b,i,a)
            alltable = self.getalltableitems()
            for a in self.bounditems:
                if not a.ID in alltable:
                    a.resetcords()

    def itemintotable(self,obj,x,y):
        self.binditem(obj)
        self.itemrefreshcords(obj,x,y)
        obj.enabled = True
    def itemrefreshcords(self,obj,x,y):
        obj.startx = (self.linesize*(x+1)+self.boxwidthsinc[x])
        obj.starty = (self.linesize*(y+1)+self.boxheightsinc[y])
        if not (type(obj) in [SLIDER]):
            obj.width = self.boxwidths[x]
            obj.height = self.boxheights[y]
            obj.startwidth = self.boxwidths[x]
            obj.startheight = self.boxheights[y]
        obj.backingdraw = self.backingdraw
        obj.scalex = self.scalesize
        obj.scaley = self.scalesize
        obj.scalesize = self.scalesize
        obj.scaleby = self.scaleby
        obj.tableobject = True
        if type(self) == SCROLLERTABLE:# and not(y==0 and len(self.titles)!=0):
            obj.startclickablerect = self.startclickablerect
            obj.clickablerect = self.clickablerect
        obj.refreshscale()
        obj.resetcords(False)
    def getalltableitems(self):
        if len(self.titles) != 0: titlerem = 1
        else: titlerem = 0
        lis = self.table[titlerem:]
        alltable = []
        for y in lis:
            alltable+=[a.ID for a in y]
        return alltable
    
    def initheightwidth(self):
        w = self.getmasterwidth()
        h = self.getmasterheight()
        ##
        ratiowidth = False
        if self.startwidth!=-1: ratiowidth = True
        if type(self.startboxwidth) == int:
            if self.columns == 0: tempboxwidth = [self.startboxwidth]
            else: tempboxwidth = [self.startboxwidth for a in range(self.columns)]
        else:
            tempboxwidth = self.startboxwidth[:]
            while len(tempboxwidth)<self.columns:
                tempboxwidth.append(-1)
        if ratiowidth:
            splitwidth = self.width-self.linesize*(self.columns+1)
            count = 0
            for a in tempboxwidth:
                if a == -1: count+=1
                elif type(a) == int: splitwidth-=a
                elif type(a) == str: splitwidth-=relativetoval(a,w,h,self.ui)
            for i,a in enumerate(tempboxwidth):
                if a == -1: tempboxwidth[i] = splitwidth/count
                
        if not (not self.compress and type(self.compress) == bool):
            if type(self.compress) == bool:
                compress = normalizelist([1 for a in tempboxwidth])
                for i in range(len(compress)):
                    if tempboxwidth[i] == -1:
                        compress[i] = 0
            elif type(self.compress) == int:
                compress = [0 for a in tempboxwidth]
                compress[self.compress] = 1
            else:
                compress = normalizelist(self.compress[:])
                if len(compress) != len(tempboxwidth):
                    raise Exception(f'Wrong length of variable "compress" in object {self.ID}')
            for i in range(len(tempboxwidth)):
                if compress[i] != 0:
                    tempboxwidth[i] = str(tempboxwidth[i])+f'-(ui.IDs["{self.ID}"].scroller.width+ui.IDs["{self.ID}"].border)*ui.IDs["{self.ID}"].scroller.active*{compress[i]}'
        self.boxwidth = []
        for a in tempboxwidth:
            self.boxwidth.append(max(relativetoval(a,w,h,self.ui),-1))
        ##
        if self.startboxheight == -1 and self.startheight!=-1:
            tempboxheight = [(self.height-self.linesize*(self.rows+1))/self.rows for a in range(self.rows)]
        elif type(self.startboxheight) == int:
            if self.rows == 0: tempboxheight = [self.startboxheight]
            else: tempboxheight = [self.startboxheight for a in range(self.rows)]
        else:
            tempboxheight = self.startboxheight[:]
            while len(tempboxheight)<self.rows:
                tempboxheight.append(-1)
            while len(tempboxheight)>self.rows and len(tempboxheight)>0 and tempboxheight[-1] == -1:
                del tempboxheight[-1]
        self.boxheight = []
        for a in tempboxheight:
            self.boxheight.append(relativetoval(a,w,h,self.ui))

    def gettablewidths(self):
        self.boxwidthsinc = []
        self.boxwidths = []
        for a in range(len(self.boxwidth)):
            if self.boxwidth[a] == -1:
                minn = 0
                for b in [self.table[c][a] for c in range(len(self.table))]:
                    if type(b) in [BUTTON,TEXT]:
                        if minn<b.textimage.get_width()+b.horizontalspacing*2*self.scale:
                            minn = b.textimage.get_width()+b.horizontalspacing*2*self.scale
                    elif type(b) in [TABLE,SCROLLERTABLE,SLIDER]:
                        if minn<b.width:
                            minn = b.width*b[1].scale
                self.boxwidthsinc.append(sum(self.boxwidths))
                self.boxwidths.append(minn/self.scale)
            else:
                self.boxwidthsinc.append(sum(self.boxwidths))
                self.boxwidths.append(self.boxwidth[a])
        self.boxwidthtotal = sum(self.boxwidths)
        self.width = self.boxwidthtotal+self.linesize*(self.columns+1)

        
    def gettableheights(self):
        self.boxheightsinc = [] 
        self.boxheights = []
        for a in range(len(self.boxheight)):
            if self.boxheight[a] == -1:
                minn = 0
                for b in [self.table[a][c] for c in range(len(self.table[0]))]:
                    if type(b) in [BUTTON,TEXT]:
                        if minn<b.textimage.get_height()+b.verticalspacing*2*self.scale:
                            minn = b.textimage.get_height()+b.verticalspacing*2*self.scale
                    elif type(b) in [TABLE,SCROLLERTABLE,SLIDER]:
                        if minn<b.height:
                            minn = b.height*b[1].scale
                self.boxheightsinc.append(sum(self.boxheights))
                self.boxheights.append(minn/self.scale)
            else:
                self.boxheightsinc.append(sum(self.boxheights))
                self.boxheights.append(self.boxheight[a])
        self.boxheighttotal = sum(self.boxheights)
        self.height = self.boxheighttotal+self.linesize*(self.rows+1)

    def estimatewidths(self):
        self.boxheightsinc = []
        self.boxheights = []
        for a in self.boxheight:
            self.boxheightsinc.append(sum(self.boxheights))
            if a == -1: self.boxheights.append(self.guessheight)
            else: self.boxheights.append(a)
        self.boxwidthsinc = []
        self.boxwidths = []
        for a in self.boxwidth:
            self.boxwidthsinc.append(sum(self.boxwidths))
            if a == -1:
                self.boxwidths.append(self.guesswidth)
            else: self.boxwidths.append(a)
        
            
    def wipe(self,titles=True):
        for i,a in enumerate(self.table):
            if titles or i>0:
                for b in a:
                    self.ui.delete(b.ID,False)
        self.data = []
        if titles:
            self.titles = []
                    
    def child_render(self,screen):
        self.draw(screen)
        
    def draw(self,screen):
        if self.enabled:
            if self.glow!=0:
                screen.blit(self.glowimage,(self.x*self.dirscale[0]-self.glow*self.scale,self.y*self.dirscale[1]-self.glow*self.scale))
            if self.borderdraw:
                if type(self) == SCROLLERTABLE: h = min(self.height,self.scroller.pageheight)
                else: h = self.height
                draw.rect(screen,self.bordercol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,(h)*self.scale),border_radius=int(self.roundedcorners*self.scale))                            
    def getat(self,row,column):
        return self.table[row+1][column]
    def row_append(self,row):
        self.rows+=1
        self.data.append(row)
        pre = self.columns
        self.preprocess()
        if pre!=self.columns:
            self.refresh()
            self.small_refresh()
        else:
            self.boxheight.append(-1)
            self.__row_init__(len(self.preprocessed)-1)
    def row_insert(self,row,index):
        if index<len(self.table):
            self.rows+=1
            self.data.insert(index,row)
            if len(self.titles)!=0: index+=1
            pre = self.columns
            self.preprocess()
            if pre!=self.columns:
                self.refresh()
                self.small_refresh()
            else:
                self.boxheight.insert(index,-1)
                self.__row_init__(index)
            return True
        else: return False
    def row_remove(self,index):
        if index<len(self.table)-1:
            self.rows-=1
            if index == -1:
                self.titles = []
                index = 0
            else:
                del self.data[index]
                if len(self.titles)!=0: index+=1
            pre = self.columns
            self.preprocess()
            if pre!=self.columns:
                self.refresh()
            else:
                for a in self.table[index]:
                    self.ui.delete(a.ID)
                del self.boxheight[index]
                del self.table[index]
                self.gettableheights()
                for a in range(index,len(self.table)):
                    for i,b in enumerate(self.table[a]):
                        self.ui.reID('tabletext'+self.tableitemID+self.ID+str(a)+str(i),b)
                        self.itemrefreshcords(b,i,a)
            self.small_refresh()
            return True
        else:
            return False
    def row_replace(self,row,index):
        self.row_remove(index)
        return self.row_insert(row,index)
        
    def __row_init__(self,index):
        self.initheightwidth()
        self.estimatewidths()
        for a in range(len(self.table)-1,index-1,-1):
            for i,b in enumerate(self.table[a]):
                self.ui.reID('tabletext'+self.tableitemID+self.ID+str(a+1)+str(i),b)
        self.table.insert(index,self.row_gentext(index))
        self.gettableheights()  
        for a in range(index,len(self.table)):
            for i,b in enumerate(self.table[a]):
                self.itemrefreshcords(b,i,a)
        self.small_refresh()
    def small_refresh(self):
        self.autoscale()
        self.initheightwidth()
        self.refreshglow()
        self.gettablewidths()
        self.gettableheights()
        self.refreshclickablerect()
        self.refreshcords()
        self.refreshbound()

class SCROLLERTABLE(TABLE):
    def render(self,screen):
        if self.killtime != -1 and self.killtime<self.ui.time:
            self.ui.delete(self.ID)
        elif self.enabled:
            self.child_render(screen)
            
            alltable = self.getalltableitems()
            
            for a in [i.ID for i in self.bounditems][:]:
                if a in self.ui.IDs and not(a in alltable):
                    self.ui.IDs[a].render(screen)
                    
            reduce = 0
            if len(self.titles) != 0:
                reduce = (self.linesize+self.boxheights[0])
            self.ui.drawtosurf(screen,alltable,self.backingcol,self.x*self.dirscale[0]+self.linesize*self.scale,self.y*self.dirscale[1]+(self.linesize+reduce)*self.scale,(self.x*self.dirscale[0]+self.linesize*self.scale,self.y*self.dirscale[1]+(self.linesize+reduce)*self.scale,(self.width-self.linesize*2)*self.scale,min(self.height-self.linesize*2-reduce,self.scroller.pageheight-self.linesize*2-reduce)*self.scale),'render',self.roundedcorners)
    def smartdraw(self,screen):
        self.child_render(screen)
            
        alltable = self.getalltableitems()
        
        for a in [i.ID for i in self.bounditems][:]:
            if a in self.ui.IDs and not(a in alltable):
                self.ui.IDs[a].draw(screen)
                
        reduce = 0
        if len(self.titles) != 0:
            reduce = (self.linesize+self.boxheights[0])
            self.ui.drawtosurf(screen,alltable,self.backingcol,self.x*self.dirscale[0]+self.linesize*self.scale,self.y*self.dirscale[1]+(self.linesize+reduce)*self.scale,(self.x*self.dirscale[0]+self.linesize*self.scale,self.y*self.dirscale[1]+(self.linesize+reduce)*self.scale,(self.width-self.linesize*2)*self.scale,min(self.height-self.linesize*2-reduce,self.scroller.pageheight-self.linesize*2-reduce)*self.scale),'draw',self.roundedcorners)

    def scrollerblocks(self,scroller):
        scroller.limitpos()
        alltable = self.getalltableitems()
        for a in alltable:
            self.ui.IDs[a].scrollcords = (0,scroller.scroll)
            self.ui.IDs[a].resetcords()
    def getheight(self):
        return min(self.height,self.pageheight)
    def refresh(self):
        self.refreshscale()
        self.preprocess()
        self.initheightwidth()
        self.estimatewidths()
        self.gentext()
        active = self.scroller.active
        self.small_refresh()
        self.scroller.refresh()
        if self.scroller.active != active:
            self.small_refresh()
        self.scrollerblocks(self.scroller)
        self.threadactive = False
    def small_refresh(self):
        self.scroller.autoscale()
        self.scroller.checkactive()
        self.autoscale()
        self.initheightwidth()
        self.refreshglow()
        self.gettablewidths()
        self.gettableheights()
        self.refreshclickablerect()
        self.refreshcords()
        self.scrollerblocks(self.scroller)
        self.refreshbound()
        
class DROPDOWN(BUTTON):
    def mainbuttonclicked(self):
        if not self.window.opening:
            self.window.open('compressup',toggleopen=False)
        else:
            self.window.shut('compressup')
    def optionclicked(self,index):
        self.active = self.options[index]
        self.titletext.settext(self.options[index])
        self.window.shut('compressup')
        self.truecommand()
    
    

# Anticlickablerect
# Non windowed winowedmenu
    
class TEXT(GUI_ITEM):
    def reset(self):
        self.refreshscale()
        self.gentext()
        self.autoscale()
        self.resetcords()
        self.refreshcords()
        self.refreshglow()
    def child_autoscale(self):
        if self.startwidth == -1:
            self.width = max([a.get_width() for a in self.textimages])/self.scale+self.horizontalspacing*2
        if self.startheight == -1:
            self.height = max([a.get_height() for a in self.textimages])/self.scale+self.verticalspacing*2
    def child_render(self,screen):
        self.getclickedon()
        self.draw(screen)
    def draw(self,screen):
        if self.enabled:
            self.animatetext()
            if self.glow!=0:
                screen.blit(self.glowimage,(self.x*self.dirscale[0]-self.glow*self.scale,self.y*self.dirscale[1]-self.glow*self.scale))
            if self.backingdraw:
                draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
            if self.borderdraw:
                draw.rect(screen,self.bordercol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),self.border*self.scale,border_radius=int(self.roundedcorners*self.scale))
            if self.pregenerated:
                if self.textcenter:
                    try:
                        screen.blit(self.textimage,(self.x*self.dirscale[0]+self.width/2*self.scale-self.textimage.get_width()/2,self.y*self.dirscale[1]+self.height/2*self.scale-self.textimage.get_height()/2))
                    except:
                        print('error in drawing',self.ID)
                else:
                    try:
                        screen.blit(self.textimage,(self.x*self.dirscale[0]+(self.horizontalspacing+self.textoffsetx)*self.scale,self.y*self.dirscale[1]+(self.verticalspacing+self.textoffsetx)*self.scale))
                    except:
                        print('error in drawing',self.ID)
            else:
                self.ui.write(screen,self.x*self.dirscale[0]+(self.horizontalspacing+self.textoffsetx)*self.scale,self.y*self.dirscale[1]+(self.verticalspacing+self.textoffsetx)*self.scale,self.text,self.textsize*self.scale,self.textcol,self.textcenter,self.font,self.bold,self.antialiasing)
    def refresh(self):
        self.refreshscale()
        self.gentext()
        self.autoscale()
        self.refreshcords()
        self.refreshglow()
        self.resetcords()
        self.refreshbound()
        self.refreshclickablerect()

class SCROLLER(GUI_ITEM):
    def reset(self):
        self.autoscale()
        self.scroll = self.startp
        self.scheight = self.height-self.border*2
        self.prevholding = self.holding
        self.refreshscale()
        self.refresh()
        self.resetcords()
        self.checkactive()
        self.refreshclickablerect()
    def child_render(self,screen):
        self.checkactive()
        if self.active:
            temp = (self.x,self.y)
            self.getclickedon(pygame.Rect(self.x*self.dirscale[0]+self.leftborder*self.scale,self.y*self.dirscale[1]+(self.border+self.scroll*(self.scheight/(self.maxp-self.minp)))*self.scale,(self.width-self.leftborder-self.rightborder)*self.scale,((self.pageheight/(self.maxp-self.minp))*self.scheight)*self.scale),smartdrag=False)
            if self.holding:
                self.scroll = (self.y-temp[1])*self.dirscale[1]/self.dirscale[0]/(self.scheight/(self.maxp-self.minp))
                self.limitpos()
            self.x,self.y = temp
            self.scrollobjects()
            self.draw(screen)
    def child_autoscale(self):
        compress = 1
        if self.screencompressed:
            if self.y*self.dirscale[1]+self.height*self.scale>self.ui.screenh:
                compress = 1-(self.y*self.dirscale[1]+self.height*self.scale-self.ui.screenh+self.screencompressed)/(self.height*self.scale)
        self.height*=compress
        self.scheight = self.height-self.border*2
        self.maxp = relativetoval(self.startmaxp,self.getmasterwidth()/self.scale,self.getmasterheight()/self.scale,self.ui)
        self.minp = relativetoval(self.startminp,self.getmasterwidth()/self.scale,self.getmasterheight()/self.scale,self.ui)
        self.pageheight = relativetoval(self.startpageheight,self.getmasterwidth()/self.scale,self.getmasterheight()/self.scale,self.ui)*compress
        
    def limitpos(self):
        if not self.active:
            self.scroll = self.minp
        elif self.scroll<self.minp:
            self.scroll = self.minp
        elif self.scroll>self.maxp-self.pageheight:
            self.scroll = self.maxp-self.pageheight

    def refresh(self):
        self.autoscale()
        self.refreshcords()
        self.checkactive()
        self.limitpos()
        self.refreshbound()
        
    def checkactive(self):
        if (self.maxp-self.minp)>self.pageheight: self.active = True
        else: self.active = False

    def setscroll(self,scroll,relative=False):
        if relative:
            self.scroll+=scroll
        else:
            self.scroll = scroll
        self.limitpos()
    def setminp(self,minp):
        self.startminp = minp
        self.autoscale()
    def setmaxp(self,maxp):
        self.startmaxp = maxp
        self.autoscale()
    def setpageheight(self,pageheight):
        self.startpageheight = pageheight
        self.autoscale()
        
    def scrollobjects(self):
        for a in self.scrollbind:
            if self.ui.IDs[a].scrollcords != (self.ui.IDs[a].scrollcords[0],self.scroll):
                self.ui.IDs[a].scrollcords = (self.ui.IDs[a].scrollcords[0],self.scroll)
                self.ui.IDs[a].resetcords()
                
    def child_refreshcords(self):
        if self.maxp-self.minp == 0: self.maxp = self.minp+0.1
##        self.sliderrect = pygame.Rect(self.x+self.border,self.y+self.border+self.scroll*(self.scheight/(self.maxp-self.minp)),self.scrollerwidth,self.scrollerheight)

    def draw(self,screen):
        if self.enabled and self.active:
            if self.glow!=0:
                screen.blit(self.glowimage,(self.x*self.dirscale[0]-self.glow*self.scale,self.y*self.dirscale[1]-self.glow*self.scale))
            draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
            draw.rect(screen,self.scrollercol,roundrect(self.x*self.dirscale[0]+self.leftborder*self.scale,self.y*self.dirscale[1]+(self.border+self.scroll*(self.scheight/(self.maxp-self.minp)))*self.scale,(self.width-self.leftborder-self.rightborder)*self.scale,((self.pageheight/(self.maxp-self.minp))*self.scheight)*self.scale),border_radius=int(self.roundedcorners*self.scale))

class SLIDER(GUI_ITEM):
    def reset(self):
        self.slider = self.startp
        self.holding = False
        self.prevholding = False
        self.holdingcords = [self.x,self.y]
        self.refreshscale()
        self.resetbutton()
        self.resetcords()
        self.roundedcorners = min([self.roundedcorners,self.width/2,self.height/2])
    def refresh(self):
        self.autoscale()
        self.limitpos()
        self.refreshbutton()
        self.refreshglow()
        self.refreshbound()
    def child_refreshcords(self):
##        self.
##        self.innerrect = pygame.Rect(self.slidercenter[0]-self.slidersize/2+self.border,self.slidercenter[1]-self.slidersize/2+self.border,self.slidersize-self.border*2,self.slidersize-self.border*2)
        self.refreshbuttoncords()
    def resetbutton(self):
        self.getslidercenter()
        try:
            self.bounditems.remove(self.button)
            self.ui.delete(self.button.ID,False)
        except:
            pass
        if type(self.data) == BUTTON: self.button = self.data
        else:
            self.button = self.ui.makebutton(0,0,self.text,self.textsize,emptyfunction,self.menu,self.ID+'button',self.layer+0.01,self.roundedcorners,width=self.slidersize,height=self.slidersize,img=self.img,dragable=self.dragable,
                                             clickdownsize=int(self.slidersize/15),col=shiftcolor(self.col,-30),scaleby=self.scaleby)

        if self.direction == 'vertical': self.button.startobjanchor = [self.button.width/2,self.button.height/2]
        else: self.button.startobjanchor = ['w/2','h/2']
        self.button.dragable = False
        self.binditem(self.button)
        
    def getslidercenter(self):
        offset = 0
        if self.containedslider: offset = self.button.width/2
        if self.maxp-self.minp != 0: pos = (self.slider-self.minp)/(self.maxp-self.minp)
        else: pos = 0
            
        self.slidercenter = (self.leftborder+offset+(self.width-self.leftborder-self.rightborder-offset*2)*pos,self.height/2)
        if self.direction == 'vertical':
            if self.containedslider: offset = self.button.height/2
            self.slidercenter = (self.width/2,self.upperborder+offset+(self.height-self.upperborder-self.lowerborder-offset*2)*pos)
    def refreshbuttoncords(self):
        self.getslidercenter()
        self.button.startx = self.slidercenter[0]
        self.button.starty = self.slidercenter[1]
        self.button.startanchor = [0,0]
        self.button.resetcords(False)
        
    def refreshbutton(self):
        self.button.refresh()
        self.refreshbuttoncords()
    def updatetext(self):
        if self.boundtext!=-1:
            self.boundtext.settext(str(self.slider))
        
    def child_render(self,screen):
        self.draw(screen)
        if self.button.holding:
            self.movetomouse()
        if self.button.clickedon == self.runcommandat:
            self.command()
        if self.movetoclick: self.movebuttontoclick()
    def movebuttontoclick(self):
        self.getclickedon(roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),False,False)
        if self.clickedon == 0:
            self.button.holding = True
            self.button.holdingcords = [self.button.width/2,self.button.height/2]
    def movetomouse(self):
        if self.maxp-self.minp != 0: pos = self.scale/(self.maxp-self.minp)
        else: pos = 0
        self.slider = (self.ui.mpos[0]-self.x*self.dirscale[0]-self.leftborder*self.scale)/((self.width-self.leftborder-self.rightborder)*pos)+self.minp
        if self.direction == 'vertical':
            self.slider = (self.ui.mpos[1]-self.y*self.dirscale[1]-self.upperborder*self.scale)/((self.height-self.upperborder-self.lowerborder)*pos)+self.minp
        if self.increment!=0: self.slider = round(self.slider/self.increment)*self.increment
        self.limitpos()
        self.updatetext()
    def limitpos(self):
        if self.slider>self.maxp:
            self.slider = self.maxp
        elif self.slider<self.minp:
            self.slider = self.minp
        self.refreshbuttoncords()
    def child_autoscale(self):
        self.maxp = relativetoval(self.startmaxp,self.getmasterwidth()/self.scale,self.getmasterheight()/self.scale,self.ui)
        self.minp = relativetoval(self.startminp,self.getmasterwidth()/self.scale,self.getmasterheight()/self.scale,self.ui)
    def setslider(self,slider,relative=False):
        if relative:
            self.slider+=slider
        else:
            self.slider = slider
        self.limitpos()
    def setminp(self,minp):
        self.startminp = minp
        self.autoscale()
    def setmaxp(self,maxp):
        self.startmaxp = maxp
        self.autoscale()

    def draw(self,screen):
        if self.enabled:
            if self.glow!=0:
                screen.blit(self.glowimage,(self.x*self.dirscale[0]-self.glow*self.scale,self.y*self.dirscale[1]-self.glow*self.scale))
            draw.rect(screen,self.bordercol,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),border_radius=int(self.roundedcorners*self.scale))
            if self.slider!=self.minp:
                if self.direction == 'vertical':
                    h = ((self.height-self.upperborder-self.lowerborder-self.button.height*self.containedslider)*((self.slider-self.minp)/(self.maxp-self.minp))+self.button.height*self.containedslider)
                    w = (self.width-self.leftborder-self.rightborder)-2*(self.roundedcorners-abs(int(min([self.roundedcorners,h/2]))))
                    draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0]+self.leftborder*self.scale,self.y*self.dirscale[1]+self.upperborder*self.scale,w*self.scale,h*self.scale),border_radius=int(self.roundedcorners*self.scale))
                else:
                    w = ((self.width-self.leftborder-self.rightborder-self.button.width*self.containedslider)*((self.slider-self.minp)/(self.maxp-self.minp))+self.button.width*self.containedslider)
                    h = (self.height-self.upperborder-self.lowerborder)-2*(self.roundedcorners-abs(int(min([self.roundedcorners,w/2]))))
                    draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0]+self.leftborder*self.scale,self.y*self.dirscale[1]+(self.height-h)/2*self.scale,w*self.scale,h*self.scale),border_radius=int(self.roundedcorners*self.scale))



class WINDOWEDMENU(GUI_ITEM):
    def reset(self):
        self.truedarken = self.darken
        self.resetcords()
        self.refresh()
        for a in self.ui.items:
            if a.menu == self.menu and a!=self and not(type(a) in [MENU]) and type(a.master[0]) in [MENU,WINDOWEDMENU]:
                self.binditem(a)
                a.refresh()
        self.ui.delete(f'auto_generated_menu:{self.menu}',False)
        self.bounditems.sort(key=lambda x: x.layer,reverse=False)
    def refresh(self):
        self.autoscale()
        self.refreshscale()
        self.refreshcords()
        self.refreshglow()
        self.refreshbound()
    def child_refreshcords(self):
        for a in self.bounditems:
            a.resetcords()
    def child_render(self,screen):
        self.draw(screen)
    def draw(self,screen):
        if self.enabled:
            darkening = pygame.Surface((self.ui.screenw,self.ui.screenh),pygame.SRCALPHA)
            darkening.fill((0,0,0,self.darken))
            screen.blit(darkening,(0,0))
            if self.glow!=0:
                screen.blit(self.glowimage,(self.x*self.dirscale[0]-self.glow*self.scale,self.y*self.dirscale[1]-self.glow*self.scale))
            if self.backingdraw:
                draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),self.border,border_radius=int(self.roundedcorners*self.scale))

class MENU(GUI_ITEM):
    def reset(self):
        self.scalesize = False
    def refresh(self):
        self.refreshscale()
        self.refreshcords()
        self.startwidth = self.ui.screenw
        self.startheight = self.ui.screenh
        self.width = self.ui.screenw
        self.height = self.ui.screenh
        self.refreshbound()
    def child_refreshcords(self):
        for a in self.bounditems:
            a.resetcords()
    def drawallmenu(self,screen,obj='self'):
        if obj == 'self':
            bound = self.bounditems
        else:
            bound = obj.bounditems
            
        for a in bound:
            if type(a) == SCROLLERTABLE:
                a.smartdraw(screen)
            else:
                a.draw(screen)
                self.drawallmenu(screen,a)
        
    def child_render(self,screen):
        pass
    def draw(self,screen):
        pass

class WINDOW(GUI_ITEM):
    def reset(self):
        self.refreshscale()
        self.autoscale()
        self.refreshcords()
        self.resetcords()
        self.refresh()
        self.clearanimations()
        self.opening = self.enabled
    def clearanimations(self):
        self.animationdata = {'moveleft':{'active':False,'progress':0,'wave':'linear','forward':True},
                              'moveright':{'active':False,'progress':0,'wave':'linear','forward':True},
                              'moveup':{'active':False,'progress':0,'wave':'linear','forward':True},
                              'movedown':{'active':False,'progress':0,'wave':'linear','forward':True},
                              'compressleft':{'active':False,'progress':0,'wave':'linear','forward':True},
                              'compressright':{'active':False,'progress':0,'wave':'linear','forward':True},
                              'compressup':{'active':False,'progress':0,'wave':'linear','forward':True},
                              'compressdown':{'active':False,'progress':0,'wave':'linear','forward':True}}
    def refresh(self):
        self.autoscale()
        self.refreshscale()
        self.refreshcords()
        self.refreshglow()
        self.refreshbound()
    def enable(self):
        self.enabled = True
        self.child_autoscale()
    def disable(self):
        self.enabled = False
        self.child_autoscale()
    def open(self,animation='default',animationlength=-1,toggleopen=True):
        if animation == 'default': animation = self.animationtype
        if animationlength == -1: animationlength = self.animationspeed
        if not self.opening:
            self.enable()
            self.opening = True
            self.makeanimation(animation,animationlength,False)
        elif toggleopen:
            self.shut()
    def shut(self,animation='default',animationlength=-1):
        if self.opening:
            if animation == 'default': animation = self.animationtype
            if animationlength == -1: animationlength = self.animationspeed
            self.opening = False
            self.makeanimation(animation,flippable=False)
            if animation == 'none': self.disable()
    def makeanimation(self,animation='default',length=-1,forward=True,flippable=True):
        if animation == 'default': animation = self.animationtype
        if length == -1: length = self.animationspeed
        if animation !='none':
            self.enable()
            for a in animation.split():
                if a.split(':')[0] in list(self.animationdata):
                    if self.animationdata[a.split(':')[0]]['active']:
                        if flippable or self.animationdata[a.split(':')[0]]['forward']!=forward:
                            self.animationdata[a.split(':')[0]]['progress'] = 1- self.animationdata[a.split(':')[0]]['progress']
                            self.animationdata[a.split(':')[0]]['forward'] = not self.animationdata[a.split(':')[0]]['forward']
                    else:
                        wave = 'sinout'
                        if len(a.split(':'))>1:
                            if a.split(':')[1] in ['linear','sin','sinin','sinout']:
                                wave = a.split(':')[1]
                        self.animationdata[a.split(':')[0]]['progress'] = 0
                        self.animationdata[a.split(':')[0]]['active'] = True
                        self.animationdata[a.split(':')[0]]['wave'] = wave
                        self.animationdata[a.split(':')[0]]['forward'] = forward
            self.animationlength = length
    def decodeanimations(self):
        xoff = 0
        yoff = 0
        objxoff = 0
        objyoff = 0
        widthoff = 0
        heightoff = 0
        for a in self.animationdata:
            if self.animationdata[a]['active']:
                prog = self.convertprogress(self.animationdata[a])
                if 'move' in a:
                    if 'left' in a: xoff-=prog*(self.x+self.width)
                    elif 'right' in a: xoff+=prog*(self.ui.screenw/self.scale-self.x)
                    if 'up' in a: yoff-=prog*(self.y+self.height)
                    elif 'down' in a: yoff+=prog*(self.ui.screenh/self.scale-self.y)
                elif 'compress' in a:
                    if 'left' in a:
                        widthoff-=prog*(self.width)
                        objxoff+=prog*(self.width)
                    elif 'right' in a:
                        widthoff-=prog*(self.width)
                        xoff+=prog*(self.width)
                    if 'up' in a:
                        heightoff-=prog*(self.height)
                        objyoff+=prog*(self.height)
                    elif 'down' in a:
                        heightoff-=prog*(self.height)
                        yoff+=prog*(self.height)
        return xoff,yoff,objxoff,objyoff,widthoff,heightoff
    def moveanimation(self):
        for a in self.animationdata:
            if self.animationdata[a]['active']:
                self.animationdata[a]['progress']+=self.ui.deltatime/self.animationlength
                if self.animationdata[a]['progress']>1:
                    self.animationdata[a]['active'] = False
                    if self.animationdata[a]['forward']:
                        self.disable()
    def convertprogress(self,data):
        progress = data['progress']
        wave = data['wave']
        if not data['forward']: progress = 1-progress
        if wave == 'sinin': return math.sin(progress*math.pi/2)
        elif wave == 'sinout': return math.sin((progress-1)*math.pi/2)+1
        elif wave == 'siun': return math.sin((progress-0.5)*math.pi)/2+0.5
        else: return progress
        
    def child_autoscale(self):
        # Rect,IDs,menu,whitelist (true=all objects in list blocked by noclickrect)
        if self.enabled:
            self.noclickrect = [(pygame.Rect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),self.getchildIDs(),self.menu,False)]
        else:
            self.noclickrect = []
        self.ui.refreshnoclickrects()
        for a in self.bounditems: a.clickablerect = self.clickablerect
    def binditem(self,obj):
        super().binditem(obj)
        obj.resetcords()
        self.child_autoscale()
        
    def render(self,screen):
        self.moveanimation()
        self.xoff,self.yoff,self.objxoff,self.objyoff,self.widthoff,self.heightoff = self.decodeanimations()
        if self.killtime != -1 and self.killtime<self.ui.time:
            self.ui.delete(self.ID)
        elif self.enabled:
            
            self.child_render(screen)
            
            self.ui.drawtosurf(screen,[a.ID for a in self.bounditems],self.col,self.x*self.dirscale[0]+self.xoff*self.scale,self.y*self.dirscale[1]+self.yoff*self.scale,(self.x*self.dirscale[0]+self.objxoff*self.scale,self.y*self.dirscale[1]+self.objyoff*self.scale,(self.width+self.widthoff)*self.scale,(self.height+self.heightoff)*self.scale),'render',self.roundedcorners)

    def child_render(self,screen):
        self.draw(screen)
    def draw(self,screen):
        if self.enabled:
            if self.glow!=0:
                screen.blit(self.glowimage,(self.x*self.dirscale[0]-self.glow*self.scale,self.y*self.dirscale[1]-self.glow*self.scale))
            if self.backingdraw:
                draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0]+self.xoff*self.scale,self.y*self.dirscale[1]+self.yoff*self.scale,(self.width+self.widthoff)*self.scale,(self.height+self.heightoff)*self.scale),border_radius=int(self.roundedcorners*self.scale))

class ANIMATION:
    def __init__(self,ui,animateID,startpos,endpos,movetype,length,wait,relativemove,command,runcommandat,skiptoscreen,acceleration,permamove,ID):
        self.startpos = startpos
        self.endpos = endpos
        self.trueendpos = 0
        self.movetype = movetype
        self.length = length
        self.acceleration = acceleration
        self.relativemove = relativemove

        self.command = command
        self.runcommandat = runcommandat

        self.ui = ui
        self.ID = ID
        self.animateID = animateID
        self.permamove = permamove
        
        self.progress = 0
        self.timetracker = 0
        self.wait = wait
        self.skip = skiptoscreen
        self.fadeout = False

        self.onitem = False
        self.bounditems = []
    def gencordlist(self,regenerating=False):
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
        if (self.skip or type(self.ui.IDs[self.animateID]) == WINDOWEDMENU) and not regenerating:
            self.findonscreen()
    def findonscreen(self):
        scale = self.ui.IDs[self.animateID].scale
        dirscale = self.ui.IDs[self.animateID].dirscale
        scords = self.startpos[:]
        ecords = self.endpos[:]
        start = self.checkonscreen(dirscale,scale,scords)
        end = self.checkonscreen(dirscale,scale,ecords)
        cross = list(self.startpos[:])
        self.fadeout = False
        if end!=start:
            if end: out = scords
            else: out = ecords
            if out[0]<0: cross[0] = -self.ui.IDs[self.animateID].width
            elif out[0]>self.ui.screenw: cross[0] = self.ui.screenw/dirscale[0]
            if out[1]<0: cross[1] = -self.ui.IDs[self.animateID].height
            elif out[1]>self.ui.screenh: cross[1] = self.ui.screenh/dirscale[1]

            
            
            if end:
                self.startpos = cross
            else:
                self.endpos = cross
                self.fadeout = True
            
            self.gencordlist(True)
    def checkonscreen(self,dirscale,scale,cords):
        return pygame.Rect(0,0,self.ui.screenw,self.ui.screenh).colliderect(pygame.Rect(cords[0],cords[1],self.ui.IDs[self.animateID].width*scale,self.ui.IDs[self.animateID].height*scale))
        
    def animate(self):
        prev = round(self.timetracker)
        if self.wait in [0,1]:
            self.timetracker+=1
        self.timetracker+=self.ui.deltatime
        new = round(self.timetracker)
        for a in range(prev,new):
            if self.move1frame():
                return True
        return False
    def move1frame(self):
        self.wait-=1
        if self.wait == 0:
            sp,ep = False,False
            if self.startpos == 'current':
                sp = True
                self.startpos = (self.ui.IDs[self.animateID].x,self.ui.IDs[self.animateID].y)
            if self.endpos == 'current':
                ep = True
                self.endpos = (self.ui.IDs[self.animateID].x,self.ui.IDs[self.animateID].y)
            if self.relativemove:
                if (sp and not ep):
                    self.endpos = ((self.startpos[0]+self.endpos[0]),(self.startpos[1]+self.endpos[1]))
                elif (ep and not sp):
                    self.startpos = ((self.startpos[0]+self.endpos[0]),(self.startpos[1]+self.endpos[1]))
            self.trueendpos = self.endpos[:]
            self.gencordlist()
        if self.wait<1:
            if self.progress<self.length:
                self.ui.IDs[self.animateID].smartcords(self.cordlist[self.progress][0],self.cordlist[self.progress][1],self.permamove)
                if type(self.ui.IDs[self.animateID]) in [TABLE,TEXTBOX,TEXT,SCROLLER,SLIDER,WINDOWEDMENU,MENU]:
                    self.ui.IDs[self.animateID].refreshcords()
                if type(self.ui.IDs[self.animateID]) == WINDOWEDMENU:
                    self.ui.IDs[self.animateID].darken = self.ui.IDs[self.animateID].truedarken*(self.progress/self.length)
                    if self.fadeout: self.ui.IDs[self.animateID].darken = self.ui.IDs[self.animateID].truedarken-self.ui.IDs[self.animateID].darken

            if self.progress == self.runcommandat or (type(self.runcommandat)==list and self.progress in self.runcommandat):
                self.command()
            self.progress+=1
            if self.progress >= self.length:
                self.finish()
                return True
        return False
    def finish(self,forcefinish=False):
        if forcefinish:
            while not self.animate():
                pass
        if self.relativemove and self.wait>0 and self.endpos!='current':
            if self.startpos == 'current':
                self.startpos = (self.ui.IDs[self.animateID].x,self.ui.IDs[self.animateID].y)
            self.endpos = (self.startpos[0]+self.endpos[0],self.startpos[1]+self.endpos[1])
        self.ui.IDs[self.animateID].smartcords(self.trueendpos[0],self.trueendpos[1],self.permamove)
        if (type(self.ui.IDs[self.animateID]) in [TABLE,TEXTBOX,TEXT,SCROLLER,SLIDER,WINDOWEDMENU,MENU]) and self.permamove:
            self.ui.IDs[self.animateID].resetcords()
        if type(self.ui.IDs[self.animateID]) == WINDOWEDMENU:
            self.ui.IDs[self.animateID].darken = self.ui.IDs[self.animateID].truedarken
        if self.progress == self.runcommandat or self.runcommandat == -1 or (type(self.runcommandat)==list and self.progress in self.runcommandat):
            self.command()

class RECT(GUI_ITEM):
    def child_render(self,screen):
        self.getclickedon()
        self.draw(screen)
    def draw(self,screen):
        if self.enabled:
            if self.glow!=0:
                screen.blit(self.glowimage,(self.x*self.dirscale[0]-self.glow*self.scale,self.y*self.dirscale[1]-self.glow*self.scale))
            if self.backingdraw:
                draw.rect(screen,self.col,roundrect(self.x*self.dirscale[0],self.y*self.dirscale[1],self.width*self.scale,self.height*self.scale),self.border*self.scale,border_radius=int(self.roundedcorners*self.scale))
            
class Style:   
    universaldefaults = {'roundedcorners': 0, 'anchor': (0,0), 'objanchor': (0,0), 'center': False, 'centery': -1, 'textsize': 50, 'font': 'calibre', 'bold': True,
                           'antialiasing': True, 'border': 3, 'upperborder': -1, 'lowerborder': -1, 'rightborder': -1, 'leftborder': -1, 'scalesize': True,
                           'scalex': -1, 'scaley': -1, 'glow': 0, 'glowcol': -1, 'col': -1, 'textcol': -1, 'backingcol': -1, 'hovercol': -1, 'clickdownsize': 4,
                           'clicktype': 0, 'textoffsetx': 0, 'textoffsety': 0, 'maxwidth': -1, 'colorkey': -1, 'togglecol': -1, 'togglehovercol': -1, 'spacing': -1,
                           'verticalspacing': -1, 'horizontalspacing': -1, 'clickableborder': 0, 'lines': 1, 'selectcol': -1, 'selectbordersize': 2,
                           'selectshrinksize': 0, 'cursorsize': -1, 'textcenter': True, 'linesize': 2, 'backingdraw': True, 'borderdraw': True, 'animationspeed': 5,
                           'scrollercol': -1, 'slidercol': -1, 'sliderbordercol': -1, 'slidersize': -1, 'increment': 0, 'guesswidth': 100, 'guessheight': 100,
                           'sliderroundedcorners': -1, 'containedslider': True, 'movetoclick': True, 'isolated': True, 'darken': 60, 'hsvashift': False}
    
    replace = {'roundedcorners': -1, 'center': -1, 'textsize': -1,'font': -1,'bold': -1,'antialiasing': -1,'border': -1, 'scalesize': -1,'glow':-1,'col':-1,'clickdownsize': -1,'clicktype': -1,'guesswidth': -1, 'guessheight': -1,
               'textoffsetx': -1,'textoffsety': -1, 'clickableborder':-1,'textcenter': -1, 'lines': -1,'linesize':-1,'backingdraw':-1,'borderdraw': -1,'animationspeed':-1,'containedslider': -1,'movetoclick': -1,'darken':-1}
    for var in list(replace):
        universaldefaults[var] = replace[var]

    defaults = copy.deepcopy(universaldefaults)
    
    wallpapercol = (255,255,255)

    UI.objectkey = {'button':BUTTON,'text':TEXT,'textbox':TEXTBOX,'table':TABLE,'scrollertable':SCROLLERTABLE,'dropdown':DROPDOWN,'slider':SLIDER,'scroller':SCROLLER,'menu':MENU,'windowedmenu':WINDOWEDMENU,'window':WINDOW,'rect':RECT}
    
    objectdefaults = {}
    for a in [UI.objectkey[o] for o in UI.objectkey]:
        objectdefaults[a] = copy.deepcopy(defaults)







        
    
