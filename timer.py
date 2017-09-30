import pygame

class Timer:

    def __init__(self, init_time, tick_length):
        self.time_left = init_time
        self.tick_length = tick_length
        self.clock = pygame.time.Clock()
        self.frozen_countdown = 0

    def get_min(self):
        return self.time_left // 60

    def get_sec(self):
        return self.time_left % 60

    def get_time_left(self):
        return self.time_left

    def tick(self):
        self.clock.tick(self.tick_length)
        if self.is_frozen():
            self.frozen_countdown -= 1
        else:
            self.time_left -= self.tick_length / 1000


    def is_frozen(self):
        return self.frozen_countdown > 0

    def freeze(self, seconds):
        self.frozen_countdown = seconds * 1000 / self.tick_length

    def is_finished(self):
        return self.time_left <= 0

    def __str__(self):
        return '{:.0f}:{:04.1f}'.format(self.get_min(), self.get_sec())