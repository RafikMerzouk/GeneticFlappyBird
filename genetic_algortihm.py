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

def tournament_selection(birds, tournament_size=3):
    tournament = np.random.choice(birds, tournament_size)
    return max(tournament, key=lambda bird: bird.score)

def roulette_wheel_selection(birds):
    total_fitness = sum(bird.score for bird in birds)
    selected_value = np.random.uniform(0, total_fitness)
    cumulative_fitness = 0
    for bird in birds:
        cumulative_fitness += bird.score
        if cumulative_fitness > selected_value:
            return bird
    return birds[-1]  # Return the last bird if none are selected

def crossover(parent1, parent2, method):
    child_brain = NeuralNetwork(parent1.brain.input_size, parent1.brain.hidden_size, parent1.brain.output_size)
    
    if method == 'uniform':
        mask = np.random.rand() < 0.5
        child_brain.weights_input_to_hidden = np.where(mask, parent1.brain.weights_input_to_hidden, parent2.brain.weights_input_to_hidden)
        child_brain.weights_hidden_to_output = np.where(mask, parent1.brain.weights_hidden_to_output, parent2.brain.weights_hidden_to_output)
        child_brain.bias_hidden = np.where(mask, parent1.brain.bias_hidden, parent2.brain.bias_hidden)
        child_brain.bias_output = np.where(mask, parent1.brain.bias_output, parent2.brain.bias_output)

    elif method == 'one_point':
        crossover_point = np.random.randint(parent1.brain.hidden_size)
        child_brain.weights_input_to_hidden[:crossover_point] = parent1.brain.weights_input_to_hidden[:crossover_point]
        child_brain.weights_input_to_hidden[crossover_point:] = parent2.brain.weights_input_to_hidden[crossover_point:]

    elif method == 'two_point':
        crossover_point1 = np.random.randint(parent1.brain.hidden_size)
        crossover_point2 = np.random.randint(parent1.brain.hidden_size)
        start, end = min(crossover_point1, crossover_point2), max(crossover_point1, crossover_point2)
        child_brain.weights_input_to_hidden[start:end] = parent1.brain.weights_input_to_hidden[start:end]
        child_brain.weights_input_to_hidden[:start] = parent2.brain.weights_input_to_hidden[:start]
        child_brain.weights_input_to_hidden[end:] = parent2.brain.weights_input_to_hidden[end:]

    elif method == 'arithmetic':
        alpha = np.random.rand()
        child_brain.weights_input_to_hidden = alpha * parent1.brain.weights_input_to_hidden + (1 - alpha) * parent2.brain.weights_input_to_hidden
        child_brain.weights_hidden_to_output = alpha * parent1.brain.weights_hidden_to_output + (1 - alpha) * parent2.brain.weights_hidden_to_output
        child_brain.bias_hidden = alpha * parent1.brain.bias_hidden + (1 - alpha) * parent2.brain.bias_hidden
        child_brain.bias_output = alpha * parent1.brain.bias_output + (1 - alpha) * parent2.brain.bias_output

    return child_brain

def generate_new_population(birds, population_size, WIDTH, HEIGHT, mutation_rate, hidden_layer_size, elitism_rate=0.1, method="uniform"):
    new_birds = []
    
    num_elites = int(elitism_rate * population_size)
    elites = sorted(birds, key=lambda bird: bird.score, reverse=True)[:num_elites]
    
    # Adding elites directly to the new population
    new_birds.extend(elites)
    
    # Select two parents and create a child for the new generation
    for _ in range(population_size - num_elites):
        parent1 = roulette_wheel_selection(birds)
        parent2 = roulette_wheel_selection(birds)
        max_attempts = 10
        attempts = 0
        while parent2 == parent1 and attempts < max_attempts:
            parent2 = roulette_wheel_selection(birds)
            attempts += 1
        
        # If parent2 is still the same as parent1 after max_attempts, choose a random bird
        if parent2 == parent1:
            parent2 = random.choice(birds)
        child_brain = crossover(parent1, parent2, method)
        child_brain.mutate(mutation_rate)  # mutation rate
        child = Bird(WIDTH // 4, HEIGHT // 2, HEIGHT, hidden_layer_size)
        child.brain = child_brain
        new_birds.append(child)

    return new_birds

