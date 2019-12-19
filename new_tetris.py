import pygame
import numpy as np
from random import choice

# переменный экрана

stack_height_cells = 20
stack_width_cells = 14
cell_size = 20
stack_width_px = stack_width_cells * cell_size
stack_height_px = stack_height_cells * cell_size

score = 0

figures = np.array([np.array([1, 1, 1, 0, 1, 0]),
                    np.array([1, 1, 1, 1, 0, 0]),
                    np.array([1, 1, 1, 0, 0, 1]),
                    np.array([0, 1, 1, 1, 1, 0]),
                    np.array([1, 1, 0, 0, 1, 1]),
                    np.array([1, 1, 1, 1]),
                    np.array([1, 1, 1, 1])]
                   )

# инициализация игрового поля

pole = np.zeros(stack_width_cells
                * stack_height_cells).reshape(stack_height_cells, stack_width_cells)

# создание рамок игрового поля

# for i in range(stack_height_cells):
#     pole[i][0] = 3
#     pole[i][stack_width_cells - 1] = 3
# for i in range(stack_width_cells):
#     pole[stack_height_cells - 1][i] = 3

s_o = pole[0][:]

# создание окна

pygame.init()
screen = pygame.display.set_mode((stack_width_px, stack_height_px))
screen.fill(pygame.Color('black'))
clock = pygame.time.Clock()
fps = 60


# класс спрайтов


class Figure:
    def __init__(self, form):
        global figures, im

        self.tr = 1  # флажок на остановку спрайта
        self.form = form  # форма спрайта
        self.coords = [0, 2]

        # описание формы спрайтаы

        if form == 'I':
            self.points = figures[im.index(form)].reshape(1, 4)
        elif form == 'O':
            self.points = figures[im.index(form)].reshape(2, 2)
        else:
            self.points = figures[im.index(form)].reshape(2, 3)

    # функция падения спрайта

    def falling(self):
        global pole, trg
        x, y = self.coords
        tr = 1
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                if (x + len(self.points)) + 1 <= stack_height_cells:
                    if (pole[x + i + 1][y + j] == 3 or pole[x + i + 1][y + j] == 2 or self.tr == 0) and self.points[i][j] == 1:
                        tr = 0  # локальный флажок на условие сдвига вниз спрайта
                else:
                    tr = 0
        if tr == 1:
            print(pole[x:x + len(self.points), y:y + len(self.points[0])])
            pole[x:x + len(self.points), y:y +
                 len(self.points[0])][pole[x:x + len(self.points), y:y +
                                           len(self.points[0])] == 1] = 0
            x += 1
            self.coords[0] += 1
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])] += self.points
        else:
            pole[x:x + len(self.points), y:y +
                 len(self.points[0])][pole[x:x + len(self.points), y:y +
                                             len(self.points[0])] == 1] = 2
            self.tr = 0
            trg = 1

    # функция сдвига спрайта влево

    def left(self):
        global pole
        x, y = self.coords
        tr = 1
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                if (y - 1) >= 0:
                    if pole[x + i][y + j - 1] != 1 and pole[x + i][y + j - 1] != 0 and self.points[i, j] == 1:
                        tr = 0
                else:
                    tr = 0
        if tr:
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])][pole[x:x + len(self.points), y:y
                                           + len(self.points[0])] == 1] = 0
            y -= 1
            self.coords[1] -= 1
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])] += self.points

    # функция сдвига спрайта вправо

    def right(self):
        global pole
        x, y = self.coords
        tr = 1
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                if (y + len(self.points[0]) + 1) <= stack_width_cells:
                    if pole[x + i][y + j + 1] != 1 and pole[x + i][y + j + 1] != 0 and self.points[i, j] == 1:
                        tr = 0
                else:
                    tr = 0
        if tr:
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])][pole[x:x + len(self.points), y:y
                                           + len(self.points[0])] == 1] = 0
            y += 1
            self.coords[1] += 1
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])] += self.points

    # функция поворота спрайта

    def rotate(self):
        global pole
        x, y = self.coords
        pole[x:x + len(self.points), y:y
             + len(self.points[0])][pole[x:x + len(self.points), y:y +
                                       len(self.points[0])] == 1] = 0
        self.points = np.rot90(self.points, -1)
        if len(self.points[0]) == 5:
            if (y - 2) > stack_width_cells:
                self.points = np.rot90(self.points)

            pole[x:x + len(self.points), y:y
                 + len(self.points[0])] += self.points
        else:
            if (y + len(self.points[0])) > stack_width_cells:
                self.points = np.rot90(self.points)

            pole[x:x + len(self.points), y:y
                 + len(self.points[0])] += self.points

    # удаление полных слоёв

    def checkout(self):
        global pole, stack_height_cells, stack_width_cells, score, s_o
        newpole = []
        sp = []
        tr = 0
        for i in range(stack_height_cells):
            if sum(pole[i]) == stack_width_cells * 2:
                tr = 1
                sp.append(i)
        if tr == 1:
            for i in range(len(sp)):
                newpole.append(s_o)
                score += 100
            for i in range(stack_height_cells):
                if sum(pole[i]) != stack_width_cells * 2 and not(i in sp):
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
                pygame.draw.rect(screen, pygame.Color('white'), (j * cell_size + 1,
                                                                 i * cell_size + 1, cell_size - 2, cell_size - 2), 0)
            elif pole[i][j] == 2:
                pygame.draw.rect(screen, pygame.Color('yellow'), (j * cell_size + 1,
                                                                  i * cell_size + 1, cell_size - 2, cell_size - 2), 0)
            elif pole[i][j] == 3:
                pygame.draw.rect(screen, pygame.Color('red'), (j * cell_size + 1,
                                                               i * cell_size + 1, cell_size - 2, cell_size - 2), 0)


im = ('T', 'L', 'J', 'S', 'Z', 'I', 'O')

fugire_counter = 0
timer_falling = 0
max_timer_falling = 60
timer_move = 0

trg = 1  # флажок на ограничение количества объектов на поле одновремено
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
