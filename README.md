# PyUI
A gui module for pygame that allows for the creation of buttons, texstboxes, tables, text, sliders and scroll bars inside the pygame module. It acts as an add on to normal pygame code, and can be seamlessly integrated into pre existing code so a simple gui can be added.
# Requirements
The only module used is pygame, and the base code to integrate PyUI into a pygame project is under 

# Documentation
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



