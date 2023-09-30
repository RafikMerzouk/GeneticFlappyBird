from game_functions import *
from genetic_algortihm import *

# Paramètres du jeu
WIDTH = 480
HEIGHT = 640
POPULATION_SIZE = 200
VISUALIZE = True

def main():
    window, clock = initialize_game(WIDTH, HEIGHT)
    birds = create_new_population(POPULATION_SIZE, WIDTH, HEIGHT)
    dead_birds = []
    pipes = [Pipe(WIDTH, HEIGHT)]
    generation = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        running = handle_events()
        
        birds, pipes, dead_birds = update_game_state(birds, pipes, dead_birds, WIDTH, HEIGHT)

        if len(birds) == 0 :
            birds = generate_new_population(dead_birds, POPULATION_SIZE, WIDTH, HEIGHT)
            dead_birds = []
            generation += 1
            reset_game(birds, pipes, WIDTH, HEIGHT)

        if VISUALIZE:
            render_game(window, birds, pipes, generation, font)
        
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
