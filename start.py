import pygame
import random

# Initialize pygame and sound
pygame.init()
pygame.mixer.init()

# Set up screen dimensions
WIDTH, HEIGHT = 400, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GAME 2048')

# Load background image
background_image = pygame.image.load('assets/13f50c80a451c7d070d4f2d8f59843c3.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Font and colors
font = pygame.font.Font('freesansbold.ttf', 24)
button_font = pygame.font.Font('freesansbold.ttf', 28)
selector_font = pygame.font.Font('freesansbold.ttf', 22)
button_color = (70, 130, 180)
button_hover_color = (100, 149, 237)
selector_color = (150, 150, 150)
text_color = (255, 255, 255)

# Button rectangles
play_button_rect = pygame.Rect(130, 170, 140, 70)
quit_button_rect = pygame.Rect(165, 420, 70, 40)
size_button_rect = pygame.Rect(150, 250, 100, 30)  # Nút để chọn kích thước lưới

# Game settings
size_options = [4, 5, 6]
current_size_index = 0  # Mặc định là 4x4
game_started = False
show_size_options = False  # Biến để hiển thị danh sách kích thước

# Function to draw buttons with hover effect
def draw_button(text, rect, hover=False):
    color = button_hover_color if hover else button_color
    pygame.draw.rect(screen, color, rect, border_radius=8)
    text_surf = button_font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=rect.center)
    screen.blit(text_surf, text_rect)

# Draw the start screen
def draw_start_screen():
    screen.blit(background_image, (0, 0))
    draw_button('Play', play_button_rect)
    draw_button('Quit', quit_button_rect)

    # Nút kích thước lưới
    grid_size_text = f'{size_options[current_size_index]}x{size_options[current_size_index]}'
    draw_button(grid_size_text, size_button_rect, hover=show_size_options)

    # Nếu người dùng nhấn vào nút kích thước, hiển thị danh sách
    if show_size_options:
        for i, size in enumerate(size_options):
            option_rect = pygame.Rect(150, 290 + i * 30, 100, 30)  # Tạo các ô kích thước
            draw_button(f'{size}x{size}', option_rect)
            if option_rect.collidepoint(pygame.mouse.get_pos()):  # Kiểm tra nếu chuột ở trên ô
                pygame.draw.rect(screen, button_hover_color, option_rect, border_radius=8)

# Main game loop
run = True
while run:
    screen.fill('gray')
    if not game_started:
        draw_start_screen()
    else:
        # Placeholder for main game screen
        screen.fill((200, 200, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if play_button_rect.collidepoint(mouse_pos):
                grid_size = size_options[current_size_index]  # Lấy kích thước lưới
                if grid_size == 4:
                    import game_4x4  # Chạy file game 4x4
                elif grid_size == 5:
                    import game_5x5  # Chạy file game 5x5
                elif grid_size == 6:
                    import game_6x6  # Chạy file game 6x6
                run = False  # Thoát vòng lặp chính để chuyển sang game mới
            elif quit_button_rect.collidepoint(mouse_pos):
                run = False
            elif size_button_rect.collidepoint(mouse_pos):
                show_size_options = not show_size_options  # Toggle the size options
            elif show_size_options:
                for i, size in enumerate(size_options):
                    option_rect = pygame.Rect(150, 290 + i * 30, 100, 30)
                    if option_rect.collidepoint(mouse_pos):
                        current_size_index = i  # Cập nhật kích thước lưới đã chọn
                        show_size_options = False  # Đóng danh sách kích thước sau khi chọn

    pygame.display.flip()

pygame.quit()
