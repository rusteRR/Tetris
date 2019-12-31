import pygame
import numpy as np
from random import choice

# переменный экрана

stack_height_cells = 30
stack_width_cells = 20
cell_size = 20
stack_width_px = stack_width_cells * cell_size
stack_height_px = stack_height_cells * cell_size

score = 0

# инициализация игрового поля

# pole = [[0 for i in range(stack_width_cells)]
#         for j in range(stack_height_cells)]

pole = np.zeros(stack_width_cells
                * stack_height_cells).reshape(stack_height_cells, stack_width_cells)

# создание рамок игрового поля

for i in range(stack_height_cells):
    pole[i][0] = 3
    pole[i][stack_width_cells - 1] = 3
for i in range(stack_width_cells):
    pole[stack_height_cells - 1][i] = 3

s_o = pole[0:0, :]
# [0 for i in range(stack_width_cells)]
# s_o[0] = 3
# s_o[-1] = 3


# создание окна

pygame.init()
screen = pygame.display.set_mode((stack_width_px, stack_height_px))
screen.fill(pygame.Color('black'))
clock = pygame.time.Clock()
fps = 60


# класс спрайтов


class Figure:
    def __init__(self, form):
        self.points = list()
        self.orn = 1  # положение объекта(вращение)
        self.tr = 1  # флажок на остановку спрайта
        self.r = 0  # количество поворотов
        self.form = form  # форма спрайта

        # описание формы спрайтаы

        if form == 'I':
            for i in range(4):
                self.points.append([0, i + 1])
        elif form == "T":
            for i in range(3):
                self.points.append([0, i + 4])
            self.points.append([1, 5])
        elif form == 'J':
            self.points.append([0, 4])
            for i in range(3):
                self.points.append([1, i + 4])
        elif form == 'L':
            self.points.append([0, 6])
            for i in range(3):
                self.points.append([1, i + 4])
        elif form == 'O':
            for i in range(2):
                self.points.append([0, i + 4])
                self.points.append([1, i + 4])
        elif form == 'S':
            for i in range(2):
                self.points.append([0, i + 4])
                self.points.append([1, i + 3])
        elif form == 'Z':
            for i in range(2):
                self.points.append([0, i + 3])
            for i in range(2):
                self.points.append([1, i + 4])

    # функция падения спрайта

    def falling(self):
        global pole, trg
        tr = 1
        for i in range(len(self.points)):
            x = self.points[len(self.points) - i - 1][0]
            y = self.points[len(self.points) - i - 1][1]
            point = pole[x + 1][y]
            if point == 3 or point == 2 or self.tr == 0:
                tr = 0  # локальный флажок на условие сдвига вниз спрайта
        for i in range(len(self.points)):
            x = self.points[len(self.points) - i - 1][0]
            y = self.points[len(self.points) - i - 1][1]
            if tr:
                pole[x][y] = 0
                self.points[len(self.points) - i - 1] = [x + 1, y]
            else:
                pole[x][y] = 2
                self.tr = 0
                trg = 1

        for i in range(len(self.points)):
            x = self.points[len(self.points) - i - 1][0]
            y = self.points[len(self.points) - i - 1][1]
            if tr:
                pole[x][y] = 1

    # функция сдвига спрайта влево

    def left(self):
        global pole
        tr = 1
        for i in range(len(self.points)):
            x = self.points[len(self.points) - i - 1][0]
            y = self.points[len(self.points) - i - 1][1]
            point = pole[x][y - 1]
            if point != 1 and point != 0:
                tr = 0
        for i in range(len(self.points)):
            x = self.points[len(self.points) - i - 1][0]
            y = self.points[len(self.points) - i - 1][1]
            if tr:
                pole[x][y] = 0
                self.points[len(self.points) - i - 1] = [x, y - 1]

        for i in range(len(self.points)):
            x = self.points[len(self.points) - i - 1][0]
            y = self.points[len(self.points) - i - 1][1]
            if tr:
                pole[x][y] = 1

    # функция сдвига спрайта вправо

    def right(self):
        global pole
        tr = 1
        for i in range(len(self.points)):
            x = self.points[len(self.points) - i - 1][0]
            y = self.points[len(self.points) - i - 1][1]
            point = pole[x][y + 1]
            if point != 1 and point != 0:
                tr = 0
        for i in range(len(self.points)):
            x = self.points[len(self.points) - i - 1][0]
            y = self.points[len(self.points) - i - 1][1]
            if tr:
                pole[x][y] = 0
                self.points[len(self.points) - i - 1] = [x, y + 1]

        for i in range(len(self.points)):
            x = self.points[len(self.points) - i - 1][0]
            y = self.points[len(self.points) - i - 1][1]
            if tr:
                pole[x][y] = 1

    # функция поворота спрайта

    def rotate(self):
        global pole
        if self.form == 'I':
            x, y = self.points[1]
            if self.orn == 1:
                if (pole[x - 1][y] + pole[x - 2][y] + pole[x + 1][y]) == 0:
                    self.orn = 2
                    self.points[0] = [x - 1, y]
                    self.points[2] = [x - 2, y]
                    self.points[3] = [x + 1, y]
                    pole[x][y + 1] = 0
                    pole[x][y + 2] = 0
                    pole[x][y - 1] = 0

                    pole[x - 1][y] = 1
                    pole[x - 2][y] = 1
                    pole[x + 1][y] = 1
            else:
                if (pole[x][y + 1] + pole[x][y + 2] + pole[x][y - 1]) == 0:
                    self.orn = 1
                    self.points[0] = [x, y + 1]
                    self.points[2] = [x, y + 2]
                    self.points[3] = [x, y - 1]
                    pole[x - 1][y] = 0
                    pole[x - 2][y] = 0
                    pole[x + 1][y] = 0

                    pole[x][y + 1] = 1
                    pole[x][y + 2] = 1
                    pole[x][y - 1] = 1

        elif self.form == "T":
            x, y = self.points[1]
            if self.orn == 1:
                if pole[x - 1][y] == 0:
                    self.orn = 2
                    self.points[((self.r % 3) + 2) % 4] = [x - 1, y]
                    pole[x - 1][y] = 1
                    pole[x][y + 1] = 0
                    self.r += 1

            elif self.orn == 2:
                if pole[x][y + 1] == 0:
                    self.orn = 3
                    self.points[((self.r % 3) + 2) % 4] = [x, y + 1]
                    pole[x][y + 1] = 1
                    pole[x + 1][y] = 0
                    self.r += 1

            elif self.orn == 3:
                if pole[x + 1][y] == 0:
                    self.orn = 4
                    self.points[((self.r % 3) + 2) % 4] = [x + 1, y]
                    pole[x + 1][y] = 1
                    pole[x][y - 1] = 0
                    self.r += 1

            elif self.orn == 4:
                if pole[x][y - 1] == 0:
                    self.orn = 1
                    self.points[((self.r % 3) + 2) % 4] = [x, y - 1]
                    pole[x][y - 1] = 1
                    pole[x - 1][y] = 0
                    self.r += 1

        elif self.form == 'J':
            x, y = self.points[2]
            if self.orn == 1:
                if (pole[x - 1][y] + pole[x - 1][y + 1] + pole[x + 1][y]) == 0:
                    self.orn = 2
                    self.points[0] = [x - 1, y + 1]
                    self.points[1] = [x - 1, y]
                    self.points[3] = [x + 1, y]
                    pole[x - 1][y - 1] = 0
                    pole[x][y - 1] = 0
                    pole[x][y + 1] = 0

                    pole[x - 1][y + 1] = 1
                    pole[x - 1][y] = 1
                    pole[x + 1][y] = 1

            elif self.orn == 2:
                if (pole[x][y + 1] + pole[x][y - 1] + pole[x + 1][y + 1]) == 0:
                    self.orn = 3
                    self.points[0] = [x + 1, y + 1]
                    self.points[1] = [x, y + 1]
                    self.points[3] = [x, y - 1]
                    pole[x - 1][y] = 0
                    pole[x - 1][y + 1] = 0
                    pole[x + 1][y] = 0

                    pole[x][y + 1] = 1
                    pole[x + 1][y + 1] = 1
                    pole[x][y - 1] = 1

            elif self.orn == 3:
                if (pole[x + 1][y - 1] + pole[x + 1][y] + pole[x - 1][y]) == 0:
                    self.orn = 4
                    self.points[0] = [x + 1, y - 1]
                    self.points[1] = [x + 1, y]
                    self.points[3] = [x - 1, y]
                    pole[x][y - 1] = 0
                    pole[x + 1][y + 1] = 0
                    pole[x][y + 1] = 0

                    pole[x + 1][y - 1] = 1
                    pole[x + 1][y] = 1
                    pole[x - 1][y] = 1

            elif self.orn == 4:
                if (pole[x][y + 1] + pole[x][y - 1] + pole[x - 1][y - 1]) == 0:
                    self.orn = 1
                    self.points[0] = [x - 1, y - 1]
                    self.points[1] = [x, y - 1]
                    self.points[3] = [x, y + 1]
                    pole[x - 1][y] = 0
                    pole[x + 1][y] = 0
                    pole[x + 1][y - 1] = 0

                    pole[x - 1][y - 1] = 1
                    pole[x][y - 1] = 1
                    pole[x][y + 1] = 1

        elif self.form == 'L':
            x, y = self.points[2]
            if self.orn == 1:
                if (pole[x - 1][y] + pole[x + 1][y + 1] + pole[x + 1][y]) == 0:
                    self.orn = 2
                    self.points[0] = [x + 1, y + 1]
                    self.points[1] = [x - 1, y]
                    self.points[3] = [x + 1, y]
                    pole[x - 1][y + 1] = 0
                    pole[x][y - 1] = 0
                    pole[x][y + 1] = 0

                    pole[x + 1][y + 1] = 1
                    pole[x - 1][y] = 1
                    pole[x + 1][y] = 1
            elif self.orn == 2:
                if (pole[x][y + 1] + pole[x][y - 1] + pole[x + 1][y - 1]) == 0:
                    self.orn = 3
                    self.points[0] = [x + 1, y - 1]
                    self.points[1] = [x, y + 1]
                    self.points[3] = [x, y - 1]
                    pole[x - 1][y] = 0
                    pole[x + 1][y + 1] = 0
                    pole[x + 1][y] = 0

                    pole[x][y + 1] = 1
                    pole[x + 1][y - 1] = 1
                    pole[x][y - 1] = 1

            elif self.orn == 3:
                if (pole[x - 1][y - 1] + pole[x + 1][y] + pole[x - 1][y]) == 0:
                    self.orn = 4
                    self.points[0] = [x - 1, y - 1]
                    self.points[1] = [x + 1, y]
                    self.points[3] = [x - 1, y]
                    pole[x][y - 1] = 0
                    pole[x + 1][y - 1] = 0
                    pole[x][y + 1] = 0

                    pole[x - 1][y - 1] = 1
                    pole[x + 1][y] = 1
                    pole[x - 1][y] = 1

            elif self.orn == 4:
                if (pole[x][y + 1] + pole[x][y - 1] + pole[x - 1][y + 1]) == 0:
                    self.orn = 1
                    self.points[0] = [x - 1, y + 1]
                    self.points[1] = [x, y - 1]
                    self.points[3] = [x, y + 1]
                    pole[x - 1][y] = 0
                    pole[x + 1][y] = 0
                    pole[x - 1][y - 1] = 0

                    pole[x - 1][y + 1] = 1
                    pole[x][y - 1] = 1
                    pole[x][y + 1] = 1

        elif self.form == 'S':
            x, y = self.points[3]
            if self.orn == 1:
                if (pole[x + 1][y + 1] + pole[x][y + 1]) == 0:
                    self.orn = 2
                    self.points[0] = [x, y + 1]
                    self.points[1] = [x + 1, y + 1]
                    self.points[2] = [x - 1, y]
                    pole[x - 1][y + 1] = 0
                    pole[x][y - 1] = 0

                    pole[x + 1][y + 1] = 1
                    pole[x][y + 1] = 1

            elif self.orn == 2:
                if (pole[x + 1][y] + pole[x + 1][y - 1]) == 0:
                    self.orn = 3
                    self.points[0] = [x + 1, y]
                    self.points[1] = [x + 1, y - 1]
                    self.points[2] = [x, y + 1]
                    pole[x + 1][y + 1] = 0
                    pole[x - 1][y] = 0

                    pole[x + 1][y - 1] = 1
                    pole[x + 1][y] = 1

            elif self.orn == 3:
                if (pole[x - 1][y - 1] + pole[x][y - 1]) == 0:
                    self.orn = 4
                    self.points[0] = [x, y - 1]
                    self.points[1] = [x - 1, y - 1]
                    self.points[2] = [x + 1, y]
                    pole[x + 1][y - 1] = 0
                    pole[x][y + 1] = 0

                    pole[x][y - 1] = 1
                    pole[x - 1][y - 1] = 1

            elif self.orn == 4:
                if (pole[x - 1][y + 1] + pole[x - 1][y]) == 0:
                    self.orn = 1
                    self.points[0] = [x - 1, y]
                    self.points[1] = [x - 1, y + 1]
                    self.points[2] = [x, y - 1]
                    pole[x - 1][y - 1] = 0
                    pole[x + 1][y] = 0

                    pole[x - 1][y + 1] = 1
                    pole[x - 1][y] = 1

        elif self.form == 'Z':
            x, y = self.points[2]
            if self.orn == 1:
                if (pole[x + 1][y] + pole[x - 1][y + 1]) == 0:
                    self.orn = 2
                    self.points[0] = [x - 1, y + 1]
                    self.points[1] = [x, y + 1]
                    self.points[3] = [x + 1, y]
                    pole[x - 1][y] = 0
                    pole[x - 1][y - 1] = 0

                    pole[x - 1][y + 1] = 1
                    pole[x + 1][y] = 1

            elif self.orn == 2:
                if (pole[x + 1][y + 1] + pole[x][y - 1]) == 0:
                    self.orn = 3
                    self.points[0] = [x + 1, y + 1]
                    self.points[1] = [x + 1, y]
                    self.points[3] = [x, y - 1]
                    pole[x][y + 1] = 0
                    pole[x - 1][y + 1] = 0

                    pole[x + 1][y + 1] = 1
                    pole[x][y - 1] = 1

            elif self.orn == 3:
                if (pole[x - 1][y] + pole[x + 1][y - 1]) == 0:
                    self.orn = 4
                    self.points[0] = [x + 1, y - 1]
                    self.points[1] = [x, y - 1]
                    self.points[3] = [x - 1, y]
                    pole[x + 1][y] = 0
                    pole[x + 1][y + 1] = 0

                    pole[x + 1][y - 1] = 1
                    pole[x - 1][y] = 1

            elif self.orn == 4:
                if (pole[x - 1][y - 1] + pole[x][y + 1]) == 0:
                    self.orn = 1
                    self.points[0] = [x - 1, y - 1]
                    self.points[1] = [x - 1, y]
                    self.points[3] = [x, y + 1]
                    pole[x][y - 1] = 0
                    pole[x + 1][y - 1] = 0

                    pole[x - 1][y - 1] = 1
                    pole[x][y + 1] = 1

    # удаление полных слоёв

    def checkout(self):
        global pole, stack_height_cells, stack_width_cells, score, s_o
        newpole = []
        sp = []
        tr = 0
        for i in range(stack_height_cells):
            if sum(pole[i]) == (stack_width_cells - 2) * 2 + 6:
                tr = 1
                sp.append(i)
        if tr == 1:
            for i in range(len(sp)):
                newpole.append(s_o)
                score += 100
            for i in range(stack_height_cells):
                if sum(pole[i]) != (stack_width_cells - 2) * 2 + 6 and not(i in sp):
                    newpole.append(pole[i])
            pole = newpole[:]


