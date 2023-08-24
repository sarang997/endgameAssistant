import chess.pgn
import chess.engine

import chess.pgn
import chess.engine

def analyze_fen_with_stockfish(fen, stockfish_path, analysis_time=1.0, num_threads=4, depth=None):
    """
    Analyze a given FEN position using Stockfish.
    
    Args:
    - fen (str): The FEN string representing the position.
    - stockfish_path (str): Path to the Stockfish binary.
    - analysis_time (float, optional): Time in seconds to spend on analysis. Default is 1 second.
    - num_threads (int, optional): Number of threads for Stockfish to use. Default is 4.
    - depth (int, optional): Depth for analysis. If provided, will override analysis_time.
    
    Returns:
    - str: Engine evaluation of the position.
    """
    # Initialize the Stockfish engine
    engine = chess.engine.SimpleEngine.popen_uci(stockfish_path)

    # Set the number of threads
    engine.configure({"Threads": num_threads})

    # Convert the FEN to a board position
    board = chess.Board(fen)

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
    
    # Close the engine
    engine.quit()

    return score_str

# Your existing analyze_game_between_moves_with_stockfish function remains here...

# Example usage:
# result = analyze_fen_with_stockfish('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1', 'stockfish-windows-x86-64-avx2 copy.exe', analysis_time=0.5, num_threads=4)
# print(result)


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
# analyze_game_between_moves_with_stockfish('fen.pgn', 'stockfish-windows-x86-64-avx2 copy.exe', start_move_number=8, end_move_number=10, analysis_time=0.5, num_threads=4)
