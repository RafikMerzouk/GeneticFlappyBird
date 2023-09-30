import pygame
import random

class Pipe:
    def __init__(self, x, HEIGHT):
        self.x = x
        self.gap_size = 150
        self.gap_position = random.randint(100, HEIGHT - 100 - self.gap_size)
        self.speed = 3
        self.width = 50
        self.color = (0, 255, 0)
        self.HEIGHT = HEIGHT
        self.scored_by = set()  # Birds that have scored by passing this pipe
    
    def move(self):
        self.x -= self.speed

    def display(self, window):
        pygame.draw.rect(window, self.color, (self.x, 0, self.width, self.gap_position))  # upper pipe
        pygame.draw.rect(window, self.color, (self.x, self.gap_position + self.gap_size, self.width, self.HEIGHT))  # lower pipe