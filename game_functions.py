import pygame
from pygame.locals import QUIT
from bird import Bird
from pipe import Pipe

def reset_game(birds, pipes, WIDTH, HEIGHT):
    for bird in birds:
        bird.reset()
    pipes.clear()
    pipes.append(Pipe(WIDTH, HEIGHT))

def initialize_game(WIDTH, HEIGHT):
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Flappy Bird")
    clock = pygame.time.Clock()
    return window, clock

def create_new_population(POPULATION_SIZE, WIDTH, HEIGHT, hidden_layer_size):
    return [Bird(WIDTH // 4, HEIGHT // 2, HEIGHT, hidden_layer_size) for _ in range(POPULATION_SIZE)]

def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            return False
    return True

def update_game_state(birds, pipes, dead_birds, WIDTH, HEIGHT):
    # Update birds and check collisions
    for bird in birds:
        bird.think(pipes)
        bird.update_position()
        if check_collision(bird, pipes, HEIGHT):
            birds.remove(bird)  # Remove bird if there's a collision
            dead_birds.append(bird)

    # Update and handle pipes
    for pipe in pipes:
        pipe.move()
        if pipe.x + pipe.width < 0:
            pipes.remove(pipe)
    if len(pipes) == 0 or pipes[-1].x <= WIDTH - 200:
        pipes.append(Pipe(WIDTH, HEIGHT))

    return birds, pipes, dead_birds

def render_game(window, birds, pipes, score, font):
    window.fill((135, 206, 235))  # SKY_BLUE
    for pipe in pipes:
        pipe.display(window)
    for bird in birds:
        bird.display(window)
    display_score(window, score, font, birds[0].score)
    pygame.display.flip()

def display_score(window, generation, font, score):
    score_text = font.render(f'Generation: {generation} Score : {score}', True, (0, 0, 0))
    window.blit(score_text, (10, 10))

def check_collision(bird, pipes, HEIGHT):
    bird_rect = pygame.Rect(bird.x, bird.y, bird.image.get_width(), bird.image.get_height())
    
    # Check if bird passed a pipe and increment score
    for pipe in pipes:
        if pipe.x + pipe.width < bird.x and bird not in pipe.scored_by:
            bird.score += 1
            pipe.scored_by.add(bird)

    # Check for collisions with pipes
    for pipe in pipes:
        upper_pipe_rect = pygame.Rect(pipe.x, 0, pipe.width, pipe.gap_position)
        lower_pipe_rect = pygame.Rect(pipe.x, pipe.gap_position + pipe.gap_size, pipe.width, HEIGHT)
        if bird_rect.colliderect(upper_pipe_rect) or bird_rect.colliderect(lower_pipe_rect):
            return True

    # Check if bird touches the ground or goes beyond the screen top
    if bird.y + bird.image.get_height() > HEIGHT or bird.y < 0:
        return True

    return False

