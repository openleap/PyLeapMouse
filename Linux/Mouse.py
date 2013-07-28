from pymouse import PyMouse
mouse = PyMouse()

def AbsoluteMouseMove(posx,posy):
    print 'move to', posx, posy
    mouse.move(int(posx), int(posy))

def AbsoluteMouseClick(posx,posy):
    print 'click on ', posx, posy
    mouse.click(posx, posy)

def AbsoluteMouseClickDown(posx, posy):
    print 'left button down'
    mouse.press(posx, posy)

def AbsoluteMouseClickUp(posx, posy):
    print 'left button up'
    mouse.release(posx, posy)

def AbsoluteMouseDrag(posx, posy):  #Only relevant in OS X(?)
    mouse.move(posx, posy)

def AbsoluteMouseRightClick(posx,posy):
    mouse.click(posx, posy, button=2)

def AbsoluteMouseScroll(posx, posy, up=True):  #PyUserInput doesn't appear to support relative scrolling
    if up is True:
        mouse.click(posx, posy, button=4)
    elif up is False:
        mouse.click(posx, posy, button=5)
    #When PyUserInput > 0.1.5 is released, the following will work:
    #mouse.scroll(posx, posy, up)

def GetDisplayWidth():
    return mouse.screen_size()[0]

def GetDisplayHeight():
    return mouse.screen_size()[1]


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
        posx = self.x
        posy = self.y
        up = False
        if y_movement < 0:
            up = True
        AbsoluteMouseScroll(posx, posy, up)


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
