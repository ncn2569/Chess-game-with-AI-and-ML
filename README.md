# ♟️ Chess AI Project
 
Dự án cờ vua với 2 loại AI: **Minimax classic** và **ML Agent (Imitation Learning)**. Có battle system để so sánh hiệu suất các agent.
 
> **Note về ML Agent:** Agent này được huấn luyện bằng Imitation Learning — chỉ học bắt chước nước đi của các kỳ thủ top thế giới (Carlsen, Nakamura, Caruana...) mà không có reward signal. Kết quả là nó đánh khá đần, không hiểu chiến thuật. Để mạnh hơn cần Self-play + MCTS kiểu AlphaZero.
 
## 🗂️ Cấu trúc
 
```
Chess-AI-Project/
├── assets/                  # Hình ảnh quân cờ (12 file PNG)
├── src/
│   ├── config.py            # Cấu hình chung
│   ├── evaluation.py        # Hàm đánh giá vị trí
│   ├── engine.py            # Minimax + Alpha-Beta + Quiescence Search
│   ├── game_view.py         # UI Pygame
│   ├── ai_battle.py         # Battle system & các AI agents
│   └── chess_ML/
│       ├── model.py         # CNN model (2×Conv + 2×FC)
│       ├── dataset.py       # Dataset loader
│       ├── auxiliary_func.py# Tiền xử lý, encode nước đi
│       ├── Chess_ML.ipynb   # Notebook huấn luyện
│       ├── data/            # PGN các kỳ thủ top thế giới
│       └── models/          # Model đã train
├── play_game.py             # Người vs Minimax AI
├── play_game_ML.py          # Người vs ML Agent
├── ai_battle.py             # AI Battle Arena
└── requirements.txt
```
 
## ⚙️ Cài đặt
 
```bash
python -m venv chess_game
chess_game\Scripts\activate      # Windows
# source chess_game/bin/activate  # Linux/Mac
 
pip install -r requirements.txt
```
 
Chuẩn bị 12 file PNG trong `assets/`:
`wP, wN, wB, wR, wQ, wK, bP, bN, bB, bR, bQ, bK` (đuôi `.png`)
 
## 🚀 Sử dụng
 
### Chơi với Minimax AI
```bash
python play_game.py
```
 
### Chơi với ML Agent
```bash
python play_game_ML.py
```
 
### AI Battle Arena
```bash
python ai_battle.py
```
So sánh hiệu suất các agent qua tournament nhiều ván, có thống kê thắng/thua/hòa và thời gian thực thi.
 
## 🤖 Kiến trúc AI
 
### Minimax Engine
- Minimax + Alpha-Beta Pruning (Negamax)
- Quiescence Search để tránh horizon effect
- Hàm đánh giá: material score + center control + mobility
 
### ML Agent (Imitation Learning)
- **Input:** ma trận 13×8×8 (12 kênh quân cờ + 1 kênh nước đi hợp lệ)
- **Model:** Conv2D(13→64) → Conv2D(64→128) → FC(8192→256) → FC(256→N)
- **Training:** Cross-entropy loss trên PGN của các kỳ thủ top thế giới
- **Inference:** chọn nước đi hợp lệ có xác suất cao nhất theo softmax
 
## 🌐 Demo
 
Thử trực tiếp trên [HuggingFace Spaces](https://huggingface.co/spaces/ncn2569/Chess_with_AI)