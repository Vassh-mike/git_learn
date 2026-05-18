import pygame
import random

# Window settings
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
CELL_SIZE = 20
assert WINDOW_WIDTH % CELL_SIZE == 0, "Window width must be a multiple of cell size."
assert WINDOW_HEIGHT % CELL_SIZE == 0, "Window height must be a multiple of cell size."
CELL_WIDTH = WINDOW_WIDTH // CELL_SIZE
CELL_HEIGHT = WINDOW_HEIGHT // CELL_SIZE

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (220, 0, 0)
DARK_GREEN = (0, 120, 0)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


def draw_rect(surface, color, position):
    x, y = position
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(surface, color, rect)


def draw_grid(surface):
    for x in range(0, WINDOW_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, DARK_GREEN, (x, 0), (x, WINDOW_HEIGHT))
    for y in range(0, WINDOW_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, DARK_GREEN, (0, y), (WINDOW_WIDTH, y))


def get_random_food_position(snake):
    while True:
        position = (random.randrange(CELL_WIDTH), random.randrange(CELL_HEIGHT))
        if position not in snake:
            return position


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Snake Game")

    snake = [(CELL_WIDTH // 2, CELL_HEIGHT // 2),
             (CELL_WIDTH // 2 - 1, CELL_HEIGHT // 2),
             (CELL_WIDTH // 2 - 2, CELL_HEIGHT // 2)]
    direction = RIGHT
    food_position = get_random_food_position(snake)
    score = 0
    game_over = False

    font = pygame.font.SysFont(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != DOWN:
                    direction = UP
                elif event.key == pygame.K_DOWN and direction != UP:
                    direction = DOWN
                elif event.key == pygame.K_LEFT and direction != RIGHT:
                    direction = LEFT
                elif event.key == pygame.K_RIGHT and direction != LEFT:
                    direction = RIGHT
                elif event.key == pygame.K_r and game_over:
                    snake = [(CELL_WIDTH // 2, CELL_HEIGHT // 2),
                             (CELL_WIDTH // 2 - 1, CELL_HEIGHT // 2),
                             (CELL_WIDTH // 2 - 2, CELL_HEIGHT // 2)]
                    direction = RIGHT
                    food_position = get_random_food_position(snake)
                    score = 0
                    game_over = False

        if not game_over:
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            if (new_head[0] < 0 or new_head[0] >= CELL_WIDTH or
                new_head[1] < 0 or new_head[1] >= CELL_HEIGHT or
                new_head in snake):
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food_position:
                    score += 1
                    food_position = get_random_food_position(snake)
                else:
                    snake.pop()

        screen.fill(BLACK)
        draw_grid(screen)

        for cell in snake:
            draw_rect(screen, GREEN, cell)
        draw_rect(screen, RED, food_position)

        score_surface = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_surface, (10, 10))

        if game_over:
            game_over_surface = font.render("Game Over - Press R to restart", True, WHITE)
            rect = game_over_surface.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            screen.blit(game_over_surface, rect)

        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    main()
