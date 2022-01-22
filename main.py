import sys
import pygame
import os.path


SPRITES = [pygame.image.load('images/flower_3.jpg'), pygame.image.load('images/flower_3.jpg'),
           pygame.image.load('images/wall2.jpg'), pygame.image.load('images/grass_4.jpg'),
           pygame.image.load('images/bee_forward.jpg'), pygame.image.load('images/bee_back.jpg'),
           pygame.image.load('images/bee_right.jpg'), pygame.image.load('images/bee_left.jpg')]
WINDOW = 1
NEXT_LEVEL = 1
FLAG = False
FLAG1 = False
PLAYER_NICKNAME = 'player'
FAILS_QUANTITY = 0
VOLUME = 0.3


class Game:
    def __init__(self):
        self.bee_pos = (0, 0)
        self.board = ''
        self.new_board = []
        self.board_with_bee = []
        self.finish_cord = (0, 0)
        self.death_cord = (0, 0)
        self.left = 10
        self.top = 10
        self.cell_size = 50
        self.width = 0
        self.height = 0
        self.sides = (0, 0)
        self.load_level()

    def set_view(self, cell_size, size):
        self.left = (size[0] - (cell_size * self.width)) // 2
        self.top = (size[1] - (cell_size * self.height)) // 2 - ((size[1] - (cell_size * self.height)) // 8)
        self.cell_size = cell_size

    def changing_level(self):
        global WINDOW, NEXT_LEVEL, FLAG
        WINDOW = 2
        if NEXT_LEVEL < 6:
            NEXT_LEVEL += 1
        else:
            WINDOW = 7
        FLAG = False
        main()

    def restart_level(self):
        global FLAG1, WINDOW, FAILS_QUANTITY
        FLAG1 = False
        WINDOW = 5
        FAILS_QUANTITY += 1
        main()

    def load_level(self):
        map_data = []
        with open(f'levels/level_{NEXT_LEVEL}.txt', 'rt') as f:
            for line in f:
                map_data.append(line)
            self.sides = self.height, self.width = int(map_data[0].split()[0]), int(map_data[0].split()[1])
            s = []
            self.board_with_bee = []
            for i in map_data[1].split():
                for j in list(i):
                    s.append(int(j))
                self.board_with_bee.append(s)
                s = []
            self.board = []
            for i in map_data[2].split():
                for j in list(i):
                    s.append(int(j))
                self.board.append(s)
                s = []
            self.board = str(self.board)
            self.bee_pos = int(map_data[3].split()[0]), int(map_data[3].split()[1])
            self.finish_cord = int(map_data[4].split()[0]), int(map_data[4].split()[1])
            self.death_cord = []
            for i in map_data[5].split():
                self.death_cord.append((int(i.split(';')[0]), int(i.split(';')[1])))

    def render(self, screen):
        for y in range(self.height):
            for x in range(self.width):
                sun_rect = SPRITES[self.board_with_bee[y][x]].get_rect(topleft=(x * self.cell_size + self.left,
                                                                                y * self.cell_size + self.top))
                screen.blit(SPRITES[self.board_with_bee[y][x]], sun_rect)
        pygame.draw.rect(screen, (0, 0, 0), (self.left - 2, self.top - 2,
                                             (self.width * self.cell_size) + 4,
                                             self.height * self.cell_size + 4), 4)

    def transfer(self):
        f1, self.new_board = [], []
        for i in self.board[2:-2].split('], ['):
            for j in i.split(', '):
                f1.append(int(j))
            self.new_board.append(f1)
            f1 = []

    def sides_check(self, move):
        if move == 'forward_move':
            new_bee_pos = (self.bee_pos[0] - 1, self.bee_pos[1])
        elif move == 'back_move':
            new_bee_pos = (self.bee_pos[0] + 1, self.bee_pos[1])
        elif move == 'right_move':
            new_bee_pos = (self.bee_pos[0], self.bee_pos[1] + 1)
        elif move == 'left_move':
            new_bee_pos = (self.bee_pos[0], self.bee_pos[1] - 1)
        if (new_bee_pos[0]) >= 0 and new_bee_pos[1] >= 0 and new_bee_pos[0] < self.sides[0] and\
                new_bee_pos[1] < self.sides[1]:
            return True
        else:
            return False

    def position_check(self):
        global FLAG, FLAG1
        if self.bee_pos == self.finish_cord:
            FLAG = True
        for i in self.death_cord:
            if self.bee_pos == i:
                FLAG1 = True

    def forward_moving(self):
        self.transfer()
        if self.sides_check('forward_move'):
            if self.new_board[(self.bee_pos[0] - 1)][(self.bee_pos[1])] != 2:
                self.bee_pos = (self.bee_pos[0] - 1, self.bee_pos[1])
        self.board_with_bee = self.new_board
        self.board_with_bee[self.bee_pos[0]][self.bee_pos[1]] = 4
        self.position_check()

    def back_moving(self):
        self.transfer()
        if self.sides_check('back_move'):
            if self.new_board[(self.bee_pos[0] + 1)][(self.bee_pos[1])] != 2:
                self.bee_pos = (self.bee_pos[0] + 1, self.bee_pos[1])
        self.board_with_bee = self.new_board
        self.board_with_bee[self.bee_pos[0]][self.bee_pos[1]] = 5
        self.position_check()

    def right_moving(self):
        self.transfer()
        if self.sides_check('right_move'):
            if self.new_board[(self.bee_pos[0])][(self.bee_pos[1] + 1)] != 2:
                self.bee_pos = (self.bee_pos[0], self.bee_pos[1] + 1)
        self.board_with_bee = self.new_board
        self.board_with_bee[self.bee_pos[0]][self.bee_pos[1]] = 6
        self.position_check()

    def left_moving(self):
        self.transfer()
        if self.sides_check('left_move'):
            if self.new_board[(self.bee_pos[0])][(self.bee_pos[1] - 1)] != 2:
                self.bee_pos = (self.bee_pos[0], self.bee_pos[1] - 1)
        self.board_with_bee = self.new_board
        self.board_with_bee[self.bee_pos[0]][self.bee_pos[1]] = 7
        self.position_check()

    def choosing_a_direction(self, direction):
        if direction == 'forward':
            self.forward_moving()
        if direction == 'back':
            self.back_moving()
        if direction == 'right':
            self.right_moving()
        if direction == 'left':
            self.left_moving()
        if direction == 'X':
            self.left_moving()


