import pygame,random,math,time,copy,ctypes
pygame.init()

def rectscaler(rect,scale):
    return pygame.Rect(rect.x*scale,rect.y*scale,rect.w*scale,rect.h*scale)
def emptyfunction():
    pass

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

class UI:
    def __init__(self,scale=1):
        pygame.key.set_repeat(350,31)
        
        self.scale = scale
        self.mouseheld = [[0,0],[0,0],[0,0]]
        self.loadtickdata()
        
        self.buttons = []
        self.tables = []
        self.textboxes = []
        self.texts = []
        self.selectedtextbox = 0
        self.IDs = {}
        
        self.activemenu = 'main'
        self.backchain = []
        self.buttondowntimer = 8
        self.checkcaps()
        self.clipboard = pygame.scrap.get('str')

        self.defaultfont = 'calibre'
        self.defaultcol = (150,150,150)
        self.defaulttextcol = (0,0,0)

    def checkcaps(self):
        hllDll = ctypes.WinDLL("User32.dll")
        self.capslock = bool(hllDll.GetKeyState(0x14))
        
    def scaleset(self,scale):
        self.scale = scale
        for a in self.buttons:
            a.refresh(self)
        for a in self.textboxes:
            titleimage = self.rendertext(a.title,a.titlesize,a.titlecol,a.titlefont,a.titlebold)
            a.gentitle(titleimage,self.scale)
            a.gentext(self)
        for a in self.tables:
            a.refresh(self)
        for a in self.texts:
            a.refresh(self)
            
    def rendergui(self,screen):
        items = self.buttons+self.textboxes+self.tables+self.texts
        items.sort(key=lambda x: x.layer,reverse=True)
        for i,a in enumerate(items):
            if a.menu == self.activemenu:
                if type(a) == BUTTON:
                    if a.render(screen,self.scale,self.mpos,self.mprs,self.mouseheld,self.buttondowntimer):
                        if a.bindtoggle != []:
                            for b in a.bindtoggle:
                                if b!=a.ID:
                                    self.IDs[b].toggle = False
                        a.command()
                        self.mouseheld[a.clicktype][1]-=1
                        
                elif type(a) == TEXTBOX:
                    a.render(screen,self.scale,self.mpos,self.mprs,self.mouseheld,self.buttondowntimer)
                    if a.selected:
                        self.selectedtextbox = self.textboxes.index(a)
                elif type(a) == TABLE:
                    a.render(screen,self.scale,self.mpos,self.mprs,self.mouseheld,self.buttondowntimer,self)
                elif type(a) == SCROLLER:
                    a.render(screen,self.scale,self.mpos,self.mprs,self.mouseheld,self.buttondowntimer)
                else:
                    a.render(screen,self.scale)
                    
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
                if self.selectedtextbox!=-1:
                    if not self.textboxes[self.selectedtextbox].selected:
                        self.selectedtextbox = -1
                    else:
                        self.textboxes[self.selectedtextbox].inputkey(self.capslock,event,self.kprs,self)
        return events
        
    def write(self,screen,x,y,text,size,col='default',center=True,font='default',bold=False,antialiasing=True):
        if font=='default': font=self.defaultfont
        if col == 'default': col = self.defaulttextcol
        largetext = pygame.font.SysFont(font,int(size*self.scale),bold)
        textsurf = largetext.render(text, antialiasing, col)
        textrect = textsurf.get_rect()
        if center:
            textrect.center = (int(x)*self.scale,int(y)*self.scale)
        else:
            textrect.x = int(x)*self.scale
            textrect.y = int(y)*self.scale
        screen.blit(textsurf, textrect)

    def rendertext(self,text,size,col='default',font='default',bold=False,antialiasing=True):
        if font=='default': font=self.defaultfont
        if col == 'default': col = self.defaulttextcol
        largetext = pygame.font.SysFont(font,int(size*self.scale),bold)
        textsurf = largetext.render(text, antialiasing, col)
        return textsurf

    def rendershape(self,name,size,col='default'):
        if col == 'default': col = self.defaulttextcol
        backcol = (255,255,255)
        if col == backcol: backcol = (0,0,0)
        if name[:4] == 'tick':
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
        elif name[:5] == 'arrow':
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
            if 'left' in name:
                surf = pygame.transform.flip(surf,True,False)
            elif 'up' in name:
                surf = pygame.transform.rotate(surf,90)
            elif 'down' in name:
                surf = pygame.transform.rotate(surf,-90)
        elif name[:5] == 'cross':
            vals = self.getshapedata(name,['width'],[0.1])
            width = vals[0]
            surf = pygame.Surface((size,size))
            surf.fill(backcol)
            drawroundedline(surf,col,(size*width,size*width),(size*(1-width),size*(1-width)),size*width)
            drawroundedline(surf,col,(size*(1-width),size*width),(size*width,size*(1-width)),size*width)
        elif name[:8] == 'settings':
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
        else:
            print('incorrect image name "'+name+'"')
        surf.set_colorkey(backcol)
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
        
    def rendertextlined(self,text,size,col='default',backingcol=(150,150,150),font='default',width=-1,bold=False,antialiasing=True,center=False,spacing=0):
        if font=='default': font=self.defaultfont
        if col == 'default': col = self.defaulttextcol
        if width==-1 and center: center = False
        
        lines = text.split('\n')
        textgen = pygame.font.SysFont(font,int(size),bold)
        
        textimages = []
        imagesize = [0,0]
        while len(lines)>0:
            newline = ''
            if width!=-1:
                while textgen.size(lines[0])[0]>width:
                    split = lines[0].rsplit(' ',1)
                    if len(split)>1:
                        slide = split[1]
                        replace = split[0]+' '
                        if split[1] == '':
                            slide = ' '
                            replace = split[0]
                    else:
                        replace = split[0][:len(split[0])-1]
                        slide = split[0][-1]
                    lines[0] = replace
                    newline = slide+newline
                    
            tempsize = textgen.size(lines[0])
            if tempsize[0]>imagesize[0]: imagesize[0] = tempsize[0]
            imagesize[1]+=tempsize[1]+spacing
            textimages.append(textgen.render(lines[0],antialiasing,col))
            del lines[0]
            if newline!='':
                lines.insert(0,newline)
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
        return surf
    
    def textlinedcordgetter(self,text,size,font='default',width=-1,bold=False,center=False,spacing=0):
        if font=='default': font=self.defaultfont
        if width==-1 and center: center = False

        lines = text.split('\n')
        for a in range(len(lines)-1):
            lines[a+1]='\n'+lines[a+1]
        if text[-2:] == '\n':
            lines.append('\n')
        processedlines = []
        textgen = pygame.font.SysFont(font,int(size),bold)
        
        imagesize = [0,0]
        while len(lines)>0:
            newline = ''
            if width!=-1:
                while textgen.size(lines[0])[0]>width:
                    split = lines[0].rsplit(' ',1)
                    if len(split)>1:
                        slide = split[1]
                        replace = split[0]+' '
                        if split[1] == '':
                            slide = ' '
                            replace = split[0]
                    else:
                        replace = split[0][:len(split[0])-1]
                        slide = split[0][-1]
                    lines[0] = replace
                    newline = slide+newline
                        
            tempsize = textgen.size(lines[0])
            if tempsize[0]>imagesize[0]: imagesize[0] = tempsize[0]
            imagesize[1]+=tempsize[1]+spacing
            processedlines.append(lines[0])
            del lines[0]
            if newline!='':
                lines.insert(0,newline)
        rowstart = []
        if center:
            for a in processedlines:
                rowstart.append(int(imagesize[0]/2)-int(textgen.size(a)[0]/2))
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
        self.IDs[ID] = obj
    def makebutton(self,x,y,text,textsize,command=emptyfunction,menu='main',col='default',bordercol=-1,hovercol=-1,textcol='default',img='none',width=-1,height=-1,border=3,clickdownsize=3,verticalspacing=0,horizontalspacing=8,roundedcorners=0,clicktype=0,textoffsetx=0,textoffsety=0,toggle=True,togglecol=-1,togglehovercol=-1,toggleable=False,drawifoff=True,bindtoggle=[],font='default',bold=False,layer=1,ID='default',returnobj=False):
        if font=='default': font=self.defaultfont
        if textcol == 'default': textcol = self.defaulttextcol
        if col == 'default': col = self.defaultcol
        if type(img) == str:
            if img == 'none': textimage = self.rendertext(text,textsize,textcol,font,bold)
            else: textimage = self.rendershape(img,textsize)
        else:
            textimage = img
            textimage = pygame.transform.scale(img,(textsize,img.get_width()*textsize/img.get_height()))
        if width == -1:
            width = textimage.get_width()+horizontalspacing*2+border*2
            if height == -1: height = textimage.get_height()+verticalspacing*2+border*2
        else:
            linedtextimage = self.rendertextlined(text,textsize,font=font,width=width,bold=bold,center=True)
            height = linedtextimage.get_height()+verticalspacing*2+border*2
        if bordercol==-1:
            bordercol = [min([255,a+20]) for a in col]
        if hovercol==-1:
            hovercol = [max([0,a-20]) for a in col]
        if togglecol==-1:
            togglecol = [max([0,a-50]) for a in col]
        if togglehovercol==-1:
            togglehovercol = [max([0,a-20]) for a in togglecol]
        if ID == 'default':
            ID = 'button '+text
        obj = BUTTON(x,y,text,textsize,command,menu,col,bordercol,hovercol,textcol,img,width,height,border,clickdownsize,roundedcorners,clicktype,textoffsetx,textoffsety,toggle,togglecol,togglehovercol,toggleable,bindtoggle,drawifoff,font,bold,layer,ID,self)
        self.addid(ID,obj)
        if returnobj:
            return obj
        else:
            self.buttons.append(obj)

    def makecheckbox(self,x,y,textsize=80,command=emptyfunction,menu='main',text='',col=(255,255,255),bordercol='default',hovercol=(255,255,255),textcol=(0,0,0),img='tick',width=-1,height=-1,border=4,clickdownsize=1,verticalspacing=-15,horizontalspacing=-15,roundedcorners=0,clicktype=0,textoffsetx=0,textoffsety=0,toggle=True,togglecol=(255,255,255),togglehovercol=(255,255,255),toggleable=True,drawifoff=False,bindtoggle=[],font='default',bold=False,layer=1,ID='tickbox',returnobj=False):
        if bordercol == 'default':
            bordercol = [min([255,a+20]) for a in self.defaultcol]
        self.makebutton(x,y,text,textsize,command,menu,col,bordercol,hovercol,textcol,img,width,height,border,clickdownsize,verticalspacing,horizontalspacing,roundedcorners,clicktype,textoffsetx,textoffsety,toggle,togglecol,togglehovercol,toggleable,drawifoff,bindtoggle,font,bold,layer,ID,returnobj)
            
    def maketextbox(self,x,y,title,width,height,menu='main',border=4,titlesize=50,titleheight=-1,titlecenter=True,textsize=40,textcenter=False,titlefont='default',titlebold=False,col='default',backingcol=-1,titlecol='default',textcol='default',upperborder=0,lowerborder=0,rightborder=0,leftborder=0,selectcol=-1,selectbordersize=2,selectshrinksize=0,roundedcorners=0,clicktype=0,textoffsetx=0,textoffsety=0,font='default',bold=False,cursorsize=-1,layer=1,ID='default',returnobj=False):
        if font=='default': font=self.defaultfont
        if textcol == 'default': textcol = self.defaulttextcol
        if titlecol == 'default': titlecol = self.defaulttextcol
        if col == 'default': col = self.defaultcol
        if titlefont=='default': titlefont=font
        if titleheight == -1:
            titleheight = titlesize
        if backingcol==-1:
            backingcol = [max([0,a-50]) for a in col]
        if selectcol==-1:
            selectcol = [min([255,a+20]) for a in col]
        titleimage = self.rendertext(title,titlesize,titlecol,titlefont,titlebold)
        if cursorsize == -1:
            cursorsize = self.gettextsize('Ty',font,textsize,bold)[1]-2
        if ID == 'default':
            ID = 'textbox '+title
        obj = TEXTBOX(x,y,width,height,border,titleheight,roundedcorners,title,titlecenter,titlesize,titlecol,titlefont,titlebold,backingcol,textcenter,textsize,textcol,col,upperborder,lowerborder,rightborder,leftborder,selectcol,selectbordersize,selectshrinksize,cursorsize,menu,clicktype,titleimage,textoffsetx,textoffsety,font,bold,layer,ID,self)
        if returnobj:
            return obj
        else:
            self.textboxes.append(obj)
            self.addid(ID,obj)
            
    def maketable(self,x,y,data='empty',titles=[],menu='main',rows=5,colomns=3,boxwidth=-1,boxheight=50,spacing=10,col='default',boxtextcol='default',boxtextsize=-1,boxcenter=True,font='default',bold=False,titlefont=-1,titlebold=-1,titleboxcol=-1,titletextcol='default',titletextsize=-1,titlecenter=True,linesize=2,linecol=-1,roundedcorners=0,layer=1,ID='default',returnobj=False):
        if font == 'default': font = self.defaultfont
        if boxtextcol == 'default': boxtextcol = self.defaulttextcol
        if titletextcol == 'default': titletextcol = self.defaulttextcol
        if col == 'default': boxcol = self.defaultcol
        else: boxcol = col
        if titleboxcol == -1: titleboxcol = boxcol
        if titlefont == -1: titlefont = font
        if titlebold == -1: titlebold = bold
        if titletextsize == -1: titletextsize = boxheight*0.8
        if boxtextsize == -1: boxtextsize = boxheight*0.8
        if linecol == -1:
            linecol = [max([0,a-20]) for a in boxcol]
        if data == 'empty':
            data = [['-' for b in range(colomns)] for a in range(rows)]
        else:
            rows = len(data)
            colomns = len(data[0])
            
        while len(titles)<colomns:
            titles.append('Column '+str(len(titles)+1))
        if ID == 'default':
            try:
                ID = 'table '+titles[0]
            except:
                ID = 'table '
        obj = TABLE(x,y,rows,colomns,data,titles,boxwidth,boxheight,spacing,menu,boxcol,boxtextcol,boxtextsize,boxcenter,font,bold,titlefont,titlebold,titleboxcol,titletextcol,titletextsize,titlecenter,linesize,linecol,roundedcorners,layer,ID,self)
        if returnobj:
            return obj
        else:
            self.tables.append(obj)
            self.addid(ID,obj)
            
    def maketext(self,x,y,text,size,menu='main',col='default',center=True,font='default',bold=False,maxwidth=-1,backingborder=4,backingcol=(255,255,255),backingdraw=0,backingwidth=-1,backingheight=-1,img='none',roundedcorners=0,layer=1,ID='default',antialiasing=True,returnobj=False):
        if font == 'default': font = self.defaultfont
        if col == 'default': col = self.defaulttextcol
        if backingcol != (255,255,255):
            backingdraw = True
        if ID == 'default':
            ID = 'text '+text
        obj = TEXT(x,y,text,size,menu,col,center,font,bold,maxwidth,backingborder,backingcol,backingdraw,backingwidth,backingheight,img,roundedcorners,antialiasing,layer,ID,self)
        if returnobj:
            return obj
        else:
            self.texts.append(obj)
            self.addid(ID,obj)

    def makescroller(self,x,y,height,width=15,minh=0,maxh=-1,pageh=100,starth=0,menu='main',col='default',scrollercol=-1,hovercol=-1,clickcol=-1,scrollerwidth=11,clicktype=0,layer=1,ID='default',returnobj=False):
        if col == 'default':
            col = [min([255,a+20]) for a in self.defaultcol]
        if scrollercol==-1:
            scrollercol = [max([0,a-30]) for a in col]
        if hovercol==-1:
            hovercol = [max([0,a-30]) for a in scrollercol]
        if clickcol==-1:
            clickcol = [max([0,a-30]) for a in hovercol]
        if ID == 'default':
            ID = 'scroller'
        if maxh == -1:
            maxh = height
        obj = SCROLLER(x,y,menu,width,height,col,scrollercol,hovercol,clickcol,scrollerwidth,minh,maxh,pageh,starth,clicktype,layer,ID,self)
        if returnobj:
            return obj
        else:
            self.texts.append(obj)
            self.addid(ID,obj)
        
    def delete(self,ID):
        try:
            if type(self.IDs[ID]) == BUTTON: self.buttons.remove(self.IDs[ID])
            if type(self.IDs[ID]) == TEXTBOX: self.textboxes.remove(self.IDs[ID])
            if type(self.IDs[ID]) == TABLE: self.tables.remove(self.IDs[ID])
            if type(self.IDs[ID]) == TEXT: self.texts.remove(self.IDs[ID])
            del self.IDs[ID]
            return True
        except:
