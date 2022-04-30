import pygame
import sys


def run_visualization():
    pygame.init()
    size = width, height = 1200, 1200
    speed = [2, 2]
    black = 0, 0, 0
    window = pygame.display.set_mode(size)

    ball = pygame.image.load("intro_ball.gif")
    ballrect = ball.get_rect()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        ballrect = ballrect.move(speed)
        if ballrect.left < 0 or ballrect.right > width:
            speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > height:
            speed[1] = -speed[1]

        window.fill(black)
        window.blit(ball, ballrect)
        pygame.draw.circle(window, (0, 255, 0),
                           [600, 600], 600, 3)
        pygame.display.flip()
    return


if __name__ == "__main__":
    run_visualization()
