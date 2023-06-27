# PyUI
A gui module for pygame that allows for the creation of buttons, texstboxes, tables, text, sliders and scroll bars.
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

## Gui Objects
There are several objects that can be made, each being produced through a command in the ui object, then being rendered through the rendergui() function.
### Buttons
### Checkbox
### Text
### Textbox
### Table
### Slider
### Scroller
### Windowed Menu
### Rect
### Circle

## Using Gui Objects
deletion/access
