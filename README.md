# 🏆 Chess AI Project - Hoàn thiện với Minimax & Battle System

Dự án AI Cờ Vua sử dụng thuật toán **Minimax với Alpha-Beta Pruning** và **AI Battle System** để so sánh hiệu suất các AI agents.

## Cấu trúc Dự án

```
Chess-AI-Project/
├── 📁 assets/                    # Hình ảnh quân cờ (đã có demo)
├── 📁 src/
│   ├── config.py                 # Cấu hình (trọng số, màu sắc, battle settings)
│   ├── evaluation.py             # Hàm đánh giá thông minh
│   ├── engine.py                 # Minimax + Alpha-Beta + Quiescence
│   ├── game_view.py              # UI Pygame với highlights
│   ├── ai_battle.py              # Battle system
│   └── genetic_algorithm.py     # Cần implement
├── 🎮 play_game.py               # Game người vs AI
├── ⚔️ ai_battle.py               # AI Battle Arena
├── 🧪 test_engine.py             # Test Minimax engine
├── 🧪 test_battle.py             # Test battle system
├── 🤖 train_ai.py                # GA training
└── 📦 requirements.txt           # Dependencies
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
python test_engine.py      # Test Minimax engine hoạt động tốt
python test_battle.py      # Test battle system  
```

### 🤖 Huấn luyện AI (genetic algorithm - chưa hoàn thành)
```bash
python train_ai.py         # Cần implement GA trước
```
## Chạy chương trình

### Chạy ngay để test AI:
```bash
python ai_battle.py
# Chọn: 3 (Random vs Minimax)
# Số ván: 10
```

### Chơi với AI:
```bash
python play_game.py
```

Dự án đã thành công trong việc tạo ra một hệ thống Chess AI hoàn chỉnh với khả năng chơi thông minh và đánh giá hiệu suất! 