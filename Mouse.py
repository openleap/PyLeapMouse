#William Yager
#Leap Python mouse controller POC

#Mouse functions in OS X
from Quartz.CoreGraphics import CGEventCreateMouseEvent
from Quartz.CoreGraphics import CGEventPost
from Quartz.CoreGraphics import CGDisplayBounds
from Quartz.CoreGraphics import kCGEventMouseMoved
from Quartz.CoreGraphics import kCGEventLeftMouseDragged
from Quartz.CoreGraphics import kCGEventLeftMouseDown
from Quartz.CoreGraphics import kCGEventLeftMouseUp
from Quartz.CoreGraphics import kCGMouseButtonLeft
from Quartz.CoreGraphics import kCGEventRightMouseDown
from Quartz.CoreGraphics import kCGEventRightMouseDown
from Quartz.CoreGraphics import kCGEventRightMouseUp
from Quartz.CoreGraphics import kCGMouseButtonRight
from Quartz.CoreGraphics import kCGHIDEventTap

def mouseEvent(type, posx, posy, button=kCGMouseButtonLeft):
    theEvent = CGEventCreateMouseEvent(
        None, 
        type, 
        (posx,posy), 
        button)
    CGEventPost(kCGHIDEventTap, theEvent)

def mouseMove(posx,posy):
    mouseEvent(kCGEventMouseMoved, posx,posy);

def mouseClick(posx,posy):
    mouseEvent(kCGEventLeftMouseDown, posx,posy);
    mouseEvent(kCGEventLeftMouseUp, posx,posy);

def mouseClickDown(posx, posy):
    mouseEvent(kCGEventLeftMouseDown, posx,posy);

def mouseClickUp(posx, posy):
    mouseEvent(kCGEventLeftMouseUp, posx,posy);

def mouseDrag(posx, posy): #A Drag is a Move where the mouse key is held down
    mouseEvent(kCGEventLeftMouseDragged, posx,posy)

def mouseRightClick(posx,posy):
    mouseEvent(kCGEventRightMouseDown, posx, posy, kCGMouseButtonRight);
    mouseEvent(kCGEventRightMouseUp, posx, posy, kCGMouseButtonRight);

#Why make a class? So we can call click(), move() etc. without specifying coordinates, state, whatever
#And also to make cross-platforming easier
class cursor(object):
    def __init__(self):
        self.x_max = CGDisplayBounds(0).size.width
        self.y_max = CGDisplayBounds(0).size.height
        self.left_button_pressed = False
        self.x = 0
        self.y = 0

    def move(self, posx, posy):
        self.x = posx
        self.y = posy
        if self.x > self.x_max: 
            self.x = self.x_max
        if self.y > self.y_max: 
            self.y = self.y_max
        if self.x < 0.0: 
            self.x = 0.0
        if self.y < 0.0: 
            self.y = 0.0
        print self.x, self.y
        if self.left_button_pressed: #We are dragging
            mouseDrag(self.x, self.y)
        else: #We are not dragging
            mouseMove(self.x, self.y)

    def click(self, posx=None, posy=None):
        if posx == None:
            posx = self.x
        if posy == None:
            posy = self.y
        mouseClick(posx, posy)
    
    def set_left_button_pressed(self, boolean_button):
        if boolean_button == True: #Pressed
            self.click_down()
        else: #not pressed
            self.click_up()
        
    def click_down(self, posx=None, posy=None):
        if posx == None:
            posx = self.x
        if posy == None:
            posy = self.y
        mouseClickDown(posx, posy)
        self.left_button_pressed = True

    def click_up(self, posx=None, posy=None):
        if posx == None:
            posx = self.x
        if posy == None:
            posy = self.y
        mouseClickUp(posx, posy)
        self.left_button_pressed = False

    def rightClick(self, posx=None, posy=None):
        if posx == None:
            posx = self.x
        if posy == None:
            posy = self.y
        mouseRightClick(posx, posy)
