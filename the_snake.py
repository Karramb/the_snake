from random import randrange

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс игры"""

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 body_color=BOARD_BACKGROUND_COLOR):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Базовый метод отрисовки, переопределенный в дочерних классах"""
        pass


class Apple(GameObject):
    """Дочерний класс для яблок"""

    def __init__(self):
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def randomize_position(self):
        """Метод задающий случайное значение для яблока"""
        return (randrange(0, 620, 20), randrange(0, 460, 20))

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Дочерний объект для Змеи"""

    def __init__(self, position=((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)),
                 body_color=SNAKE_COLOR, positions=[]):
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        super().__init__(position, body_color)
        self.positions = positions
        self.positions.insert(0, position)
        self.last = None

    def update_direction(self):
        """Метод для обновления направления"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для движения змеи"""
        self.head_position = self.get_head_position()
        self.positions.insert(0, self.check_out_range(self.direction))
        self.last = self.positions.pop()

    def draw(self):
        """Метод для отрисовки змеи"""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод для получения координат головы змеи"""
        return self.positions[0]

    def reset(self):
        """Метод для перезапуска игры, если змея съела сама себя"""
        self.direction = RIGHT
        self.next_direction = None
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions.clear()
        self.positions.insert(0, self.position)

    def check_out_range(self, direction):
        """Метод для получения координат движения змеи,\
            плюс проверка на выход змеи за границы экрана"""
        if direction is UP:
            if self.head_position[1] - GRID_SIZE < 0:
                return (self.head_position[0], SCREEN_HEIGHT - GRID_SIZE)
            else:
                return (self.head_position[0],
                        self.head_position[1] - GRID_SIZE)
        elif direction is DOWN:
            if self.head_position[1] + GRID_SIZE >= SCREEN_HEIGHT:
                return (self.head_position[0], 0)
            else:
                return (self.head_position[0],
                        self.head_position[1] + GRID_SIZE)
        elif direction is RIGHT:
            if self.head_position[0] + GRID_SIZE >= SCREEN_WIDTH:
                return (0, self.head_position[1])
            else:
                return (self.head_position[0] + GRID_SIZE,
                        self.head_position[1])
        elif direction is LEFT:
            if self.head_position[0] - GRID_SIZE < 0:
                return (SCREEN_WIDTH - GRID_SIZE, self.head_position[1])
            else:
                return (self.head_position[0] - GRID_SIZE,
                        self.head_position[1])


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Функция для считывания нажатия клавиш"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def check_on_eat(snake_object, apple_object):
    """Функция проверки съедено лии яблоко и\
        если да - выдача новых координат яблоку не входящих в длину змеи"""
    if snake_object.get_head_position() == apple_object.position:
        snake_object.positions.insert(0, apple_object.position)
        while True:
            new_random_position = apple_object.randomize_position()
            if new_random_position not in snake_object.positions:
                apple_object.position = new_random_position
                break


def check_eat_itself(snake_object):
    """Функция проверки не съела ли змея сама себя"""
    snake_object.head_position = snake_object.get_head_position()
    if snake_object.head_position in snake_object.positions[
            1:len(snake_object.positions)]:
        return True


def main():
    """Инициализация PyGame:"""
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if check_eat_itself(snake):
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        check_on_eat(snake, apple)
        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT
#                 and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT
#                 and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
