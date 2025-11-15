import chess
import random
import time
from . import evaluation

def random_move(board):
    """
    Trả về một nước đi ngẫu nhiên từ các nước đi hợp lệ.
    """
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None
    return random.choice(legal_moves)

def find_best_move(board, weights_dict, depth):
    """
    Tìm nước đi tốt nhất sử dụng Minimax với Alpha-Beta Pruning.
    """
    legal_moves = list(board.legal_moves)
    if not legal_moves:
        return None
    
    start_time = time.time()
    print(f"AI đang tính toán với độ sâu {depth}...")
    
    best_move = None
    max_eval = -float('inf')
    alpha = -float('inf')
    beta = float('inf')
    nodes_evaluated = 0
    
    # Sắp xếp các nước đi để tối ưu alpha-beta pruning
    # Ưu tiên các nước đi ăn quân và chiếu
    def move_priority(move):
        score = 0
        # Nước đi ăn quân có ưu tiên cao
        if board.piece_at(move.to_square):
            captured_piece = board.piece_at(move.to_square)
            piece_values = {chess.PAWN: 10, chess.KNIGHT: 30, chess.BISHOP: 30, 
                          chess.ROOK: 50, chess.QUEEN: 90, chess.KING: 900}
            score += piece_values.get(captured_piece.piece_type, 0)
        
        # Kiểm tra xem có chiếu không
        board.push(move)
        if board.is_check():
            score += 50
        board.pop()
        
        return score
    
    sorted_moves = sorted(legal_moves, key=move_priority, reverse=True)
    
    for i, move in enumerate(sorted_moves):
        board.push(move)
        
        # Gọi minimax với negamax
        eval_score = -minimax_search(board, weights_dict, depth - 1, -beta, -alpha)
        nodes_evaluated += 1
        
        board.pop()
        
        if eval_score > max_eval:
            max_eval = eval_score
            best_move = move
        
        alpha = max(alpha, eval_score)
        if beta <= alpha:
            break  # Alpha-beta pruning
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    
    print(f"AI chọn nước đi: {best_move.uci() if best_move else 'None'}")
    print(f"Điểm đánh giá: {max_eval:.2f}")
    print(f"Thời gian: {elapsed_time:.2f}s, Nodes: {nodes_evaluated}")
    
    return best_move

def minimax_search(board, weights_dict, depth, alpha, beta):
    """
    Hàm đệ quy Minimax với Alpha-Beta Pruning (Negamax implementation)
    """
    
    # Điều kiện dừng: game over
    if board.is_game_over():
        eval_score = evaluation.evaluate_board(board, weights_dict)
        return eval_score if board.turn == chess.WHITE else -eval_score
    
    # Khi depth = 0, sử dụng quiescence search
    if depth == 0:
        return quiescence_search(board, weights_dict, alpha, beta)
    
    max_eval = -float('inf')
    legal_moves = list(board.legal_moves)
    
    # Sắp xếp nước đi để tối ưu pruning
    def move_priority(move):
        score = 0
        if board.piece_at(move.to_square):
            captured_piece = board.piece_at(move.to_square)
            piece_values = {chess.PAWN: 10, chess.KNIGHT: 30, chess.BISHOP: 30,
                          chess.ROOK: 50, chess.QUEEN: 90, chess.KING: 900}
            score += piece_values.get(captured_piece.piece_type, 0)
        return score
    
    sorted_moves = sorted(legal_moves, key=move_priority, reverse=True)
    
    for move in sorted_moves:
        board.push(move)
        
        # Gọi đệ quy với negamax
        eval_score = -minimax_search(board, weights_dict, depth - 1, -beta, -alpha)
        
        board.pop()
        
        max_eval = max(max_eval, eval_score)
        alpha = max(alpha, eval_score)
        
        # Alpha-beta pruning
        if beta <= alpha:
            break
    
    return max_eval

def quiescence_search(board, weights_dict, alpha, beta):
    """
    Quiescence search để đánh giá tốt hơn các vị trí có capture
    """
    # Đánh giá vị trí hiện tại
    stand_pat = evaluation.evaluate_board(board, weights_dict)
    stand_pat = stand_pat if board.turn == chess.WHITE else -stand_pat
    
    if stand_pat >= beta:
        return beta
    if alpha < stand_pat:
        alpha = stand_pat
    
    # Chỉ xem xét các nước đi capture
    capture_moves = [move for move in board.legal_moves if board.piece_at(move.to_square)]
    
    for move in capture_moves:
        board.push(move)
        score = -quiescence_search(board, weights_dict, -beta, -alpha)
        board.pop()
        
        if score >= beta:
            return beta
        if score > alpha:
            alpha = score
    
    return alpha