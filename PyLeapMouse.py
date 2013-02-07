#William Yager
#Leap Python mouse controller POC

import Leap #Official Leap Library
import Mouse #OS-Specific mouse control functions
from PalmControl import Palm_Control_Listener #For palm-tilt based control
from FingerControl import Finger_Control_Listener #For finger-pointing control
import sys


def main():
    print "Use --finger (or no options) for pointer finger control,\nand --palm for palm control.\nRead README.md for more info."
    cursor = Mouse.cursor()#Create a cursor object, which controls the cursor position, clicking, etc

    listener = None; #I'm tired and can't think of a way to organize this segment nicely

    #Create a custom listener object which controls the cursor
    if len(sys.argv) == 1: #Finger pointer mode
        listener = Finger_Control_Listener(cursor)
        print "Using finger mode..."
    elif sys.argv[1].lower() == "--finger": #Also finger control mode
        listener = Finger_Control_Listener(cursor)
        print "Using finger mode..."
    elif sys.argv[1].lower() == "--palm": #Palm control mode
        listener = Palm_Control_Listener(cursor)
        print "Using palm mode..."
    else:
        print "Error parsing input options"
        exit(1)

    controller = Leap.Controller()#Get a Leap controller
    print "Adding Listener."
    controller.add_listener(listener)#Attach the listener


    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()
    # Remove the sample listener when done
    controller.remove_listener(listener)

main()