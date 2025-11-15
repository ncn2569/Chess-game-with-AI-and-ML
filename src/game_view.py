import pygame
import chess
from . import config

def load_piece_images():
    """
    Tải 12 hình ảnh quân cờ từ thư mục assets.
    Trả về một dict: {'wP': img, 'wR': img, ..., 'bK': img}
    """
    images = {}
    pieces = ['P', 'N', 'B', 'R', 'Q', 'K']
    colors = ['w', 'b']
    
    for color in colors:
        for piece in pieces:
            key = f"{color}{piece}"
            filename = f"{key}.png"
            try:
                image = pygame.image.load(f"{config.ASSET_PATH}{filename}")
                image = pygame.transform.scale(image, (config.SQUARE_SIZE, config.SQUARE_SIZE))
                images[key] = image
            except FileNotFoundError:
                print(f"Lỗi: Không tìm thấy file {config.ASSET_PATH}{filename}")
                # Tạo ảnh rỗng thay thế
                images[key] = pygame.Surface((config.SQUARE_SIZE, config.SQUARE_SIZE), pygame.SRCALPHA)

    return images

def draw_board(screen):
    """Vẽ bàn cờ (các ô vuông)"""
    for r in range(8):
        for c in range(8):
            color = config.COLORS["white"] if (r + c) % 2 == 0 else config.COLORS["black"]
            pygame.draw.rect(screen, color, 
                             (c * config.SQUARE_SIZE, 
                              r * config.SQUARE_SIZE, 
                              config.SQUARE_SIZE, 
                              config.SQUARE_SIZE))

def draw_pieces(screen, board, images):
    """
    Vẽ các quân cờ lên bàn cờ, dựa trên trạng thái `board` của python-chess.
    """
    for i in range(64):
        square = chess.SQUARES[i]  # 0 (A1) -> 63 (H8)
        piece = board.piece_at(square)
        
        if piece is not None:
            # Lấy key (ví dụ: 'wP', 'bN')
            color = 'w' if piece.color == chess.WHITE else 'b'
            piece_type = piece.symbol().upper()
            image_key = f"{color}{piece_type}"
            
            # Chuyển đổi chess.Square (0-63) sang tọa độ (x, y) của Pygame
            file = chess.square_file(square)  # Cột 0 (A) -> 7 (H)
            rank = chess.square_rank(square)  # Hàng 0 (1) -> 7 (8)
            
            # Pygame vẽ từ trên xuống, Chess đếm từ dưới lên
            x = file * config.SQUARE_SIZE
            y = (7 - rank) * config.SQUARE_SIZE
            
            screen.blit(images[image_key], (x, y))

def draw_highlight(screen, square):
    """Tô sáng ô được chọn"""
    if square is not None:
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        x = file * config.SQUARE_SIZE
        y = (7 - rank) * config.SQUARE_SIZE
        
        # Tạo một bề mặt trong suốt để tô sáng
        highlight_surface = pygame.Surface((config.SQUARE_SIZE, config.SQUARE_SIZE), pygame.SRCALPHA)
        highlight_surface.fill(config.COLORS["highlight"])
        screen.blit(highlight_surface, (x, y))