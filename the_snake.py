from random import randrange, choice

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

    def draw_object(self, position, body_color):
        """Метод отрисовки"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw():
        """Метод отрисовки для переопределения в дочерних классах"""
        pass


class Apple(GameObject):
    """Дочерний класс для яблок"""

    def __init__(self):
        super().__init__(APPLE_COLOR)
        self.randomize_position([(SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)])

    def randomize_position(self, positions):
        """Метод задающий случайное значение для яблока не входящее в змею"""
        while True:
            self.position = (randrange(0, 620, 20), randrange(0, 460, 20))
            if self.position not in positions:
                break


class Snake(GameObject):
    """Дочерний объект для Змеи"""

    def __init__(self, body_color=SNAKE_COLOR):
        self.next_direction = None
        super().__init__(body_color)
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.last = None
        self.reset()
        self.direction = RIGHT

    def update_direction(self):
        """Метод для обновления направления"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод для движения змеи"""
        head_x, head_y = self.get_head_position()
        direction_x, direction_y = self.direction
        self.position = (((head_x + (direction_x * GRID_SIZE)) % SCREEN_WIDTH),
                         ((head_y + (direction_y * GRID_SIZE))
                          % SCREEN_HEIGHT))
        self.positions.insert(0, self.position)
        if self.length < len(self.positions):
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Метод для отрисовки змеи"""
        for position in self.positions[:-1]:
            GameObject.draw_object(self, position, self.body_color)
        # Отрисовка головы змейки
        GameObject.draw_object(self, self.positions[0], self.body_color)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод для получения координат головы змеи"""
        return self.positions[0]

    def reset(self):
        """Метод для перезапуска игры, если змея съела сама себя"""
        self.direction = choice([DOWN, UP, RIGHT, LEFT])
        self.next_direction = None
        self.positions = [self.position]
        self.length = 1


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
        if snake.positions[0] in snake.positions[1:len(snake.positions)]:
            snake.reset()
            apple.randomize_position(snake.positions)
            screen.fill(BOARD_BACKGROUND_COLOR)
        if snake.positions[0] == apple.position:
            snake.positions.insert(0, apple.position)
            apple.randomize_position(snake.positions)
        snake.draw()
        apple.draw_object(apple.position, apple.body_color)
        pg.display.update()


if __name__ == '__main__':
    main()
