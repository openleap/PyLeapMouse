#William Yager
#Leap Python mouse controller POC

import Leap
import Mouse
import LeapFunctions
import time
import sys


def main():
    cursor = Mouse.cursor()#Create a cursor object, which controls the cursor position, clicking, etc

    listener = LeapFunctions.Listener(cursor)#Create a custom listener object which controls the cursor

    controller = Leap.Controller()#Get a Leap controller
    print "Adding Listener."
    controller.add_listener(listener)#Attach the listener


    # Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()
    # Remove the sample listener when done
    controller.remove_listener(listener)

main()