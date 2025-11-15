# Chess AI Project - Minimax & Genetic Algorithm

Dự án AI Cờ Vua sử dụng thuật toán Minimax (Alpha-Beta Pruning) và Genetic Algorithm để huấn luyện AI.

## Cấu trúc Dự án

```
ChessAI_Pygame/
├── assets/                  # Thư mục chứa hình ảnh quân cờ (12 file .png)
│   ├── bB.png              # Bishop đen
│   ├── bK.png              # King đen
│   ├── bN.png              # Knight đen
│   ├── bP.png              # Pawn đen
│   ├── bQ.png              # Queen đen
│   ├── bR.png              # Rook đen
│   ├── wB.png              # Bishop trắng
│   ├── wK.png              # King trắng
│   ├── wN.png              # Knight trắng
│   ├── wP.png              # Pawn trắng
│   ├── wQ.png              # Queen trắng
│   └── wR.png              # Rook trắng
├── src/
│   ├── __init__.py         # Package init
│   ├── config.py           # Cấu hình game (màn hình, màu sắc, trọng số)
│   ├── evaluation.py       # (KHUNG) Hàm lượng giá bàn cờ
│   ├── engine.py           # (KHUNG) Thuật toán Minimax với Alpha-Beta
│   ├── genetic_algorithm.py # (KHUNG) Genetic Algorithm
│   └── game_view.py        # (HOÀN THÀNH) Logic vẽ Pygame
├── play_game.py            # (HOÀN THÀNH) File chạy game chính
├── train_ai.py             # (HOÀN THÀNH) File huấn luyện GA
└── requirements.txt        # Danh sách thư viện cần thiết
```

## Cài đặt

### 1. Cài đặt Python
Yêu cầu Python 3.10 trở lên.

### 2. Cài đặt thư viện

```bash
python -m venv chess_game

pip install -r requirements.txt
```

### 3. Chuẩn bị hình ảnh quân cờ
Bạn cần cung cấp 12 file PNG trong thư mục `assets/`:
- `wP.png`, `wN.png`, `wB.png`, `wR.png`, `wQ.png`, `wK.png` (quân trắng)
- `bP.png`, `bN.png`, `bB.png`, `bR.png`, `bQ.png`, `bK.png` (quân đen)

## Sử dụng

### 🎮 Chơi với AI
```bash
.\chess_game\Scripts\activate

python play_game.py
```

### ⚔️ AI Battle Arena (MỚI!)
```bash
python ai_battle.py
```
**Tính năng:**
- Đấu Random AI vs Minimax AI
- Chọn độ sâu Minimax (1-3)
- Tournament với nhiều ván đấu
- Thống kê chi tiết thắng/thua/hòa
- Đo thời gian thực thi

### 🧪 Test hệ thống
```bash
python test_features.py    # Test UI features
python test_engine.py      # Test Minimax engine  
python test_battle.py      # Test battle system
```

### 🤖 Huấn luyện AI (sau khi hoàn thành code)
```bash
python train_ai.py
```

## Nhiệm vụ của Người dùng

Bạn cần tự hiện thực các file sau:

### 1. `src/evaluation.py`
- Hàm `evaluate_board()`: Lượng giá vị thế bàn cờ
- Xử lý các trường hợp kết thúc game
- Tính điểm dựa trên vật chất và vị trí

### 2. `src/engine.py`
- Hàm `random_move()`: Trả về nước đi ngẫu nhiên
- Hàm `find_best_move()`: Tìm nước đi tốt nhất
- Hàm `minimax_search()`: Thuật toán Minimax với Alpha-Beta Pruning

### 3. `src/genetic_algorithm.py`
- `play_game_headless()`: Mô phỏng ván cờ không GUI
- `calculate_fitness()`: Tính fitness của một chromosome
- `initialize_population()`: Khởi tạo quần thể
- `selection()`: Chọn lọc cha mẹ
- `crossover()`: Lai ghép
- `mutate()`: Đột biến

## Ghi chú

- File `game_view.py` đã được hiện thực đầy đủ logic vẽ Pygame
- File `play_game.py` và `train_ai.py` đã sẵn sàng sử dụng
- Hiện tại AI sử dụng nước đi ngẫu nhiên, bạn cần thay thế bằng Minimax
- Các lỗi import sẽ biến mất sau khi cài đặt `python-chess` và `pygame`

## Cấu trúc Code

### Game Loop (play_game.py)
1. Xử lý input người chơi
2. AI tính toán nước đi
3. Vẽ bàn cờ và quân cờ
4. Kiểm tra game over

### Training Loop (train_ai.py)
1. Khởi tạo quần thể
2. Tính fitness cho từng cá thể
3. Chọn lọc, lai ghép, đột biến
4. Lặp lại qua các thế hệ

Chúc bạn code vui vẻ! 🎯

trọng số của các quân cờ:
pawn: 10
knight: 30
bishop: 30
rook: 50
queen: 90
king: 900