##            if printerror: print('failed to delete object:',ID)
            return False
                
    def movemenu(self,moveto):
        self.backchain.append(self.activemenu)
        self.activemenu = moveto
    def menuback(self):
        if len(self.backchain)>0:
            self.activemenu = self.backchain[-1]
            del self.backchain[-1]
        
            

class BUTTON:
    def __init__(self,x,y,text,textsize,command,menu,col,bordercol,hovercol,textcol,img,width,height,border,clickdownsize,roundedcorners,clicktype,textoffsetx,textoffsety,toggle,togglecol,togglehovercol,toggleable,bindtoggle,drawifoff,font,bold,layer,ID,ui):
        self.x = x
        self.y = y
        self.text = text
        self.textsize = textsize
        self.command = command
        self.img = img
        self.menu = menu
        self.layer = layer
        self.ID = ID
        
        self.col = col
        self.bordercol = bordercol
        self.hovercol = hovercol
        self.textcol = textcol
        
        self.width = width
        self.height = height
        self.border = border
        self.innerwidth = self.width-self.border*2
        self.innerheight = self.height-self.border*2
        self.clickdownsize = clickdownsize
        self.roundedcorners = roundedcorners

        self.toggle = toggle
        self.togglecol = togglecol
        self.togglehovercol = togglehovercol
        self.toggleable = toggleable
        self.bindtoggle = bindtoggle
        if self.bindtoggle!=[]: self.toggle = False
        self.drawifoff = drawifoff
        
        self.clicktype = clicktype
        self.textoffsetx = textoffsetx
        self.textoffsety = textoffsety
        self.font = font
        self.bold = bold
        self.refresh(ui)
        
    def gentext(self,ui):
        if type(self.img) == str:
            if self.img == 'none':
                self.textimage = ui.rendertextlined(self.text,self.textsize,self.textcol,self.col,self.font,self.width,self.bold,True,True)
                self.textimage = pygame.transform.scale(self.textimage,(self.textimage.get_width()*ui.scale,self.textimage.get_height()*ui.scale))
            else:
                self.textimage = ui.rendershape(self.img,self.textsize*ui.scale,self.textcol)
        else:
            scale = self.textsize/self.img.get_height()*ui.scale
            self.textimage = pygame.transform.scale(self.img,(self.img.get_height()*scale,self.img.get_width()*scale))
            
    def refresh(self,ui):
        self.rect = pygame.Rect(self.x-self.width/2,self.y-self.height/2,self.width,self.height)
        self.innerwidth = self.width-self.border*2
        self.innerheight = self.height-self.border*2
        self.gentext(ui)
        
    def render(self,screen,scale,mpos,mprs,mouseheld,buttondowntimer):
        self.innerrect = pygame.Rect(self.x-self.innerwidth/2,self.y-self.innerheight/2,self.innerwidth,self.innerheight)
        if self.rect.collidepoint(mpos):
            if mprs[self.clicktype] and mouseheld[self.clicktype][1]>0:
                self.innerrect = pygame.Rect(self.x-self.innerwidth/2+self.clickdownsize,self.y-self.innerheight/2+self.clickdownsize,self.innerwidth-self.clickdownsize*2,self.innerheight-+self.clickdownsize*2)
                if self.toggle: self.draw(screen,self.hovercol,scale)
                else: self.draw(screen,self.togglehovercol,scale)
                if mouseheld[self.clicktype][1] == buttondowntimer:
                    if self.toggleable:
                        if self.toggle: self.toggle = False
                        else: self.toggle = True
                    return True
            else:
                if self.toggle: self.draw(screen,self.hovercol,scale)
                else: self.draw(screen,self.togglehovercol,scale)
        else:
            if self.toggle: self.draw(screen,self.col,scale)
            else: self.draw(screen,self.togglecol,scale)
        return False
    def draw(self,screen,innercol,scale):
        pygame.draw.rect(screen,self.bordercol,rectscaler(self.rect,scale),border_radius=int(self.roundedcorners*scale))
        pygame.draw.rect(screen,innercol,rectscaler(self.innerrect,scale),border_radius=int(self.roundedcorners*scale))
        if (self.drawifoff and not self.toggle) or self.toggle:
            screen.blit(self.textimage,((self.x+self.textoffsetx)*scale-self.textimage.get_width()/2,(self.y+self.textoffsety)*scale-self.textimage.get_height()/2))

