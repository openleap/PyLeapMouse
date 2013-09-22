import sys, os, ConfigParser
from leap import Leap, CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class Motion_Control_Listener(Leap.Listener):  #The Listener that we attach to the controller. This listener is for motion control
    def __init__(self, mouse):
        super(Motion_Control_Listener, self).__init__()  #Initialize like a normal listener

    def on_init(self, controller):
        self.init_list_of_commands()

        print "Initialized"

    def init_list_of_commands(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read("./commands.ini")

        self.commands = [
                ScreentapCommand(),
                SwiperightCommand(),
                SwipeleftCommand(),
                CounterclockwiseCommand(),
                ClockwiseCommand(),
                KeytapCommand()
        ]

    def on_connect(self, controller):
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
        if not frame.hands.empty:  #Make sure we have some hands to work with
            for command in self.commands:
                if(command.applicable(frame)):
                    self.execute(frame, command.name)

    def execute(self, frame, command_name):
        number_for_fingers = self.get_fingers_code(frame)
        if(self.config.has_option(command_name, number_for_fingers)):
            syscommand = self.config.get(command_name, number_for_fingers)
            print(syscommand)
            os.system(syscommand)

    def get_fingers_code(self, frame):
        return "%dfinger" % len(frame.fingers)

class ScreentapCommand():
    def __init__(self):
        self.name = "screentap"

    def applicable(self, frame):
        return(frame.gestures()[0].type == Leap.Gesture.TYPE_SCREEN_TAP)

class KeytapCommand():
    def __init__(self):
        self.name = "keytap"

    def applicable(self, frame):
        return(frame.gestures()[0].type == Leap.Gesture.TYPE_KEY_TAP)

class SwiperightCommand():
    def __init__(self):
        self.name = "swiperight"

    def applicable(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])
        return(swipe.state == Leap.Gesture.STATE_STOP
                and swipe.type == Leap.Gesture.TYPE_SWIPE
                and swipe.direction[0] < 0)

class SwipeleftCommand():
    def __init__(self):
        self.name = "swipeleft"

    def applicable(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])
        return(swipe.state == Leap.Gesture.STATE_STOP
                and swipe.type == Leap.Gesture.TYPE_SWIPE
                and swipe.direction[0] > 0)

class ClockwiseCommand():
    def __init__(self):
        self.name = "clockwise"

    def applicable(self, frame):
        circle = CircleGesture(frame.gestures()[0])
        return(circle.state == Leap.Gesture.STATE_STOP and
                circle.type == Leap.Gesture.TYPE_CIRCLE and
                circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4)

class CounterclockwiseCommand():
    def __init__(self):
        self.name = "counterclockwise"

    def applicable(self, frame):
        circle = CircleGesture(frame.gestures()[0])
        return(circle.state == Leap.Gesture.STATE_STOP and
                circle.type == Leap.Gesture.TYPE_CIRCLE and
                circle.pointable.direction.angle_to(circle.normal) > Leap.PI/4)
