class shape(object): 
    def __init__(self, coconut): 
        self.fruit = coconut 
     
    def printMyself(self): 
        print "I am a shape named {0}".format(self.fruit)

class polyCube(shape):
    def __init__(self, coconut, length, width, height):
        # Call the constructor of the inherited class
        super(polyCube, self).__init__(coconut)
 
        # Store the data associated with this inherited class
        self.length = length
        self.width = width
        self.height = height
 
    def printMyself(self):
        shape.printMyself(self)
        print 'I am also a cube with dimensions %.2f, %.2f, %.2f.' % (self.length, self.width, self.height)
 
 
class polySphere(shape):
    def __init__(self, coconut, radius):
        # Call the constructor of the inherited class
        super(polySphere, self).__init__(coconut)
 
        # Store the data associated with this inherited class
        self.radius = radius
 
    def printMyself(self):
        shape.printMyself(self)
        print 'I am also a sphere with a radius of %.2f.' % self.radius
 
cube1 = polyCube('firstCube', 2.0, 1.0, 3.0)
cube2 = polyCube('secondCube', 3.0, 3.0, 3.0)
sphere1 = polySphere('firstSphere', 2.2)
sphere2 = polySphere('secondSphere', 2.5)
shape1 = shape('myShape')
cube1.printMyself()
cube2.printMyself()
sphere1.printMyself()
sphere2.printMyself()






