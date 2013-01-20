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

class mouse_manager(object):
        def __init__(self):
            self.xcounter = 0.0
            self.ycounter = 0.0

        def add(self, (x, y)):
            self.xcounter = self.xcounter + x
            self.ycounter = self.ycounter + y
            split_x = math.modf(self.xcounter)#saves the float part (remainder) into the counter
            split_y = math.modf(self.ycounter)#and the int part into the movement
            self.xcounter = split_x[0]
            xmovement = int(split_x[1])
            self.ycounter = split_y[0]
            ymovement = int(split_y[1])
            return xmovement, ymovement   


class Listener(Leap.Listener): #The Listener that we attach to the controller
    def __init__(self, cursor):
        super(Listener, self).__init__() #Initialize like a normal listener
        #Initialize a bunch of stuff specific to this implementation
        self.screen = None
        self.screen_resolution = (0,0)
        self.cursor = cursor #The cursor object that lets us control mice cross-platform
        self.mouse_button_debouncer = debouncer(5) #A signal debouncer that ensures a reliable, non-jumpy click
        self.mouse_manager = mouse_manager()

    def on_init(self, controller):
        if controller.calibrated_screens.empty:
            print "Calibrate your Leap screen feature"
        self.screen = controller.calibrated_screens[0]
        self.screen_resolution = (self.screen.width_pixels, self.screen.height_pixels)

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
            rightmost_hand = None #We always have at least one "right hand"
            if len(frame.hands) < 2: #Just one hand
                rightmost_hand = frame.hands[0]
            else: #Multiple hands. We have a right AND a left
                rightmost_hand = max(frame.hands, key=lambda hand: hand.palm_position.x) #Get rightmost hand
                leftmost_hand = min(frame.hands, key=lambda hand: hand.palm_position.x) #Get leftmost hand
                self.do_gesture_recognition(leftmost_hand) #This may or may not run
            self.do_mouse_stuff(rightmost_hand) #This will always run when a hand is present
                       
    def do_mouse_stuff(self, hand): #Take a hand and use it as a mouse
         hand_normal_direction = Geometry.to_vector(hand.palm_normal)
         hand_direction = Geometry.to_vector(hand.direction)
         roll = hand_normal_direction.roll()
         pitch = hand_normal_direction.pitch()
         mouse_velocity = self.convert_angles_to_mouse_velocity(roll, pitch)
         movement = self.mouse_manager.add(mouse_velocity)
         self.cursor.move(self.cursor.x + movement[0], self.cursor.y + movement[1])

    def convert_angles_to_mouse_velocity(self, roll, pitch): #Angles are in radians
        x_movement = 5.0*math.copysign((4.0*math.sin(roll) + 2.0*roll)*math.sin(roll), roll)
        y_movement = 5.0*math.copysign((4.0*math.sin(pitch) + 2.0*pitch)*math.sin(pitch), pitch)
        return (x_movement, y_movement)

    def do_gesture_recognition(self, hand):
        if not hand.fingers.empty: #One or more open fingers on this hand
            self.mouse_button_debouncer.signal(True) #Tell the debouncer we got a positive sample
        else: #No open fingers
            self.mouse_button_debouncer.signal(False) #Tell the debouncer we got a negative sample
        if self.mouse_button_debouncer.state != self.cursor.left_button_pressed: #The cursor should be pressed/unpressed
            self.cursor.set_left_button_pressed(self.mouse_button_debouncer.state)



def sort_fingers_by_distance_from_screen(fingers):
    new_finger_list = [finger for finger in fingers] #Copy the list of fingers
    new_finger_list.sort(key=lambda x: x.tip_position.z) #Sort by increasing z
    return new_finger_list #Lower indices = closer to screen

def has_thumb(hand): #The level of accuracy with this function is surprisingly high
    if hand.fingers.empty: #We assume no thumbs
        return False
    distances = []
    palm_position = Geometry.to_vector(hand.palm_position)
    for finger in hand.fingers: #Make a list of all distances from the center of the palm
        finger_position = Geometry.to_vector(finger.tip_position)
        difference = finger_position - palm_position
        distances.append(difference.norm()) #Record the distance from the palm to the fingertip
    average = sum(distances)/len(distances)
    minimum = min(distances)
    if average - minimum > 20: #Check if the finger closest to the palm is more than 20mm closer than the average distance
        return True
    else:
        return False

def has_two_pointer_fingers(hand): #Checks if we are using two pointer fingers
    if len(hand.fingers) < 2: #Obviously not
        return False
    sorted_fingers = sort_fingers_by_distance_from_screen(hand.fingers)
    finger1_pos = Geometry.to_vector(sorted_fingers[0].tip_position)
    finger2_pos = Geometry.to_vector(sorted_fingers[1].tip_position)
    difference = finger1_pos - finger2_pos
    if difference.norm() < 40: #Check if the fingertips are close together
        return True
    else:
        return False

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

