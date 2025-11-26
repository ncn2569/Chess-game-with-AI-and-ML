import numpy as np
from chess import Board


def board_to_matrix(board: Board):
    """
    Chuyển một Board -> mảng 13x8x8
    - 0..5: các loại quân của trắng
    - 6..11: các loại quân của đen
    - 12: các ô mà một nước hợp lệ có thể đi tới
    """
    arr = np.zeros((13, 8, 8), dtype=np.float32)
    pieces = board.piece_map()
    for sq, pc in pieces.items():
        r, c = divmod(sq, 8)
        # index kênh: offset màu + loại (loại bắt đầu từ 0)
        color_offset = 0 if pc.color else 6
        type_idx = pc.piece_type - 1
        channel = color_offset + type_idx
        arr[channel, r, c] = 1.0

    # đánh dấu ô đích của tất cả nước hợp lệ ở kênh cuối cùng
    for mv in board.legal_moves:
        tr = mv.to_square
        r_to, c_to = divmod(tr, 8)
        arr[12, r_to, c_to] = 1.0

    return arr

def create_input_for_nn(games): # hàm tạo dữ liệu đầu vào cho nn từ danh sách ván cờ
    X = []
    y = []
    # Duyệt qua từng ván cờ
    for game in games:
        board = game.board() 
        for move in game.mainline_moves(): 
            X.append(board_to_matrix(board))
            y.append(move.uci())
            board.push(move)
    return np.array(X, dtype=np.float32), np.array(y)


def encode_moves(moves):
    move_to_int = {move: idx for idx, move in enumerate(set(moves))}
    return np.array([move_to_int[move] for move in moves], dtype=np.float32), move_to_int