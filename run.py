from utils import fetch_lichess_games
from analyze import analyze_games_in_file
import os
#define the variables here
max_games = 10
lichess_username = "DeadWater"
games_output_path = "games.pgn"

#define which type of endgame positions you want to get
white_allowed_pieces = ['K', 'R', 'P', 'P', 'P']       # White can have King and Rook and 3 Pawns
black_allowed_pieces = ['k', 'r', 'p', 'p', 'p']  # Black can have King, Rook, and 2 Pawns

#save the games to a pgn file
file_exists = os.path.exists(games_output_path)
if file_exists:
    print("the games already exist!")
else:
    games = fetch_lichess_games(lichess_username, max_games=max_games, save_to_file=games_output_path)

analyze_games_in_file(games_output_path, white_allowed_pieces, black_allowed_pieces)

