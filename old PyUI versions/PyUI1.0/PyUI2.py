import pygame,random,math,time,copy,ctypes
pygame.init()

def rectscaler(rect,scale):
    return pygame.Rect(rect.x*scale,rect.y*scale,rect.w*scale,rect.h*scale)

    
class UI:
    def __init__(self,scale=1):
        pygame.key.set_repeat(350,31)
        
        self.scale = scale
        self.mouseheld = [[0,0],[0,0],[0,0]]
        self.loadtickdata()
        
        self.buttons = []
        self.textboxes = []
        self.selectedtextbox = 0
        
        self.activemenu = 'main'
        self.backchain = []
        self.buttondowntimer = 8
        self.checkcaps()

        self.defaultfont = 'impact'

    def checkcaps(self):
        hllDll = ctypes.WinDLL("User32.dll")
        self.capslock = bool(hllDll.GetKeyState(0x14))
        
    def scaleset(self,scale):
        self.scale = scale
        for a in self.buttons:
            textimage = self.maketext(a.text,a.textsize,a.textcol,a.font,a.bold)
            a.gentext(textimage)
        for a in self.textboxes:
            titleimage = self.maketext(a.title,a.titlesize,a.titlecol,a.titlefont,a.titlebold)
            a.gentext(titleimage)
        
    def loadtickdata(self):
        mpos = pygame.mouse.get_pos()
        self.mpos = [mpos[0]/self.scale,mpos[1]/self.scale]
        self.mprs = pygame.mouse.get_pressed()
        self.kprs = pygame.key.get_pressed()
        for a in range(3):
            if self.mprs[a] and not self.mouseheld[a][0]: self.mouseheld[a] = [1,self.buttondowntimer]
            elif self.mprs[a]: self.mouseheld[a][1] -= 1
            if not self.mprs[a]: self.mouseheld[a][0] = 0

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_CAPSLOCK:
                    if self.capslock: self.capslock = False
                    else: self.capslock = True
                if self.selectedtextbox!=-1:
                    self.textboxes[self.selectedtextbox].inputkey(self.capslock,event,self.kprs,self)
                    if not self.textboxes[self.selectedtextbox].selected:
                        self.selectedtextbox = -1
        
    def write(self,screen,x,y,text,size,col=(0,0,0),center=True,font='default',bold=False,antialiasing=True):
        if font=='default': font=self.defaultfont
        largetext = pygame.font.SysFont(font,int(size*self.scale),bold)
        textsurf = largetext.render(text, antialiasing, col)
        textrect = textsurf.get_rect()
        if center:
            textrect.center = (int(x)*self.scale,int(y)*self.scale)
        else:
            textrect.x = int(x)*self.scale
            textrect.y = int(y)*self.scale
        screen.blit(textsurf, textrect)

    def maketext(self,text,size,col=(0,0,0),font='default',bold=False,antialiasing=True):
        if font=='default': font=self.defaultfont
        largetext = pygame.font.SysFont(font,int(size*self.scale),bold)
        textsurf = largetext.render(text, antialiasing, col)
        return textsurf
    def maketextlined(self,text,size,col=(0,0,0),backingcol=(150,150,150),font='default',width=-1,bold=False,antialiasing=True,center=False,spacing=0):
        if font=='default': font=self.defaultfont
        if width==-1 and center: center = False
        
        lines = text.split('\n')
        textgen = pygame.font.SysFont(font,int(size*self.scale),bold)
        
        textimages = []
        imagesize = [0,0]
        while len(lines)>0:
            newline = ''
            if width!=-1:
                while textgen.size(lines[0])[0]>width:
                    split = lines[0].rsplit(' ',1)
                    if len(split)>0:
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
                    
