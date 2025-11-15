import pygame
import chess
import sys
from src import config, game_view, engine

def get_square_from_mouse(pos):
    """Chuyển đổi tọa độ (x, y) của chuột sang index (0-63) của ô cờ"""
    x, y = pos
    file = x // config.SQUARE_SIZE
    rank = 7 - (y // config.SQUARE_SIZE) # Đảo ngược trục y
    return chess.square(file, rank)

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Chess AI (User Implementation)")
    clock = pygame.time.Clock()

    # Tải tài nguyên
    try:
        images = game_view.load_piece_images()
        print("Tải hình ảnh quân cờ thành công.")
    except Exception as e:
        print(f"Lỗi khi tải hình ảnh: {e}")
        print("Vui lòng đảm bảo thư mục 'assets' có đủ 12 file .png")
        pygame.quit()
        sys.exit()

    board = chess.Board()
    
    # Sử dụng trọng số chuẩn để chơi
    # TODO: Người dùng có thể thay đổi bằng trọng số đã huấn luyện
    ai_weights = config.STANDARD_WEIGHTS
    
    player_is_white = True # Tạm thời người chơi luôn là Trắng
    is_ai_turn = False
    
    selected_square = None # Ô cờ người dùng click (index 0-63)
    player_clicks = []     # [ô_bắt_đầu, ô_kết_thúc]

    running = True
    while running:
        # 1. Xử lý Input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Xử lý click chuột (chỉ khi đến lượt người)
            if event.type == pygame.MOUSEBUTTONDOWN and not is_ai_turn:
                pos = pygame.mouse.get_pos()
                square = get_square_from_mouse(pos)
                
                piece = board.piece_at(square)
                
                if not player_clicks:
                    # Click lần 1: Chọn quân
                    if piece is not None and piece.color == board.turn:
                        selected_square = square
                        player_clicks.append(square)
                else:
                    # Click lần 2: Chọn ô đích
                    player_clicks.append(square)
                    
                    # Tạo nước đi
                    from_sq_name = chess.SQUARE_NAMES[player_clicks[0]]
                    to_sq_name = chess.SQUARE_NAMES[player_clicks[1]]
                    move_uci = f"{from_sq_name}{to_sq_name}"
                    
                    # Xử lý phong cấp (tự động phong Hậu)
                    piece_type = board.piece_at(player_clicks[0]).piece_type
                    if piece_type == chess.PAWN and (to_sq_name[1] == '8' or to_sq_name[1] == '1'):
                        move_uci += 'q' 
                    
                    try:
                        move = chess.Move.from_uci(move_uci)
                        if move in board.legal_moves:
                            board.push(move)
                            is_ai_turn = True
                        else:
                            print(f"Nước đi không hợp lệ: {move_uci}")
                    except ValueError:
                        print(f"Nước đi không hợp lệ (format): {move_uci}")
                    
                    # Reset clicks
                    player_clicks = []
                    selected_square = None
        
        # 2. Lượt của AI
        if is_ai_turn and not board.is_game_over():
            print("AI đang suy nghĩ...")
            pygame.display.set_caption("AI đang suy nghĩ...")
            
            ai_move = engine.find_best_move(board, ai_weights, config.PLAY_SEARCH_DEPTH)
            
            if ai_move:
                board.push(ai_move)
                print(f"AI đi: {ai_move.uci()}")
            else:
                print("AI không tìm thấy nước đi (có thể game over).")
                
            is_ai_turn = False
            pygame.display.set_caption("Chess AI (User Implementation)")

        # 3. Vẽ lên màn hình
        game_view.draw_board(screen)
        if selected_square is not None:
            game_view.draw_highlight(screen, selected_square)
        game_view.draw_pieces(screen, board, images)
        
        pygame.display.flip()
        
        # 4. Kiểm tra Game Over
        if board.is_game_over():
            print("--- GAME OVER ---")
            print(f"Kết quả: {board.result()}")
            pygame.time.wait(5000) # Chờ 5 giây
            running = False

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()