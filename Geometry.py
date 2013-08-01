#William Yager
#Leap Python mouse controller POC


import math
from leap import Leap


def to_vector(leap_vector):
    return vector(leap_vector.x, leap_vector.y, leap_vector.z)


class vector(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def __add__(self, other):
        return vector(self.x + other.x, self.y+other.y, self.z+other.z)
    def __sub__(self, other):
        return vector(self.x - other.x, self.y - other.y, self.z - other.z)
    def __mul__(self, other):  #The * operator is dot product
        return self.dot(other)
    def dot(self, other):
        return self.x*other.x + self.y*other.y+self.z*other.z
    def __pow__(self, other):  #The ** operator allows us to multiply a vector by a scalar
        return self.scalar_mult(other)
    def scalar_mult(self, other):
        return vector(self.x * other, self.y*other, self.z*other)
    def cross(self, other):
        x = self.y * other.z - other.y * self.z
        y = -(self.x * other.z - other.x * self.z)
        z = self.x * other.y - other.x * self.y
        return vector(x,y,z)
    def __mod__(self, other):  #The % operator is cross product
        return self.cross(other)
    def norm(self):  #Length of self
        return math.sqrt(1.0*self.dot(self))
    def distance(self, other):
        return (self-other).norm()  #Find difference and then the length of it
    def unit_vector(self):
        magnitude = self.norm()
        return vector(1.0*self.x/magnitude, 1.0*self.y/magnitude, 1.0*self.z/magnitude)
    def to_leap(self):
        return Leap.Vector(self.x, self.y, self.z)
    def pitch(self):
        return math.atan(1.0*self.z/self.y)
    def roll(self):
        return math.atan(1.0*self.x/self.y)
    def yaw(self):
        return math.atan(1.0*self.x/self.z)


class segment(object):
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
    #Shortest distance code based off of http://geomalgorithms.com/a07-_distance.html
    def min_distance_infinite(self, other):  #Return shortest distance between two lines
        u = self.point2 - self.point1
        v = other.point2 - other.point1
        w = self.point1 - other.point1
        a = u * u
        b = u * v
        c = v * v
        d = u * w
        e = v * w
        D = a * c - b * b
        sc = 0.0
        tc = 0.0
        basically_zero = .000000001
        if D < basically_zero:
            sc = 0.0
            if b > c:
                tc = d/b
            else:
                tc = e/c
        else:
            sc = (b * e - c * d) / D
            tc = (a * e - b * d) / D
        dP = w + u**sc - v**tc
        return dP.norm()
    def min_distance_finite(self, other):  #Return shortest distance between two segments
        u = self.point2 - self.point1
        v = other.point2 - other.point1
        w = self.point1 - other.point1
        a = u * u  #* here is cross product
        b = u * v
        c = v * v
        d = u * w
        e = v * w
        D = a * c - b * b
        sc = 0.0
        sN = 0.0
        sD = D
        tc = 0.0
        tN = 0.0
        tD = D
        basically_zero = .000000001
        if D < basically_zero:
            sN = 0.0
            sD = 1.0
            tN = e
            tD = c
        else:
            sN = (b*e - c*d)
            tN = (a*e - b*d)
            if sN < 0.0:
                sN = 0.0
                tN = e
                tD = c
            elif sN > sD:
                sN = sD
                tN = e + b
                tD = c
        if(tN < 0.0):
            tN = 0.0
            if(-d < 0.0):
                sN = 0.0
            elif (-d > a):
                sN = sD
            else:
                sN = -d
                sD = a
        elif tN > tD:
            tN = tD
            if (-d + b) < 0.0:
                sN = 0
            elif (-d + b) > a:
                sN = sD
            else:
                sN = (-d + b)
                sD = a
        if abs(sN) < basically_zero:
            sc = 0
        else:
            sc = sN / sD
        if abs(tN) < basically_zero:
            tc = 0.0
        else:
            tc = tN / tD
        dP = w + u**sc - v**tc  #I'm pretty sure dP is the actual vector linking the lines
        return dP.norm()


class line(segment):
    def __init__(self, point1, direction_vector):
        self.point1 = point1
        self.direction = direction_vector.unit_vector()
        self.point2 = point1 + self.direction


def angle_between_vectors(vector1, vector2):
    #cos(theta)=dot product / (|a|*|b|)
    top = vector1 * vector2  #* is dot product
    bottom = vector1.norm() * vector2.norm()
    angle = math.acos(top/bottom)
    return angle  #In radians
