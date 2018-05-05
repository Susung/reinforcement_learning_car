import pymunk
from pygame.color import *

class Obstacles:

    def addObstacles(space):
        #obstacle definition
        obstacles = [
            {'x' : 200, 'y' : 350, 'r' : 100},
            {'x' : 700, 'y' : 200, 'r' : 125},
            {'x' : 530, 'y' : 430, 'r' : 35},
            {'x' : 80, 'y' : 150, 'r' : 10}
        ]

        #create obstacle physics objects
        for o in obstacles:
            o_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
            o_body.position = o['x'], o['y']
            o_shape = pymunk.Circle(o_body, o['r'])
            o_shape.color = THECOLORS["red"]
            o_shape.collision_type = 2
            space.add(o_body, o_shape)

    def addWalls(space):
        #if you want to add additional walls, copy the content below except that first is point 1, second is point 2, and third is thickness
        static = [
            pymunk.Segment(space.static_body, (50, 50), (50, 550), 5)
            ,pymunk.Segment(space.static_body, (50, 550), (650, 550), 5)
            ,pymunk.Segment(space.static_body, (650, 550), (650, 50), 5)
            ,pymunk.Segment(space.static_body, (50, 50), (650, 50), 5)
        ]

        #create wall objects
        for s in static:
            s.collision_type = 2
            s.color = THECOLORS["red"]
        space.add(static)
