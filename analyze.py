import chess.pgn

# white_allowed_pieces = ['K', 'B', 'P', 'P', 'P']       # White can have King and Rook
# black_allowed_pieces = ['k', 'n', 'p', 'p']  # Black can have King, Rook, and Pawn

def position_meets_criteria(board, white_allowed_pieces, black_allowed_pieces):
    """
    Check if the given position matches the exact allowed pieces (and their counts) for white and black.
    
    Args:
    - board (chess.Board): A board object from the python-chess library.
    - white_allowed_pieces (list): List of allowed white pieces with exact counts.
    - black_allowed_pieces (list): List of allowed black pieces with exact counts.
    
    Returns:
    - bool: True if the position meets the criteria, otherwise False.
    """
    # Counting pieces on the board
    white_counts = {piece: list(board.piece_map().values()).count(chess.Piece.from_symbol(piece)) for piece in ['K', 'Q', 'R', 'B', 'N', 'P']}
    black_counts = {piece: list(board.piece_map().values()).count(chess.Piece.from_symbol(piece.lower())) for piece in ['K', 'Q', 'R', 'B', 'N', 'P']}

    # Checking counts against allowed pieces
    for piece in ['K', 'Q', 'R', 'B', 'N', 'P']:
        if white_counts[piece] != white_allowed_pieces.count(piece):
            return False 
        if black_counts[piece] != black_allowed_pieces.count(piece.lower()):
            return False
            
    return True


def analyze_game_for_position(game, white_allowed_pieces, black_allowed_pieces, output_filename):
    """
    Analyze the game move-by-move based on allowed pieces criteria for white and black.
    If any position in the game meets the criteria, save the FEN to a file and print a green message;
    otherwise, print the URL of the game (from the "Site" tag).
    
    Args:
    - game (chess.pgn.Game): A game object from the python-chess library.
    - white_allowed_pieces (list): List of allowed white pieces with exact counts.
    - black_allowed_pieces (list): List of allowed black pieces with exact counts.
    - output_filename (str): The name of the file to save FENs of positions meeting the criteria.
    """
    board = game.board()

    for move in game.mainline_moves():
        board.push(move)
        if position_meets_criteria(board, white_allowed_pieces, black_allowed_pieces):
            # Save the FEN to the specified file
            save_fen_to_file(board.fen(), output_filename)
            # Green message
            print("\033[92mFound a position meeting the specified criteria.\033[0m")
            print("FEN of the position:", board.fen())
            return

    # If no such position is found, print the game's URL in red
    game_url = game.headers.get("Site", "URL not found")
    print("\033[91mGame does not meet the specified criteria. Game URL:\033[0m", game_url)
    print("\n" + "="*50 + "\n")


    # If no such position is found, print the game's URL in red
    game_url = game.headers.get("Site", "URL not found")
    print("\033[91mGame does not meet the specified criteria. Game URL:\033[0m", game_url)
    print("\n" + "="*50 + "\n")

def get_fen_of_desired_postion(filename, white_allowed_pieces, black_allowed_pieces, output_filename):
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
            analyze_game_for_position(game, white_allowed_pieces, black_allowed_pieces, output_filename)

def save_fen_to_file(fen, filename):
    """
    Save a FEN to a file.
    
    Args:
    - fen (str): The FEN string to save.
    - filename (str): The name of the file to save the FEN.
    """
    with open(filename, 'a') as file:  # 'a' mode appends to the file
        file.write(fen + '\n')  # Write the FEN followed by a newline

# Example usage:
# get_fen_of_desired_postion("games.pgn", white_allowed_pieces, black_allowed_pieces)
