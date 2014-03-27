#William Yager
#Leap Python mouse controller POC
#This file is for pointer-finger-based control (--finger and default)


import math
import sys
from leap import Leap, Mouse
from MiscFunctions import *


class Finger_Control_Listener(Leap.Listener):  #The Listener that we attach to the controller. This listener is for pointer finger movement
    def __init__(self, mouse, smooth_aggressiveness=8, smooth_falloff=1.3):
        super(Finger_Control_Listener, self).__init__()  #Initialize like a normal listener
        #Initialize a bunch of stuff specific to this implementation
        self.screen = None
        self.screen_resolution = (1920,1080)
        self.cursor = mouse.absolute_cursor()  #The cursor object that lets us control mice cross-platform
        self.mouse_position_smoother = mouse_position_smoother(smooth_aggressiveness, smooth_falloff) #Keeps the cursor from fidgeting
        self.mouse_button_debouncer = debouncer(5)  #A signal debouncer that ensures a reliable, non-jumpy click
        self.most_recent_pointer_finger_id = None  #This holds the ID of the most recently used pointing finger, to prevent annoying switching

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
        finger = frame.fingers.frontmost
        stabilizedPosition = finger.stabilized_tip_position
        interactionBox = frame.interaction_box
        normalizedPosition = interactionBox.normalize_point(stabilizedPosition)
        if finger.touch_zone > 0:
            finger_count = len(frame.fingers)
            if finger.touch_zone == 1:
                self.cursor.set_left_button_pressed(False)
                if finger_count < 5:
                    self.cursor.move(normalizedPosition.x * self.screen_resolution[0], self.screen_resolution[1] - normalizedPosition.y * self.screen_resolution[1])
                elif finger_count == 5:
                    finger_velocity = finger.tip_velocity
                    x_scroll = self.velocity_to_scroll_amount(finger_velocity.x)
                    y_scroll = self.velocity_to_scroll_amount(finger_velocity.y)
                    self.cursor.scroll(x_scroll, y_scroll)
                else:
                    print "Finger count: %s" % finger_count
            elif finger.touch_zone == 2:
                if finger_count == 1:
                    self.cursor.set_left_button_pressed(True)
                elif finger_count == 2:
                    self.cursor.set_left_button_pressed(True)
                    self.cursor.move(normalizedPosition.x * self.screen_resolution[0], self.screen_resolution[1] - normalizedPosition.y * self.screen_resolution[1])
        #if(finger.touch_distance > -0.3 and finger.touch_zone != Leap.Pointable.ZONE_NONE):
	    #self.cursor.set_left_button_pressed(False)
	    #self.cursor.move(normalizedPosition.x * self.screen_resolution[0], self.screen_resolution[1] - normalizedPosition.y * self.screen_resolution[1])
        #elif(finger.touch_distance <= -0.4):
            #self.cursor.set_left_button_pressed(True)
        #    print finger.touch_distance

    def do_scroll_stuff(self, hand):  #Take a hand and use it as a scroller
        fingers = hand.fingers  #The list of fingers on said hand
        if not fingers.is_empty:  #Make sure we have some fingers to work with
            sorted_fingers = sort_fingers_by_distance_from_screen(fingers)  #Prioritize fingers by distance from screen
            finger_velocity = sorted_fingers[0].tip_velocity  #Get the velocity of the forwardmost finger
            x_scroll = self.velocity_to_scroll_amount(finger_velocity.x)
            y_scroll = self.velocity_to_scroll_amount(finger_velocity.y)
            self.cursor.scroll(x_scroll, y_scroll)

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

    def do_mouse_stuff(self, hand):  #Take a hand and use it as a mouse
        fingers = hand.fingers  #The list of fingers on said hand
        if not fingers.is_empty:  #Make sure we have some fingers to work with
            pointer_finger = self.select_pointer_finger(fingers)  #Determine which finger to use
            
            try:
                intersection = self.screen.intersect(pointer_finger, True)  #Where the finger projection intersects with the screen
                if not math.isnan(intersection.x) and not math.isnan(intersection.y):  #If the finger intersects with the screen
                    x_coord = intersection.x * self.screen_resolution[0]  #x pixel of intersection
                    y_coord = (1.0 - intersection.y) * self.screen_resolution[1]  #y pixel of intersection
                    x_coord,y_coord = self.mouse_position_smoother.update((x_coord,y_coord)) #Smooth movement
                    self.cursor.move(x_coord,y_coord)  #Move the cursor
                    if has_thumb(hand):  #We've found a thumb!
                        self.mouse_button_debouncer.signal(True)  #We have detected a possible click. The debouncer ensures that we don't have click jitter
                    else:
                        self.mouse_button_debouncer.signal(False)  #Same idea as above (but opposite)

                    if self.cursor.left_button_pressed != self.mouse_button_debouncer.state:  #We need to push/unpush the cursor's button
                        self.cursor.set_left_button_pressed(self.mouse_button_debouncer.state)  #Set the cursor to click/not click
            except Exception as e:
                print e

    def select_pointer_finger(self, possible_fingers):  #Choose the best pointer finger
        sorted_fingers = sort_fingers_by_distance_from_screen(possible_fingers)  #Prioritize fingers by distance from screen
        if self.most_recent_pointer_finger_id != None:  #If we have a previous pointer finger in memory
             for finger in sorted_fingers:  #Look at all the fingers
                if finger.id == self.most_recent_pointer_finger_id:  #The previously used pointer finger is still in frame
                    return finger  #Keep using it
        #If we got this far, it means we don't have any previous pointer fingers OR we didn't find the most recently used pointer finger in the frame
        self.most_recent_pointer_finger_id = sorted_fingers[0].id  #This is the new pointer finger
        return sorted_fingers[0]
