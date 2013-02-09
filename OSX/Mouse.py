#William Yager
#Leap Python mouse controller POC


#Mouse functions in OS X
from Quartz.CoreGraphics import (CGEventCreateMouseEvent,CGEventPost,CGDisplayBounds,
    CGEventCreateScrollWheelEvent,CGEventSourceCreate,kCGScrollEventUnitPixel,
    kCGScrollEventUnitLine,kCGEventMouseMoved,kCGEventLeftMouseDragged,
    kCGEventLeftMouseDown,kCGEventLeftMouseUp,kCGMouseButtonLeft,kCGEventRightMouseDown,
    kCGEventRightMouseDown,kCGEventRightMouseUp,kCGMouseButtonRight,kCGHIDEventTap)


#OS X specific: We use CGEventCreateMouseEvent(source, mouse[Event]Type, mouseCursorPosition, mouseButton)
#to make our events, and we post them with CGEventPost(tapLocation, event).
#We can usually/always set "source" to None (Null) and mouseButton to 0 (as the button is implied in the event type)
Event = CGEventCreateMouseEvent  #Easier to type. Alias "Event()" to "CGEventCreateMouseEvent()"

def Post(event):  #Posts the event. I don't want to type "CGEventPost(kCGHIDEventTap," every time.
    CGEventPost(kCGHIDEventTap, event)

def AbsoluteMouseMove(posx,posy):
    event = Event(None, kCGEventMouseMoved, (posx, posy), 0)
    Post(event)

def AbsoluteMouseClick(posx,posy):
    AbsoluteMouseClickDown(posx,posy)
    AbsoluteMouseClickUp(posx,posy)

def AbsoluteMouseClickDown(posx, posy):
    event = Event(None, kCGEventLeftMouseDown, (posx, posy), 0)
    Post(event)

def AbsoluteMouseClickUp(posx, posy):
    event = Event(None, kCGEventLeftMouseUp, (posx, posy), 0)
    Post(event)

def AbsoluteMouseDrag(posx, posy):  #A Drag is a Move where the mouse key is held down
    event = Event(None, kCGEventLeftMouseDragged, (posx, posy), 0)
    Post(event)

def AbsoluteMouseRightClick(posx,posy):
    event = Event(None, kCGEventRightMouseDown, (posx, posy), 0)
    Post(event)
    event = Event(None, kCGEventRightMouseUp, (posx, posy), 0)
    Post(event)

def RelativeMouseScroll(x_movement, y_movement):  #Movements should be no larger than +- 10
    scrollWheelEvent = CGEventCreateScrollWheelEvent(
            None,  #No source
            kCGScrollEventUnitPixel,  #We are using pixel units
            2,  #Number of wheels(dimensions)
            y_movement,
            x_movement)
    CGEventPost(kCGHIDEventTap, scrollWheelEvent)


def GetDisplayWidth():
    return CGDisplayBounds(0).size.width

def GetDisplayHeight():
    return CGDisplayBounds(0).size.height


#A cursor that does commands based on absolute position (good for finger pointing)
class absolute_cursor(object):
    def __init__(self):
        self.x_max = GetDisplayWidth() - 1
        self.y_max = GetDisplayHeight() - 1
        self.left_button_pressed = False
        self.x = 0
        self.y = 0

    def move(self, posx, posy):  #Move to coordinates
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
        if self.left_button_pressed:  #We are dragging
            AbsoluteMouseDrag(self.x, self.y)
        else:  #We are not dragging
            AbsoluteMouseMove(self.x, self.y)

    def click(self, posx=None, posy=None):  #Click at coordinates (current coordinates by default)
        if posx == None:
            posx = self.x
        if posy == None:
            posy = self.y
        AbsoluteMouseClick(posx, posy)
    
    def set_left_button_pressed(self, boolean_button):  #Set the state of the left button
        if boolean_button == True:  #Pressed
            self.click_down()
        else:  #Not pressed
            self.click_up()
        
    def click_down(self, posx=None, posy=None):
        if posx == None:
            posx = self.x
        if posy == None:
            posy = self.y
        AbsoluteMouseClickDown(posx, posy)
        self.left_button_pressed = True

    def click_up(self, posx=None, posy=None):
        if posx == None:
            posx = self.x
        if posy == None:
            posy = self.y
        AbsoluteMouseClickUp(posx, posy)
        self.left_button_pressed = False

    def rightClick(self, posx=None, posy=None):
        if posx == None:
            posx = self.x
        if posy == None:
            posy = self.y
        AbsoluteMouseRightClick(posx, posy)

    def scroll(self, x_movement, y_movement):
        RelativeMouseScroll(x_movement, y_movement)


#Allows for relative movement instead of absolute movement. This implementation is not a "true" relative mouse,
#but is really just a relative wrapper for an absolute mouse. Not the best way to do it, but I need to 
#figure out how to send raw "mouse moved _this amount_" events. This class is (as of writing) untested.
#It's only here in case someone else wants to figure out how to do this properly on OS X.
#It's pretty easy on windows. There is a win32 API function for sending raw mouse data that can do this.
class relative_cursor(absolute_cursor):
    def __init__(self):
        absolute_cursor.__init__(self)

    def move(self, x_amt, y_amt):
        self.x = self.x + x_amt
        self.y = self.y + y_amt
        if self.x > self.x_max: 
            self.x = self.x_max
        if self.y > self.y_max: 
            self.y = self.y_max
        if self.x < 0.0: 
            self.x = 0.0
        if self.y < 0.0: 
            self.y = 0.0
        if self.left_button_pressed:  #We are dragging
            AbsoluteMouseDrag(self.x, self.y)
        else:  #We are not dragging
            AbsoluteMouseMove(self.x, self.y)