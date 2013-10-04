import sys, os, ConfigParser
from leap import Leap, CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class Motion_Control_Listener(Leap.Listener):  #The Listener that we attach to the controller. This listener is for motion control
    def __init__(self, mouse):
        super(Motion_Control_Listener, self).__init__()  #Initialize like a normal listener

    def on_init(self, controller):
        self.read_config() #Read the config file
        self.init_list_of_commands() #Initialize the list of recognized commands

        print "Initialized"

    def read_config(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("./commands.ini")

    def init_list_of_commands(self):
        #Initialize all commands an put it in an array
        self.commands = [
                ScreentapCommand(),
                SwiperightCommand(),
                SwipeleftCommand(),
                CounterclockwiseCommand(),
                ClockwiseCommand(),
                KeytapCommand()
        ]

    def on_connect(self, controller):
        #Enable all gestures
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()  #Grab the latest 3D data
        if not frame.hands.is_empty:  #Make sure we have some hands to work with
            for command in self.commands: #Loop all enabled commands
                if(command.applicable(frame)): #If the motion associated to the command is triggered
                    self.execute(frame, command.name) #Execute the command

    def execute(self, frame, command_name):
        number_for_fingers = self.get_fingers_code(frame) #Get a text correspond to the number of fingers
        if(self.config.has_option(command_name, number_for_fingers)): #If the command if finded in the config file
            syscommand = self.config.get(command_name, number_for_fingers) #Prepare the command
            print(syscommand)
            os.system(syscommand) #Execute the command

    def get_fingers_code(self, frame):
        return "%dfinger" % len(frame.fingers)


class ScreentapCommand():
    def __init__(self):
        self.name = "screentap"
        #The name of the command in the config file

    #Return true if the command is applicable
    def applicable(self, frame):
        return(frame.gestures()[0].type == Leap.Gesture.TYPE_SCREEN_TAP)

class KeytapCommand():
    def __init__(self):
        self.name = "keytap" #The name of the command in the config file

    #Return true if the command is applicable
    def applicable(self, frame):
        return(frame.gestures()[0].type == Leap.Gesture.TYPE_KEY_TAP)

class SwiperightCommand():
    def __init__(self):
        self.name = "swiperight" #The name of the command in the config file

    #Return true if the command is applicable
    def applicable(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])
        return(swipe.state == Leap.Gesture.STATE_STOP
                and swipe.type == Leap.Gesture.TYPE_SWIPE
                and swipe.direction[0] < 0)

class SwipeleftCommand():
    def __init__(self):
        self.name = "swipeleft" #The name of the command in the config file

    #Return true if the command is applicable
    def applicable(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])
        return(swipe.state == Leap.Gesture.STATE_STOP
                and swipe.type == Leap.Gesture.TYPE_SWIPE
                and swipe.direction[0] > 0)

class ClockwiseCommand():
    def __init__(self):
        self.name = "clockwise" #The name of the command in the config file

    #Return true if the command is applicable
    def applicable(self, frame):
        circle = CircleGesture(frame.gestures()[0])
        return(circle.state == Leap.Gesture.STATE_STOP and
                circle.type == Leap.Gesture.TYPE_CIRCLE and
                circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4)

class CounterclockwiseCommand():
    def __init__(self):
        self.name = "counterclockwise" #The name of the command in the config file

    #Return true if the command is applicable
    def applicable(self, frame):
        circle = CircleGesture(frame.gestures()[0])
        return(circle.state == Leap.Gesture.STATE_STOP and
                circle.type == Leap.Gesture.TYPE_CIRCLE and
                circle.pointable.direction.angle_to(circle.normal) > Leap.PI/4)
