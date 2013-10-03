#William Yager
#Leap Python mouse controller POC
import sys
from leap import Leap, Mouse
from PalmControl import Palm_Control_Listener  #For palm-tilt based control
from FingerControl import Finger_Control_Listener  #For finger-pointing control
from MotionControl import Motion_Control_Listener  #For motion control

def show_help():
    print "----------------------------------PyLeapMouse----------------------------------"
    print "Use --finger (or blank) for pointer finger control, and --palm for palm control."
    print "Set smooth aggressiveness (# samples) with \"--smooth-aggressiveness [# samples]\""
    print "Set smooth falloff with \"--smooth-falloff [% per sample]\""
    print "Read README.md for even more info.\n"

def main():
    if "-h" in sys.argv or "--help" in sys.argv:
        show_help()
        return

    print "----------------------------------PyLeapMouse----------------------------------"
    print "Use --finger (or blank) for pointer finger control, and --palm for palm control."
    print "Use -h or --help for more info.\n"

    #Default
    finger_mode = True
    palm_mode = False
    motion_mode = False
    smooth_aggressiveness = 8
    smooth_falloff = 1.3

    for i in range(0,len(sys.argv)):
        arg = sys.argv[i].lower()
        if "--palm" in arg:
            finger_mode = False
            palm_mode = True
            motion_mode = False
        if "--motion" in arg:
            finger_mode = False
            palm_mode = False
            motion_mode = True
        if "--smooth-falloff" in arg:
            smooth_falloff = float(sys.argv[i+1])
        if "--smooth-aggressiveness" in arg:
            smooth_aggressiveness = int(sys.argv[i+1])

    listener = None;  #I'm tired and can't think of a way to organize this segment nicely

    #Create a custom listener object which controls the mouse
    if finger_mode:  #Finger pointer mode
        listener = Finger_Control_Listener(Mouse, smooth_aggressiveness=smooth_aggressiveness, smooth_falloff=smooth_falloff)
        print "Using finger mode..."
    elif palm_mode:  #Palm control mode
        listener = Palm_Control_Listener(Mouse)
        print "Using palm mode..."
    elif motion_mode:  #Motion control mode
        listener = Motion_Control_Listener(Mouse)
        print "Using motion mode..."


    controller = Leap.Controller()  #Get a Leap controller
    controller.set_policy_flags(Leap.Controller.POLICY_BACKGROUND_FRAMES)
    print "Adding Listener."
    controller.add_listener(listener)  #Attach the listener

    #Keep this process running until Enter is pressed
    print "Press Enter to quit..."
    sys.stdin.readline()
    #Remove the sample listener when done
    controller.remove_listener(listener)

main()
