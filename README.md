# PyUI
A gui module for pygame that allows for the creation of buttons, texstboxes, tables, text, sliders and scroll bars inside the pygame module. It acts as an add on to normal pygame code, and can be seamlessly integrated into pre existing code so a simple gui can be added.
# Requirements and file info
The only module used is pygame, and the base code to integrate PyUI into a pygame project is under.
- [PyUI.py](https://github.com/LazerWolfeGod/PyUI/blob/master/PyUI.py) This is the only file required to use the module.
- [PyUI vector maker.py](https://github.com/LazerWolfeGod/PyUI/blob/master/PyUI%20vector%20maker.py) Used to create images inside PyUI, a simple vector image using bezier curves. Clicking the PyUI button will then output a list of numbers that can be placed into pyuis code for the images to be then usde inside of PyUI, see In build images section of documentation for more info.
- [basic start.py](https://github.com/LazerWolfeGod/PyUI/blob/master/_basic%20start_.py) The code to create and init Pygame and PyUI, then create a game loop. Useful as a baseline for making something with PyUI.
- [pyuitesting.py](https://github.com/LazerWolfeGod/PyUI/blob/master/pyuitesting.py) The program I use to develope and test PyUI, it contains several buttons,tables, textboxes etc.
- [/old PyUI versions](https://github.com/LazerWolfeGod/PyUI/tree/master/old%20PyUI%20versions) A file containing all of the previous versions of PyUI while I was not using github.

# Installation
The entire module is inside The single [PyUI.py](https://github.com/LazerWolfeGod/PyUI/blob/master/PyUI.py) file. To download throught github simply download that file and either place it in the same folder as the project it is being used in, or the lib folder where python is installed on your computer.

It can be installed through pip, however the name PyUI was taken so its under the name [UIpygame](https://pypi.org/project/UIpygame/).
```
pip install uipygame
```
When importing the module, if installed through github use:
```
import PyUI
```
If installed though pip use:
```
from UIpygame import PyUI
```

# Documentation
## Base code
This is the same code from [basic start.py](https://github.com/LazerWolfeGod/PyUI/blob/master/_basic%20start_.py) but commented.
```py
## importing modules
import pygame
import PyUI
#if installed through pip use
#from UIpygame import PyUI
pygame.init()

## setting up pygame and PyUI
screenw = 1200
screenh = 900
# creates screen objects of size screenw and screenh
# resizable tag allows the screen to be scaled, remove it to lock screen size
screen = pygame.display.set_mode((screenw, screenh),pygame.RESIZABLE)
pygame.scrap.init()
# ui object is how most of the PyUI module is operated through
ui = PyUI.UI()
# when done is set to True the gameloop ends
done = False
# clock keeps fps consistant at 60
clock = pygame.time.Clock()


# main game loop
while not done:
    # grabs event data like button inputs and mouse position
    pygameeventget = ui.loadtickdata()
    for event in pygameeventget:
        if event.type == pygame.QUIT:
            done = True
    # fills screen with white
    screen.fill((255,255,255))

    # draws and processes all gui objects
    ui.rendergui(screen)
    # displays all changes to the monitor screen
    pygame.display.flip()
    # maintains 60 fps
    clock.tick(60)
# shuts pygame window                                           
pygame.quit() 
```

## Initialiazation
The ui object is how the user accesses all of PyUIs features, it contains all of the necessary functions and variables for using and manipulating the gui. It must be initially created at the start of any program using PyUI with.
the ui object has mutltiple in built defaults vaiables that are used to set the default values when creating a gui object, these can be changed from the in built defaults at the begining of the program.

Example init code:
```py
ui = PyUI.UI()
## these are the in built PyUI defaults
ui.defaultfont = 'calibre'
ui.defaultcol = (150,150,150)
ui.defaulttextcol = (0,0,0)
ui.defaultbackingcol = (255,255,255)
ui.defaultanimationspeed = 30
```

## Menu System
Every object in PyUI has a menu it is displayed on, with the current menu being stored in the ui.activemenu variable. When a new object is created it will be automatically placed on the 'main' menu.
You can move between menus using 2 functions in the ui object:
```py
ui.movemenu('new menu','left')
ui.menuback()
```
The menumove function will swap the activemenu to the menu entered, with an optional direction which will animate all menu objects moving away, and the all the objects on the new menu moving in making a clean slide from one menu to another. The menuback function will move to the previous activemenu and doing the reverse direction of the previous used slide. 

## Gui Objects
There are several objects that can be made, each being produced through a command in the ui object, then being rendered through the rendergui() function.
### Buttons
A button is simple object that can be clicked on to run a command. Buttons can be made toggleable, meaning they swap between a toggled and not toggled state, its state can be accessed by the variable "toggle".
### Checkbox
A checkbox is a button with in built defaults to make it into a textbox, it can be treated in the same way a button is.
### Text
Text is an object that displays text, it can be given a command.
### Textbox
Textboxes can be typed in, a command can be attached for when keys are pressed, or when enter is pressed. If the end of the textbox is reached a scroller is added to the side. The text in the textbox can be accessed by the varible "text".
### Table
Tables are grids of objects, they can contain text objects, buttons or textboxes. If strings are entered it auto generates a text objected to fill the space.
### Slider
Sliders contain a bar that a button is moved back and forth on when clicked and dragged. The amount the slider is slid can be accessed by the "slider"
### Scroller
Scrollers are similar to sliders, however have a set height of the bar being moved. The bar is not a button object, it is in built into the scroller and therefore is more limiting in terms of design.
### Windowed Menu
A windowed menu is a replacement for a menu, give it a menu and a behindmenu and then all gui objects on its menu will be drawn onto the windowed menu, with 0 0 starting at the upper left corner of the windowed menu not the screen. This means when the activemenu is a windowed menu, the behind menu will still be displayed.
### Rect
A simple rectangle with no additional function.
### Circle
A circle is actually a rect object, with equal width and height and roundedcorners set to half the width(radius), creating a circle from the same rect object. This means it can be treated the same way a Rect is.

## Using Gui Objects
Using the ui object, objects can be accessed and deleted.
To access an object you must give the object an ID when it is generated, and then using the ui.IDs dictionary it can be accessed. When objects are changed in any way, eg moving its x and y position or changing the text inside it, the objects refresh function should be used, if it is only moved the refreshcords function should be used. To delete an object use the ui.delete function, passing in objects ID that is to be deleted.

Example code:
```py
## make a button at x=100,y=200 with the text 'Test Button' 
ui.makebutton(100,200,'Test Button',ID='test button')
## update the buttons x position
ui.IDs['test button'].x = 150
ui.IDs['test button'].refreshcords(ui)
## update the text on the button
ui.IDs['test button'].text = 'New'
ui.IDs['test button'].refresh(ui)
## delete object
ui.delete('test button')
```

## Object Positioning
The screen can be dynamically scaled horizontally and vertically, so objects need to be able to be positioned relative to points on the screen rather than always relative to the top left corner. For example, if you wanted an object to be centered around the middle of the screen, simply giving the x and y of the center will not surfise for stretching the screen in only one direction. PyUI's solution to this is anchor points, essentialling changing the origin point for an object, and then the point on the object this is bound too and lastly the x and y positioning of the anchor point to the objectanchor point.

To make an object Always be in the center of the screen the anchor variable should be set to ('w/2','h/2'), this will take the height and width of the screen and set it relative to those lengths. The object anchor should also be set to the center of the object, which can either be done by setting it to ('w/2','h/2'), or just setting center=True, which will default the object center to that. And finally setting x and y to 0, as the objects center will be the same as the center of the screen.

For a more complex example, an object that needs to be always 20 pixels from the bottom of the screen and its distance to the left side of the screen is always 10% the width of the screen. For this The anchor needs to be ('w*0.1','h-20'), this will ensure the width is always a tenth of the screens width, and the y is always 20 pixels lower than the screens height. The object anchor will then need to be the bottom left corner of the object, meaning it is (0,'h'), and lastly the x and y will still be 0 as these 2 points should be the same.

## In built images
When giving text into a PyUI object you can add a set of in built images giving a range of useful symbols. 
There are 2 main types of images, those that are drawn manually and those drawn using [PyUI vector maker.py](https://github.com/LazerWolfeGod/PyUI/blob/master/PyUI%20vector%20maker.py) Used to create images inside PyUI, a simple vector image using bezier curves. Clicking the PyUI button will then output a list of numbers that can be placed into pyuis code for the images to be then usde inside of PyUI, see In build images section of documentation for more info.
Those drawn manually have access to being edited as each has a set of variables that can be used to change properties of the image, which the vector based one is only one set image.
The images can be added by placing the name of the image in {}, or leaving the brackets empty and setting the img variable to the image name.
Setting an img to a loaded image with pygame.image.load('example.png') will not place it into the {}, but will completely overwrite the text.
Manual images have variables that can be changed to edit the image, all in the form ' variable=value ' with a space on either side.
All images can be given:
-the suffix 'up', 'left' or 'down' to rotate it where the default direction is right.
-'scale=float', which will directly modify the scale variable of the image allowing for different sized images to appear in text.
-An colour in the form of an rgb value in 'col=(r,g,b)' with no spaces.
-If the entered text is in the form {"text" variables=...} or {'text' variables=....} it will render text allowing for unique colour/size/font etc in the same text object.

Example code:
```py
ui.maketext(100,100,'This is a cross {cross}')
ui.makebutton(200,100,'This is lots of crosses {}{}{}{}{}',img='cross')
ui.makebutton(300,100,'This is an small arrow pointing up {arrow stick=0.3 up}')
```

### Manual in built images
most variables that edit the image shape are a value between 0 and 1 representing a percentage of the full size of the image.
- 'tick' A simple tick shape.
  - 'thickness' A variable that changes the thickness of the, default = 0.2
- 'cross' A simple cross shape.
  - 'width' The width of the lines on the cross, default = 0.1
- 'arrow' A simple arrow with point and stick. the width of the image is based of the stick and point length.
  - 'stick' The length of the stick of the arrow, default = 0.95
  - 'point' The length of the point of the arrow, default = 0.45
  - 'smooth' The amount of curve the corners of the arrow has, not recomended at low resolutions, default = 0
  - 'width' The width of the stick of the arrow, default = 0.2
- 'settings' The gear symbol commonly used to represent settings.
  - 'innercircle' The radius of the inner circle, default = 0.15
  - 'outercircle' The radius of the outer circle, default = 0.35
  - 'prongs' The number of prongs the gear has, default = 6
  - 'prongwidth' The width of each prong, default = 0.2
  - 'prongsteepness' Controls angle of the prongs, default = 1.1
- 'play' A simple play button triangle.
  - 'rounded' Rounds the corners of the triangle, default = 0
- 'pause' Two rectangles to represent a pause button
  - 'rounded' Rounds the corners of the Rectangle, default = 0
- 'skip' A rectange and play image together, giving a skip symbol.
  - 'rounded' Rounds the rectangle and play image, defulat = 0
  - 'thickness' Changes the width of the rectangle, default = 0.25
  - 'offset' Changes the x position of the rectangle relative to the triangle, default = -0.35
- 'clock' A simple clock image with minute and hour hand.
  - 'hour' sets the position of the hour hand on the clock, default = 0
  - 'minute' sets the position of the minute hand on the clock, default = 20
  - 'minutehandwidth' sets the width of the minute hand, default = 0.05
  - 'hourhandwidth' sets the width of the hour hand, default = 0.05
  - 'circlewidth' sets the width of the outer circle, default = 0.05
- 'loading' Makes some dots spinning in a circle, it returns a single image. If you want to animate it set img=[PyUI.loadinganimation()], which will return a list of all the image names to make an animated loading symbol.
  - 'points' Sets the number of points around the circle, default = 12
  - 'largest' Sets the point which is the largest, then trailing in size as it goes round, default = 0
  -  'traildrop' The size the circles decrease by moving round, default = 0.015
  -  'spotsize' The size of the largest dot, default = 0.1
- 'dots' Makes an image of default 3 dots for a more button.
  - 'num' The number of dots, default = 3
  - 'seperation' The distance between each dot, default = 0.3
  - 'radius' The radius of each dot, default 0.1
- '"sample text"' must be inside quotes to work, can take any text and text in it will not be processed by the in built image system, so works as a way to put {} in text.
  - 'bold' Boolean dictating if the text is bold, default = False
  - 'italic' Boolean dictating if the text is italic, default = False
  - 'strikethrough' Boolean dictating if the text has a line though it, default = False
  - 'underlined' Boolean dictating if the text is underlined, default = False
  - 'antialias' Boolean dictating if the text is antialiased, default = True

### Vector in built images
- 'heart' A heart
- 'smiley' A simple smiley face
- 'happy face' Same thing as smiley just it looks more happy
- 'search' The magnifying glass image generally used for a search function
- 'shuffle' The twisting arrows image used to represent shuffle 
- 'pfp' The monochrome head and shoulders shape
- 'speaker' A speaker symbol
- 'mute' The speaker with an X instead of lines to represent mute
- 'pencil' A simple pencil design.
- 'youtube' A symbol that looks like the youtube play button
- 'queue' The youtube symbol but with some lines behind to try and be a queue symbol (idk this one didnt turn out great)
- 'star' A 5 pointed star

## Object variables
All objects have a range of variables that can be changed to edit the object being made, most objects share similar variables and do the same job for each object so can be described in one, rather than a different set for each object.
### General variables
- **x** = The x position of the top left corner of the object relative to the anchor(default is 0,0).
- **y** = The y position of the top leftcorner of the object relative to the anchor(default is 0,0).
- **width** = The full width of the object.
- **height** = The full height of the object.
- **menu** = The menu the object is on, if set to 'universal' it will be displayed on all menus.
- **ID** = The ID of the object, if one of the same name already exists a 1/2/3 etc is added to the end of the ID.
- **layer** = The display order of the object, lower number means drawn underneath and default is 1.
- **roundedcorners** = Rounds the corners of the object by, the value given is the radius of the quarter circle in each corner of the rect
- **menuexceptions** = if menu = 'universal', a list of the menus it doesnt display on
- **anchor** = The point treated as the origin by the object, refer to Object Positioning for more info.
- **objanchor** = The point on the object its x and y act on, refer to Object Positioning for more info.
- **enabled** = stops the object from being rendered if False.
- **center** = Auto sets objanchor to the center of the object.
- **centery** = Auto sets specifically the vertical center of the object.
- **scalesize** = Boolean that allows/doesnt allow the object to scale in size when the screen is resized.
- **scalex** = Boolean that allows/doesnt allow the object to scale closer to its origin in the x direction when the screen is resized.
- **scaley** = Boolean that allows/doesnt allow the object to scale closer to its origin in the y direction when the screen is resized.
- **border** = Sets the pixel size of the border of the object.
- **upperborder** = Sets pixel size of only the upper border.
- **lowerborder** = Sets pixel size of only the lower border
- **rightborder** = Sets pixel size of only the right border.
- **leftborder** = Sets pixel size of only the left border.
- **spacing** = Sets the pixel distance between the text and the border inside an object.
- **verticalspacing** = Sets the vertical pixel distance between the text and the border inside an object.
- **horizontalspacing** = Sets the horizontal pixel distance between the text and the border inside an object.
- **command** = Any function that is than run by the object, this can be a PyUI function like menumove or delete, or any user created function. To give the function inputs use the syntax

```py
command=lambda: testfunction('function arguements')
```

- **runcommandat** = Used to control when a command is ran when clicking a button, 0=when first clicked, 1=every tick the button is held, 2=when the button is released.
- **clickablerect** = The actual on screen rect (must be Pygame.Rect) that the object can be clicked on in, this is unaffected by any scale variables.
- **col** = The overall colour of the object, other colours used if not set by the user will be based off this colour. If not set col defaults to the ui.default col variable.
- **backingcol** = The colour of the backing,mostly interchangeable with bordercol, if unset it will default to adding 20 to the the r,g and b number of col.
- **bordercol** = Interchangable with backingcol, just used as it is more intuative for some objects.
- **backingdraw** = Boolean that toggles if the backing is drawn.
- **borderdraw** = Boolean that toggles if the border is drawn.
- **glow** = An int that changes the size of the glow effect around an object, defaults to no glow.
- **glowcol** = Edits the colour of the glow specifically.

### Text variables
text
textsize
img
colorkey
font
bold
antialiasing
pregenerated
textcol
textoffsetx
textoffsety
animationspeed

### Button specific
hovercol
clickdownsize
clicktype
maxwidth
dragable
toggle
toggleable
toggletext
toggleimg
togglecol
togglehovercol
bindtoggle

### Textbox specific
lines
linelimit
selectcol
selectbordersize
selectshrinksize
cursorsize
textcenter
chrlimit
numsonly
enterreturns
commandifenter
commandifkey

### Table specific
data
titles
boxwidth
boxheight
linesize

### Scroller/Slider specific
minp
maxp
startp
#### Scroller
scrollercol
scrollerwidth
pageheight
#### Slider
slidercol
sliderbordercol
slidersize
increment
sliderroundedcorners
button
direction
containedslider
movetoclick

### Windowed menu specific
behindmenu
isolated
darken