class TEXTBOX:
    def __init__(self,x,y,width,height,border,titleheight,roundedcorners,title,titlecenter,titlesize,titlecol,titlefont,titlebold,backingcol,textcenter,textsize,textcol,textbackingcol,upperborder,lowerborder,rightborder,leftborder,selectcol,selectbordersize,selectshrinksize,cursorsize,menu,clicktype,titleimage,textoffsetx,textoffsety,font,bold,layer,ID,ui):
        self.x = x
        self.y = y
        
        self.width = width
        self.height = height
        self.border = border
        self.titleheight = titleheight
        self.roundedcorners = roundedcorners
        self.rect = pygame.Rect(self.x-width/2,self.y-titleheight/2,self.width,self.height)
        self.innerrect = pygame.Rect(self.x-width/2+self.border,self.y-titleheight/2+self.titleheight+self.border,self.width-self.border*2,self.height-self.border*2-self.titleheight)

        self.title = title
        self.titlecenter = titlecenter
        self.titlesize = titlesize
        self.titlecol = titlecol
        self.titlefont = titlefont
        self.titlebold = titlebold
        self.backingcol = backingcol
        self.titleimage = titleimage

        self.textcenter = textcenter
        self.textsize = textsize
        self.textcol = textcol
        self.textbackingcol = textbackingcol
        self.textoffsetx = textoffsetx
        self.textoffsety = textoffsety
        self.font = font
        self.bold = bold
        
        self.upperborder = upperborder
        self.lowerborder = lowerborder
        self.rightborder = rightborder
        self.leftborder = leftborder

        self.menu = menu
        self.layer = layer
        self.ID = ID
        self.clicktype = clicktype

        self.selected = False
        self.selectcol = selectcol
        self.selectbordersize = selectbordersize
        self.selectshrinksize = selectshrinksize
        self.textselected = [False,0,0]
        self.clickstartedinbound = False
        
        self.text = ''
        self.typeline = 0
        self.typingcursor = -1
        self.visualtypingcursor = -1
        self.cursorsize = cursorsize

        self.gentitle(self.titleimage,ui.scale)
        self.gentext(ui)

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
        elif event.key == pygame.K_RETURN: item = '\n'
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
        else:
            if backspace or delete or item != '':
                self.text = self.text[:self.textselected[1]]+item+self.text[self.textselected[2]:]
                self.typingcursor = self.textselected[1]-1+len(item)
                self.textselected = [False,0,0]
            
        self.gentext(ui)
    def gentitle(self,titleimage,scale):
        self.titleimage = titleimage
        self.titleimagerect = self.titleimage.get_rect()
        if self.titlecenter: self.titleimagerect.center = (self.x*scale,self.y*scale)
        else:
            self.titleimage.x = (self.x-self.width/2)*scale
            self.titleimage.y = (self.y-self.titleheight/2)*scale
    def refresh(self,ui):
        self.rect = pygame.Rect(self.x-self.width/2,self.y-self.titleheight/2,self.width,self.height)
        self.innerrect = pygame.Rect(self.x-self.width/2+self.border,self.y-self.titleheight/2+self.titleheight+self.border,self.width-self.border*2,self.height-self.border*2-self.titleheight)
        self.gentext(ui)
    def gentext(self,ui):
        self.chrcorddatalined = ui.textlinedcordgetter(self.text,self.textsize,self.font,self.width-self.border*2-self.leftborder-self.rightborder,self.bold,center=self.textcenter)
        self.chrcorddata = []
        for a in self.chrcorddatalined:
            self.chrcorddata+=a
        self.textimage = ui.rendertextlined(self.text,self.textsize,self.textcol,self.backingcol,self.font,self.width-self.border*2-self.leftborder-self.rightborder,self.bold,center=self.textcenter)
        self.textimage = pygame.transform.scale(self.textimage,(self.textimage.get_width()*ui.scale,self.textimage.get_height()*ui.scale))
        self.textimagerect = self.textimage.get_rect()
        if self.textcenter: self.textimagerect.center = (self.x+self.textoffsetx+(self.leftborder+self.rightborder)/2,self.y+self.titleheight/2+self.border+self.textimage.get_height()/2+self.textoffsety+self.upperborder)
        else:
            self.textimagerect.x = self.x-self.width/2+self.border+self.textoffsetx+self.leftborder
            self.textimagerect.y = self.y+self.titleheight/2+self.border+self.textoffsety+self.upperborder
        self.refreshcursor()
    def refreshcursor(self):
        if self.textcenter: imageoffset = ((self.width-self.border*2)/2-self.textimage.get_width()/2)
        else: imageoffset = 0
        if self.typingcursor != -1: self.linecenter = [self.chrcorddata[self.typingcursor][1][0]+self.chrcorddata[self.typingcursor][2][0]/2+imageoffset,self.chrcorddata[self.typingcursor][1][1]]
        elif len(self.chrcorddata)>0: self.linecenter = [self.chrcorddata[self.typingcursor+1][1][0]-self.chrcorddata[self.typingcursor+1][2][0]/2+imageoffset,self.chrcorddata[self.typingcursor+1][1][1]]
        else:
            if not self.textcenter: self.linecenter = [0,self.textsize*0.3]
            else: self.linecenter = [self.width/2,self.textsize*0.3]
                
        #print([self.chrcorddata[a][0] for a in range(len(self.chrcorddata))],self.text,self.typingcursor)
   
    def render(self,screen,scale,mpos,mprs,mouseheld,buttondowntimer):
        self.typeline+=1
        self.selectrect = pygame.Rect(self.x-self.width/2+self.border-self.selectbordersize,self.y-self.titleheight/2+self.titleheight+self.border-self.selectbordersize,self.width-self.border*2+self.selectbordersize*2,self.height-self.border*2-self.titleheight+self.selectbordersize*2)
        if self.typeline == 80:
            self.typeline = 0

        if self.rect.collidepoint(mpos) and mprs[self.clicktype]:
            self.selectrect = pygame.Rect(self.x-self.width/2+self.border-self.selectbordersize+self.selectshrinksize,self.y-self.titleheight/2+self.titleheight+self.border-self.selectbordersize+self.selectshrinksize,self.width-self.border*2+self.selectbordersize*2-self.selectshrinksize*2,self.height-self.border*2-self.titleheight+self.selectbordersize*2-self.selectshrinksize*2)
            self.draw(screen,scale,True)
            if mouseheld[self.clicktype][1] == buttondowntimer:
                self.typingcursor = min([max([self.findclickloc(mpos)+1,0]),len(self.chrcorddata)])-1
                self.textselected[2] = self.typingcursor+1
                if len(self.chrcorddata)!=0: self.textselected[0] = True
                self.textselected[1] = self.typingcursor+1
                self.refreshcursor()
                self.selected = True
                self.clickstartedinbound = True
                return True
        else:
            if mprs[self.clicktype] and mouseheld[self.clicktype][1] == buttondowntimer:
                self.clickstartedinbound = False
                self.selected = False
            if not self.rect.collidepoint(mpos) and mprs[self.clicktype] and not mouseheld[self.clicktype]:
                self.selected = False
                self.textselected = [False,0,0]
            self.draw(screen,scale,False)
        if mprs[self.clicktype] and mouseheld[self.clicktype][1] != buttondowntimer and self.clickstartedinbound:
            self.textselected[2] = min([max([self.findclickloc(mpos)+1,0]),len(self.chrcorddata)])
        elif not self.clickstartedinbound:
            self.textselected[0] = False
        return False
    def findclickloc(self,mpos=-1,relativempos=-1):
        if len(self.chrcorddata)==0:
            return -1
        else:
            if relativempos == -1: self.relativempos = (mpos[0]-self.x+self.width/2-self.border-self.leftborder,mpos[1]-self.y-self.titleheight/2-self.border-self.upperborder)
            else: self.relativempos = relativempos
            dis = [0,10000]
            for i,a in enumerate(self.chrcorddatalined):
                if abs(a[0][1][1]-self.relativempos[1])<dis[1]:
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
    def draw(self,screen,scale,clicking): 
        pygame.draw.rect(screen,self.backingcol,rectscaler(self.rect,scale),border_radius=int(self.roundedcorners*scale))
        pygame.draw.rect(screen,self.textbackingcol,rectscaler(self.innerrect,scale),border_radius=int(self.roundedcorners*scale))
        if self.selected: pygame.draw.rect(screen,self.selectcol,rectscaler(self.selectrect,scale),self.selectbordersize,border_radius=int((self.roundedcorners+self.selectbordersize)*scale))
        screen.blit(self.titleimage,self.titleimagerect)
        screen.blit(self.textimage,rectscaler(self.textimagerect,scale))
        if self.typeline>20 and self.selected:
            pygame.draw.line(screen,self.textcol,((self.x-self.width/2+self.border+self.linecenter[0]+self.leftborder)*scale,(self.y+self.titleheight/2+self.border+self.linecenter[1]-self.cursorsize/2+self.upperborder)*scale),((self.x-self.width/2+self.border+self.linecenter[0]+self.leftborder)*scale,(self.y+self.titleheight/2+self.border+self.linecenter[1]+self.cursorsize/2+self.upperborder)*scale),2)
        if self.textselected[0] and self.textselected[1]!=self.textselected[2]:
            #print(min([self.textselected[1],self.textselected[2]]),max([self.textselected[1],self.textselected[2]]))
            trect = [1000000,0,0,0]
            for a in range(min([self.textselected[1],self.textselected[2]]),max([self.textselected[1],self.textselected[2]])):
                if self.chrcorddata[a][0] != '\n':
                    trect[0] = (self.x-self.width/2+self.border+self.leftborder+self.chrcorddata[a][1][0]-self.chrcorddata[a][2][0]/2)*scale
                    trect[1] = (self.y+self.titleheight/2+self.border+self.upperborder+self.chrcorddata[a][1][1]-self.chrcorddata[a][2][1]/2)*scale
                    trect[2] = self.chrcorddata[a][2][0]*scale
                    trect[3] = self.chrcorddata[a][2][1]*scale
                surf = pygame.Surface((trect[2],trect[3]))
                surf.set_alpha(180)
                surf.fill((51,144,255))
                screen.blit(surf,(trect[0],trect[1]))
        
                



