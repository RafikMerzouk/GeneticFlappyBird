import numpy as np
from bird import Bird
from neural_network import NeuralNetwork
import random

def select_parents(birds):
    # Roulette wheel selection
    fitness_sum = sum([bird.score for bird in birds])
    pick = np.random.rand() * fitness_sum
    current_sum = 0
    for bird in birds:
        current_sum += bird.score
        if current_sum > pick:
            return bird
    return birds[-1]  # Return the last bird if none are selected

def crossover(parent1, parent2):
    child_brain = NeuralNetwork(parent1.brain.input_size, parent1.brain.hidden_size, parent1.brain.output_size)
    
    # Crossover weights and biases
    child_brain.weights_input_to_hidden = np.where(np.random.rand() < 0.5, parent1.brain.weights_input_to_hidden, parent2.brain.weights_input_to_hidden)
    child_brain.weights_hidden_to_output = np.where(np.random.rand() < 0.5, parent1.brain.weights_hidden_to_output, parent2.brain.weights_hidden_to_output)
    child_brain.bias_hidden = np.where(np.random.rand() < 0.5, parent1.brain.bias_hidden, parent2.brain.bias_hidden)
    child_brain.bias_output = np.where(np.random.rand() < 0.5, parent1.brain.bias_output, parent2.brain.bias_output)
    
    return child_brain

def generate_new_population(birds, population_size, WIDTH, HEIGHT):
    new_birds = []
    
    # Select two parents and create a child for the new generation
    for _ in range(population_size):
        parent1 = select_parents(birds)
        parent2 = select_parents(birds)
        max_attempts = 10
        attempts = 0
        while parent2 == parent1 and attempts < max_attempts:
            parent2 = select_parents(birds)
            attempts += 1
        
        # If parent2 is still the same as parent1 after max_attempts, choose a random bird
        if parent2 == parent1:
            parent2 = random.choice(birds)
        child_brain = crossover(parent1, parent2)
        child_brain.mutate(0.1)  # 10% mutation rate
        child = Bird(WIDTH // 4, HEIGHT // 2, HEIGHT)
        child.brain = child_brain
        new_birds.append(child)

    return new_birds
