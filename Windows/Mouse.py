#William Yager
#Leap Python mouse controller POC


#Mouse functions in Windows
import ctypes
win32 = ctypes.windll.user32

def AbsoluteMouseMove(posx,posy):
    win32.SetCursorPos(int(posx),int(posy))
    #According to some guy on stackoverflow, it might be wise to replace
    #this with
    #win32.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE,
    #    int(x/SCREEN_WIDTH*65535.0), int(y/SCREEN_HEIGHT*65535.0))
    #but I have not tested this.

def AbsoluteMouseClick(posx,posy):
    #posx,posy ignored
    AbsoluteMouseClickDown(posx,posy)
    AbsoluteMouseClickUp(posx,posy)

def AbsoluteMouseClickDown(posx, posy):
    #posx,posy ignored
    win32.mouse_event(0x02,0,0,0,0)

def AbsoluteMouseClickUp(posx, posy):
    #posx,posy ignored
    win32.mouse_event(0x04,0,0,0,0)

def AbsoluteMouseDrag(posx, posy):  #Only relevant in OS X(?)
    AbsoluteMouseMove(posx, posy)

def AbsoluteMouseRightClick(posx,posy):
    #posx,posy ignored
    win32.mouse_event(0x08,0,0,0,0)
    win32.mouse_event(0x10,0,0,0,0)

def RelativeMouseScroll(x_movement, y_movement):  #Movements should be no larger than +- 10
    #Windows evidently doesn't really support sideways scrolling. 
    win32.mouse_event(0x0800,0,0,int(y_movement),0)

def GetDisplayWidth():
    return win32.GetSystemMetrics(0)

def GetDisplayHeight():
    return win32.GetSystemMetrics(1)


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
#I will be "actually" implementing this on Windows shortly. OSX TBD.
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