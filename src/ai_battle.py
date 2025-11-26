import chess
import time
import random
from typing import Tuple, Optional, Dict, Any
from . import engine, config
from chess import Board, pgn   
from .chess_ML.model import ChessModel
import torch
import pickle
import numpy as np
class AIAgent:
    """Base class cho các AI agent"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.total_time = 0.0
        self.moves_made = 0
    
    def get_move(self, board: chess.Board, time_limit: float = 10.0) -> Optional[chess.Move]:
        """Trả về nước đi tốt nhất. Phải được override bởi subclass"""
        raise NotImplementedError
    
    def reset_stats(self):
        """Reset statistics"""
        self.total_time = 0.0
        self.moves_made = 0
    
    def get_average_time(self) -> float:
        """Trả về thời gian trung bình mỗi nước đi"""
        return self.total_time / max(1, self.moves_made)

class RandomAgent(AIAgent):
    """AI agent chọn nước đi ngẫu nhiên"""
    
    def __init__(self):
        super().__init__("Random AI", "Chọn nước đi ngẫu nhiên")
    
    def get_move(self, board: chess.Board, time_limit: float = 10.0) -> Optional[chess.Move]:
        start_time = time.time()
        
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            return None
        
        move = random.choice(legal_moves)
        
        elapsed = time.time() - start_time
        self.total_time += elapsed
        self.moves_made += 1
        
        return move

class MinimaxAgent(AIAgent):
    """AI agent sử dụng Minimax với Alpha-Beta Pruning"""
    
    def __init__(self, depth: int = 2, weights: Dict[str, int] = None):
        super().__init__(f"Minimax AI (depth {depth})", f"Minimax với Alpha-Beta, độ sâu {depth}")
        self.depth = depth
        self.weights = weights or config.STANDARD_WEIGHTS.copy()
    
    def get_move(self, board: chess.Board, time_limit: float = 10.0) -> Optional[chess.Move]:
        start_time = time.time()
        
        # Sử dụng engine hiện có
        move = engine.find_best_move(board, self.weights, self.depth)
        
        elapsed = time.time() - start_time
        self.total_time += elapsed
        self.moves_made += 1
        
        # Kiểm tra time limit (có thể implement timeout cho minimax sau)
        if elapsed > time_limit:
            print(f"⚠️  {self.name} vượt thời gian: {elapsed:.2f}s > {time_limit}s")
        
        return move

class MLAgent(AIAgent):
    """AI agent sử dụng Machine Learning (model + mapping có sẵn)"""
    
    def __init__(self, model=None, move_to_idx: Dict[str, int] = None, idx_to_move: Dict[int, str] = None):
        super().__init__("ML AI", "Machine Learning Agent")
        with open("src\chess_ML\models\heavy_move_to_int_1", "rb") as file:
            self.move_to_int = pickle.load(file) #load mapping
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu") # sử dụng GPU nếu có

        # Load the model
        self.model = ChessModel(num_classes=len(self.move_to_int))
        self.model.load_state_dict(torch.load("src/chess_ML/models/TORCH_1_100EPOCHS.pth"))
        self.model.to(self.device)
        self.model.eval()  # Set the model to evaluation mode (it may be reductant)

        self.int_to_move = {v: k for k, v in self.move_to_int.items()}
    def board_to_matrix(self, board: Board):
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
    def prepare_input(self, board: Board):
        matrix = self.board_to_matrix(board)
        X_tensor = torch.tensor(matrix, dtype=torch.float32).unsqueeze(0)
        return X_tensor
    
    def get_move(self, board: chess.Board, time_limit: float = 10.0) -> Optional[chess.Move]:
        start_time = time.time()
        legal_moves = list(board.legal_moves)
        X_tensor = self.prepare_input(board).to(self.device)
        with torch.no_grad():
            logits = self.model(X_tensor)
        
        logits = logits.squeeze(0)  # Remove batch dimension
        
        probabilities = torch.softmax(logits, dim=0).cpu().numpy()  # Convert to probabilities
        legal_moves = list(board.legal_moves)
        legal_moves_uci = [move.uci() for move in legal_moves] # lấy danh sách những nước hợp lệ
        sorted_indices = np.argsort(probabilities)[::-1]
        for move_index in sorted_indices: #duyệt từ cao xuống thấp
            move = self.int_to_move[move_index] # chuyển từ index sang uci
            if move in legal_moves_uci: #nếu nước đó hợp lệ
                chosen_move = chess.Move.from_uci(move) 
                elapsed = time.time() - start_time
                self.total_time += elapsed
                self.moves_made += 1
                return chosen_move
    
        
        elapsed = time.time() - start_time
        self.total_time += elapsed
        self.moves_made += 1
        
        # optional: cảnh báo nếu vượt time limit
        if elapsed > time_limit:
            print(f"⚠️  {self.name} vượt thời gian: {elapsed:.2f}s > {time_limit}s")
        return None  # Không tìm được nước đi hợp lệ
    

class GameResult:
    """Kết quả của một ván game"""
    
    def __init__(self, winner: str, reason: str, moves_count: int, 
                 white_time: float, black_time: float, total_time: float):
        self.winner = winner  # "white", "black", "draw"
        self.reason = reason  # "checkmate", "stalemate", "timeout", etc.
        self.moves_count = moves_count
        self.white_time = white_time
        self.black_time = black_time
        self.total_time = total_time

def play_game(white_agent: AIAgent, black_agent: AIAgent, 
              silent: bool = True, max_moves: int = 200) -> GameResult:
    """
    Chơi một ván cờ giữa hai AI agents
    
    Args:
        white_agent: AI chơi quân trắng
        black_agent: AI chơi quân đen
        silent: Không in chi tiết nước đi
        max_moves: Giới hạn số nước đi để tránh game vô hạn
    
    Returns:
        GameResult: Kết quả của ván game
    """
    board = chess.Board()
    start_time = time.time()
    moves_played = 0
    
    if not silent:
        print(f"\n🎮 Bắt đầu game: {white_agent.name} (Trắng) vs {black_agent.name} (Đen)")
    
    while not board.is_game_over() and moves_played < max_moves:
        current_agent = white_agent if board.turn == chess.WHITE else black_agent
        
        try:
            move = current_agent.get_move(board, config.BATTLE_TIME_LIMIT)
            
            if move is None or move not in board.legal_moves:
                # Nước đi không hợp lệ - thua ngay
                winner = "black" if board.turn == chess.WHITE else "white"
                reason = "illegal_move"
                break
            
            board.push(move)
            moves_played += 1
            
            if not silent:
                turn_str = "Trắng" if board.turn == chess.BLACK else "Đen"  # board.turn đã đổi
                print(f"{moves_played}. {turn_str}: {move.uci()}")
                
        except Exception as e:
            # Lỗi trong quá trình tính toán - thua ngay
            if not silent:
                print(f"❌ Lỗi từ {current_agent.name}: {e}")
            winner = "black" if board.turn == chess.WHITE else "white"
            reason = "error"
            break
    
    # Xác định kết quả
    total_time = time.time() - start_time
    
    if moves_played >= max_moves:
        winner = "draw"
        reason = "max_moves_reached"
    elif board.is_game_over():
        result = board.result()
        if result == "1-0":
            winner = "white"
        elif result == "0-1":
            winner = "black"
        else:
            winner = "draw"
        
        # Xác định lý do cụ thể
        if board.is_checkmate():
            reason = "checkmate"
        elif board.is_stalemate():
            reason = "stalemate"
        elif board.is_insufficient_material():
            reason = "insufficient_material"
        elif board.is_seventyfive_moves():
            reason = "75_moves_rule"
        elif board.is_fivefold_repetition():
            reason = "repetition"
        else:
            reason = "other_draw"
    
    white_time = white_agent.get_average_time() * (moves_played + 1) // 2
    black_time = black_agent.get_average_time() * moves_played // 2
    
    return GameResult(winner, reason, moves_played, white_time, black_time, total_time)

def run_tournament(agent1: AIAgent, agent2: AIAgent, num_games: int = 10) -> Dict[str, Any]:
    """
    Chạy tournament giữa hai AI agents
    
    Args:
        agent1: AI agent thứ nhất
        agent2: AI agent thứ hai  
        num_games: Số ván đấu (sẽ chơi cả trắng và đen)
    
    Returns:
        Dict chứa kết quả tournament
    """
    print(f"\n🏆 BẮT ĐẦU TOURNAMENT")
    print(f"🤖 {agent1.name} vs {agent2.name}")
    print(f"⚔️  Số ván đấu: {num_games}")
    print("=" * 60)
    
    results = []
    agent1_stats = {"wins": 0, "draws": 0, "losses": 0}
    agent2_stats = {"wins": 0, "draws": 0, "losses": 0}
    
    # Reset stats
    agent1.reset_stats()
    agent2.reset_stats()
    
    tournament_start = time.time()
    
    for game_num in range(num_games):
        # Xen kẽ màu: game chẵn agent1 = trắng, game lẻ agent1 = đen
        if game_num % 2 == 0:
            white_agent, black_agent = agent1, agent2
            agent1_color, agent2_color = "white", "black"
        else:
            white_agent, black_agent = agent2, agent1
            agent1_color, agent2_color = "black", "white"
        
        print(f"\n🎯 Game {game_num + 1}/{num_games}")
        print(f"   Trắng: {white_agent.name}")
        print(f"   Đen: {black_agent.name}")
        
        game_start = time.time()
        result = play_game(white_agent, black_agent, silent=True)
        game_time = time.time() - game_start
        
        results.append(result)
        
        # Cập nhật thống kê
        if result.winner == agent1_color:
            agent1_stats["wins"] += 1
            agent2_stats["losses"] += 1
            winner_name = agent1.name
        elif result.winner == agent2_color:
            agent2_stats["wins"] += 1
            agent1_stats["losses"] += 1
            winner_name = agent2.name
        else:
            agent1_stats["draws"] += 1
            agent2_stats["draws"] += 1
            winner_name = "Hòa"
        
        # In kết quả game
        print(f"   ⏱️  Thời gian: {game_time:.2f}s")
        print(f"   🏁 Kết quả: {winner_name} ({result.reason})")
        print(f"   📊 Số nước: {result.moves_count}")
    
    tournament_time = time.time() - tournament_start
    
    # In thống kê tổng kết
    print("\n" + "=" * 60)
    print("📊 KẾT QUẢ TOURNAMENT")
    print("=" * 60)
    
    print(f"\n🤖 {agent1.name}:")
    print(f"   🏆 Thắng: {agent1_stats['wins']}")
    print(f"   🤝 Hòa: {agent1_stats['draws']}")
    print(f"   💔 Thua: {agent1_stats['losses']}")
    win_rate1 = (agent1_stats['wins'] + agent1_stats['draws'] * 0.5) / num_games * 100
    print(f"   📈 Tỷ lệ thắng: {win_rate1:.1f}%")
    print(f"   ⏱️  Thời gian trung bình/nước: {agent1.get_average_time():.3f}s")
    
    print(f"\n🤖 {agent2.name}:")
    print(f"   🏆 Thắng: {agent2_stats['wins']}")
    print(f"   🤝 Hòa: {agent2_stats['draws']}")
    print(f"   💔 Thua: {agent2_stats['losses']}")
    win_rate2 = (agent2_stats['wins'] + agent2_stats['draws'] * 0.5) / num_games * 100
    print(f"   📈 Tỷ lệ thắng: {win_rate2:.1f}%")
    print(f"   ⏱️  Thời gian trung bình/nước: {agent2.get_average_time():.3f}s")
    
    print(f"\n⏰ Tổng thời gian tournament: {tournament_time:.2f}s")
    print(f"⚡ Thời gian trung bình/game: {tournament_time/num_games:.2f}s")
    
    # Xác định winner
    if win_rate1 > win_rate2:
        print(f"\n🎉 WINNER: {agent1.name} ({win_rate1:.1f}% vs {win_rate2:.1f}%)")
    elif win_rate2 > win_rate1:
        print(f"\n🎉 WINNER: {agent2.name} ({win_rate2:.1f}% vs {win_rate1:.1f}%)")
    else:
        print(f"\n🤝 TIE: {win_rate1:.1f}% vs {win_rate2:.1f}%")
    
    return {
        "agent1_stats": agent1_stats,
        "agent2_stats": agent2_stats,
        "win_rate1": win_rate1,
        "win_rate2": win_rate2,
        "total_time": tournament_time,
        "avg_game_time": tournament_time / num_games,
        "results": results
    }