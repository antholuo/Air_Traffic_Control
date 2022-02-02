# SpaceRyde Internship Coding Challenge
# setup.py
# Februry 2022
# Anthony Luo, a26luo@uwaterloo.ca / antholuo@gmail.com

"""What this file does:
- creates pygame window
- calculates holding areas with a buffer zone around runways.
- randomly spawns planes
"""

import pygame
import sys

from consts import *

# some colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def calculate_landing_area():
    """
    Returns a list of rects.
    Note that rects are returned with left top width height...
    :return:
    """
    rects = []


    # even rects to the right, odd rects to the left
    i = 0;
    tog = "l";
    while i < NUM_RUNWAYS:
        if tog == "l":
            left = - ((i+1)*RUNWAY_WIDTH + i*RUNWAY_SPACING + RUNWAY_SPACING / 2)
            right = - ((i)*RUNWAY_WIDTH + i*RUNWAY_SPACING + RUNWAY_SPACING / 2)
            top = RUNWAY_LENGTH / 2
            bottom = - (RUNWAY_LENGTH / 2)

            rects.append((left, top, RUNWAY_WIDTH, RUNWAY_LENGTH))
        if tog == "r":
            left = (i) * RUNWAY_WIDTH + i * RUNWAY_SPACING + RUNWAY_SPACING / 2
            right = (i+1) * RUNWAY_WIDTH + i * RUNWAY_SPACING + RUNWAY_SPACING / 2
            top = RUNWAY_LENGTH / 2
            bottom = - (RUNWAY_LENGTH / 2)

            rects.append((left, top, RUNWAY_WIDTH, RUNWAY_LENGTH))

        i+=1

    return rects

def blitmap(disp,map, maprect):
    disp.mapsurface = pygame.transform.smoothscale(map, maprect.size)
    disp.fill(0)
    disp.blit(disp.mapsurface, maprect)

def draw():
    SCALING = 0.05 # each pixel = 50 meters

    pygame.init()
    clk = pygame.time.Clock()
    SW, SH = 22000*SCALING, 22000*SCALING # original meta is 1 pixel = 1 meter, we are thus drawing 20km diameter with 1km buffer on each side
    disp = pygame.display.set_mode((SW, SH))
    pygame.display.set_caption("ATC Controller")

    disp.fill(BLACK)

    # Draw ATC Control area
    pygame.draw.circle(disp, BLUE, (SW / 2, SH / 2), 10000 * SCALING, 1)

    # draw runways left top width height
    rects = calculate_landing_area();
    for rect in rects:
        for x in rect:
            x *= SCALING
    for rect in rects:
        print("drawing rects")
        pygame.draw.rect(disp, WHITE, rect)
    # are these so small that we cannot see them?

    done = False
    GO_HERE = False
    while(not done):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.K_ESCAPE == True:
                print("WE GOT HERE")
                done = True
            if GO_HERE or event.type == pygame.MOUSEBUTTONDOWN:
                # todo: allow us to scale and zoom
                if event.button == 4 or event.button == 5:
                    zoom = 2 if event.button == 4 else 0.5
                    mx, my = event.pos
                    left = mx + (maprect.left - mx) * zoom
                    right = mx + (maprect.right - mx) * zoom
                    top = my + (maprect.top - my) * zoom
                    bottom = my+ (maprect.bottom - my ) * zoom
                    maprect = pygame.Rect(left, top, bottom, right-left, bottom-top)
                    blitmap()
        

        pygame.display.flip()

        clk.tick(10)
    sys.exit()

draw()
