# game objects
# class Vector, Gameobject, World created by Zhang chenyang
# edited at 2018/04/27/19:04
import pygame
import math

class Vector(object):
    def __init__(self, x = 0.0, y = 0.0):
        self.x = x;
        self.y = y;
    def __str__(self):
        return "(%s, %s)"%(self.x, self.y)
    
    @classmethod
    def vector_of_points(cls, x, y):
        return cls(y[0] - x[0], y[1] - x[1])
    def __add__(self, vec):
        if type(vec) == type((1, 2)):
            return Vector(self.x + vec[0], self.y + vec[1])
        else:
            return Vector(self.x + vec.x, self.y + vec.y)
    def __sub__(self, vec):
        if type(vec) == type((1, 2)):
            return Vector(self.x - vec[0], self.y - vec[1])
        else:
            return Vector(self.x - vec.x, self.y - vec.y)
    def __mul__(self, scal):
        return Vector(self.x * scal, self.y * scal);
    def __truediv__(self, scal):
        return Vector(self.x / scal, self.y / scal)
    #reprogram the function of + - * /

    def __getitem__(self, ind):
        if ind == 0:
            return self.x
        elif ind == 1:
            return self.y
        else:
            pass
    #reprogram for indexing

    def get_magnitude(self):
        mag = math.sqrt(self.x * self.x + self.y * self.y);
        return mag
    #return the magnitude of the vector

    def get_normalized(self):
        mag = Vector.get_magnitude(self);
        if mag == 0:
            return Vector(0,0)
        else:
            nor = Vector(self.x / mag, self.y / mag);
            return nor
    #return the normalized vector( when the magnitude is 1)

    def get_angle(self):
        if self.x == 0:
            if self.y > 0:
                return pi/2
            else:
                return 3*pi/2
        else:
            ang = math.tan(self.y / self.x);
            if self.y < 0:
                return ang + pi
            else:
                return ang

    def v(self):
        return self.x, self.y

class Gameobj(object):
    def __init__(self, world, name, image):
        self.world = world
        self.name = name
        self.image = image
        self.image_actual = image
        self.direction = 0
        self.location = Vector(0, 0)
        self.destination = Vector(0, 0)
        self.old_destination = Vector(0, 0)
        self.speed = 0
        self.brain = None
        self.id = 0

    def print_obj_info(self):
        print('object details')
        print('world: ',self.world)
        print('name: ',self.name)
        print('image: ',self.image)
        print('image actual: ',self.image_actual)
        print('direction: ',self.direction)
        print('location: ',self.location)
        print('destination: ',self.destination)
        print('old destination: ',self.old_destination)
        print('speed: ',self.speed)
        print('brain: ',self.brain) 
        print('obj id: ',self.id)

    def help(self):
        print('world refers to a reference to the object, (useful or not unknown)')
        print('name is the name of the object')
        print('image is the image that contains all the image may be used for this object, (animation)')
        print('image_actual is the image that will be blit at this time')
        print('direction shows where the object face, now only has 2 directions, left and right')
        print('location is the current location')
        print('destination is the current destination')
        print('old destination is for lower usage of cpu for some functions')
        print('speed is the current speed')
        print('brain has not been developed yet')
        print('object id')

    def render(self,surface,loc):
        x, y = self.location.v()
        w, h = self.image.get_size()
        sw, sh = surface.get_size()
        if loc.x - w < x < loc.x + sw + w and loc.y - h < y < loc.y + sh + h:
            surface.blit(self.image_actual, (x - loc.x - w/2, y - loc.y - h/2))

    def move(self):
        if self.old_destination != self.destination:
            self.update_image()
        if self.destination != self.location:
            location_to_destination = self.destination - self.location
            nor = location_to_destination.get_normalized()
            velocity = nor * self.speed
            if location_to_destination.get_magnitude() > velocity.get_magnitude():
                self.location = self.location + velocity
            else:
                self.location = self.destination
            self.old_destination = self.destination
        # move the object controlled by speed, locaiton and destination

    def update_image(self):
        if self.destination.x < self.location.x:
            self.direction = 1
        else:
            self.direction = 0
        if self.direction == 0:
            self.image_actual = pygame.transform.flip(self.image, True, False)
        else:
            self.image_actual = self.image
        # flip the image, further functions (such as animations) please written here
        
        
    
class World(object):
    def __init__(self, surface, background):
        self.surface = surface
        self.background = background
        self.location = Vector(0, 0)
        self.object = []
        self.mouse_count = [0, 0, 0]
        self.mouse_pos = Vector(0, 0)

    def help(self):
        print('surface is the surface that all the image will be blitted on')
        print('background is the background image (map) of the game')
        print('location is the coordinate of left-up cornor of the screen on the background')
        print('object is a list of objects in the game')
        print('mouse_count counts the time a player hold his/her mouse')
        print('mouse_pos is the position of mouse')

    def move_surface(self):
        x,y = self.mouse_pos.v()
        if x > 750 and self.location.x < self.background.get_width() - self.surface.get_width():
            self.location = self.location + (15, 0)
            if self.location.x > self.background.get_width() - self.surface.get_width():
                self.location.x = self.background.get_width() - self.surface.get_width()
        elif x < 50 and self.location.x > 0:
            self.location = self.location - (15, 0)
            if self.location.x < 0:
                self.location.x = 0
        if y > 550 and self.location.y < self.background.get_height() - self.surface.get_height():
            self.location = self.location + (0, 15)
            if self.location.y > self.background.get_height() - self.surface.get_height():
                self.location.y = self.background.get_height() - self.surface.get_height()
        elif y < 50 and self.location.y > 0:
            self.location = self.location - (0, 15)
            if self.location.y < 0:
                self.location.y = 0
        # move the locaion of surface to display

    def render(self,a):
        self.move_surface()
        back = self.background.subsurface(self.location.v(), self.surface.get_size())
        self.surface.blit(back, (0, 0))
        self.set_destination(a)
        x,y = pygame.mouse.get_pos()
        self.mouse_pos = Vector(x, y)
        for o in self.object:
            o.render(self.surface, self.location)
            o.move()
        # display everything on the surface

    def set_destination(self,a):
        lm, mm, rm = pygame.mouse.get_pressed()
        if rm:
            self.mouse_count[2] += 1
        else:
            self.mouse_count[2] = 0
        if self.mouse_count[2] == 1:
            for o in self.object:
                o.destination = self.mouse_pos + self.location
        if 0 < self.mouse_count[2] < 10:
            for o in self.object:
                w, h = a.get_size()
                x, y = o.destination.v()
                sx, sy = self.location.v()
                self.surface.blit(a, (x - sx - w/2, y - sy - h/2))
        # set new destination of objects 
    
            


    
    

   