def load_image(name, color_key=None, folder=None):
    fullname = ''
    if folder == 'window_fons':
        fullname = os.path.join('images', 'window_fons', name)
    elif folder == 'level_animation':
        fullname = os.path.join('images', 'level_animation', name)
    elif folder == 'level_intro':
        fullname = os.path.join('images', 'level_intro', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image', name)
        raise SystemExit(message)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


all_sprites = pygame.sprite.Group()


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        global all_sprites
        all_sprites = pygame.sprite.Group()
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


def music(settings):
    pygame.mixer.music.load('music/game_fon_music.ogg')
    if settings:
        pygame.mixer.music.play(-1)
    else:
        pygame.mixer.music.stop()
    pygame.mixer.music.set_volume(VOLUME)


def music_volume(tuning):
    global VOLUME
    if tuning == 'up':
        VOLUME += 0.1
        pygame.mixer.music.set_volume(VOLUME)
    if tuning == 'low':
        VOLUME -= 0.1
        pygame.mixer.music.set_volume(VOLUME)


def text_output(text_coord, intro_text, font, screen):
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)


def terminate():
    pygame.quit()
    sys.exit()


def main():
    if WINDOW == 1:
        start_window()
    if WINDOW == 2:
        level_start_window()
    if WINDOW == 3:
        animation_window()
    if WINDOW == 4:
        game_window()
    if WINDOW == 5:
        level_lose_window()
    if WINDOW == 6:
        registration_window()
    if WINDOW == 7:
        finish_window()
    if WINDOW == 8:
        info_window()


