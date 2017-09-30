from abc import ABC, abstractmethod
from constants import *
from math import sin, cos, pi, atan, sqrt


class Entity(ABC):

    def __init__(self, init_x, init_y, init_vx, init_vy, mass, radius):
        self.x, self.y, self.vx, self.vy, self.mass, self.radius = init_x, init_y, init_vx, init_vy, mass, radius

    @abstractmethod
    def draw(self, surface):
        pass

    @abstractmethod
    def update(self, keys):
        pass

    def get_pos(self):
        return (int(self.x), int(self.y))

    def get_speed(self):
        return sqrt(self.vx ** 2 + self.vy ** 2)

    def get_friction(self, value, friction = FRICTION, threshold = THRESHOLD):
        value *= friction
        return value

    def get_dir_angle(self):
        if self.vx == 0:
            return pi / -2 if self.vy > 0 else pi / 2
        else:
            return atan(-1 * self.vy / self.vx) + (pi if self.vx < 0 else 0)

    def bounce(self, bounce_angle, friction = 1, speed = 0):
        if speed == 0:
            speed = self.get_speed() * friction
        dir_angle = self.get_dir_angle() + pi
        dir_angle += 2 * (bounce_angle - dir_angle)
        self.vx, self.vy = speed * cos(dir_angle), -1 * speed * sin(dir_angle)

        self.x += self.vx
        self.y += self.vy

    def check_collision(self, other):
        x_diff = self.x - other.x
        y_diff = self.y - other.y
        dist = sqrt(x_diff ** 2 + y_diff ** 2)
        return dist < (self.radius + other.radius)

    def collide(self, other):
        new_vx = (self.mass - other.mass) / (self.mass + other.mass) * self.vx + \
                 2 * other.mass / (self.mass + other.mass) * other.vx
        new_vy = (self.mass - other.mass) / (self.mass + other.mass) * self.vy + \
                 2 * other.mass / (self.mass + other.mass) * other.vy

        other.vx = (other.mass - self.mass) / (self.mass + other.mass) * other.vx + \
                   2 * self.mass / (self.mass + other.mass) * self.vx
        other.vy = (other.mass - self.mass) / (self.mass + other.mass) * other.vy + \
                   2 * self.mass / (self.mass + other.mass) * self.vy

        self.vx, self.vy = new_vx, new_vy