##                    if ' ' in lines[0]:
##                        split = lines[0].rsplit(' ',1)
##                        split[0]+=' '
##                        if split[-1] == '': del split[-1]
##                    else: split = []
##                    if len(split)>1:
##                        if newline!='': newline = ' '+newline
##                        newline = split[1]+newline
##                        lines[0] = split[0]
##                    else:
##                        newline = lines[0][-1]+newline
##                        lines[0] = lines[0].removesuffix(lines[0][-1])
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
        processedlines = []
        textgen = pygame.font.SysFont(font,int(size*self.scale),bold)
        
        imagesize = [0,0]
        while len(lines)>0:
            newline = ''
            if width!=-1:
                while textgen.size(lines[0])[0]>width:
                    split = lines[0].rsplit(' ',1)
                    if len(split)>0:
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
                    
##                    if ' ' in lines[0]:
##                        split = lines[0].rsplit(' ',1)
##                        split[0]+=' '
##                        if split[-1] == '': del split[-1]
##                    else: split = []
##                    if len(split)>1:
##                        if newline!='': newline = ' '+newline
##                        newline = split[1]+newline
##                        lines[0] = split[0]
##                    else:
##                        newline = lines[0][-1]+newline
##                        lines[0] = lines[0].removesuffix(lines[0][-1])
                        
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
        for i,a in enumerate(processedlines):
            corddata.append([])
            for b in range(len(a)):
                lettersize = textgen.size(a[b])
                linesize = textgen.size(a[:b+1])
                corddata[-1].append([a[b],(rowstart[i]+linesize[0]-lettersize[0]/2,yinc+lettersize[1]/2),lettersize])
            yinc+=textgen.size(a)[1]+spacing
        return corddata
                
        
    
    def makebutton(self,x,y,text,textsize,command,menu='main',col=(150,150,150),bordercol=-1,hovercol=-1,textcol=(0,0,0),width=-1,height=-1,border=3,verticalspacing=0,horizontalspacing=8,roundedcorners=0,clicktype=0,textoffsetx=0,textoffsety=0,font='default',bold=False):
        if font=='default': font=self.defaultfont
        textimage = self.maketext(text,textsize,textcol,font,bold)
        if width == -1: width = textimage.get_width()+horizontalspacing*2+border*2
        if height == -1: height = textimage.get_height()+verticalspacing*2+border*2
        if bordercol==-1:
            ncol = []
            for a in col:
                ncol.append(min([255,a+20]))
            bordercol = ncol
        if hovercol==-1:
            ncol = []
            for a in col:
                ncol.append(max([0,a-20]))
            hovercol = ncol
        self.buttons.append(BUTTON(x,y,text,textsize,command,menu,col,bordercol,hovercol,textcol,width,height,width-border*2,height-border*2,roundedcorners,clicktype,textimage,textoffsetx,textoffsety,font,bold))
        
    def maketextbox(self,x,y,title,width,height,menu='main',border=4,titlesize=50,titleheight=-1,titlecenter=True,textsize=40,textcenter=False,titlefont='default',titlebold=False,col=(150,150,150),backingcol=(100,100,100),titlecol=(0,0,0),textcol=(0,0,0),roundedcorners=0,clicktype=0,textoffsetx=0,textoffsety=0,font='default',bold=False,cursorsize=-1):
        if font=='default': font=self.defaultfont
        if titlefont=='default': titlefont=font
        if titleheight == -1:
            titleheight = titlesize
        if cursorsize == -1:
            cursorsize = textsize*0.6
        titleimage = self.maketext(title,titlesize,titlecol,titlefont,titlebold)
        self.textboxes.append(TEXTBOX(x,y,width,height,border,titleheight,roundedcorners,title,titlecenter,titlesize,titlecol,titlefont,titlebold,backingcol,textcenter,textsize,textcol,col,cursorsize,menu,clicktype,titleimage,textoffsetx,textoffsety,font,bold,self))
        
    def rendergui(self,screen):
        for a in self.buttons:
            if a.menu == self.activemenu:
                if a.render(screen,self.mpos,self.mprs,self.mouseheld,self.buttondowntimer,self.scale):
                    a.command()
                    self.mouseheld[a.clicktype][1]-=1
        for a in self.textboxes:
            if a.menu == self.activemenu:
                a.render(screen,self.scale,self.mpos,self.mprs,self.mouseheld)
                
    def movemenu(self,moveto):
        self.backchain.append(self.activemenu)
        self.activemenu = moveto
    def menuback(self):
        if len(self.backchain)>0:
            self.activemenu = self.backchain[-1]
            del self.backchain[-1]
        
            