def start_window():
    pygame.init()
    pygame.display.set_caption('Bee Quest')
    size = 400, 500
    screen = pygame.display.set_mode(size)
    music(True)
    fon = pygame.transform.scale(load_image('start_picture_v12.jpg', color_key=None, folder='window_fons'), (400, 500))
    screen.blit(fon, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        music(True)
                    elif event.key == pygame.K_F2:
                        music(False)
                    elif event.key == pygame.K_UP:
                        music_volume('up')
                    elif event.key == pygame.K_DOWN:
                        music_volume('low')
                    else:
                        global WINDOW
                        WINDOW = 6
                        main()
                else:
                    # global WINDOW
                    WINDOW = 6
                    main()

        pygame.display.flip()
    pygame.quit()


def registration_window():
    pygame.init()
    pygame.display.set_caption('Bee Quest')
    size = 400, 500
    screen = pygame.display.set_mode(size)

    input_field = pygame.Rect(100, 175, 140, 32)
    screen_field = pygame.Rect(0, 0, 400, 500)
    pos_x, pos_y = 100, 175
    clock = pygame.time.Clock()
    click_of_color = pygame.Color(141, 182, 205)
    click_on_color = pygame.Color(30, 144, 255)
    color = click_of_color
    active = False
    text = ''

    font = pygame.font.Font(None, 32)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # and text != '':
                    global PLAYER_NICKNAME
                    PLAYER_NICKNAME = text
                    global WINDOW
                    WINDOW = 8
                    main()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_field.collidepoint(event.pos):
                    active = True
                    color = click_on_color
                else:
                    active = False
                    color = click_of_color
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F1:
                    music(True)
                if event.key == pygame.K_F2:
                    music(False)
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                        pos_x -= 20 if pos_x > 100 else pos_x == pos_x
                    else:
                        if screen_field.collidepoint(pos_x, pos_y):
                            pos_x += 20
                            text += event.unicode
        txt_surface = font.render(text, True, color)
        width = max(200, txt_surface.get_width() + 10)
        input_field.w = width
        fon = pygame.transform.scale(load_image(f'registration_fon.jpg', color_key=None, folder='window_fons'), (400, 500))
        screen.blit(fon, (0, 0))
        screen.blit(txt_surface, (input_field.x + 5, input_field.y + 5))
        pygame.draw.rect(screen, color, input_field, 2)
        pygame.display.flip()
        clock.tick(30)
    pygame.quit()


def info_window():
    pygame.init()
    pygame.display.set_caption('Bee Quest')
    size = 400, 500
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image(f'info_fon1.jpg', color_key=None, folder='window_fons'), size)
    screen.blit(fon, (0, 0))
    input_field = pygame.Rect(45, 255, 308, 130)
    pygame.draw.rect(screen, (0, 0, 0), input_field, 4)
    input_field = pygame.Rect(20, 90, 358, 150)
    pygame.draw.rect(screen, (0, 0, 0), input_field, 4)
    intro_text = [f"             Тебе предстоит пройти несколько",
                  f"    уровней, перед каждым уровнем будет",
                  f"    показана анимация пчелы, чьи движе -",
                  f"    - ния показывают какое направление",
                  f"    выбрать на развилке."]
    intro_text1 = [f"                 Передвижение - WASD",
                   f"                 Вкл/выкл музыку - F1/F2",
                   f"                 Изменение громкости - ",
                   f"                   стрелки вверх/вниз"]
    font = pygame.font.Font(None, 25)
    text_output(90, intro_text, font, screen)
    text_output(260, intro_text1, font, screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        music(True)
                    elif event.key == pygame.K_F2:
                        music(False)
                    elif event.key == pygame.K_UP:
                        music_volume('up')
                    elif event.key == pygame.K_DOWN:
                        music_volume('low')
                    else:
                        global WINDOW
                        WINDOW = 2
                        main()
                else:
                    WINDOW = 2
                    main()
        pygame.display.flip()
    pygame.quit()


def level_start_window():
    pygame.init()
    pygame.display.set_caption('Bee Quest')
    size = 400, 500
    screen = pygame.display.set_mode(size)

    fon = pygame.transform.scale(load_image(f'level_start_picture_{NEXT_LEVEL}.jpg', color_key=None, folder='level_intro'), (400, 500))
    screen.blit(fon, (0, 0))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        music(True)
                    elif event.key == pygame.K_F2:
                        music(False)
                    elif event.key == pygame.K_UP:
                        music_volume('up')
                    elif event.key == pygame.K_DOWN:
                        music_volume('low')
                    else:
                        global WINDOW
                        WINDOW = 3
                        main()
                else:
                    WINDOW = 3
                    main()
        pygame.display.flip()
    pygame.quit()


def level_lose_window():
    pygame.init()
    pygame.display.set_caption('Bee Quest')
    size = 400, 500
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image(f'level_start_picture_{NEXT_LEVEL}.jpg', color_key=None, folder='level_intro'), (400, 500))
    screen.blit(fon, (0, 0))
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        music(True)
                    elif event.key == pygame.K_F2:
                        music(False)
                    elif event.key == pygame.K_UP:
                        music_volume('up')
                    elif event.key == pygame.K_DOWN:
                        music_volume('low')
                    else:
                        global WINDOW
                        WINDOW = 4  # 3
                        main()
                else:
                    WINDOW = 4  # 3
                    main()
        pygame.display.flip()
    pygame.quit()


