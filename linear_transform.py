import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons

class Vector:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
    
    def __add__(self, other: "Vector"):
        return Vector(self.x + other.x, self.y + other.y)
    
    def __sub__(self, other: "Vector"):
        return Vector(self.x - other.x, self.y - other.y)

    def mag(self):
        return np.sqrt(self.x **  + self.y ** 2)

    def coord(self):
        return f"({self.x:.2f}, {self.y:.2f})"