# фуdнкция отрисовки экрана


def render():
    screen.fill(pygame.Color('black'))
    col = ['green', 'purple', 'blue', 'orange']
    for i in range(stack_height_cells):
        for j in range(stack_width_cells):
            if pole[i][j] == 1:
                pygame.draw.rect(screen, pygame.Color('green'), (j * cell_size + 1,
                                                                 i * cell_size + 1, cell_size - 2, cell_size - 2), 0)
            elif pole[i][j] == 0:
                pygame.draw.rect(screen, pygame.Color('black'), (j * cell_size + 1,
                                                                 i * cell_size + 1, cell_size - 2, cell_size - 2), 0)
            elif pole[i][j] == 2:
                pygame.draw.rect(screen, pygame.Color('yellow'), (j * cell_size + 1,
                                                                  i * cell_size + 1, cell_size - 2, cell_size - 2), 0)
            elif pole[i][j] == 3:
                pygame.draw.rect(screen, pygame.Color('red'), (j * cell_size + 1,
                                                               i * cell_size + 1, cell_size - 2, cell_size - 2), 0)


im = ('I', 'J', 'L', 'O', 'S', 'T', 'Z')

fugire_counter = 0
timer_falling = 0
max_timer_falling = 60
timer_move = 0

trg = 1  # флажок на ограничение количества объектов на поле одновреме
run = True
while run:
    render()
    pygame.display.flip()

    timer_move += 1

    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            run = False
    if key[pygame.K_LEFT] and timer_move > 10:
        figure.left()
        timer_move = 0
    if key[pygame.K_RIGHT] and timer_move > 10:
        figure.right()
        timer_move = 0
    if key[pygame.K_UP] and timer_move > 10:
        figure.rotate()
        timer_move = 0
    if key[pygame.K_DOWN] and timer_move > 5:
        timer_move = 0
        timer_falling = -1

    if timer_falling < 0:
        timer_falling = max_timer_falling
        figure.checkout()
        figure.falling()
        if fugire_counter > 5:
            fugire_counter = 0
            max_timer_falling -= 5
    else:
        timer_falling -= 1

    if trg:
        figure = Figure(choice(im))
        trg = 0
        fugire_counter += 1

    clock.tick(fps)

print('Your score', score)
pygame.quit()
