import chess.pgn

def position_meets_criteria(board):
    """
    Check if the given position contains only kings, rooks, and pawns 
    and has at least one king, one rook, and one pawn for both sides.
    """
    fen_parts = board.fen().split(' ')
    piece_placement = fen_parts[0]  # Only take the piece placement part of the FEN

    # Check for any other pieces
    if any(piece in piece_placement for piece in ['q', 'Q', 'b', 'B', 'n', 'N']):
        return False

    white_kings = piece_placement.count('K')
    white_rooks = piece_placement.count('R')
    white_pawns = piece_placement.count('P')
    
    black_kings = piece_placement.count('k')
    black_rooks = piece_placement.count('r')
    black_pawns = piece_placement.count('p')
    
    if (white_kings >= 1 and white_rooks >= 1 and white_pawns >= 1 and
        black_kings >= 1 and black_rooks >= 1 and black_pawns >= 1):
        return True

    return False



def analyze_game_for_position(game):
    """
    Analyze the game move-by-move. If any position in the game has only king, rook, and pawns for both sides,
    print a green message along with the FEN of the position; 
    otherwise, print the URL of the game (from the "Site" tag).
    
    Args:
    - game (chess.pgn.Game): A game object from the python-chess library.
    """
    board = game.board()

    for move in game.mainline_moves():
        board.push(move)
        if position_meets_criteria(board):
            # Green message
            print("\033[92mFound a position with only king, rook, and pawns for both sides.\033[0m")
            print("FEN of the position:", board.fen())
            return

    # If no such position is found, print the game's URL in red
    game_url = game.headers.get("Site", "URL not found")
    print("\033[91mGame does not meet the specified criteria. Game URL:\033[0m", game_url)
    print("\n" + "="*50 + "\n")



def analyze_games_in_file(filename):
    """
    Iterate over each game in the PGN file and analyze it.
    
    Args:
    - filename (str): The name of the PGN file containing the games.
    """
    with open(filename, 'r') as pgn_file:
        while True:
            game = chess.pgn.read_game(pgn_file)
            if game is None:  # End of file
                break
            analyze_game_for_position(game)

# Example usage:
analyze_games_in_file("games.pgn")
