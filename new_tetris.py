import pygame
import numpy as np
from random import choice
import os
import keyboard

# переменные экрана

top = 70
left = 20
stack_height_cells = 20
stack_width_cells = 10
cell_size = 20
stack_width_px = stack_width_cells * cell_size + 150
stack_height_px = stack_height_cells * \
    cell_size + cell_size * 2 + top - cell_size

# переменная счёта

score = 0
score_history = [0]
best_score_history = [0]

# формирование игровых фигур

figures = np.array([np.array([1, 1, 1, 0, 1, 0]),
                    np.array([2, 2, 2, 2, 0, 0]),
                    np.array([3, 3, 3, 0, 0, 3]),
                    np.array([0, 4, 4, 4, 4, 0]),
                    np.array([5, 5, 0, 0, 5, 5]),
                    np.array([6, 6, 6, 6]),
                    np.array([7, 7, 7, 7])]
                   )

# инициализация игрового поля

pole = np.zeros(stack_width_cells
                * stack_height_cells).reshape(stack_height_cells, stack_width_cells)

# создание окна

pygame.init()
screen = pygame.display.set_mode((stack_width_px, stack_height_px))
clock = pygame.time.Clock()
fps = 60


# класс фигур


class Figure:
    def __init__(self, form):
        global figures, im, pole

        self.col = im.index(form) + 1  # цвет фигуры
        self.tr = 1  # флажок на остановку спрайта
        self.form = form  # форма спрайта
        self.coords = [0, 3]  # координаты фигуры

        # описание формы фигуры

        if form == 'I':
            self.points = figures[im.index(form)].reshape(1, 4)
        elif form == 'O':
            self.points = figures[im.index(form)].reshape(2, 2)
        else:
            self.points = figures[im.index(form)].reshape(2, 3)

        # отображение фигуры на игровом поле

        x, y = self.coords
        pole1 = self.points * pole[x:x
                                   + len(self.points), y:y + len(self.points[0])]
        if np.any(pole1):
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])] += self.points * 10
        else:
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])] += self.points

    # функция полной остановки фигуры

    def stop(self):
        self.tr = 0

    # функция, возвращающая цвет фигуры

    def get_col(self):
        return self.col

    # функция падения фигуры

    def falling(self):
        global pole, trg
        x, y = self.coords
        tr = 1
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                if (x + len(self.points)) + 1 <= stack_height_cells:
                    p = abs(pole[x + i + 1][y + j])
                    c = self.points[i][j]
                    if pole[x + i + 1][y + j] != self.col:
                        if (((p + 2) % (p + 1)) % 2 == 1 and ((c + 2) % (c + 1)) % 2 == 1) or self.tr == 0:
                            tr = 0  # локальный флажок на условие сдвига вниз фигуры
                else:
                    tr = 0
        if tr == 1:
            pole[x:x + len(self.points), y:y +
                 len(self.points[0])][pole[x:x + len(self.points), y:y + len(self.points[0])] == self.col] = 0
            x += 1
            self.coords[0] += 1
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])] += self.points
        else:
            pole[x:x + len(self.points), y:y +
                 len(self.points[0])][pole[x:x + len(self.points), y:y + len(self.points[0])] == self.col] = -self.col
            self.tr = 0
            trg = 1

    # функция сдвига фигуры влево

    def left(self):
        global pole
        x, y = self.coords
        tr = 1
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                if (y - 1) >= 0:
                    if pole[x + i][y + j - 1] != self.col and pole[x + i][y + j - 1] != 0 and self.points[i, j] == self.col:
                        tr = 0
                else:
                    tr = 0
        if tr:
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])][pole[x:x + len(self.points), y:y
                                           + len(self.points[0])] == self.col] = 0
            y -= 1
            self.coords[1] -= 1
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])] += self.points

    # функция сдвига фигуры вправо

    def right(self):
        global pole
        x, y = self.coords
        tr = 1
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                if (y + len(self.points[0]) + 1) <= stack_width_cells:
                    if pole[x + i][y + j + 1] != self.col and pole[x + i][y + j + 1] != 0 and self.points[i, j] == self.col:
                        tr = 0
                else:
                    tr = 0
        if tr:
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])][pole[x:x + len(self.points), y:y
                                           + len(self.points[0])] == self.col] = 0
            y += 1
            self.coords[1] += 1
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])] += self.points

    # функция поворота фигуры

    def rotate(self):
        global pole
        x, y = self.coords
        if self.tr:
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])][pole[x:x + len(self.points), y:y +
                                           len(self.points[0])] == self.col] = 0
            self.points = np.rot90(self.points, -1)
            if (y + len(self.points[0])) > stack_width_cells or (x + len(self.points)) > stack_height_cells:
                self.points = np.rot90(self.points)
                pole[x:x + len(self.points), y:y
                     + len(self.points[0])] += self.points
            else:
                pole1 = self.points * \
                    pole[x:x + len(self.points), y:y + len(self.points[0])]
                self.points = np.rot90(self.points)
                pole[x:x + len(self.points), y:y
                     + len(self.points[0])] += self.points
                if not(np.any(pole1)):
                    pole[x:x + len(self.points), y:y
                         + len(self.points[0])][pole[x:x + len(self.points), y:y +
                                                   len(self.points[0])] == self.col] = 0
                    self.points = np.rot90(self.points, -1)
                    if (y + len(self.points[0])) > stack_width_cells:
                        self.points = np.rot90(self.points)

                    pole[x:x + len(self.points), y:y
                         + len(self.points[0])] += self.points


