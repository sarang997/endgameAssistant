import chess.pgn
import chess.engine

def analyze_game_between_moves_with_stockfish(pgn_path, stockfish_path, start_move_number, end_move_number, analysis_time=1.0, num_threads=4, depth=None):
    # Load the game from the PGN file
    with open(pgn_path, 'r') as f:
        game = chess.pgn.read_game(f)

    # Set up the Stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    # Set the number of threads
    engine.configure({"Threads": num_threads})

    board = game.board()
    for idx, move in enumerate(game.mainline_moves()):
        board.push(move)
        
        # Adjust for standard chess move numbering
        current_move_number = (idx // 2) + 1
        
        if current_move_number >= start_move_number:
            
            if current_move_number > end_move_number:
                break
            
            # Set analysis limit
            if depth:
                limit = chess.engine.Limit(depth=depth)
            else:
                limit = chess.engine.Limit(time=analysis_time)
            
            info = engine.analyse(board, limit)
            
            # Adjust the score to be from White's perspective
            score = info['score'].relative.score()
            if score is None:
                # Mate score
                mate_val = info['score'].relative.mate()
                if mate_val > 0:
                    score_str = f"-M{mate_val}"
                else:
                    score_str = f"M{-mate_val}"
            else:
                # Convert centipawn score to a standard +/- format
                score_str = f"{score / 100:.2f}"
            
            color = "White" if idx % 2 == 0 else "Black"
            print(f"Move {current_move_number} ({color}): {move} - Evaluation: {score_str}")

    # Close the engine
    engine.quit()

# Example usage:
analyze_game_between_moves_with_stockfish('fen.pgn', 'stockfish-windows-x86-64-avx2 copy.exe', start_move_number=8, end_move_number=10, analysis_time=0.5, num_threads=4)