class BUTTON:
    def __init__(self,x,y,text,textsize,command,menu,col,bordercol,hovercol,textcol,width,height,innerwidth,innerheight,roundedcorners,clicktype,textimage,textoffsetx,textoffsety,font,bold):
        self.x = x
        self.y = y
        self.text = text
        self.textsize = textsize
        self.command = command
        self.menu = menu
        
        self.col = col
        self.bordercol = bordercol
        self.hovercol = hovercol
        self.textcol = textcol
        
        self.width = width
        self.height = height
        self.innerwidth = innerwidth
        self.innerheight = innerheight
        self.innershrinksize = 3
        self.roundedcorners = roundedcorners
        self.rect = pygame.Rect(self.x-self.width/2,self.y-self.height/2,self.width,self.height)

        self.clicktype = clicktype
        self.textoffsetx = textoffsetx
        self.textoffsety = textoffsety
        self.font = font
        self.bold = bold
        self.gentext(textimage)
        
    def gentext(self,textimage):
        self.textimage = textimage
        
    def render(self,screen,mpos,mprs,mouseheld,buttondowntimer,scale):
        self.innerrect = pygame.Rect(self.x-self.innerwidth/2,self.y-self.innerheight/2,self.innerwidth,self.innerheight)
        if self.rect.collidepoint(mpos):
            if mprs[self.clicktype] and mouseheld[self.clicktype][1]>0:
                self.innerrect = pygame.Rect(self.x-self.innerwidth/2+self.innershrinksize,self.y-self.innerheight/2+self.innershrinksize,self.innerwidth-self.innershrinksize*2,self.innerheight-+self.innershrinksize*2)
                self.draw(screen,self.hovercol,scale)
                if mouseheld[self.clicktype][1] == buttondowntimer:
                    return True
            else: self.draw(screen,self.hovercol,scale)
        else: self.draw(screen,self.col,scale)
        return False
    def draw(self,screen,innercol,scale):
        pygame.draw.rect(screen,self.bordercol,rectscaler(self.rect,scale),border_radius=self.roundedcorners)
        pygame.draw.rect(screen,innercol,rectscaler(self.innerrect,scale),border_radius=self.roundedcorners)
        screen.blit(self.textimage,((self.x+self.textoffsetx)*scale-self.textimage.get_width()/2,(self.y+self.textoffsety)*scale-self.textimage.get_height()/2))

