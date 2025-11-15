import pygame

# Kích thước màn hình
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 640
SQUARE_SIZE = SCREEN_WIDTH // 8

# Màu sắc (RGB)
COLORS = {
    "white": (238, 238, 210),
    "black": (118, 150, 86),
    "highlight": (246, 246, 130, 100),  # Màu vàng nhạt, có alpha
    "valid_move": (173, 216, 230, 120),  # Xanh nhạt cho nước đi hợp lệ
    "capture_move": (255, 99, 71, 120),  # Đỏ cho nước đi ăn quân
    "game_over_bg": (0, 0, 0, 180),     # Nền đen trong suốt cho game over
    "game_over_text": (255, 255, 255),  # Trắng cho text
    "button_bg": (70, 130, 180),        # Xanh dương cho nút
    "button_hover": (100, 149, 237)     # Xanh nhạt hơn khi hover
}

# Đường dẫn tài nguyên
ASSET_PATH = "assets/"

# Trọng số chuẩn (dùng cho AI cơ sở hoặc test)
STANDARD_WEIGHTS = {
    "pawn": 10,
    "knight": 30,
    "bishop": 30,
    "rook": 50,
    "queen": 90,
    "king": 900
}

# Độ sâu tìm kiếm khi CHƠI
# (Độ sâu khi HUẤN LUYỆN sẽ được định nghĩa trong train_ai.py)
PLAY_SEARCH_DEPTH = 1

# Cấu hình cho AI Battle
BATTLE_SEARCH_DEPTH = 2  # Độ sâu cho battle (nhanh hơn)
BATTLE_TIME_LIMIT = 10   # Giới hạn thời gian mỗi nước đi (giây)
MAX_MOVES_PER_GAME = 200 # Giới hạn số nước đi mỗi ván (tránh vô hạn)