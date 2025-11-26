# import torch
# import pickle
# import numpy as np
# from chess import Board
# from MachineLearning.helper import board_to_matrix
# from MachineLearning.model import ChessModel

# # Load mapping
# with open(r"D:\nhập môn AI\BTL2\Chess-game-with-AI-and-ML\model\move_to_int", "rb") as file:
#     move_to_int = pickle.load(file)

# int_to_move = {v: k for k, v in move_to_int.items()}

# # Setup device
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# # Load model
# model = ChessModel(num_classes=len(move_to_int))
# model.load_state_dict(torch.load(
#     r"D:\nhập môn AI\BTL2\Chess-game-with-AI-and-ML\model\nguyen_model100epochwithvaluehead.pth",
#     map_location=device
# ))
# model.to(device)
# model.eval()


# def prepare_input(board: Board):
#     matrix = board_to_matrix(board)
#     X_tensor = torch.tensor(matrix, dtype=torch.float32).unsqueeze(0)
#     return X_tensor


# def predict_move(board: Board):
#     X_tensor = prepare_input(board).to(device)

#     with torch.no_grad():
#         logits = model(X_tensor)

#     logits = logits.squeeze(0)
#     probabilities = torch.softmax(logits, dim=0).cpu().numpy()

#     legal_moves = list(board.legal_moves)
#     legal_moves_uci = [m.uci() for m in legal_moves]

#     sorted_indices = np.argsort(probabilities)[::-1]

#     for idx in sorted_indices:
#         move_uci = int_to_move[idx]
#         if move_uci in legal_moves_uci:
#             return move_uci

#     return None