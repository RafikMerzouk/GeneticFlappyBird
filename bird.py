import pygame
from neural_network import NeuralNetwork


class Bird:
    def __init__(self, x, y, HEIGHT):
        self.x = x
        self.y = y
        self.speed = 0
        self.gravity = 0.5
        self.jump_strength = -8
        self.image = pygame.image.load("bird.png")
        self.HEIGHT = HEIGHT
        self.score = 0

        # Initialize the bird's brain
        self.brain = NeuralNetwork(input_size=4, hidden_size=8, output_size=1)

    def update_position(self):
        self.speed += self.gravity
        self.y += self.speed

    def jump(self):
        self.speed = self.jump_strength

    def display(self, window):
        window.blit(self.image, (self.x, self.y))

    def think(self, pipes):
        # For simplicity, consider only the nearest pipe
        nearest_pipe = None
        nearest_distance = float('inf')
        for pipe in pipes:
            distance = pipe.x + pipe.width - self.x
            if 0 < distance < nearest_distance:
                nearest_distance = distance
                nearest_pipe = pipe

        if nearest_pipe:
            inputs = [
                self.y / self.HEIGHT,
                nearest_pipe.gap_position / self.HEIGHT,
                (nearest_pipe.gap_position + nearest_pipe.gap_size) / self.HEIGHT,
                self.speed / 10
            ]
            decision = self.brain.predict(inputs)
            if decision == 1:
                self.jump()

    def reset(self):
        self.y = self.HEIGHT // 2
        self.speed = 0
        self.score = 0