class TABLE:
    def __init__(self,x,y,rows,colomns,data,titles,boxwidths,boxheight,spacing,menu,boxcol,boxtextcol,boxtextsize,boxcenter,boxfont,boxbold,titlefont,titlebold,titleboxcol,titletextcol,titletextsize,titlecenter,linesize,linecol,roundedcorners,layer,ID,ui):
        self.x = x
        self.y = y
        self.rows = rows
        self.colomns = colomns
        self.data = data
        self.titles = titles
        self.menu = menu
        self.layer = layer
        self.ID = ID

        self.linesize = linesize
        self.linecol = linecol

        self.boxwidth = boxwidths
        self.boxheight = boxheight
        self.spacing = spacing
        self.boxcol = boxcol
        self.boxtextcol = boxtextcol
        self.boxtextsize = boxtextsize
        self.boxfont = boxfont
        self.boxbold=boxbold
        self.boxcenter = boxcenter

        self.titlefont = titlefont
        self.titlebold = titlebold
        self.titlecenter = titlecenter
        self.titleboxcol = titleboxcol
        self.titletextcol = titletextcol
        self.titletextsize = titletextsize

        self.roundedcorners = roundedcorners
        self.refresh(ui)

    def refresh(self,ui):
        self.rows = len(self.data)
        self.colomns = len(self.titles)
        self.labeleddata = []
        temp = copy.copy(self.data)
        temp.insert(0,copy.copy(self.titles))
        print(self.data)
        for a in temp:
            self.labeleddata.append([])
            for b in a:
                if type(b) == str: self.labeleddata[-1].append(['text',b])
                elif type(b) == int: self.labeleddata[-1].append(['text',str(b)])
                elif type(b) == list: self.labeleddata[-1].append(['text',str(b)])

                elif type(b) == BUTTON: self.labeleddata[-1].append(['button',b])
                elif type(b) == TEXTBOX: self.labeleddata[-1].append(['textbox',b])
                elif type(b) == pygame.Surface or type(b) == TEXT:
                    if type(b) == TEXT: b = b.textimage
                    if a == temp[0]: self.labeleddata[-1].append(['image',pygame.transform.scale(b,(b.get_width()*(self.titletextsize/b.get_height()),self.titletextsize))])
                    else: self.labeleddata[-1].append(['image',pygame.transform.scale(b,(b.get_width()*(self.boxtextsize/b.get_height()),self.boxtextsize))])
                else: print('unrecognised data type in table:',b)
        self.gentext(ui)
        self.boxwidthsinc = []
        if self.boxwidth == -1:
            self.boxwidths = []
            for a in range(len(self.tableimages[0])):
                minn = 0
                for b in [self.tableimages[c][a] for c in range(len(self.tableimages))]:
                    if b[0] == 'text':
                        if minn<b[1].get_width():
                            minn = b[1].get_width()
                    elif b[0] == 'button':
                        if minn<b[1].textimage.get_width():
                            minn = b[1].textimage.get_width()
                minn+=self.spacing*2*ui.scale
                self.boxwidthsinc.append(sum(self.boxwidths))
                self.boxwidths.append(minn/ui.scale)
        else:
            if type(self.boxwidth) == int:
                temp = []
                for a in range(len(self.tableimages[0])):
                    self.boxwidthsinc.append(sum(temp))
                    temp.append(self.boxwidth)
                self.boxwidths = temp
            else:
                self.boxwidths = self.boxwidth
                for a in range(len(self.tableimages[0])):
                    self.boxwidthsinc.append(sum(self.boxwidths[:a]))
                
        for a in range(len(self.tableimages)):
            for i,b in enumerate(self.tableimages[a]):
                if b[0] == 'text':
                    if (a != 0 and self.boxcenter) or (a == 0 and self.titlecenter):
                        b[2].center = ((self.x+self.linesize*(i+1)+self.boxwidthsinc[i]+self.boxwidths[i]/2)*ui.scale,(self.y+self.linesize+(self.linesize+self.boxheight)*a+self.boxheight/2)*ui.scale)
                    else:
                        b[2].x = (self.x+self.linesize*(i+1)+self.boxwidthsinc[i]+self.spacing)*ui.scale
                        b[2].y = (self.y+self.linesize+(self.linesize+self.boxheight)*a)*ui.scale
                elif b[0] == 'button':
                    b[1].x = self.x+self.linesize*(i+1)+self.boxwidthsinc[i]+self.boxwidths[i]/2
                    b[1].y = self.y+self.linesize+(self.linesize+self.boxheight)*a+self.boxheight/2
                    b[1].width = self.boxwidths[i]
                    b[1].height = self.boxheight
                    b[1].refresh(ui)
                elif b[0] == 'textbox':
                    b[1].x = self.x+self.linesize*(i+1)+self.boxwidthsinc[i]+self.boxwidths[i]/2
                    b[1].y = self.y+self.linesize+(self.linesize+self.boxheight)*a+b[1].titleheight/2
                    b[1].width = self.boxwidths[i]
                    b[1].height = self.boxheight
                    b[1].refresh(ui)

        self.boxwidthtotal = sum(self.boxwidths)
        self.rect = pygame.Rect(self.x,self.y,self.linesize*(self.colomns+1)+self.boxwidthtotal,(self.boxheight+self.linesize)*(self.rows+1)+self.linesize)
    
    def render(self,screen,scale,mpos,mprs,mouseheld,buttondowntimer,ui):
        self.draw(screen,scale,mpos,mprs,mouseheld,buttondowntimer,ui)
        
    def draw(self,screen,scale,mpos,mprs,mouseheld,buttondowntimer,ui):
        pygame.draw.rect(screen,self.linecol,rectscaler(self.rect,scale),border_radius=int(self.roundedcorners*scale))
        for y in range(self.rows+1):
            for x in range(self.colomns):
                if y == 0:
                    pygame.draw.rect(screen,self.titleboxcol,rectscaler(pygame.Rect(self.x+self.linesize*(x+1)+self.boxwidthsinc[x],self.y+self.linesize+(self.linesize+self.boxheight)*y,self.boxwidths[x],self.boxheight),scale),border_radius=int(self.roundedcorners*scale))
                else:
                    pygame.draw.rect(screen,self.boxcol,rectscaler(pygame.Rect(self.x+self.linesize*(x+1)+self.boxwidthsinc[x],self.y+self.linesize+(self.linesize+self.boxheight)*y,self.boxwidths[x],self.boxheight),scale),border_radius=int(self.roundedcorners*scale))
                if self.tableimages[y][x][0] == 'text':
                    screen.blit(self.tableimages[y][x][1],self.tableimages[y][x][2])
                else:
                    if self.tableimages[y][x][0] == 'button':
                        if self.tableimages[y][x][1].render(screen,scale,mpos,mprs,mouseheld,buttondowntimer):
                            self.tableimages[y][x][1].command()
                    if self.tableimages[y][x][0] == 'textbox':
                        self.tableimages[y][x][1].render(screen,scale,mpos,mprs,mouseheld,buttondowntimer)
                        if self.tableimages[y][x][1].selected:
                            ui.selectedtextbox = ui.textboxes.index(self.tableimages[y][x][1])
                            


    def gentext(self,ui):
        self.tableimages = []
        for a in range(len(self.labeleddata)):
            self.tableimages.append([])
            for i,b in enumerate(self.labeleddata[a]):
                if b[0] == 'text':
                    if a==0: img = ui.rendertext(b[1],self.titletextsize,self.titletextcol,self.titlefont,self.titlebold)
                    else: img = ui.rendertext(b[1],self.boxtextsize,self.boxtextcol,self.boxfont,self.boxbold)
                    rec = img.get_rect()
                    self.tableimages[-1].append(['text',img,rec])
                elif b[0] == 'button':
                    b[1].roundedcorners = self.roundedcorners
                    self.tableimages[-1].append(['button',b[1]])
                elif b[0] == 'textbox':
                    b[1].roundedcorners = self.roundedcorners
                    self.tableimages[-1].append(['textbox',b[1]])
                    if not b[1] in ui.textboxes:
                        ui.textboxes.append(b[1])
                elif b[0] == 'image':
                    if a==0: scale = self.boxtextsize/b[1].get_height()
                    else: scale = self.titletextsize/b[1].get_height()
                    img = pygame.transform.scale(b[1],(b[1].get_width()*scale,b[1].get_height()*scale))
                    rec = img.get_rect()
                    self.tableimages[-1].append(['text',b[1],rec])

