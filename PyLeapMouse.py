#William Yager
#Leap Python mouse controller POC


import sys
if sys.platform == "darwin":
    import OSX.Leap as Leap
    import OSX.Mouse as Mouse
else:
    import Windows.Leap as Leap
    import Windows.Mouse as Mouse
from PalmControl import Palm_Control_Listener  #For palm-tilt based control
from FingerControl import Finger_Control_Listener  #For finger-pointing control


def main():
    print "Use --finger (or no options) for pointer finger control,\nand --palm for palm control.\nRead README.md for more info."

    listener = None;  #I'm tired and can't think of a way to organize this segment nicely

    #Create a custom listener object which controls the mouse
    if len(sys.argv) == 1:  #Finger pointer mode
        listener = Finger_Control_Listener(Mouse)
        print "Using finger mode..."
    elif sys.argv[1].lower() == "--finger":  #Also finger control mode
        listener = Finger_Control_Listener(Mouse)
        print "Using finger mode..."
    elif sys.argv[1].lower() == "--palm":  #Palm control mode
        listener = Palm_Control_Listener(Mouse)
        print "Using palm mode..."
    else:
        print "Error parsing input options"
        exit(1)

    controller = Leap.Controller()  #Get a Leap controller
    print "Adding Listener."
    controller.add_listener(listener)  #Attach the listener

    #Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()
    #Remove the sample listener when done
    controller.remove_listener(listener)

main()