class TEXTBOX:
    def __init__(self,x,y,width,height,border,titleheight,roundedcorners,title,titlecenter,titlesize,titlecol,titlefont,titlebold,backingcol,textcenter,textsize,textcol,textbackingcol,cursorsize,menu,clicktype,titleimage,textoffsetx,textoffsety,font,bold,ui):
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

        self.menu = menu
        self.clicktype = clicktype

        self.text = ''
        self.selected = True
        self.typeline = 0
        self.typingcursor = -1
        self.cursorsize = cursorsize

        self.gentitle(self.titleimage)
        self.gentext(ui)

    def inputkey(self,caps,event,kprs,ui):
        if kprs[pygame.K_LSHIFT]:
            if caps: caps = False
            else: caps = True
        item = ''
        remove = False
        esc = False
        enter = False
        unicodechrs = '''#',-./0123456789;=[\]`'''
        shiftunicodechrs = '''~@<_>?)!"£$%^&*(:+{|}¬'''
        if event.key>32 and event.key<127:
            if (event.key>96 and event.key<123):
                if caps: item = chr(event.key-32)
                else: item = chr(event.key)
            elif chr(event.key) in unicodechrs:
                if not kprs[pygame.K_LSHIFT]: item = chr(event.key)
                else: item = shiftunicodechrs[list(unicodechrs).index(chr(event.key))]
        elif event.key == pygame.K_BACKSPACE:
            remove = True
        elif event.key == pygame.K_ESCAPE:
            self.selected = False
        elif event.key == pygame.K_RETURN:
            item = '\n'
        elif event.key == pygame.K_SPACE:
            item = ' '
        elif event.key == pygame.K_LEFT:
            if self.typingcursor>-1: self.typingcursor-=1
        elif event.key == pygame.K_RIGHT:
            if self.typingcursor<len(self.text): self.typingcursor+=1
        
        if item != '':
            self.text = self.text[:self.typingcursor+1]+item+self.text[self.typingcursor+1:]
            if item!='\n':self.typingcursor+=len(item)
        if remove:
            self.typingcursor-=1
            self.text = self.text[:self.typingcursor+1]+self.text[self.typingcursor+2:]
        self.gentext(ui)
    def gentitle(self,titleimage):
        self.titleimage = titleimage
        self.titleimagerect = self.titleimage.get_rect()
        if self.titlecenter: self.titleimagerect.center = (self.x,self.y)
        else:
            self.titleimage.x = self.x-self.width/2
            self.titleimage.y = self.y-self.titleheight/2
    def gentext(self,ui):
        self.chrcorddatalined = ui.textlinedcordgetter(self.text,self.textsize,self.font,self.width-self.border*2,self.bold,center=self.textcenter)
        self.chrcorddata = []
        for a in self.chrcorddatalined:
            self.chrcorddata+=a
        self.textimage = ui.maketextlined(self.text,self.textsize,self.textcol,self.backingcol,self.font,self.width-self.border*2,self.bold,center=self.textcenter)
        self.textimagerect = self.textimage.get_rect()
        if self.textcenter: self.textimagerect.center = (self.x+self.textoffsetx,self.y+self.titleheight/2+self.border+self.textimage.get_height()/2+self.textoffsety)
        else:
            self.textimagerect.x = self.x-self.width/2+self.border+self.textoffsetx
            self.textimagerect.y = self.y+self.titleheight/2+self.border+self.textoffsety

        if self.typingcursor != -1: self.linecenter = [self.chrcorddata[self.typingcursor][1][0]+self.chrcorddata[self.typingcursor][2][0]/2,self.chrcorddata[self.typingcursor][1][1]]
        elif len(self.chrcorddata)>0: self.linecenter = [self.chrcorddata[self.typingcursor+1][1][0]-self.chrcorddata[self.typingcursor+1][2][0]/2,self.chrcorddata[self.typingcursor+1][1][1]]
        else:
            if not self.textcenter: self.linecenter = [0,self.textsize/2]
            else: linecenter = [self.width/2,self.textsize/2]
                
        #print([self.chrcorddata[a][0] for a in range(len(self.chrcorddata))],self.text,self.typingcursor)
   
    def render(self,screen,scale,mpos,mprs,mouseheld):
        self.typeline+=1
        if self.typeline == 80:
            self.typeline = 0
            
        if self.rect.collidepoint(mpos) and mprs[self.clicktype]:
            self.draw(screen,scale)
            if mouseheld[self.clicktype][1] == buttondowntimer:
                self.selected = True
                return True
        else:
##            if not self.rect.collidepoint(mpos) and mprs[self.clicktype]:
##                self.selected = False
            self.draw(screen,scale)
        return False
    def draw(self,screen,scale): 
        pygame.draw.rect(screen,self.backingcol,rectscaler(self.rect,scale))
        pygame.draw.rect(screen,self.textbackingcol,rectscaler(self.innerrect,scale))
        screen.blit(self.titleimage,self.titleimagerect)
        screen.blit(self.textimage,self.textimagerect)
        if self.typeline>20:
            pygame.draw.line(screen,self.textcol,(self.x-self.width/2+self.border+self.linecenter[0],self.y+self.titleheight/2+self.border+self.linecenter[1]-self.cursorsize/2),(self.x-self.width/2+self.border+self.linecenter[0],self.y+self.titleheight/2+self.border+self.linecenter[1]+self.cursorsize/2),2)
        
    




