import pygame
import keyboard
import numpy as np
import os
from random import choice

# переменные экрана

top = 70
left = 20
stack_height_cells = 20
stack_width_cells = 10
cell_size = 20
stack_width_px = stack_width_cells * cell_size + 150
stack_height_px = stack_height_cells * \
    cell_size + cell_size * 2 + top - cell_size

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

pole = np.zeros(stack_width_cells *
                stack_height_cells).reshape(stack_height_cells, stack_width_cells)

# создание окна

pygame.init()
screen = pygame.display.set_mode((stack_width_px, stack_height_px))
screen.fill(pygame.Color('black'))
clock = pygame.time.Clock()
fps = 60


# класс спрайтов


class Figure:
    def __init__(self, form):
        global figures, im, pole

        self.col = im.index(form)
        self.tr = 1  # флажок на остановку спрайта
        self.form = form  # форма спрайта
        self.coords = [0, 3]

        # описание формы спрайтаы

        if form == 'I':
            self.points = figures[im.index(form)].reshape(1, 4)
        elif form == 'O':
            self.points = figures[im.index(form)].reshape(2, 2)
        else:
            self.points = figures[im.index(form)].reshape(2, 3)

        x, y = self.coords
        pole[x:x + len(self.points), y:y + len(self.points[0])] += self.points

    def stop(self):
        self.tr = 0

    def get_col(self):
        return self.col

    # функция падения спрайта

    def falling(self):
        global pole, trg
        x, y = self.coords
        tr = 1
        for i in range(len(self.points)):
            for j in range(len(self.points[i])):
                if (x + len(self.points)) + 1 <= stack_height_cells:
                    if ((pole[x + i + 1][y + j] == 3 or pole[x + i + 1][y + j] == 2) and self.points[i][j] == 1) or self.tr == 0:
                        tr = 0  # локальный флажок на условие сдвига вниз спрайта
                else:
                    tr = 0
        if tr == 1:
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])][pole[x:x + len(self.points), y:y + len(self.points[0])] == 1] = 0
            x += 1
            self.coords[0] += 1
            pole[x:x + len(self.points), y:y +
                 len(self.points[0])] += self.points
        else:
            pole[x:x + len(self.points), y:y
                 + len(self.points[0])][pole[x:x + len(self.points), y:y +
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
            pole[x:x + len(self.points), y:y +
                 len(self.points[0])][pole[x:x + len(self.points), y:y +
                                           len(self.points[0])] == 1] = 0
            y -= 1
            self.coords[1] -= 1
            pole[x:x + len(self.points), y:y +
                 len(self.points[0])] += self.points

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
            pole[x:x + len(self.points), y:y +
                 len(self.points[0])][pole[x:x + len(self.points), y:y +
                                           len(self.points[0])] == 1] = 0
            y += 1
            self.coords[1] += 1
            pole[x:x + len(self.points), y:y +
                 len(self.points[0])] += self.points

    # функция поворота спрайта

    def rotate(self):
        global pole
        x, y = self.coords
        pole[x:x + len(self.points), y:y +
             len(self.points[0])][pole[x:x + len(self.points), y:y +
                                         len(self.points[0])] == 1] = 0
        self.points = np.rot90(self.points, -1)
        if (y + len(self.points[0])) > stack_width_cells or (x + len(self.points)) > stack_height_cells:
            self.points = np.rot90(self.points)
            pole[x:x + len(self.points), y:y +
                 len(self.points[0])] += self.points
        else:
            pole1 = self.points + \
                pole[x:x + len(self.points), y:y + len(self.points[0])]
            self.points = np.rot90(self.points)
            pole[x:x + len(self.points), y:y +
                 len(self.points[0])] += self.points
            if not(3 in pole1):
                pole[x:x + len(self.points), y:y +
                     len(self.points[0])][pole[x:x + len(self.points), y:y +
                                                 len(self.points[0])] == 1] = 0
                self.points = np.rot90(self.points, -1)
                if (y + len(self.points[0])) > stack_width_cells:
                    self.points = np.rot90(self.points)

                pole[x:x + len(self.points), y:y +
                     len(self.points[0])] += self.points


class Graphics:
    def __init__(self, sound_on=1, score=0):
        self.sound_on = sound_on
        self.icons_coords = {}
        self.score = score
        self.create_icons()

    def create_icons(self):
        self.create_sound_icon()
        self.create_next_song_icon()
        self.create_prev_song_icon()
        self.create_new_game_icon()
        self.draw_title()
        self.draw_score()
        self.draw_next_figure()

    def draw_next_figure(self):
        font_score = pygame.font.SysFont('Britannic', 16)
        next_figur = font_score.render('NEXT FIGURE:', 1, (255, 168, 0))
        x, y = self.icons_coords['numbers'][0] + \
            8, self.icons_coords['numbers'][1] + 80
        screen.blit(next_figur, (x, y))
        next_fig = next_figure(0)
        s = ['I', 'S', 'Z', 'T', 'O', 'L', 'J']
        sp = [(x + 15, y + 60), (x + 15, y + 50), (x + 15, y + 50), (x +
                                                                     15, y + 50), (x + 30, y + 50), (x + 20, y + 50), (x + 20, y + 50)]
        fullname = next_fig + '_fig.PNG'
        image = load_image(fullname)
        screen.blit(image, sp[s.index(next_fig)])
        # if next_fig == 'I':
        #     image = load_image('I_fig.PNG')
        #     screen.blit(image, (x + 15, y + 60))
        # elif next_fig == 'S':
        #     image = load_image('S_fig.PNG')
        #     screen.blit(image, (x + 15, y + 50))
        # elif next_fig == 'Z':
        #     image = load_image('Z_fig.PNG')
        #     screen.blit(image, (x + 15, y + 50))
        # elif next_fig == 'T':
        #     image = load_image('T_fig.PNG')
        #     screen.blit(image, (x + 15, y + 50))
        # elif next_fig == 'O':
        #     image = load_image('O_fig.PNG')
        #     screen.blit(image, (x + 30, y + 50))
        # elif next_fig == 'L':
        #     image = load_image('L_fig.PNG')
        #     screen.blit(image, (x + 20, y + 50))
        # elif next_fig == 'J':
        #     image = load_image('J_fig.PNG')
        #     screen.blit(image, (x + 20, y + 50))

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

    def draw_title(self):
        image_x = 90
        self.title = load_image('title.PNG')
        x = 5
        y = 5
        screen.blit(self.title, (x, y, x + image_x, top))

    def create_new_game_icon(self):
        image_x = 90
        image_y = 40
        self.new_game_icon = load_image('new_game.png')
        x, y = self.icons_coords['prev_song'][0], self.icons_coords['prev_song'][1] - 50
        screen.blit(self.new_game_icon, (x, y, x + image_x, y + image_y))
        self.icons_coords['new_game'] = (
            x, y + 10, x + image_x, y + image_y - 10)

    def create_sound_icon(self):
        image_x = 30
        image_y = 30
        x = left + stack_width_cells * cell_size + 3 * cell_size
        y = top + (stack_height_cells - 3) * cell_size
        if self.sound_on % 2:
            self.sound_icon = load_image('sound.png')
            screen.blit(self.sound_icon, (x, y))
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.unpause()
        else:
            self.sound_icon = load_image('sound_off.png')
            screen.blit(self.sound_icon, (x, y))
            pygame.mixer.music.pause()
        self.icons_coords['sound'] = (x, y, x + image_x, y + image_y)

    def create_next_song_icon(self):
        image_x = 20
        image_y = 20
        self.next_song_icon = load_image('next_song.png')
        x = self.icons_coords['sound'][2] + 10
        y = self.icons_coords['sound'][1] + 5
        screen.blit(self.next_song_icon, (x, y, x + image_x, y + image_y))
        self.icons_coords['next_song'] = (x, y, x + image_x, y + image_y)

    def create_prev_song_icon(self):
        image_x = 20
        image_y = 20
        self.prev_song_icon = load_image('prev_song.png')
        x = self.icons_coords['sound'][0] - image_x - 10
        y = self.icons_coords['sound'][1] + 5
        screen.blit(self.prev_song_icon, (x, y, x + image_x, y + image_y))
        self.icons_coords['prev_song'] = (x, y, x + image_x, y + image_y)

    def change_music(self, i):
        fullname = os.path.join('data', f'music{i % 7}.mp3')
        pygame.mixer.music.load(fullname)
        pygame.mixer.music.play(-1)

    def get_coords(self):
        return self.icons_coords

# удаление полных слоёв


def checkout():
    global pole, score
    k = 0
    for i in range(stack_height_cells):
        if sum(pole[i]) == stack_width_cells * 2:
            pole = np.delete(pole, i, 0)
            pole = np.insert(pole, 0, [0 for i in range(stack_width_cells)]).reshape(
                stack_height_cells, stack_width_cells)
            k += 1
    sc = [100, 300, 700, 1500]
    if k > 0:
        score += sc[k - 1]


def new_game():
    global pole, score
    figure.stop()
    pole = np.zeros(stack_width_cells
                    * stack_height_cells).reshape(stack_height_cells, stack_width_cells)
    max_timer_falling = 60
    score = 0


# фуdнкция отрисовки экрана


def render():
    screen.fill(pygame.Color('black'))
    col = ['white', 'green', 'black', 'red',
           'black', 'orange', 'blue', 'purple']
    fig_col = ['purple', 'orange', 'dark blue',
               'green', 'red', 'blue', 'yellow']
    for i in range(stack_height_cells):
        for j in range(stack_width_cells):
            if int(pole[i, j]) == 1:
                pygame.draw.rect(screen, pygame.Color(fig_col[figure.get_col()]), (left + j * cell_size + 1,
                                                                                   top + i * cell_size + 1, cell_size - 2, cell_size - 2), 0)
            else:
                pygame.draw.rect(screen, pygame.Color(col[int(pole[i, j])]), (left + j * cell_size + 1,
                                                                              top + i * cell_size + 1, cell_size - 2, cell_size - 2), 0)


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


def next_figure(i):
    return next_figures[i]


def load_image(name):
    fullname = os.path.join('data', name)
    image = pygame.image.load(fullname)
    image = image.convert_alpha()
    return image


def move(e):
    if e.event_type == 'down':
        if e.name == 'left':
            figure.left()
        if e.name == 'right':
            figure.right()


keyboard.hook(move)

im = ['T', 'L', 'J', 'S', 'Z', 'I', 'O']


available_figures = im.copy()
next_figures = []


next_figures.append(choice(available_figures))
available_figures.remove(next_figures[0])
next_figures.append(choice(available_figures))
available_figures.remove(next_figures[1])
available_figures.append(next_figures[0])


i = 0
fullname = os.path.join('data', f'music{i}.mp3')
pygame.mixer.music.load(fullname)
pygame.mixer.music.play(-1)
sound_on = 0
icons_coords = Graphics().get_coords()


fugire_counter = 0
timer_falling = 0
max_timer_falling = 60
timer_move = 0
max_fugire_counter = 5
trg = 1  # флажок на ограничение количества объектов на поле одновремено
run = True
while run:
    render()
    draw_border()
    Graphics(sound_on, score)
    pygame.display.flip()

    timer_move += 1

    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if event.type == pygame.QUIT:
            run = False
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
    # if key[pygame.K_LEFT] and timer_move > 5:
    #     figure.left()
    #     timer_move = 0
    # if key[pygame.K_RIGHT] and timer_move > 5:
    #     figure.right()
    #     timer_move = 0
    if key[pygame.K_UP] and timer_move > 10:
        figure.rotate()
        timer_move = 0
    if key[pygame.K_DOWN] and timer_move > 5:
        timer_move = 0
        timer_falling = -1
    if key[pygame.K_n]:
        new_game()
    if (3 in pole) or (4 in pole) or (5 in pole):
        pygame.time.wait(2000)
        new_game()
    # if mouse[0] and timer_move > 5:
    #     figure.left()
    #     timer_move = 0
    # if mouse[2] and timer_move > 5:
    #     figure.right()
    #     timer_move = 0
    # if mouse[1] and timer_move > 5:
    #     timer_move = 0
    #     timer_falling = -1

    if trg:
        figure = Figure(next_figures.pop(0))
        next_figures.append(choice(available_figures))
        available_figures.remove(next_figures[1])
        available_figures.append(next_figures[0])
        trg = 0
        fugire_counter += 1

    if timer_falling < 0:
        timer_falling = max_timer_falling
        figure.falling()
        if fugire_counter > max_fugire_counter:
            fugire_counter = 0
            max_timer_falling -= 5
            max_fugire_counter += 2
    else:
        timer_falling -= 1

    checkout()
    clock.tick(fps)
    # keyboard.wait()
pygame.quit()
