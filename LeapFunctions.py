#William Yager
#Leap Python mouse controller POC

import Leap
import Geometry
import math

class debouncer(object): #Takes a "signal" and debounces it.
    def __init__(self, debounce_time): #Takes as an argument the number of opposite samples it needs to debounce.
        self.opposite_counter = 0 #Number of contrary samples vs agreeing samples.
        self.state = False #Default state.
        self.debounce_time = debounce_time #Number of samples to change states (debouncing threshold)

    def signal(self, value): #Update the signal.
        if value != self.state: #we are receiving a different signal than what we have been
            self.opposite_counter = self.opposite_counter + 1
        else: #we are recieving the same signal that we have been
            self.opposite_counter = self.opposite_counter - 1

        if self.opposite_counter < 0: self.opposite_counter = 0
        if self.opposite_counter > self.debounce_time: self.opposite_counter = self.debounce_time
        #no sense building up negative or huge numbers of agreeing/contrary samples

        if self.opposite_counter >= self.debounce_time: #we have seen a lot of evidence that our internal state is wrong
            self.state = not self.state #change internal state
            self.opposite_counter = 0 #we reset the number of contrary samples
        return self.state #return the debounced signal (may help keep code cleaner)

class Listener(Leap.Listener): #The Listener that we attach to the controller
    def __init__(self, cursor):
        super(Listener, self).__init__() #Initialize like a normal listener
        #Initialize a bunch of stuff specific to this implementation
        self.screen = None
        self.width = 0
        self.height = 0
        self.cursor = cursor #The cursor object that lets us control mice cross-platform
        self.mouse_button_debouncer = debouncer(5) #A signal debouncer that ensures a reliable, non-jumpy click

    def on_init(self, controller):
        if controller.calibrated_screens.empty:
            print "Calibrate your Leap screen feature"
        self.screen = controller.calibrated_screens[0]
        self.width = self.screen.width_pixels
        self.height = self.screen.height_pixels

        print "Initialized"

    def on_connect(self, controller):
        print "Connected"

    def on_disconnect(self, controller):
        print "Disconnected"

    def on_exit(self, controller):
        print "Exited"

    def on_frame(self, controller):
        frame = controller.frame() #Grab the latest 3D data
        if not frame.hands.empty: #Make sure we have some hands to work with
            hand = frame.hands[0] #The first hand
            fingers = hand.fingers #The list of fingers on said hand
            if not fingers.empty: #Make sure we have some fingers to work with
                sorted_fingers = sort_fingers_by_distance_from_screen(fingers) #Prioritize fingers by distance from screen
                pointer_finger = sorted_fingers[0] #Finger closest to screen
                intersection = self.screen.intersect(pointer_finger, True) #Where the finger projection intersects with the screen
                if not math.isnan(intersection.x) and not math.isnan(intersection.y): #If the finger intersects with the screen
                    x_coord = intersection.x * self.width #x pixel of intersection
                    y_coord = (1.0 - intersection.y) * self.height #y pixel of intersection
                    #print x_coord, y_coord #For debugging
                    self.cursor.move(x_coord,y_coord) #Move the cursor
                    if len(hand.fingers) > 1: #We've found a thumb!
                        #print "second finger detected"
                        #print '+'
                        self.mouse_button_debouncer.signal(True) #We have detected a possible click. The debouncer ensures that we don't have click jitter
                    else:
                        #print '-'
                        self.mouse_button_debouncer.signal(False) #Same as above

                    if self.cursor.left_button_pressed != self.mouse_button_debouncer.state: #We need to push/unpush the cursor's button
                        #print "clicked:"
                        #print self.mouse_button_debouncer.state
                        self.cursor.set_left_button_pressed(self.mouse_button_debouncer.state) #Set the cursor to click/not click

def sort_fingers_by_distance_from_screen(fingers):
    new_finger_list = [finger for finger in fingers] #Copy the list of fingers
    new_finger_list.sort(key=lambda x: x.tip_position.z) #Sort by increasing z
    return new_finger_list #Lower indices = closer to screen

#Check if the vectors of length 'vector_length' shooting out of a pair of fingers intersect within tolerance 'tolerance'
def finger_vectors_intersect(finger1, finger2, vector_length, tolerance):
    #Take Leap Finger objects and produce two line segment objects
    finger_1_location = Geometry.to_vector(finger1.tip_position)
    finger_1_direction = Geometry.to_vector(finger1.direction)
    finger_1_vector = finger_1_direction.unit_vector() ** vector_length;#** is scalar mult
    finger_1_endpoint = finger_1_vector + finger_1_location
    finger_1_segment = Geometry.segment(finger_1_location, finger_1_endpoint)

    finger_2_location = Geometry.to_vector(finger2.tip_position)
    finger_2_direction = Geometry.to_vector(finger2.direction)
    finger_2_vector = finger_2_direction.unit_vector() ** vector_length;#** is scalar mult
    finger_2_endpoint = finger_2_vector + finger_2_location
    finger_2_segment = Geometry.segment(finger_2_location, finger_2_endpoint)

    minimum_distance = finger_1_segment.min_distance_finite(finger_2_segment)

    if minimum_distance <= tolerance:
        return True
    return False

