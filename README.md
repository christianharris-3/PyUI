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
```cmd
pip install uipygame
```
```py
# When importing the module, if installed through github use:
import PyUI

# If installed though pip use:
from UIpygame import PyUI
```

# Documentation
## Base code
This is the same code from [basic start.py](https://github.com/LazerWolfeGod/PyUI/blob/master/_basic%20start_.py) but commented.
```py
## importing modules
import pygame
pygame.init()

#use depending on installed through github or pip
import PyUI as pyui
from UIpygame import PyUI as pyui

## setting up pygame and PyUI
screenw = 1200
screenh = 900
# creates screen objects of size screenw and screenh
# resizable tag allows the screen to be scaled, remove it to lock screen size
screen = pygame.display.set_mode((screenw, screenh),pygame.RESIZABLE)
# ui object is how most of the PyUI module is operated through
ui = pyui.UI()
# when done is set to True the gameloop ends
done = False
# clock keeps fps consistant at 60
clock = pygame.time.Clock()


# main game loop
while not done:
    # grabs event data like button inputs and mouse position and ruturns pygame event data
    # can be treated the same as pygame.event.get() function
    for event in ui.loadtickdata():
        if event.type == pygame.QUIT:
            done = True
    # fills screen with the wallpaper col, defaults to white
    screen.fill(pyui.Style.wallpapercol)

    # draws and processes all gui objects
    ui.rendergui(screen)
    # displays all changes to the monitor screen
    pygame.display.flip()
    # maintains 60 fps
    clock.tick(60)
# shuts pygame window                                           
pygame.quit() 
```

## Initialiazation and Style System
The UI object is how the user accesses all of PyUIs features, it contains all of the necessary functions and variables for using and manipulating the gui. It should be initially created at the start of any program using PyUI so the module can be used and a GUI created.

A style is a set of default varibles, stored inside the Style class. The style class stores the defaults for a large set of variables, and it will act as the default value for all new objects unless that value is specified when creating the obejct. Styles can be set through the function ui.setstyle(), or via using one of the in built default styles. A default value can be set specifically for each unique object, which is done by adding the objectname and underscore before the variable name.

Example code:
```py
ui = PyUI.UI()
# load a default style
ui.styleload_lightblue()
# sets some specific values
ui.setstyle(col=(255,0,0),roundedcorners=4,wallpapercol=(255,0,0))
# set values specifically for buttons
ui.setstyle(button_font='impact',button_textsize='40')
```
There are multiple default styles, all loaded through the styleload function, all represented in this image.
![image](https://github.com/LazerWolfeGod/PyUI/assets/74326592/764e2fb8-ba43-441d-bce4-1645350d73b3)
```py
#The set of values that can be edited through style system
col, textsize, textcol, roundedcorners, font, bold, wallpapercol
backingcol, hovercol, togglecol, togglehovercol, animationspeed
spacing, verticalspacing, horizontalspacing, backingdraw, borderdraw
border, upperborder, lowerborder, rightborder, leftborder
scalesize, scalex, scaley, antialiasing, colorkey, maxwidth
anchor, objanchor, center, centery, glow, glowcol
clickdownsize, clicktype, clickableborder, textoffsetx, textoffsety
lines, selectcol, selectbordersize, selectshrinksize, cursorsize, textcenter
slidersize, increment, containedslider, movetoclick
isolated, darken, hsvashift
```

## Gui Objects
There are several objects that can be made, each being produced through a command in the ui object, then being rendered through the rendergui() function.
### Buttons
A button is simple object that can be clicked on to run a command. Buttons can be made toggleable, meaning they swap between a toggled and not toggled state, its state can be accessed by the variable "toggle".

```py
# Creates a button that when clicked deletes itself
ui.makeButton(20, 20, 'This Button Deletes Itself', 40, lambda: ui.delete('delete button'), ID='delete button',
              maxwidth=200, spacing=5, rounded_corners=10)
```
### Checkbox
A checkbox is a button with in built defaults to make it into a textbox, it can be treated in the same way a button is.

```py
# Makes 3 bound checkboxes, so only 1 can be toggled at once
ui.makeCheckbox(30, 110, 60, ID='checkbox 1', bindtoggle=['checkbox 2', 'checkbox 3'], toggle=True)
ui.makeCheckbox(90, 110, 60, ID='checkbox 2', bindtoggle=['checkbox 1', 'checkbox 3'], toggle=False)
ui.makeCheckbox(150, 110, 60, ID='checkbox 3', bindtoggle=['checkbox 1', 'checkbox 2'], toggle=False)
```
### Labeled checkbox
The labeled check box is a combination of the text object and a checkbox, as inputs it takes everything the same as with a checkbox, however the text input now controls the text that is displayed next to it. As input it also takes a textpos variable, which can be either "left" or "right" and controls if the text is put to the left or right of the checkbox. The horizontal spacing variable is used to control how far away from the text is from checkbox.
### Text
Text is an object that displays text, it can be given a command. Text can have trouble with antialiasing, as the antialiasing can only be done onto a set surface, so pregenerating the text and reblitting the same image every frame may look bad on a changing background. The background colour may need to be given to give the text something to antialias onto, however if that fails to look good set pregenerated to False, meaning new text is blitted every frame, giving perfect antialiasing but very bad performance.
```py
# makes a text object bound to the bottom right of the screen
ui.maketext(0,0,'Bottom Right',60,anchor=('w-10','h-10'),objanchor=('w','h'),backingcol=(255,255,255))
```
### Textbox
Textboxes can be typed in, a command can be attached for when keys are pressed, or when enter is pressed. If the end of the textbox is reached a scroller is added to the side. The text in the textbox can be accessed by the variable "text". Textboxes can be given functions to run when either enter is pressed or a key is pressed depending on what is set.

```py
# A simple textbox with 2 lines for text
ui.makeTextbox(20, 170, '', 200, 2)
```
### Table 
Tables are grids of objects, they can contain text objects, buttons or textboxes. Tables have a set of row editing functions for efficiency, including: 
- table.row_append(ui,row) adds a row of data to then end of the table
- table.row_insert(ui,row,index) inserts a row into a specific index in the data list
- table.row_remove(ui,index) deletes a row of a set index from data, giving an index of -1 will delete the title
- table.row_replace(ui,row,index) deletes the row at the given index, and replaces it with the new row
Tables can be refreshed through threading, working the same as the refresh function but in a thread: table.threadrefresh()

```py
# Makes a table with a variety of different features
data = [['Test', ui.maketext(0, 0, 'Colour', textcol=(255, 100, 0), backingcol=(50, 0, 255), spacing=5, textcenter=True,
                             roundedcorners=4)],
        [ui.makeTextbox(0, 0, textsize=25, spacing=3), '{clock}'],
        [ui.makeButton(0, 0, 'Button', border=5, spacing=10), 6]]

ui.makeTable(240, 20, data, spacing=10, roundedcorners=4)
```
### Scroller Table
A table that works nearly exactly like a normal table, however creates a scroller to its right that scrolls the table up and down. The height of the scroller and therefore table is controlled through the pageheight variable. The compress variable is used to shrink the size of the table when the scroller is active, if set to true it will reduce down the columns it can, any column with an automatic width can not be reduced. Setting it to an int will only reduce that column and only if that column can be reduced. Lastly it can be set to a list in which the length has to be equal to the number of columns, and the ratio of the values put in will reduce the columns by the given ratios.

```py
# Create some random dummy data to fill the table
data = [['Test', ui.maketext(0, 0, 'Colour', textcol=(255, 100, 0), backingcol=(50, 0, 255))],
        [ui.makeTextbox(0, 0, textsize=25, spacing=3), '{clock}'],
        [ui.makeButton(0, 0, 'Button', spacing=4), 3]]
# Generate the scroller table, second column will compress_table
table = ui.makescrollertable(240, 20, data, ['Text', '{shuffle}'], boxwidth=200, compress=1, textcenter=True)
# Add new data to the table, forcing the scroller to become active
for a in range(5):
  table.row_append(['new line', len(table.table)])
```
### Slider
Sliders contain a bar that a button is moved back and forth on when clicked and dragged. The amount the slider is slid can be accessed by the "slider" variable.
--note to self talk about the binding text and textboxes thing

```py
# Make slider with a button with text changing depending on the sliders position
def updatetext():
    ui.IDs['slider button'].setText(str(ui.IDs['slider'].slider))


ui.makeslider(30, 280, 450, 20, button=ui.makeButton(0, 0, '4', ID='slider button'), command=updatetext, ID='slider',
              increment=1)
```
### Scroller
Scrollers are similar to sliders, however have a set height of the bar being moved. The bar is not a button object, it is in built into the scroller and therefore is more limiting in terms of design.
### Windowed Menu
A windowed menu is a replacement for a menu, give it a menu and a behindmenu and then all gui objects on its menu will be drawn onto the windowed menu, with 0 0 starting at the upper left corner of the windowed menu not the screen. This means when the activemenu is a windowed menu, the behind menu will still be displayed.
### Window
Acts very similar to a windowed menu, however acts without a seperate menu. Objects cant be placed on it by putting them on the same menu as the window, as it is not a seperate menu. Instead to put objects on the menu either when it is first created pass the attached objects into the windows "bounditems" parameter list, or after it is created run the window.binditem(object) code to bind it. The window can be open and shut through window.open() and window.shut(), open will automatically shut it the menu if it is already open unless the "toggleopen" parameter of the open function is set to false, while shut will always shut the menu. 

The menu will animate opening and shutting, there are 8 different types of animation, each can be given one of 4 waves. The animation sections split into 2 types, "move" and "compress", with move being the window moves off screen in a given direction, while comress being where a menu gets squished into a specific direction. 
The wave changes how the speed of the animation changes, the waves being "linear" where the speed remains consistent, "sin" starts slow and ends slow, speeds up in the middle, "sinin" starts fast and slows down and "sinout" starts slow and speeds up.
When giving an animation to an object, it is given in a single string where multiple types of different waves can be given in a string. 
The string should look like this: "moveup:sinout compressdown:linear moveleft"
Each animation is seperated by a space, with the wave being after a colon without spaces. If no wave is given, it defaults to "sinout".

```py
# Create a window with a textbox on it
window = ui.makewindow(200, 30, 200, 200, animationtype='compressup moveleft', bounditems=[
  ui.makeTextbox(10, 10, width=180, lines=2)])

# Add a button to the window
window.bindItem(ui.makeButton(10, 100, 'test'))
# Make a button to open the menu
ui.makeButton(20, 80, 'open menu', 40, lambda: window.open())
```
### Rect
A simple rectangle with no additional function.
### Circle
A circle is actually a rect object, with equal width and height and roundedcorners set to half the width(radius), creating a circle from the same rect object. This means it can be treated the same way a Rect is.
### Search Bar
A composite object made of a textbox, 2 buttons and some text. Whatever function is inputed as the command will be run when a user clicks the enter key, or the search button. The cross just wipes the textbox, and text arguement is used to create the display text.
### DropDown
A dropdown is an object used to select one of multiple items in a list. When clicked it opens a window object containing a scroller table with a button for each item that can be selected. The command is ran when a button on the scroller table is pressed and the main display text is swapped out. The active text can be accessed through the objects "active" attribute.
```py
# Function to output the selected item
def output():
    print(ui.IDs['dropdown'].active)
# Creates the dropdown menu with that function
ui.makedropdown(10,10,['Option 1','Option 2','Option 3'],
                command=output,ID='dropdown')
```
## Using Gui Objects
Using the ui object, objects can be accessed and deleted.
To access an object you must give the object an ID when it is generated, and then using the ui.IDs dictionary it can be accessed. The make function also returns the object, meaning it can be stored and used in your code. When objects are changed in any way, eg moving its x and y position or changing the text inside it, the objects refresh function should be used. To delete an object use the ui.delete function, passing in objects ID that is to be deleted. Some functions exist for setting specific values, primarly settext, which allows the refresh function to not be used.
Example code:

```py
## make a button at x=100,y=200 with the text 'Test Button' 
button = ui.makeButton(100, 200, 'Test Button', ID='test button')
## update the text on the button
button.setText('New Text')
## update the buttons font
ui.IDs['test button'].font = 'helvetica'
ui.IDs['test button'].refresh()
## delete object
ui.delete('test button')
```

## Menu System
Every object in PyUI has a menu in the form of a string which dictates what menu it is displayed on, with the current menu being stored in the ui.activemenu variable. When a new object is created it will be automatically placed on the 'main' menu.
You can move between menus using 2 functions in the ui object:
```py
ui.movemenu('new menu','left')
ui.menuback()
```
The menumove function will swap the activemenu to the menu entered, with an optional direction which will animate all menu objects moving away, and the all the objects on the new menu moving in making a clean slide from one menu to another. The menuback function will move to the previous activemenu and doing the reverse direction of the previous used slide. 

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
ui.maketext(100, 100, 'This is a cross {cross}')
ui.makeButton(100, 200, 'This is lots of crosses {}{}{}{}{}', img='cross')
ui.makeButton(100, 300, 'This is an small arrow pointing up {arrow stick=0.3 up}')
```
In built images can also be added by the user in code, you can add a pygame.Surface object with a corrisponding name to access it by, allowing with the same syntax that image to be accessed. 
```py
ui.addinbuiltimage('tree',pygame.image.load('example.png'))
ui.maketext(100,100,{tree})
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
- 'on' An on button
- 'lock' A lock symbol

## Useful Tools
The main UI object has several functions that can be used for various purposes, some of these functions are seperate from the ui object as just independant functions.

### Colour Functions
There are several useful functions for processing rgb values of colour.
- The first is a basic interpolation function that takes 2 rgb or rgba values and a weight of 0 to 1, interpolating between them.
    ```py
    col1 = (255,0,0)
    col2 = (0,0,255)
    weight = 0.3
    newcolour = pyui.colav(col1,col2,weight)
    ```
- Second is a more useable collection of this, generating a list of colours that fade through multiple colours. The inputs are a list of colours, which must contain at least 2 rgb colours, and an int for the number of colours generated per 2 colours. e.g. inputting a list of 3 colours, red, green and blue, and the number 10, will return a list of 20 colours, fading through red, green and blue.
    ```py
    cols = [(255,0,0),(0,255,0),(0,0,255)]
    sizeperfade = 10
    fade = pyui.genfade(cols,sizeperfade)
    ```
- Last is a function to make a colour lighter or darker, where a single rgb is input along with an int, where the int is a value -255 to 255. Returned is a new colour that is lighter or darker by thje given value, positive makes it lighter negative makes darker.
     ```py
    col = (100,150,100)
    shift = 40
    newcol = pyui.shiftcolor(col,shift)
    ```
### Collision functions
These are some functions i designed for (another project)[https://github.com/LazerWolfeGod/Car-Game], that i have put into PyUI as they may be useful.
####
- The first function is used to calculate the distance between a rectangle and a given point, the rect input can be either a pygame.Rect, or a tuple in the form (x,y,width,height), and the point is a simple (x,y) tuple. It returns a distance of 0 if the point is colliding with the rectangle.
   ```py
   point = (100,20)
   rect = (20,30,60,100)
   distance = pyui.distancetorect(point,rect)
   ```
- Second is a function to calculate if and where 2 lines cross, the inputs are L1 and L2, which are 2 lines represneted by 2 sets of points. multipled variables are returned, if the lines do not cross False and an int is returned, the int being some info for debugging, if they do cross returned is True, an x and a y. The x and y being the crossing points.
    ```py
    L1 = [(10,40),(20,90)]
    L2 = [(5,20),(40,60)]
    cross = pyui.linecross(L1,L2)
    if cross[0]:
        print('x':cross[1],'y':cross[2])
    ```
- Next is a very similar function with a similar purpose, this function takes a circle and a line and returns if they cross and where they cross if they do. L1 is the line, L2 is the circle in the form of a point and a radius. Similar formating for the returned value, only one point is returned.
    ```py
    L1 = [(10,40),(20,90)]
    L2 = [(40,50),40]
    cross = pyui.linecirclecross(L1,L2)
    if cross[0]:
        print('x':cross[1][0],'y':cross[1][1])
    ```
- Last is a function to detect if a point is inside a polygon, taking a single point and a list of points. This is done by drawing a line out from the point and counting how many times this point crosses the polygon, if its even the point is outside if its odd the point is inside. A single Boolean True/False is returned
    ```py
    point = (50,80)
    polygon = [(10,20),(50,90),(30,50)]
    collide = pyui.polycollide(point,polygon)
    ```
### UI object functions
The ui object has multiple utility functions for a range uses.
#### printtree
The function printtree is a debugging tool for outputting the object tree, or what objects are bound to each other. The only objects that are not bound to anything are menu objects and windowedmenu objects. The menu objects are automatically created and processed, no user input is required. The only input to the function is not needed, by default the function will print out the ID of every object, however an object ID or object itself can be input, only outputing the tree below that object.
#### quit
The quit function exits pygame via queueing a pygame.quit event. Acts as a simple and effective way to exit the entire pygame program.
#### write
The write function takes several variables as input, however the primary is a surface, x and y pos, some text and a textsize. Some rendered text is then displayed to the surface, no value is returned as the pygame surface is just edited.

## Object variables
All objects have a range of variables that can be changed to edit the object being made, most objects share similar variables and do the same job for each object so can be described in one, rather than a different set for each object.
Colours are given in the form (r,g,b) where r, g and b are integers >= 0 and <= 255.
When looking at a function in code the most common value is -1, this means it is being later set to some form of default. For most of these variables the default can be set using the [style system](#Style-System).
### General variables
- **x**-***int/float*** = The x position of the top left corner of the object relative to the anchor(default is 0,0).
- **y**-***int/float*** = The y position of the top leftcorner of the object relative to the anchor(default is 0,0).
- **width**-***int/float*** = The full width of the object.
- **height**-***int/float*** = The full height of the object.
- **menu**-***str/list[str]*** = The menu the object is on, can be given a list of menus that it will appear on. if the string "animate" is the list the object will animate with the rest of the menu when moving menus.
- **ID**-***str*** = The ID of the object, if one of the same name already exists a 1/2/3 etc is added to the end of the ID.
- **layer**-***int/float*** = The display order of the object, lower number means drawn underneath and default is 1.
- **roundedcorners**-***int/float*** = Rounds the corners of the object by, the value given is the radius of the quarter circle in each corner of the rect
- **bounditems**-***list[any PyUI GUI object]***  = A list of objects bound to the object being made.
- **killtime**-***int/float*** = A time in seconds between the creation of the object and the object being automatically deleted.
- **anchor**-***(str/int/float,str/int/float)*** = The point treated as the origin by the object, refer to Object Positioning for more info.
- **objanchor**-***(str/int/float,str/int/float)*** = The point on the object its x and y act on, refer to Object Positioning for more info.
- **enabled**-***bool*** = stops the object from being rendered if False.
- **center**-***bool*** = Auto sets objanchor to the center of the object.
- **centery**-***bool*** = Auto sets specifically the vertical center of the object.
- **scalesize**-***bool*** = Boolean that allows/doesnt allow the object to scale in size when the screen is resized.
- **scalex**-***bool*** = Boolean that allows/doesnt allow the object to scale closer to its origin in the x direction when the screen is resized.
- **scaley**-***bool*** = Boolean that allows/doesnt allow the object to scale closer to its origin in the y direction when the screen is resized.
- **scaleby**-***bool*** = Defaults to the global variable "autoscale" in the UI object, setting scaleby to "vertical" will make the object scalesize based on the changing height of the screen, while setting it to "horizontal" will do the same but for screen width.
- **border**-***int/float*** = Sets the pixel size of the border of the object.
- **upperborder**-***int/float*** = Sets pixel size of only the upper border.
- **lowerborder**-***int/float*** = Sets pixel size of only the lower border
- **rightborder**-***int/float*** = Sets pixel size of only the right border.
- **leftborder**-***int/float*** = Sets pixel size of only the left border.
- **spacing**-***int/float*** = Sets the pixel distance between the text and the border inside an object.
- **verticalspacing**-***int/float*** = Sets the vertical pixel distance between the text and the border inside an object.
- **horizontalspacing**-***int/float*** = Sets the horizontal pixel distance between the text and the border inside an object.
- **command**-***function*** = Any function that is then run by the object, this can be a PyUI function like menumove or delete, or any user created function. To give the function inputs use the syntax

```py
command=lambda: testfunction('function arguements')
```

- **runcommandat**-***int:0/1/2*** = Used to control when a command is ran when clicking a button, 0=when first clicked, 1=every tick the button is held, 2=when the button is released.
- **clickablerect**-***Pygame.Rect/tuple(x,y,w,h)*** = Tuple can contain text in terms of w and h, where w and h are relative to the size of this object, and x and y are based around the top left corner of the object.
- **col**-***(r,g,b)*** = The overall colour of the object, other colours used if not set by the user will be based off this colour. If not set col defaults to the ui.default col variable.
- **backingcol**-***(r,g,b)/int*** = The colour of the backing,mostly interchangeable with bordercol, if unset it will default to adding 20 to the the r, g and b number of col. Setting it to an Int will add that int value to col instead of 20.
- **bordercol**-***(r,g,b)*** = Interchangable with backingcol, just used as it is more intuative for some objects.
- **backingdraw**-***bool*** = Boolean that toggles if the backing is drawn.
- **borderdraw**-***bool*** = Boolean that toggles if the border is drawn.
- **glow**-***int*** = An value that changes the size of the glow effect around an object, defaults to no glow.
- **glowcol**-***(r,g,b,a)*** = Edits the colour of the glow specifically.
- **refreshbind**-***list[str]*** = A list of object IDs that will be refreshed when this object is refreshed.

### Text variables
- **text**-***str*** = The text that is displayed, can be used with [in build images](#In-built-images) with all objects. Textboxes require imgdisplay to be true for this to take effect.
- **textsize**-***int/float*** = The size of the text.
- **img**-***pygame.Surface/str*** = Used inside the [in build image system](#In-built-images), can also be used to input an image through pygame with img=pygame.image.load('image.png'), if a list of items are inputed it will animate through each item.
- **colorkey**-***(r,g,b)*** = The rgb colorkey used for the text image. [more info](https://www.pygame.org/docs/ref/surface.html)
- **font**-***str*** = The name of the font of the text, to see all valid fonts use pygame.font.get_fonts()
- **bold**-***bool*** = Boolean to control if text is in bold.
- **antialiasing**-***bool*** = Boolean to control if text is antialiased.
- **pregenerated**-***bool*** = Default is False, if True it regenerates the text image every frame resulting in no antialiasing problems, may result in large drop in fps is used too much.
- **textcol**-***(r,g,b)*** = The colour of the text displayed.
- **textoffsetx**-***int/float*** = Used to configure the x position of where the text is placed on the object, postive most right and negative moves left.
- **textoffsety**-***int/float*** = Same as textoffsetx but for y position, up is negative down is positive.
- **animationspeed**-***int: >0*** = The number of frames of each animation frame.

### Button specific
- **hovercol**-***(r,g,b)*** = The colour the backing goes when the mouse hovers over it.
- **clickdownsize**-***int/float*** = The number of pixels the moved in by when the button is clicked down.
- **clicktype**-***int:0/1/2*** = The mousebutton used to click the button, default = 0 (left click), 1 is middle click, 2 is right click.
- **clickableborder**-***int*** = A number in pixels that increases hitbox of a button
- **maxwidth**-***int/float*** = The max width of the text, the text will move onto a new line to keep within this limit.
- **dragable**-***bool*** = Boolean that controls if the button can be dragged
- **toggle**-***bool*** = Sets the starting toggle varible of the obect, this variable is toggled by a toggleable button and is used to access if it is toggled or not.
- **toggleable**-***bool*** = Sets if the button can be toggled.
- **toggletext**-***str*** = The display text when the button is toggled, all same functions as normal text and defaults to normal text if empty.
- **toggleimg**-***str/*** = Same as toggletext except for img variable.
- **togglecol**-***(r,g,b)*** = The backingcol for the text for when it is toggled
- **togglehovercol**-***(r,g,b)*** = The colour when hovering and toggled.
- **bindtoggle**-***list[str]*** = A list of object IDs that are toggled off when it is toggled on, the object can have its own ID in the list and be unaffected.
- **presskeys**-***list[pygame.K_key]/pygame.K_key*** = The keys that when pressed will press the button. Works when the object is on the active menu, the key is given as [pygame constants](https://www.pygame.org/docs/ref/key.html) e.g. pygame.K_SPACE or pygame.K_u.

### Textbox specific
- **lines**-***int*** = The number of lines of text that can be stored in the textbox, it auto sets the height of the textbox based on textsize.
- **linelimit**-***int*** = The number of lines that can be used and scrolled to (doesnt work very well).
- **selectcol**-***(r,g,b)*** = The colour of the border that appears when a textbox is selected.
- **selectbordersize**-***int*** = The size of the border in pixels, set to 0 to remove border.
- **selectshrinksize**-***int*** = The amount the border moves in by when clicking, (inner image is blitted after so recomended this isnt used)
- **cursorsize**-***int*** = Size in pixels of the cursor, defaults to textsize.
- **textcenter**-***bool*** = Dictates if the text is centered on each line.
- **chrlimit**-***int*** = The charcter limit in the text.
- **numsonly**-***bool*** = Only allows numbers to be typed, filter works by attempting to turn the text into a float meaning any string that can be passed to the float() function is allowed.
- **enterreturns**-***bool*** = Controls if enter starts a new line (quite broken dont use).
- **commandifenter**-***bool*** = Controls if the enter key runs the command.
- **commandifkey**-***bool*** = Controls if any key input runs the command.
- **imgdisplay**-***bool*** = Controls if the [in build image system](#In-built-images) runs inside of the textbox (can be quite laggy if too much text+in built images when editing text).
- **attachscroller**-***bool*** = If False the automaticly added scroller is removed entirely, defaults to True.
- **intscroller**-***bool*** = If the number is float or int (can be enforced with numsonly variable) and the scroller on the textbox is inactive, the scrollwheel can be used to increase/decrease the value. As well as this if the textbox is clicked and the mouse moved up/down the value will also increase/decrease.
- **minint**-***int/float*** = Sets a minimum value that the texts number value can be. Default is negative infinity, meaning no minimum value.
- **maxint**-***int/float*** = Sets a maximum value that the texts number value can be. Default is infinity, meaning no maximum value.
- **intwraparound**-***bool*** = Toggles if when using intscroller if the number gets larger than maxint/smaller than minint it wraps round to be minint/maxint.

### Table specific
- **data**-***list[list[int/str/button/textbox/text/table/slider/pygame.Surface]]*** = A 2D list containing all of the info the body of the table, each item can be a variety of data types. The format is each inner list is a row in the table.
- **titles**-***list[int/str/button/textbox/text/table/slider/pygame.Surface]*** = A 1D list that can be left empty for no titles, works the exact same as a single row in data
- **boxwidth**-***int/list[int]*** = Sets the widths of each column in pixels, a value of -1 will auto fit to the width of the items i that column. Giving an int will use that int value for every column of the table, default is -1 meaning every column is auto fitted. 
- **boxheight**-***int/list[int]*** = Exact same function and use as boxwidth however for rows not columns.
- **linesize**-***int/float*** = The pixel size of the width of each line seperating objects in the table.
- **guesswidth**-***int/float*** = When using threading to refresh a table the table, there is no value for boxwidth/height if it is -1, so it assumes this value to be the width of the table before resetting back to proper values when the refresh is finished.
- **guessheight**-***int/float*** = Same as guesswidth but for height of boxes.

### Scroller Table specific
- **pageheight**-***int/float*** = The display height of the table, and the height of the scoller that appears next to it. When the table changes in size the display height will stick to this value.
- **compress**-***bool/int/list[float/int]*** = Default to True, used to shrink the size of the table when the scroller is active, if set to False the table will not change in size when the scroller appears, if True it will reduce down the columns it can, any column with an automatic width can not be reduced. Setting it to an int will only reduce that column and only if that column can be reduced. Lastly it can be set to a list in which the length has to be equal to the number of columns, and the ratio of the values put in will reduce the columns by the given ratios.
- **scrollerwidth**-***int*** = The width in pixels of the scroller attached to the table.
- **screencompressed**-***int/bool*** = If False no change, otherwise it cuts of a table (shrinking the pageheight), when it goes below the screen. The int given gives the number of pixels of space given between the table and the bottom of the screen.

### Scroller/Slider specific
- **minp**-***int*** = The lower bound for the objects scroll/slider value
- **maxp**-***int: >minp*** = The lower upper for the objects scroll/slider value
- **startp**-***int: >minp,<maxp*** = The point inbetween minp and maxp that the object starts its value at.
#### Scroller
- **scrollercol** = Remove this it does nothing
- **pageheight**-***int/float*** = The height of the page that can be seen, dictates the height of the clickable part of the scroller. if the page height it larger than maxp-minp the scroller will not display.
- **scrollbind**-***list[str]*** = A list of object IDs that are scrolled when the scroller is moved
#### Slider
- **slidersize**-***int/float*** = The width and height of the button on the slider.
- **increment**-***int/float*** = The value by which the the sliders value locks to multiples of, ie setting it to 1 will mean the .slider value will only be integer values.
- **sliderroundedcorners** = Remove this it does nothing
- **button**-***button object*** = The button object that is then locked onto the slider, allows for the same customizability a button has but on a slider.
- **direction**-***str*** = either 'vertical' or 'horizontal', setting if the button moves up and down or left and right.
- **containedslider**-***bool*** = Will auto set the button to be contained inside the slider.
- **movetoclick**-***bool*** = Sets if clicking anywhere in the slider moves the slider to that point on it.

### Windowed menu/window specific
- **behindmenu**-***str*** = The name of the menu that the windowedmenu appears on top of, only required for windowed menus.
- **isolated**-***bool*** = Controls if objects on the behindmenu can be used while the menu is active, this only works for windowedmenus, while this works for both: If True clicking anywhere other than the windowed menu will shut it, if False clicking on only the button that brought up the menu will shut it.
- **darken**-***int: >=0,<=255*** = The alpha value from 0 to 255 that darkens the behind menu when the windowedmenu or window is open.
- **autoshutwindows**-***list[IDs]*** = A list of strings, where each string is the ID of a window object. When this window object is opened, all windows in this list are automatically shut.



