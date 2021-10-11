# CENG 487 Assignment1 by
# Erdem Taylan
# StudentId: 240206013
# 11 2020

import math

#Vector class for initializing vector and vector operations
class Vec3d:

    #initialization of a vector, and its element
    def __init__(self, x: float, y: float, z: float, w: float = 0): #w is 0 to be ineffective
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    #adding operation for 2 vector
    def __add__(self, other): 
        return Vec3d(self.x + other.x, self.y + other.y, self.z + other.z)

    #subtraction operation for 2 vector
    def __sub__(self, other):
        return Vec3d(self.x - other.x, self.y - other.y, self.z - other.z)

    #product of a scalar and vector
    def __mul__(self, other: float):
        return Vec3d(self.x * other, self.y * other, self.z * other)

    #division of vector by a scalar
    def __truediv__(self, other: float):
        return self * other ** -1

    #magnitude of a vector
    def abs(self):
        return math.sqrt(self.dot(self))

    #string representation of a matrix
    def __str__(self):
        return f"({self.x}, {self.y}, {self.z}, {self.w})"

    #printable representation of the object
    def __repr__(self):
        return f"{str(self)}"

    #dot product
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z + self.w * other.w

    #cross Product
    def cross(self, vector):
        return Vec3d(self.y * vector.z - self.z * vector.y, self.z * vector.x - self.x * vector.z,
                     self.x * vector.y - self.y * vector.x)

    #projection of a vector
    def projection(self, other):
        return other * (self.dot(other) / other.dot(other)) 

    #angle between two vectors
    def angle(self, other):
        return math.acos(self.dot(other) / (self.abs * other.abs)) 
