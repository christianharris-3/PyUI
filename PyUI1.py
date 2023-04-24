import pygame,random,math,time,copy,ctypes
pygame.init()

def rectscaler(rect,scale):
    return pygame.Rect(rect.x*scale,rect.y*scale,rect.w*scale,rect.h*scale)

    
class UI:
    def __init__(self,scale=1):
        self.scale = scale
        self.mouseheld = [[0,0],[0,0],[0,0]]
        self.loadtickdata()
        
        self.buttons = []
        self.textboxes = []
        self.selectedtextbox = -1
        
        self.activemenu = 'main'
        self.backchain = []
        self.buttondowntimer = 8
        self.checkcaps()

    def checkcaps(self):
        hllDll = ctypes.WinDLL("User32.dll")
        self.capslock = bool(hllDll.GetKeyState(0x14))
        
    def scaleset(self,scale):
        self.scale = scale
        for a in self.buttons:
            textimage = self.maketext(a.text,a.textsize,a.textcol)
            a.gentext(textimage)
        
    def loadtickdata(self):
        mpos = pygame.mouse.get_pos()
        self.mpos = [mpos[0]/self.scale,mpos[1]/self.scale]
        self.mprs = pygame.mouse.get_pressed()
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
                    self.texboxes[self.selectedtextbox].inputkey(self.capslock,event)
                    if not self.texboxes[self.selectedtextbox].selected:
                        self.selectedtextbox = -1
        
    def write(self,screen,x,y,text,size,col=(0,0,0),center=True,font='impact',bold=False,antialiasing=True):
        largetext = pygame.font.SysFont(font,int(size*self.scale),bold)
        textsurf = largetext.render(text, antialiasing, col)
        textrect = textsurf.get_rect()
        if center:
            textrect.center = (int(x)*self.scale,int(y)*self.scale)
        else:
            textrect.x = int(x)*self.scale
            textrect.y = int(y)*self.scale
        screen.blit(textsurf, textrect)

    def maketext(self,text,size,col=(0,0,0),font='impact',bold=False,antialiasing=True):
        largetext = pygame.font.SysFont(font,int(size*self.scale),bold)
        textsurf = largetext.render(text, antialiasing, col)
        return textsurf
    
    def makebutton(self,x,y,text,textsize,command,menu='main',col=(150,150,150),bordercol=-1,hovercol=-1,textcol=(0,0,0),width=-1,height=-1,border=3,verticalspacing=0,horizontalspacing=8,roundedcorners=0,clicktype=0,textoffsetx=0,textoffsety=0):
        textimage = self.maketext(text,textsize,textcol)
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
        self.buttons.append(BUTTON(x,y,text,textsize,command,menu,col,bordercol,hovercol,textcol,width,height,width-border*2,height-border*2,roundedcorners,clicktype,textimage,textoffsetx,textoffsety))
        
    def maketextbox(self,x,y,title,width,height,menu='main',border=4,titlesize=50,titleheight=-1,titlecenter=True,textsize=40,textcenter=False,col=(150,150,150),backingcol=(100,100,100),titlecol=(0,0,0),textcol=(0,0,0),roundedcorners=0):
        if titleheight == -1:
            titleheight = titlesize
        self.textboxes.append(TEXTBOX(x,y,width,height,border,titleheight,roundedcorners,title,titlecenter,titlesize,titlecol,backingcol,textcenter,textsize,textcol,col,menu))
        
    def rendergui(self,screen):
        for a in self.buttons:
            if a.menu == self.activemenu:
                if a.render(screen,self.mpos,self.mprs,self.mouseheld,self.buttondowntimer,self.scale):
                    a.command()
                    self.mouseheld[a.clicktype][1]-=1
        for a in self.textboxes:
            if a.menu == self.activemenu:
                a.render(screen,self.scale)
    def movemenu(self,moveto):
        self.backchain.append(self.activemenu)
        self.activemenu = moveto
... (126 lines left)
Collapse
message.txt
10 KB
﻿
import pygame,random,math,time,copy,ctypes
pygame.init()

def rectscaler(rect,scale):
    return pygame.Rect(rect.x*scale,rect.y*scale,rect.w*scale,rect.h*scale)

    
