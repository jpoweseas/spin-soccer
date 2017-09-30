import pygame
from constants import *
from math import sin, cos, pi, atan, sqrt
from entity import Entity
from constants import get_friction
from ball import Ball


class Player(Entity):

    def __init__(self, init_x, init_y, color, controls):
        Entity.__init__(self, init_x, init_y, 0, 0, 3, PLAYER_RADIUS)
        self.up, self.left, self.down, self.right, self.turn_left, self.turn_right, self.throw = controls
        self.init_x, self.init_y = init_x, init_y
        self.color = color
        self.angle, self.vrad = 0, 0.1
        self.has_ball = False
        self.frozen = False
        self.ball_cooldown = 0

    def get_ball_pos(self):
        return (int(self.x + HAND_DISTANCE * cos(self.angle)), int(self.y - HAND_DISTANCE * sin(self.angle)))

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.get_pos(), PLAYER_RADIUS)
        if self.has_ball:
            pygame.draw.circle(surface, BLACK, self.get_ball_pos(), BALL_RADIUS)
        else:
            pygame.draw.circle(surface, self.color, self.get_ball_pos(), HAND_RADIUS)

    def update(self, keys):
        if self.frozen:
            return

        self.x += self.vx
        self.y += self.vy
        self.angle += self.vrad

        self.vx = get_friction(self.vx)
        self.vy = get_friction(self.vy)
        self.vrad = get_friction(self.vrad, friction=THROW_FRICTION)

        if keys[self.up]:
            self.vy -= PLAYER_XY_ACCEL
        if keys[self.left]:
            self.vx -= PLAYER_XY_ACCEL
        if keys[self.down]:
            self.vy += PLAYER_XY_ACCEL
        if keys[self.right]:
            self.vx += PLAYER_XY_ACCEL
        if keys[self.turn_left]:
            self.vrad += PLAYER_RAD_ACCEL
        if keys[self.turn_right]:
            self.vrad -= PLAYER_RAD_ACCEL
        if keys[self.throw] and self.has_ball:
            self.has_ball = False
            return True

        self.ball_cooldown -= 1

        return False

    def get_thrown_ball(self):
        ball_speed = abs(HAND_DISTANCE * self.vrad)
        ball_angle = self.angle + (abs(self.vrad) / self.vrad * pi / 2 if self.vrad != 0 else 0)

        ball_vx = ball_speed * cos(ball_angle) + self.vx
        ball_vy = -1 * ball_speed * sin(ball_angle) + self.vy
        ball_x = self.get_ball_pos()[0] + ball_vx
        ball_y = self.get_ball_pos()[1] + ball_vy

        self.ball_cooldown = 20

        return Ball(ball_x, ball_y, ball_vx, ball_vy)

    def can_catch_ball(self):
        return self.ball_cooldown <= 0

    def reset(self):
        self.x = self.init_x
        self.y = self.init_y
        self.vx, self.vy, self.vrad, self.angle = 0, 0, 0, pi / 2

    def unfreeze(self):
        self.frozen = False