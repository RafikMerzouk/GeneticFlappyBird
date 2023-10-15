import numpy as np
from game_functions import *
from genetic_algortihm import *
import multiprocessing
from scipy.stats import linregress

# Paramètres du jeu
WIDTH = 480
HEIGHT = 640
POPULATION_SIZE = 200
VISUALIZE = False
NUM_TRIALS = 64
# Define hyperparameter ranges
population_sizes = [200]
mutation_rates = [0.1]
hidden_layer_sizes = [11]
methods = ["uniform", "one_point", "two_point", "arithmetic"]

best_score = -np.inf  # You want to maximize the score
best_hyperparameters = None

def run_genetic_algorithm(num_generations, population_size, mutation_rate, hidden_layer_size, method, visualize=False):
    if visualize:
        window, clock = initialize_game(WIDTH, HEIGHT)
        font = pygame.font.Font(None, 36)
    birds = create_new_population(population_size, hidden_layer_size, WIDTH, HEIGHT)
    generation_info = {'generation': [], 'best_score': [], 'average_score': []}
    dead_birds = []
    pipes = [Pipe(WIDTH, HEIGHT)]
    generation = 0

    while generation < num_generations:
        if visualize:
            running = handle_events()
            if not running:
                break
        birds, pipes, dead_birds = update_game_state(birds, pipes, dead_birds, WIDTH, HEIGHT)

        if len(birds) == 0:
            best_bird_score = max(dead_birds, key=lambda bird: bird.score).score
            average_score = sum(bird.score for bird in dead_birds) / len(dead_birds)

            generation_info['generation'].append(generation)
            generation_info['best_score'].append(best_bird_score)
            generation_info['average_score'].append(average_score)

            birds = generate_new_population(dead_birds, population_size, WIDTH, HEIGHT, mutation_rate, hidden_layer_size, method)
            dead_birds = []
            pipes = reset_game(birds, pipes, WIDTH, HEIGHT)
            pipes = [Pipe(WIDTH, HEIGHT)]
            generation += 1

        if visualize:
            render_game(window, birds, pipes, generation, font)
            clock.tick(60)

    if visualize:
        pygame.quit()

    return generation_info

def thread_function(args):
    i, population_size, mutation_rate, hidden_layer_size, return_dict, method = args
    generation_info = run_genetic_algorithm(300, population_size, mutation_rate, hidden_layer_size, method)
    
    if generation_info['average_score']:
        slope, _, _, _, _ = linregress(range(len(generation_info['average_score'])), generation_info['average_score'])
        return_dict[i] = {
            'slope': slope,
            'hyperparameters': {
                'population_size': population_size,
                'mutation_rate': mutation_rate,
                'hidden_layer_size': hidden_layer_size,
                'method': method
            }
        }
    print(f'Trial number {i}')

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    args_list = []

    trial_number = 0
    for population_size in population_sizes:
        for mutation_rate in mutation_rates:
            for hidden_layer_size in hidden_layer_sizes:
                for method in methods :
                    args_list.append((trial_number, population_size, mutation_rate, hidden_layer_size, return_dict, method))
                    trial_number += 1

    pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
    pool.map(thread_function, args_list)

    # Here you can find the best hyperparameters from return_dict
    best_trial = max(return_dict.items(), key=lambda x: x[1]['slope'])
    print(f"Best hyperparameters: {best_trial[1]['hyperparameters']}")

