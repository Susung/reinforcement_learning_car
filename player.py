import pymunk
import pygame
from pymunk.vec2d import Vec2d
from pygame.color import *
import math

class Player(object):
    def __init__(self, space, screen, x, y, r):
        #you may edit these values
        self.spread_distance = 10 #spread distance between sonar points
        self.num_sonar_points = 30 #number of sonar points

        #player physics object declaration
        self.player_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.player_body.position = x,y
        self.player_shape = pymunk.Circle(self.player_body, r)
        self.player_shape.color = THECOLORS["green"]
        self.player_shape.collision_type = 1

        self.screen = screen
        self.space = space
        self.space.add(self.player_body, self.player_shape)

        self.collided = False

    def reset(self):
        self.player_body.position = 400,400

    #reward function
    def getReward(self):
        if self.collided == True:
            self.collided = False
            return -500
        else:
            return 0

    def rotate(self, angle):
        self.player_body.angle += angle
        self.player_body.velocity = 100 * Vec2d(1, 0).rotated(self.player_body.angle)

    def drawSonar(self):
        readings = []
        x = self.player_body.position.x
        y = self.player_body.position.y
        angle = self.player_body.angle
        # Make our arms.
        arm_left = self.make_sonar_arm(x, y)
        arm_middle = arm_left
        arm_right = arm_left

        # Rotate them and get readings.
        readings.append(self.get_arm_distance(arm_left, x, y, angle, 0.75))
        readings.append(self.get_arm_distance(arm_middle, x, y, angle, 0))
        readings.append(self.get_arm_distance(arm_right, x, y, angle, -0.75))

        pygame.display.update()

        return readings

    def make_sonar_arm(self, x, y):
        spread = self.spread_distance  # Default spread.
        distance = 25  # Gap before first sensor.
        arm_points = []
        for i in range(1, self.num_sonar_points):
            arm_points.append((distance + x + (spread * i), y))

        return arm_points

    def get_arm_distance(self, arm, x, y, angle, offset):
        # Used to count the distance.
        i = 0

        # Look at each point and see if we've hit something.
        for point in arm:
            i += 1
            rotated_p = self.get_rotated_point(x, y, point[0], point[1], angle + offset)
            if rotated_p[0] <= 0 or rotated_p[1] <= 0 or rotated_p[0] >= 1280 or rotated_p[1] >= 800:
                return i  # Sensor is off the screen.
            obs = self.screen.get_at(rotated_p)
            if obs == THECOLORS['red']:
                return i
            pygame.draw.circle(self.screen, (255, 255, 255), (rotated_p), 2)
        return i

    def get_rotated_point(self, x1, y1, x2, y2, radians):
        x = x1 + math.cos(radians) * math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        y = y1 + math.sin(radians) * math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
        y = -y + 800#pymunk coordinates and pygame coordinates differ
        return int(x), int(y)
