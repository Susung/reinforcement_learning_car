import sys

import pygame
from pygame.locals import *
from pygame.color import *

import pymunk
from pymunk.vec2d import Vec2d
import pymunk.pygame_util

from obstacles import Obstacles
from player import Player
from nn import NN

def main():
    #changing the height might mess up the sonar, let me know if it does
    width, height = 1280,800

    #create game screen & physics
    pygame.init()
    running = True
    screen = pygame.display.set_mode((width,height))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 16)
    space = pymunk.Space()
    space.gravity = 0,0

    #create player (x pos, y pos, radius)
    player = Player(space, screen, 400, 400, 30)

    #collision handler callback
    def handle(arbiter, space, data):
        player.reset()
        player.collided = True
        return True
    handler = space.add_collision_handler(1,2)
    handler.begin = handle

    #dont omit
    draw_options = pymunk.pygame_util.DrawOptions(screen)

    #create obstacles
    Obstacles.addWalls(space)
    Obstacles.addObstacles(space)

    #create nn
    nn = NN()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT or \
                event.type == KEYDOWN and (event.key in [K_ESCAPE, K_q]):
                running = False
        screen.fill(pygame.color.THECOLORS["black"])

        #draw screen, update physics objects
        #physics objects must be updated & drawn first so that sonar dots can detect red color
        space.debug_draw(draw_options)
        pygame.display.flip()
        dist = player.drawSonar()#array of distance values, [left up right]
        screen.fill(pygame.color.THECOLORS["black"])

        #choose action
        action = nn.getAction()

        #do action
        player.rotate(0.01)

        #get reward
        reward = player.getReward()

        #update screen
        space.debug_draw(draw_options)
        pygame.display.flip()

        #get new dist
        dist = player.drawSonar()

        #train
        nn.getHighestQPrime()
        nn.train(123123)


        fps = 60
        dt = 1./fps
        space.step(dt)
        clock.tick(fps)
        input()

if __name__ == '__main__':
    sys.exit(main())
