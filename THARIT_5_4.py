import math

class Cuboid:
    def __init__(self, width, height, depth):
        self.width = width
        self.height = height
        self.depth = depth
        
    def volume(self):
        v = self.width * self.height * self.depth
        return v
    
    def surface_area(self):
        a = 2*(self.width*self.height + self.width*self.depth + self.height*self.depth)
        return a
    
    def diagonal(self):
        d = math.sqrt(pow(self.width,2) + pow(self.height,2) + pow(self.depth,2))
        return d
    # pass

shape1 = Cuboid(width=6, height=4, depth=5)
assert shape1.volume() == 120
assert shape1.surface_area() == 148
assert shape1.diagonal() == math.sqrt(77)

shape2 = Cuboid(width=3, height=3, depth=2)
assert shape2.volume() == 18
assert shape2.surface_area() == 42
assert shape2.diagonal() == math.sqrt(22)