# класс графического оформления игры


class Graphics:
    def __init__(self, sound_on=1, score=0, last_score=0, best_score=0):
        self.sound_on = sound_on
        self.icons_coords = {}
        self.score = score
        self.last_score = last_score
        self.best_score = best_score
        self.create_icons()

    # функция создания всех надписей и кнопок

    def create_icons(self):
        self.create_sound_icon()
        self.create_next_song_icon()
        self.create_prev_song_icon()
        self.create_new_game_icon()
        self.draw_title()
        self.draw_score()
        self.draw_next_figure()
        self.increase_volume()
        self.decrease_volume()
        self.draw_best_score()

    # функция отображения следующей фигуры

    def draw_next_figure(self):
        font_score = pygame.font.SysFont('Britannic', 16)
        next_figur = font_score.render('NEXT FIGURE:', 1, (255, 168, 0))
        x, y = self.icons_coords['numbers'][0] + \
            8, self.icons_coords['numbers'][1] + 80
        pygame.draw.line(screen, (255, 168, 0),
                         (x - 10, y - 10), (x + 100, y - 10))
        pygame.draw.line(screen, (255, 168, 0),
                         (x - 10, y + 105), (x + 100, y + 105))
        screen.blit(next_figur, (x, y))
        next_fig = next_figure(0)
        s = ['I', 'S', 'Z', 'T', 'O', 'L', 'J']
        sp = [(x + 3, y + 60), (x + 15, y + 50), (x + 15, y + 50), (x
                                                                    + 15, y + 50), (x + 30, y + 50), (x + 20, y + 50), (x + 20, y + 50)]
        fullname = next_fig + '_fig.PNG'
        image = load_image(fullname)
        screen.blit(image, sp[s.index(next_fig)])

    # функция вывода счёта

    def draw_score(self):
        num_str = str(self.score)
        if len(num_str) < 7:
            num_str = num_str.rjust(7, '0')
        x = left + (stack_width_cells + 1) * cell_size + 10
        y = top - 60
        font_score = pygame.font.SysFont('Britannic', 30)
        score = font_score.render('SCORE:', 1, (255, 168, 0))
        screen.blit(score, (x, y))
        font_score = pygame.font.SysFont('Britannic', 24)
        numbers = font_score.render(f'{num_str}', 1, (255, 168, 0))
        screen.blit(numbers, (x - 7, y + 40))
        self.icons_coords['score'] = (x, y)
        self.icons_coords['numbers'] = (x - 7, y + 40)

    def draw_best_score(self):
        num_str = str(self.last_score)
        best_score_str = str(self.best_score).rjust(7, '0')
        num_str = num_str.rjust(7, '0')
        x = left + (stack_width_cells + 1) * cell_size + 12
        y = top + 175
        font_score = pygame.font.SysFont('Britannic', 16)
        last_score = font_score.render('LAST SCORE:', 1, (255, 168, 0))
        screen.blit(last_score, (x, y))
        font_score = pygame.font.SysFont('Britannic', 16)
        numbers = font_score.render(f'{str(num_str)}', 1, (255, 168, 0))
        screen.blit(numbers, (x + 12, y + 20))
        pygame.draw.line(screen, (255, 168, 0),
                         (x - 11, y + 45), (x + 100, y + 45))
        best_score = font_score.render('BEST SCORE:', 1, (255, 168, 0))
        numbers = font_score.render(f'{str(best_score_str)}', 1, (255, 168, 0))
        screen.blit(best_score, (x, y + 60))
        screen.blit(numbers, (x + 12, y + 80))
        pygame.draw.line(screen, (255, 168, 0),
                         (x - 11, y + 105), (x + 100, y + 105))

    # функция отрисовки названия игры

    def draw_title(self):
        image_x = 90
        self.title = load_image('title.PNG')
        x = 5
        y = 5
        screen.blit(self.title, (x, y, x + image_x, top))

    # функция создания кнопки новой игры

    def create_new_game_icon(self):
        image_x = 90
        image_y = 40
        self.new_game_icon = load_image('new_game.png')
        x, y = self.icons_coords['prev_song'][0], self.icons_coords['prev_song'][1] - 50
        screen.blit(self.new_game_icon, (x, y, x + image_x, y + image_y))
        self.icons_coords['new_game'] = (
            x, y + 10, x + image_x, y + image_y - 10)

    # функция создания кнопки включения и отключения звука

    def create_sound_icon(self):
        image_x = 30
        image_y = 30
        x = left + stack_width_cells * cell_size + 3 * cell_size
        y = top + (stack_height_cells - 3) * cell_size
        if self.sound_on % 2:
            self.sound_icon = load_image('sound.png')
            screen.blit(self.sound_icon, (x, y))
            pygame.mixer.music.unpause()
        else:
            self.sound_icon = load_image('sound_off.png')
            screen.blit(self.sound_icon, (x, y))
            pygame.mixer.music.pause()
        self.icons_coords['sound'] = (x, y, x + image_x, y + image_y)

    # функция создания кнопки переключения музыки вперёд

    def create_next_song_icon(self):
        image_x = 20
        image_y = 20
        self.next_song_icon = load_image('next_song.png')
        x = self.icons_coords['sound'][2] + 10
        y = self.icons_coords['sound'][1] + 5
        screen.blit(self.next_song_icon, (x, y, x + image_x, y + image_y))
        self.icons_coords['next_song'] = (x, y, x + image_x, y + image_y)

    # функция создания кнопки переключения музыки назад

    def create_prev_song_icon(self):
        image_x = 20
        image_y = 20
        self.prev_song_icon = load_image('prev_song.png')
        x = self.icons_coords['sound'][0] - image_x - 10
        y = self.icons_coords['sound'][1] + 5
        screen.blit(self.prev_song_icon, (x, y, x + image_x, y + image_y))
        self.icons_coords['prev_song'] = (x, y, x + image_x, y + image_y)

    # функция смены музыки

    def change_music(self, i):
        fullname = os.path.join('data', f'music{i % 7}.mp3')
        pygame.mixer.music.load(fullname)
        pygame.mixer.music.play(-1)

    def increase_volume(self):
        image_x = 20
        image_y = 20
        self.increase_volume_icon = load_image('increase_volume.png')
        x = self.icons_coords['prev_song'][0] + 10
        y = self.icons_coords['prev_song'][1] + 30
        screen.blit(self.increase_volume_icon,
                    (x, y, x + image_x, y + image_y))
        self.icons_coords['increase_volume'] = (x, y, x + image_x, y + image_y)

    def decrease_volume(self):
        image_x = 20
        image_y = 5
        self.decrease_volume_icon = load_image('decrease_volume.png')
        x = self.icons_coords['increase_volume'][0] + 45
        y = self.icons_coords['increase_volume'][1] + 8
        screen.blit(self.decrease_volume_icon,
                    (x, y, x + image_x, y + image_y))
        self.icons_coords['decrease_volume'] = (x, y, x + image_x, y + image_y)

    # функция, возвращающая положение объекта

    def get_coords(self):
        return self.icons_coords


