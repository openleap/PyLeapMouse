#William Yager
#Leap Python mouse controller POC
#This file contains miscellaneous functions that are not interface-specific


import math
import sys
if sys.platform == "darwin":
    import OSX.Leap as Leap
else:
    import Windows.Leap as Leap
import Geometry


class debouncer(object):  #Takes a binary "signal" and debounces it.
    def __init__(self, debounce_time):  #Takes as an argument the number of opposite samples it needs to debounce.
        self.opposite_counter = 0  #Number of contrary samples vs agreeing samples.
        self.state = False  #Default state.
        self.debounce_time = debounce_time  #Number of samples to change states (debouncing threshold).

    def signal(self, value):  #Update the signal.
        if value != self.state:  #We are receiving a different signal than what we have been.
            self.opposite_counter = self.opposite_counter + 1
        else:  #We are recieving the same signal that we have been
            self.opposite_counter = self.opposite_counter - 1

        if self.opposite_counter < 0: self.opposite_counter = 0
        if self.opposite_counter > self.debounce_time: self.opposite_counter = self.debounce_time
        #No sense building up negative or huge numbers of agreeing/contrary samples

        if self.opposite_counter >= self.debounce_time:  #We have seen a lot of evidence that our internal state is wrong
            self.state = not self.state  #Change internal state
            self.opposite_counter = 0  #We reset the number of contrary samples
        return self.state  #Return the debounced signal (may help keep code cleaner)


class n_state_debouncer(object):  #A signal debouncer that has `number_of_states` states
    def __init__(self, debounce_time, number_of_states):
        self.state_counters = [0]*number_of_states  #One counter for every state
        self.state = 0  #Default state
        self.debounce_time = debounce_time

    def signal(self, signal_value):
        if signal_value < 0 or signal_value >= len(self.state_counters):  #Check for invalid state
            raise Exception("Invalid state. Out of bounds.")
            return
        self.state_counters[signal_value] = self.state_counters[signal_value] + 1  #Increment signalled state
        for i in range(0,len(self.state_counters)):
            if i is not signal_value: self.state_counters[i] = self.state_counters[i] - 1  #Decrement all others
        for i in range(0,len(self.state_counters)):  #Fix bounds and check for a confirmed state change
            if self.state_counters[i] < 0: self.state_counters[i] = 0
            if self.state_counters[i] >= self.debounce_time:  #Confirmed new state at index i
                self.state_counters[i] = self.debounce_time
                for x in range(0,len(self.state_counters)): 
                    if x is not i: self.state_counters[x] = 0  #Zero out all other state counters
                self.state = i  #Save the new state
        return self.state


class mouse_manager(object):  #The original intent of this object was to allow for smoother mouse movements. However, I hope to eliminate it soon.
    def __init__(self):
        self.xcounter = 0.0
        self.ycounter = 0.0

    #Returns the integer part of the mouse movement, stores the leftover float part for later
    def add(self, (x, y)):
        self.xcounter = self.xcounter + x
        self.ycounter = self.ycounter + y
        split_x = math.modf(self.xcounter)  #Saves the float part (remainder) into the counter
        split_y = math.modf(self.ycounter)  #And the int part into the movement
        self.xcounter = split_x[0]
        xmovement = int(split_x[1])
        self.ycounter = split_y[0]
        ymovement = int(split_y[1])
        return xmovement, ymovement  


def sort_fingers_by_distance_from_screen(fingers):
    new_finger_list = [finger for finger in fingers]  #Copy the list of fingers
    new_finger_list.sort(key=lambda x: x.tip_position.z)  #Sort by increasing z
    return new_finger_list  #Lower indices = closer to screen


def has_thumb(hand):  #The level of accuracy with this function is surprisingly high
    if hand.fingers.empty:  #We assume no thumbs
        return False
    distances = []
    palm_position = Geometry.to_vector(hand.palm_position)
    for finger in hand.fingers:  #Make a list of all distances from the center of the palm
        finger_position = Geometry.to_vector(finger.tip_position)
        difference = finger_position - palm_position
        distances.append(difference.norm())  #Record the distance from the palm to the fingertip
    average = sum(distances)/len(distances)
    minimum = min(distances)
    if average - minimum > 20:  #Check if the finger closest to the palm is more than 20mm closer than the average distance
        #Note: I have recieved feedback that a smaller value may work better. I do have big hands, however
        return True
    else:
        return False


def has_two_pointer_fingers(hand):  #Checks if we are using two pointer fingers
    if len(hand.fingers) < 2:  #Obviously not
        return False
    sorted_fingers = sort_fingers_by_distance_from_screen(hand.fingers)
    finger1_pos = Geometry.to_vector(sorted_fingers[0].tip_position)
    finger2_pos = Geometry.to_vector(sorted_fingers[1].tip_position)
    difference = finger1_pos - finger2_pos
    if difference.norm() < 40:  #Check if the fingertips are close together
        return True
    else:
        return False


#Check if the vectors of length 'vector_length' shooting out of a pair of fingers intersect within tolerance 'tolerance'
def finger_vectors_intersect(finger1, finger2, vector_length, tolerance):
    #Take Leap Finger objects and produce two line segment objects
    finger_1_location = Geometry.to_vector(finger1.tip_position)
    finger_1_direction = Geometry.to_vector(finger1.direction)
    finger_1_vector = finger_1_direction.unit_vector() ** vector_length;  #** is scalar mult
    finger_1_endpoint = finger_1_vector + finger_1_location
    finger_1_segment = Geometry.segment(finger_1_location, finger_1_endpoint)

    finger_2_location = Geometry.to_vector(finger2.tip_position)
    finger_2_direction = Geometry.to_vector(finger2.direction)
    finger_2_vector = finger_2_direction.unit_vector() ** vector_length;  #** is scalar mult
    finger_2_endpoint = finger_2_vector + finger_2_location
    finger_2_segment = Geometry.segment(finger_2_location, finger_2_endpoint)

    minimum_distance = finger_1_segment.min_distance_finite(finger_2_segment)

    if minimum_distance <= tolerance:
        return True
    return False
