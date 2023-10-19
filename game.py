from game_functions import *
from genetic_algortihm import *
from pynput import keyboard
import pickle
import matplotlib.pyplot as plt

exit_script = False

def on_press(key):
    global exit_script
    try:
        if key.char == 'q':
            exit_script = True
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

# Paramètres du jeu
WIDTH = 480
HEIGHT = 640
POPULATION_SIZE = 250
VISUALIZE = True

def main():
    try:
        with open('generation_info.pkl', 'rb') as file:
            generation_info = pickle.load(file)
    except FileNotFoundError:
        generation_info = {
            'generation': [],
            'best_score': [],
            'average_score': []
        }
    if VISUALIZE :
        window, clock = initialize_game(WIDTH, HEIGHT)
        font = pygame.font.Font(None, 36)
    birds = create_new_population(POPULATION_SIZE, WIDTH, HEIGHT, 5)
    
    dead_birds = []
    pipes = [Pipe(WIDTH, HEIGHT)]
    generation = 0
    for bird in birds:
        generation = bird.brain.load('best_model.pkl', load_model=True)  # Set load_model to False to skip loading
    running = True
    while running:
        if VISUALIZE :
            running = handle_events()
        
        birds, pipes, dead_birds = update_game_state(birds, pipes, dead_birds, WIDTH, HEIGHT)

        if len(birds) == 0 :
            birds = generate_new_population(dead_birds, POPULATION_SIZE, WIDTH, HEIGHT, 0.1, 11)
            if not VISUALIZE :
                print(f'generation number {generation}, max score : {max(dead_birds, key=lambda bird: bird.score).score}')
            generation_info['generation'].append(generation)
            generation_info['best_score'].append(max([dead_bird.score for dead_bird in dead_birds]))
            generation_info['average_score'].append(sum([dead_bird.score for dead_bird in dead_birds]) / len(birds))
            dead_birds = []
            generation += 1
            reset_game(birds, pipes, WIDTH, HEIGHT)

        if VISUALIZE:
            render_game(window, birds, pipes, generation, font)
            clock.tick(60)
        if exit_script:
            break

    pygame.quit()
    best_bird = max(birds, key=lambda bird: bird.score)
    best_bird.brain.save('best_model.pkl', generation)
    with open('generation_info.pkl', 'wb') as file:
        pickle.dump(generation_info, file)
    plt.plot(generation_info['generation'], generation_info['best_score'], label='Best Score')
    plt.plot(generation_info['generation'], generation_info['average_score'], label='Average Score')
    plt.xlabel('Generation')
    plt.ylabel('Score')
    plt.title('Performance over Generations')
    plt.legend()
    plt.savefig(f'scores.png')

if __name__ == "__main__":
    main()
