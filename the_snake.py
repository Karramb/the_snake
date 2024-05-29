from random import randrange

import pygame as pg

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
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Базовый класс игры"""

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR):
        self.body_color = body_color
        """Позиция оставлена, т.к. это требование pytest"""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))

    def draw(self, position, body_color):
        """Метод отрисовки"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Дочерний класс для яблок"""

    def __init__(self):
        self.position = ((SCREEN_WIDTH // 4), (SCREEN_HEIGHT // 4))
        self.body_color = APPLE_COLOR

    def randomize_position(self, snake_object):
        """Метод задающий случайное значение для яблока не входящее в змею"""
        while True:
            new_random_position = (randrange(0, 620, 20),
                                   randrange(0, 460, 20))
            if new_random_position not in snake_object.positions:
                self.position = new_random_position
                break


class Snake(GameObject):
    """Дочерний объект для Змеи"""

    def __init__(self, body_color=SNAKE_COLOR):
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        super().__init__(body_color)
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.positions = [self.position]
        self.last = None

    def update_direction(self):
        """Метод для обновления направления"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для движения змеи"""
        self.head_position = self.get_head_position()
        head_x, head_y = self.head_position[0], self.head_position[1]
        direction_x, direction_y = self.direction[0], self.direction[1]
        self.position = (((head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH),
                         ((head_y + (direction_y * GRID_SIZE))
                          % SCREEN_HEIGHT))
        self.positions.insert(0, self.position)
        self.last = self.positions.pop()

    def draw(self):
        """Метод для отрисовки змеи"""
        for position in self.positions[:-1]:
            GameObject.draw(self, position, self.body_color)
        # Отрисовка головы змейки
        GameObject.draw(self, self.positions[0], self.body_color)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод для получения координат головы змеи"""
        return self.positions[0]

    def reset(self):
        """Метод для перезапуска игры, если змея съела сама себя"""
        self.direction = RIGHT
        self.next_direction = None
        self.positions = [self.position]


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Функция для считывания нажатия клавиш"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                pg.quit()
                raise SystemExit


def check_on_eat(snake_object, apple_object):
    """Функция проверки съедено ли яблоко и\
        если да - запуск метода randomize_position"""
    if snake_object.get_head_position() == apple_object.position:
        snake_object.positions.insert(0, apple_object.position)
        apple_object.randomize_position(snake_object)


def check_eat_itself(snake_object, apple_object):
    """Функция проверки не съела ли змея сама себя"""
    snake_object.head_position = snake_object.get_head_position()
    if snake_object.head_position in snake_object.positions[
            1:len(snake_object.positions)]:
        snake_object.reset()
        apple_object.randomize_position(snake_object)
        screen.fill(BOARD_BACKGROUND_COLOR)


def main():
    """Инициализация pg:"""
    pg.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake()
    apple = Apple()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        """Не понял комментария про эти 2 функции - я могу написать эти условия
        в коде, но какая разница и зачем, если с
        функциями тело игры вылядит понятнее"""
        check_eat_itself(snake, apple)
        check_on_eat(snake, apple)
        apple.draw(apple.position, apple.body_color)
        snake.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
