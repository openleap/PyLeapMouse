#William Yager
#Leap Python mouse controller POC
#This file is for palm-tilt and gesture-based control (--palm)


import math
from leap import Leap, Mouse
import Geometry
from MiscFunctions import *


class Palm_Control_Listener(Leap.Listener):  #The Listener that we attach to the controller. This listener is for palm tilt movement
    def __init__(self, mouse):
        super(Palm_Control_Listener, self).__init__()  #Initialize like a normal listener
        #Initialize a bunch of stuff specific to this implementation
        self.cursor = mouse.relative_cursor()  #The cursor object that lets us control mice cross-platform
        self.gesture_debouncer = n_state_debouncer(5,3)  #A signal debouncer that ensures a reliable, non-jumpy gesture detection

    def on_init(self, controller):
        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame()  #Grab the latest 3D data
        if not frame.hands.is_empty:  #Make sure we have some hands to work with
            rightmost_hand = None  #We always have at least one "right hand"
            if len(frame.hands) < 2:  #Just one hand
                self.do_mouse_stuff(frame.hands[0])  #If there's only one hand, we assume it's to be used for mouse control
            else:  #Multiple hands. We have a right AND a left
                rightmost_hand = max(frame.hands, key=lambda hand: hand.palm_position.x)  #Get rightmost hand
                leftmost_hand = min(frame.hands, key=lambda hand: hand.palm_position.x)  #Get leftmost hand
                self.do_gesture_recognition(leftmost_hand, rightmost_hand)  #This will run with >1 hands in frame

    def do_mouse_stuff(self, hand):  #Take a hand and use it as a mouse
         hand_normal_direction = Geometry.to_vector(hand.palm_normal)
         hand_direction = Geometry.to_vector(hand.direction)
         roll = hand_normal_direction.roll()
         pitch = hand_normal_direction.pitch()
         mouse_velocity = self.convert_angles_to_mouse_velocity(roll, pitch)
         self.cursor.move(mouse_velocity[0], mouse_velocity[1])

    #The gesture hand signals what action to do,
    #The mouse hand gives extra data (if applicable)
    #Like scroll speed/direction
    def do_gesture_recognition(self, gesture_hand, mouse_hand):
        if len(gesture_hand.fingers) == 2:  #Two open fingers on gesture hand (scroll mode)
            self.gesture_debouncer.signal(2)  #Tell the debouncer we've seen this gesture
        elif len(gesture_hand.fingers) == 1:  #One open finger on gesture hand (click down)
            self.gesture_debouncer.signal(1)
        else:  #No open fingers or 3+ open fingers (click up/no action)
            self.gesture_debouncer.signal(0)
        #Now that we've told the debouncer what we *think* the current gesture is, we must act
        #On what the debouncer thinks the gesture is
        if self.gesture_debouncer.state == 2:  #Scroll mode
            y_scroll_amount = self.velocity_to_scroll_amount(mouse_hand.palm_velocity.y)  #Mouse hand controls scroll amount
            x_scroll_amount = self.velocity_to_scroll_amount(mouse_hand.palm_velocity.x)
            self.cursor.scroll(x_scroll_amount, y_scroll_amount)
        elif self.gesture_debouncer.state == 1:  #Click/drag mode
            if not self.cursor.left_button_pressed: self.cursor.click_down()  #Click down (if needed)
            self.do_mouse_stuff(mouse_hand)  #We may want to click and drag
        elif self.gesture_debouncer.state == 0:  #Move cursor mode
            if self.cursor.left_button_pressed: self.cursor.click_up()  #Click up (if needed)
            self.do_mouse_stuff(mouse_hand)

    def velocity_to_scroll_amount(self, velocity):  #Converts a finger velocity to a scroll velocity
        #The following algorithm was designed to reflect what I think is a comfortable
        #Scrolling behavior.
        vel = velocity  #Save to a shorter variable
        vel = vel + math.copysign(300, vel)  #Add/subtract 300 to velocity
        vel = vel / 150
        vel = vel ** 3  #Cube vel
        vel = vel / 8
        vel = vel * -1  #Negate direction, depending on how you like to scroll
        return vel

    def convert_angles_to_mouse_velocity(self, roll, pitch):  #Angles are in radians
        x_movement = 5.0*math.copysign((4.0*math.sin(roll) + 2.0*roll)*math.sin(roll), roll)
        y_movement = 5.0*math.copysign((4.0*math.sin(pitch) + 2.0*pitch)*math.sin(pitch), pitch)
        return (x_movement, y_movement)