class UI:
    def __init__(self,scale=1):
        self.scale = scale
        self.mouseheld = [[0,0],[0,0],[0,0]]
        self.loadtickdata()
        
        self.buttons = []
        self.textboxes = []
        self.selectedtextbox = -1
        
        self.activemenu = 'main'
        self.backchain = []
        self.buttondowntimer = 8
        self.checkcaps()

    def checkcaps(self):
        hllDll = ctypes.WinDLL("User32.dll")
        self.capslock = bool(hllDll.GetKeyState(0x14))
        
    def scaleset(self,scale):
        self.scale = scale
        for a in self.buttons:
            textimage = self.maketext(a.text,a.textsize,a.textcol)
            a.gentext(textimage)
        
    def loadtickdata(self):
        mpos = pygame.mouse.get_pos()
        self.mpos = [mpos[0]/self.scale,mpos[1]/self.scale]
        self.mprs = pygame.mouse.get_pressed()
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
                    self.texboxes[self.selectedtextbox].inputkey(self.capslock,event)
                    if not self.texboxes[self.selectedtextbox].selected:
                        self.selectedtextbox = -1
        
    def write(self,screen,x,y,text,size,col=(0,0,0),center=True,font='impact',bold=False,antialiasing=True):
        largetext = pygame.font.SysFont(font,int(size*self.scale),bold)
        textsurf = largetext.render(text, antialiasing, col)
        textrect = textsurf.get_rect()
        if center:
            textrect.center = (int(x)*self.scale,int(y)*self.scale)
        else:
            textrect.x = int(x)*self.scale
            textrect.y = int(y)*self.scale
        screen.blit(textsurf, textrect)

    def maketext(self,text,size,col=(0,0,0),font='impact',bold=False,antialiasing=True):
        largetext = pygame.font.SysFont(font,int(size*self.scale),bold)
        textsurf = largetext.render(text, antialiasing, col)
        return textsurf
    
    def makebutton(self,x,y,text,textsize,command,menu='main',col=(150,150,150),bordercol=-1,hovercol=-1,textcol=(0,0,0),width=-1,height=-1,border=3,verticalspacing=0,horizontalspacing=8,roundedcorners=0,clicktype=0,textoffsetx=0,textoffsety=0):
        textimage = self.maketext(text,textsize,textcol)
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
        self.buttons.append(BUTTON(x,y,text,textsize,command,menu,col,bordercol,hovercol,textcol,width,height,width-border*2,height-border*2,roundedcorners,clicktype,textimage,textoffsetx,textoffsety))
        
    def maketextbox(self,x,y,title,width,height,menu='main',border=4,titlesize=50,titleheight=-1,titlecenter=True,textsize=40,textcenter=False,col=(150,150,150),backingcol=(100,100,100),titlecol=(0,0,0),textcol=(0,0,0),roundedcorners=0):
        if titleheight == -1:
            titleheight = titlesize
        self.textboxes.append(TEXTBOX(x,y,width,height,border,titleheight,roundedcorners,title,titlecenter,titlesize,titlecol,backingcol,textcenter,textsize,textcol,col,menu))
        
    def rendergui(self,screen):
        for a in self.buttons:
            if a.menu == self.activemenu:
                if a.render(screen,self.mpos,self.mprs,self.mouseheld,self.buttondowntimer,self.scale):
                    a.command()
                    self.mouseheld[a.clicktype][1]-=1
        for a in self.textboxes:
            if a.menu == self.activemenu:
                a.render(screen,self.scale)
    def movemenu(self,moveto):
        self.backchain.append(self.activemenu)
        self.activemenu = moveto
    def menuback(self):
        if len(self.backchain)>0:
            self.activemenu = self.backchain[-1]
            del self.backchain[-1]
        
            

class BUTTON:
    def __init__(self,x,y,text,textsize,command,menu,col,bordercol,hovercol,textcol,width,height,innerwidth,innerheight,roundedcorners,clicktype,textimage,textoffsetx,textoffsety):
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
    def __init__(self,x,y,width,height,border,titleheight,roundedcorners,title,titlecenter,titlesize,titlecol,backingcol,textcenter,textsize,textcol,textbackingcol,menu):
        self.x = x
        self.y = y
        
        self.width = width
        self.height = height
        self.border = border
        self.titleheight = titleheight
        self.roundedcorners = roundedcorners
        self.rect = pygame.Rect(self.x,self.y,self.width,self.height)
        self.innerrect = pygame.Rect(self.x+self.border,self.y+self.titleheight+self.border,self.width-self.border*2,self.height-self.border*2-self.titleheight)

        self.title = title
        self.titlecenter = titlecenter
        self.titlesize = titlesize
        self.titlecol = titlecol
        self.backingcol = backingcol

        self.textcenter = textcenter
        self.textsize = textsize
        self.textcol = textcol
        self.textbackingcol = textbackingcol

        self.menu = menu

        self.text = ''
        self.selected = False
        self.typeline = 0

    def inputkey(self,caps,event):
        item = ''
        remove = False
        esc = False
        enter = False
        
        if event.key<123 and event.key>64:
            if (caps or kprs[pygame.K_LSHIFT]) and (event.key>96 and event.key<121):
                item = chr(event.key-32)
            else:
                item = chr(event.key)
        elif chr(event.key) in ''' !"£$%^&*()-_=+[{]};:'@#~,<.>/?`¬\|''':
            item = chr(event.key)
        if event.key == pygame.K_BACKSPACE:
            remove = True
        if event.key == pygame.K_ESCAPE:
            self.selected = False
        if event.key == pygame.K_RETURN:
            enter = True
        if item != '':
            self.text += item
        if remove:
            self.text = self.text[:-1]

    def render(self,screen,scale):
        if self.typeline>40:
            ntext = self.text+'|'
        else:
            ntext = self.text
        pygame.draw.rect(screen,self.backingcol,rectscaler(self.rect,scale))
        pygame.draw.rect(screen,self.textbackingcol,rectscaler(self.innerrect,scale))
        #screen.blit(self.titleimage,self.titlerect)
        #write(self.rect.x*scale,self.rect.y*scale,ntext,(0,0,0),50,screen,True)
        self.typeline+=1
        if self.typeline == 80:
            self.typeline = 0
    
