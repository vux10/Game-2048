import pygame
import random

pygame.init()

# Khởi tạo âm thanh
pygame.mixer.init()
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

merge_sound = pygame.mixer.Sound('merge_sound.wav')

# initial set up
WIDTH = 600  # Tăng kích thước cửa sổ
HEIGHT = 700
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048 6x6')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# Thiết lập icon reset + undo
reset_icon = pygame.image.load('assets/reset.png').convert_alpha()
undo_icon = pygame.image.load('assets/undo.png').convert_alpha()

# 2048 game color library
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# game variables initialize
board_values = [[0 for _ in range(6)] for _ in range(6)]  # Thay đổi kích thước thành 6x6
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high
move_history = []
score_history = []

def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 500, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (230, 65))
    screen.blit(game_over_text2, (170, 105))


def save_board_state():
    global move_history, score_history
    move_history.append([row[:] for row in board_values])
    score_history.append(score)

def undo_last_move():
    global board_values, score, move_history, score_history
    if len(move_history) > 0:
        board_values = move_history.pop()
        score = score_history.pop()

def take_turn(direc, board):
    global score
    merged = [[False for _ in range(6)] for _ in range(6)]

    if direc == 'UP':
        for i in range(6):
            for j in range(6):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if i - shift > 0 and board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':
        for i in range(4, -1, -1):
            for j in range(6):
                shift = 0
                for q in range(5, i, -1):
                    if board[q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[i + shift][j] = board[i][j]
                    board[i][j] = 0
                if i + shift < 5 and board[i + shift][j] == board[i + shift + 1][j] and not merged[i + shift + 1][j] \
                        and not merged[i + shift][j]:
                    board[i + shift + 1][j] *= 2
                    score += board[i + shift + 1][j]
                    board[i + shift][j] = 0
                    merged[i + shift + 1][j] = True

    elif direc == 'LEFT':
        for i in range(6):
            for j in range(6):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if j - shift > 0 and board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':
        for i in range(6):
            for j in range(4, -1, -1):
                shift = 0
                for q in range(5, j, -1):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j + shift] = board[i][j]
                    board[i][j] = 0
                if j + shift < 5 and board[i][j + shift] == board[i][j + shift + 1] and not merged[i][j + shift + 1] \
                        and not merged[i][j + shift]:
                    board[i][j + shift + 1] *= 2
                    score += board[i][j + shift + 1]
                    board[i][j + shift] = 0
                    merged[i][j + shift + 1] = True

    merge_sound.play()
    return board


def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = random.randint(0, 5)
        col = random.randint(0, 5)
        if board[row][col] == 0:
            count += 1
            if random.randint(1, 10) == 10:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 600, 600], 0, 10)
    score_text = font.render(f'Score: {score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 610))
    screen.blit(high_score_text, (10, 650))
    reset_icon_resized = pygame.transform.scale(reset_icon, (32, 32))
    undo_icon_resized = pygame.transform.scale(undo_icon, (32, 32))
    screen.blit(reset_icon_resized, (480, 630))
    screen.blit(undo_icon_resized, (540, 630))


def draw_pieces(board):
    for i in range(6):
        for j in range(6):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)

#Main
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '':
        save_board_state() #Lưu trạng thái trước khi di chuyển
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if game_over:
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(6)] for _ in range(6)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Kiểm tra nút Reset
            if 480 <= mouse_pos[0] <= 480 + 32 and 630 <= mouse_pos[1] <= 630 + 32:
                board_values = [[0 for _ in range(6)] for _ in range(6)]
                spawn_new = True
                init_count = 0
                score = 0
                direction = ''
                game_over = False
                move_history = []
                score_history = []
            # Kiểm tra nút Undo
            if 540 <= mouse_pos[0] <= 540 + 32 and 630 <= mouse_pos[1] <= 630 + 32:
                if len(move_history) > 0: #chỉ undo khi có lịch sử
                    undo_last_move()
                    spawn_new = False #không tạo ô mới khi undo

    if score > high_score:
        high_score = score

    pygame.display.flip()
pygame.quit()