# функция удаление полных слоёв


def checkout():
    global pole, score
    k = 0
    for i in range(stack_height_cells):
        p = 1
        tr = 1
        for j in range(stack_width_cells):
            p *= pole[i][j]
            if pole[i][j] > 0:
                tr = 0
        if tr and p != 0:
            pole = np.delete(pole, i, 0)
            pole = np.insert(pole, 0, [0 for i in range(stack_width_cells)]).reshape(
                stack_height_cells, stack_width_cells)
            k += 1
    sc = [100, 300, 700, 1500, 3100, 6300, 12500, 25100]
    if k > 0:
        score += sc[k - 1]


# функция начала новой игры


def new_game():
    global pole, score, trr, im, available_figures, next_figures, last_score, tt
    available_figures = im.copy()
    next_figures = []
    next_figures.append(choice(available_figures))
    available_figures.remove(next_figures[0])
    next_figures.append(choice(available_figures))
    available_figures.remove(next_figures[1])
    available_figures.append(next_figures[0])

    figure.stop()
    trr = 1
    tt = 1
    pole = np.zeros(stack_width_cells *
                    stack_height_cells).reshape(stack_height_cells, stack_width_cells)
    max_timer_falling = 60
    max_figure_counter = 5

    score_history.append(score)
    if score > best_score_history[-1]:
        best_score_history.append(score)

    score = 0

# функция отрисовки экрана


