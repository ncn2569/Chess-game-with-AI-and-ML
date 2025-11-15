import chess
from . import config

def evaluate_board(board, weights_dict):
    """
    Hàm lượng giá bàn cờ.
    TODO: Người dùng sẽ tự hiện thực hàm này.
    
    Yêu cầu:
    1. Phải xử lý các trường hợp kết thúc game (chiếu hết, hết nước đi).
    2. Tính điểm dựa trên vật chất (dùng weights_dict) và các yếu tố khác
       (ví dụ: vị trí, cấu trúc tốt...).
    3. Luôn trả về điểm số từ GÓC NHÌN CỦA QUÂN TRẮNG.
       (Điểm dương = Trắng lợi, Điểm âm = Đen lợi)
    """
    
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -float('inf') # Đen thắng (Trắng bị chiếu hết)
        else:
            return float('inf')  # Trắng thắng (Đen bị chiếu hết)
    
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    # --- Phần đã hiện thực ---
    # Logic đếm vật chất dựa trên trọng số
    score = 0
    
    # Đếm và tính điểm cho từng loại quân
    piece_types = {
        chess.PAWN: "pawn",
        chess.KNIGHT: "knight", 
        chess.BISHOP: "bishop",
        chess.ROOK: "rook",
        chess.QUEEN: "queen",
        chess.KING: "king"
    }
    
    for piece_type, weight_key in piece_types.items():
        white_pieces = len(board.pieces(piece_type, chess.WHITE))
        black_pieces = len(board.pieces(piece_type, chess.BLACK))
        score += weights_dict[weight_key] * (white_pieces - black_pieces)
    
    # Thêm bonus cho vị trí trung tâm (đơn giản)
    center_squares = [chess.D4, chess.D5, chess.E4, chess.E5]
    for square in center_squares:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.WHITE:
                score += 1
            else:
                score -= 1
    
    # Bonus cho di chuyển (mobility)
    current_turn = board.turn
    
    # Đếm số nước đi hợp lệ cho trắng
    if current_turn == chess.WHITE:
        white_mobility = len(list(board.legal_moves))
        board.turn = chess.BLACK
        black_mobility = len(list(board.legal_moves))
        board.turn = chess.WHITE
    else:
        black_mobility = len(list(board.legal_moves))
        board.turn = chess.WHITE
        white_mobility = len(list(board.legal_moves))
        board.turn = chess.BLACK
    
    score += (white_mobility - black_mobility) * 0.1
    
    # Hàm phải trả về điểm từ góc nhìn của Trắng
    return score