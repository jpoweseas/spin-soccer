import pygame
from constants import *
from constants import get_friction
from math import pi, atan, sqrt, sin, cos
from entity import Entity


class Ball(Entity):

    def __init__(self, init_x, init_y, init_vx, init_vy):
        Entity.__init__(self, init_x, init_y, init_vx, init_vy, 1, BALL_RADIUS)

    def update(self):
        if self.x < 0:
            self.vx = abs(self.vx)
        if self.x > SCREEN_WIDTH:
            self.vx = -1 * abs(self.vx)
        if self.y < 0:
            self.vy = abs(self.vy)
        if self.y > SCREEN_HEIGHT:
            self.vy = -1 * abs(self.vy)

        self.vx = get_friction(self.vx, friction=BALL_FRICTION)
        self.vy = get_friction(self.vy, friction=BALL_FRICTION)

        self.x += self.vx
        self.y += self.vy

    def draw(self, surface):
        pygame.draw.circle(surface, BLACK, self.get_pos(), BALL_RADIUS)