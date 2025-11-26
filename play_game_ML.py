import sys
import time
import pygame
import chess

from src import config, game_view
from src.ai_battle import MLAgent

def get_square_from_mouse(pos):
    x, y = pos
    file = x // config.SQUARE_SIZE
    rank = 7 - (y // config.SQUARE_SIZE)
    return chess.square(file, rank)

def main():
    pygame.init()
    screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
    pygame.display.set_caption("Play vs MLAgent")
    clock = pygame.time.Clock()

    try:
        images = game_view.load_piece_images()
    except Exception as e:
        print(f"Failed to load piece images: {e}")
        pygame.quit()
        sys.exit(1)

    board = chess.Board()

    # Player config
    player_is_white = True  # True: human plays White, False: human plays Black
    is_ai_turn = not player_is_white if board.turn == chess.WHITE else player_is_white

    # Instantiate MLAgent (uses config paths if available)
    try:
        ml_agent = MLAgent()
    except Exception as e:
        print(f"Failed to initialize MLAgent: {e}")
        pygame.quit()
        sys.exit(1)

    selected_square = None
    player_clicks = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Human input only when it's human's turn
            if event.type == pygame.MOUSEBUTTONDOWN and not is_ai_turn:
                pos = pygame.mouse.get_pos()
                square = get_square_from_mouse(pos)
                piece = board.piece_at(square)

                if not player_clicks:
                    if piece is not None and piece.color == board.turn:
                        selected_square = square
                        player_clicks.append(square)
                else:
                    player_clicks.append(square)
                    from_sq = chess.SQUARE_NAMES[player_clicks[0]]
                    to_sq = chess.SQUARE_NAMES[player_clicks[1]]
                    move_uci = f"{from_sq}{to_sq}"

                    # Auto promotion to queen
                    pt = board.piece_at(player_clicks[0]).piece_type
                    if pt == chess.PAWN and (to_sq[1] == '8' or to_sq[1] == '1'):
                        move_uci += 'q'

                    try:
                        move = chess.Move.from_uci(move_uci)
                        if move in board.legal_moves:
                            board.push(move)
                            is_ai_turn = True
                        else:
                            print(f"Illegal move: {move_uci}")
                    except ValueError:
                        print(f"Invalid UCI format: {move_uci}")

                    player_clicks = []
                    selected_square = None

        # AI turn (MLAgent)
        if is_ai_turn and not board.is_game_over():
            pygame.display.set_caption("AI đang suy nghĩ...")
            start = time.time()
            try:
                ai_move = ml_agent.get_move(board, time_limit=getattr(config, "BATTLE_TIME_LIMIT", 10.0))
            except Exception as e:
                print(f"MLAgent error during move selection: {e}")
                ai_move = None
            elapsed = time.time() - start

            if ai_move and ai_move in board.legal_moves:
                board.push(ai_move)
                print(f"MLAgent đi: {ai_move.uci()} (took {elapsed:.2f}s)")
            else:
                print("MLAgent did not return a legal move, choosing random/legal fallback.")
                # attempt a safe fallback
                legal = list(board.legal_moves)
                if legal:
                    board.push(legal[0])

            is_ai_turn = False
            pygame.display.set_caption("Play vs MLAgent")

        # Draw
        game_view.draw_board(screen)
        if selected_square is not None:
            game_view.draw_highlight(screen, selected_square)
        game_view.draw_pieces(screen, board, images)
        pygame.display.flip()

        # Game over handling
        if board.is_game_over():
            print("--- GAME OVER ---")
            print(f"Result: {board.result()}  Reason: {board.outcome()}")
            pygame.time.wait(4000)
            running = False

        clock.tick(60)

    pygame.quit()
    sys.exit(0)

if __name__ == "__main__":
    main()