class TEXT:
    def __init__(self,x,y,text,size,menu,col,center,font,bold,maxwidth,backingborder,backingcol,backingdraw,backingwidth,backingheight,img,roundedcorners,antialiasing,layer,ID,ui):
        self.x = x
        self.y = y
        self.text = text
        self.size = size
        self.col = col
        self.center = center
        self.font = font
        self.bold = bold
        self.img = img
        self.antialiasing = antialiasing

        self.maxwidth = maxwidth

        self.backingcol = backingcol
        self.backingborder = backingborder
        self.backingdraw = backingdraw
        self.backingwidth = backingwidth
        self.backingheight = backingheight
        self.roundedcorners = roundedcorners

        self.menu = menu
        self.layer = layer
        self.ID = ID
        
        self.refresh(ui)
        
    def render(self,screen,scale):
        self.draw(screen,scale)
    def draw(self,screen,scale):
        if self.backingdraw:
            pygame.draw.rect(screen,self.backingcol,rectscaler(self.backingrect,scale),border_radius=int(self.roundedcorners*scale))
        screen.blit(self.textimage,self.textrect)
        
    def refresh(self,ui):
        self.gentext(ui)
    def gentext(self,ui):
        if type(self.img) == str:
            if self.img == 'none':
                if self.maxwidth == -1:
                    self.textimage = ui.rendertext(self.text,self.size,self.col,self.font,self.bold,self.antialiasing)
                else:
                    self.textimage = ui.rendertextlined(self.text,self.size,self.col,self.backingcol,self.font,self.maxwidth,self.bold,self.antialiasing,self.center)
                    self.textimage = pygame.transform.scale(self.textimage,(self.textimage.get_width()*ui.scale,self.textimage.get_height()*ui.scale))
            else:
                self.textimage = ui.rendershape(self.img,self.size*ui.scale,self.col)
        else:
            scale = self.size/self.img.get_height()*ui.scale
            self.textimage = pygame.transform.scale(self.img,(self.img.get_height()*scale,self.img.get_width()*scale))

        self.textrect = self.textimage.get_rect()
        if self.center:
            self.textrect.center = (self.x*ui.scale,self.y*ui.scale+self.textimage.get_height()/2*ui.scale)
        else:
            self.textrect.x = self.x*ui.scale
            self.textrect.y = self.y*ui.scale
        if self.backingwidth == -1: bw = self.textrect.width/ui.scale+self.backingborder*2
        else: bw = self.backingwidth
        if self.backingheight == -1: bh = self.textrect.height/ui.scale+self.backingborder*2
        else: bh = self.backingheight
        if self.center: self.backingrect = pygame.Rect(self.x-bw/2,self.y-bh/2+self.textimage.get_height()/2,bw,bh)
        else: self.backingrect = pygame.Rect(self.x-self.backingborder,self.y-self.backingborder,bw,bh)