def animation_window():
    pygame.init()
    size = 400, 500
    screen = pygame.display.set_mode(size)
    sprite_cord = [5, 11, 11, 5, 9, 5]
    AnimatedSprite(load_image(f'level_animation_{NEXT_LEVEL}.jpg', color_key=None, folder='level_animation'), 10, sprite_cord[NEXT_LEVEL - 1],
                   163, 145)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_F1:
                        music(True)
                    elif event.key == pygame.K_F2:
                        music(False)
                    elif event.key == pygame.K_UP:
                        music_volume('up')
                    elif event.key == pygame.K_DOWN:
                        music_volume('low')
                    else:
                        global WINDOW
                        WINDOW = 4
                        main()
                else:
                    WINDOW = 4
                    main()
        fon = pygame.transform.scale(load_image(f'animation_fon_2.jpg', color_key=None, folder='window_fons'), size)
        screen.blit(fon, (0, 0))
        input_field = pygame.Rect(120, 100, 160, 170)
        pygame.draw.rect(screen, (0, 0, 0), input_field, 4)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(6)
    pygame.quit()


def game_window():
    pygame.init()
    pygame.display.set_caption('Bee Quest')
    size = 400, 500
    screen = pygame.display.set_mode(size)
    game = Game()
    game.set_view(50, size)
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    game.choosing_a_direction('forward')
                elif event.key == pygame.K_s:
                    game.choosing_a_direction('back')
                elif event.key == pygame.K_a:
                    game.choosing_a_direction('left')
                elif event.key == pygame.K_d:
                    game.choosing_a_direction('right')
                elif event.key == pygame.K_F1:
                    music(True)
                elif event.key == pygame.K_F2:
                    music(False)
                elif event.key == pygame.K_UP:
                    music_volume('up')
                elif event.key == pygame.K_DOWN:
                    music_volume('low')
        screen.fill((255, 255, 255))
        game.render(screen)
        pygame.display.flip()
        clock.tick(7)
        if FLAG:
            game.changing_level()
        if FLAG1:
            game.restart_level()
    pygame.quit()


def finish_window():
    pygame.init()
    pygame.display.set_caption('Bee Quest')
    size = 400, 500
    screen = pygame.display.set_mode(size)
    fon = pygame.transform.scale(load_image(f'finish_fon.jpg', color_key=None, folder='window_fons'), size)
    screen.blit(fon, (0, 0))
    input_field = pygame.Rect(45, 100, 308, 120)
    pygame.draw.rect(screen, (0, 0, 0), input_field, 4)
    intro_text = [f"      Поздравляю тебя,",
                  f"      {PLAYER_NICKNAME}",
                  f"      Ошибок допущенно: {FAILS_QUANTITY}"]
    font = pygame.font.Font(None, 35)
    text_output(100, intro_text, font, screen)
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                terminate()
        pygame.display.flip()
    pygame.quit()


if __name__ == '__main__':
    sys.exit(main())