def render():
    screen.fill(pygame.Color('black'))
    fig_col = [(205, 0, 205), (255, 140, 15), (20, 15, 255),
               (105, 255, 0), (255, 5, 0), (0, 255, 255), (245, 220, 10)]
    for i in range(27):
        fig_col.append((0, 0, 0))
    for i in range(stack_height_cells):
        for j in range(stack_width_cells):
            if int(pole[i, j]) == 0:
                pygame.draw.rect(screen, pygame.Color('white'), (left + j * cell_size + 1,
                                                                 top + i * cell_size + 1, cell_size - 2, cell_size - 2), 0)
            elif abs(int(pole[i, j])) < 8:
                pygame.draw.rect(screen, fig_col[abs(int(pole[i, j])) - 1], (left + j * cell_size + 1,
                                                                             top + i * cell_size + 1, cell_size - 2, cell_size - 2), 0)
            else:
                pygame.draw.rect(screen, pygame.Color('black'), (left + j * cell_size + 1,
                                                                 top + i * cell_size + 1, cell_size - 2, cell_size - 2), 0)

# функция отрислвки краёв игрового поля


def draw_border():
    color = (80, 80, 80)
    for i in range(stack_height_cells + 2):
        pygame.draw.rect(screen, color, (left - cell_size,
                                         top - cell_size + cell_size * i + 1, cell_size - 1, cell_size - 2), 0)
    for i in range(stack_height_cells + 2):
        pygame.draw.rect(screen, color, (left + cell_size * stack_width_cells + 1,
                                         top - cell_size + cell_size * i + 1, cell_size - 1, cell_size - 2), 0)

    for i in range(stack_width_cells):
        pygame.draw.rect(screen, color, (left + cell_size * i + 1,
                                         top - cell_size + 1, cell_size - 2, cell_size - 2), 0)

    for i in range(stack_width_cells):
        pygame.draw.rect(screen, color, (left + cell_size * i + 1,
                                         top + stack_height_cells * cell_size + 1, cell_size - 2, cell_size - 2), 0)


# функция, возвращающая форму следующей фигуры


def next_figure(i):
    return next_figures[i]


# функция загрузки изображения


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


# функция движения фигуры по горизонтали


def move(e):
    if tt:
        if e.event_type == 'down':
            if e.name == 'left':
                figure.left()
            if e.name == 'right':
                figure.right()


keyboard.hook(move)

# создание цикла фигур, без 2 одинаковых подряд

im = ['T', 'L', 'J', 'S', 'Z', 'I', 'O']

available_figures = im.copy()
next_figures = []

next_figures.append(choice(available_figures))
available_figures.remove(next_figures[0])
next_figures.append(choice(available_figures))
available_figures.remove(next_figures[1])
available_figures.append(next_figures[0])

# загрузка музыки

i = 0
volume = 0.3
fullname = os.path.join('data', f'music{i}.mp3')
pygame.mixer.music.load(fullname)
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(volume)
sound_on = 0
icons_coords = Graphics().get_coords()

# задание игровый параметров

figure_counter = 0
timer_falling = 0
max_timer_falling = 60
timer_move = 0
max_figure_counter = 5

t = 1
tt = 1
trg = 1  # флажок на ограничение количества объектов на поле одновремено
trr = 1  # флажок на полную остановку игры
run = True
while run:
    pygame.display.flip()
    render()
    draw_border()
    Graphics(sound_on, score, score_history[-1], best_score_history[-1])

    checkout()

    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_n:
                new_game()
            if event.key == pygame.K_p:
                tt = 1 - tt
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                x, y = event.pos
                coords = icons_coords['sound']
                if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
                    sound_on += 1
                coords = icons_coords['next_song']
                if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
                    i += 1
                    Graphics().change_music(i)
                coords = icons_coords['prev_song']
                if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
                    i -= 1
                    Graphics().change_music(i)
                coords = icons_coords['new_game']
                if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
                    new_game()
                coords = icons_coords['increase_volume']
                if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
                    if volume <= 0.9:
                        volume += 0.1
                        pygame.mixer.music.set_volume(volume)
                coords = icons_coords['decrease_volume']
                if coords[0] <= x <= coords[2] and coords[1] <= y <= coords[3]:
                    if 0.1 < volume:
                        volume -= 0.1
                        pygame.mixer.music.set_volume(volume)

    if tt:
        timer_move += 1

        if key[pygame.K_UP] and timer_move > 10:
            figure.rotate()
            timer_move = 0
        if key[pygame.K_DOWN] and timer_move > 5 and trr:
            timer_move = 0
            timer_falling = -1
            score += 1

        a = pole > 7
        if np.any(a):
            trr = 0

        if trg and trr:
            figure = Figure(next_figures.pop(0))
            next_figures.append(choice(available_figures))
            available_figures.remove(next_figures[1])
            available_figures.append(next_figures[0])
            trg = 0
            figure_counter += 1

        if timer_falling < 0:
            timer_falling = max_timer_falling
            figure.falling()
            if figure_counter > max_figure_counter:
                figure_counter = 0
                max_timer_falling -= 5
                max_figure_counter += 2
        else:
            timer_falling -= 1

    clock.tick(fps)

pygame.quit()