class SCROLLER:
    def __init__(self,x,y,menu,width,height,col,scrollercol,hovercol,clickcol,scrollerwidth,minh,maxh,pageh,starth,clicktype,layer,ID,ui):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        self.col = col
        self.scrollercol = scrollercol
        self.hovercol = hovercol
        self.clickcol = clickcol
        self.scrollerwidth = scrollerwidth
        self.border = (self.width-self.scrollerwidth)/2

        self.minh = minh
        self.maxh = maxh
        self.pageh = pageh
        self.starth = starth
        self.scroll = starth

        self.holding = False

        self.clicktype = clicktype
        self.menu = menu
        self.layer = layer
        self.ID = ID

        self.refresh()
        
    def render(self,screen,scale,mpos,mprs,mouseheld,buttondowntimer):
        if self.holding:
            self.scroll = mpos[1]-self.holdingcords[1]
            if self.scroll<self.minh:
                self.scroll = self.minh
            elif self.scroll>self.maxh-self.scrollerheight-self.border*2:
                self.scroll = self.maxh-self.scrollerheight-self.border*2
            self.refresh()
        if self.sliderrect.collidepoint(mpos):
            if not self.holding:
                self.draw(screen,scale,self.hovercol)
            if mprs[self.clicktype]:
                self.draw(screen,scale,self.clickcol)
                if mouseheld[self.clicktype][1] == buttondowntimer:
                    self.holding = True
                    self.holdingcords = [mpos[0]-self.sliderrect.x,mpos[1]-self.sliderrect.y]

        else:
            if self.holding: self.draw(screen,scale,self.clickcol)
            else: self.draw(screen,scale,self.scrollercol)
        if not mprs[self.clicktype]:
            self.draw(screen,scale,self.scrollercol)
            self.holding = False
    def draw(self,screen,scale,scrollercol):
        pygame.draw.rect(screen,self.col,rectscaler(self.rect,scale))
        pygame.draw.rect(screen,scrollercol,rectscaler(self.sliderrect,scale))
        
    def refresh(self):
        self.scrollerheight = (self.pageh/(self.maxh-self.minh))*self.height
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.sliderrect = pygame.Rect(self.x+self.border,self.y+self.border+self.scroll,self.scrollerwidth,self.scrollerheight)
    























    
        

        
        
                          




