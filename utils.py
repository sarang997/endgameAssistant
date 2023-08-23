import requests

max_games = 10
lichess_username = "DeadWater"

def fetch_lichess_games(username, max_games=10, save_to_file=None):
    """
    Fetch recent games of a Lichess user and optionally save to a file.
    
    Args:
    - username (str): The Lichess username.
    - max_games (int): Maximum number of games to fetch. Default is 10.
    - save_to_file (str): Filename to save the games. If None, won't save. Default is None.
    
    Returns:
    - list of games in PGN format.
    """
    url = f"https://lichess.org/api/games/user/{username}"
    params = {
        'max': max_games,
        'pgnInJson': False  # to get the response in PGN format
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch games. Status code: {response.status_code}")
    
    games = response.text.strip().split("\n\n\n")
    
    if save_to_file:
        save_games_to_file(games, save_to_file)
    
    return games

def save_games_to_file(games, filename):
    """
    Save games to a file.
    
    Args:
    - games (list): List of games in PGN format.
    - filename (str): The name of the file to save the games.
    """
    with open(filename, 'w') as file:
        for game in games:
            file.write(game)
            file.write("\n\n\n")  # Separate games with three newlines

def load_games_from_file(filename):
    """
    Load games from a file.
    
    Args:
    - filename (str): The name of the file from which to load the games.
    
    Returns:
    - list of games in PGN format.
    """
    with open(filename, 'r') as file:
        content = file.read().strip()
        games = content.split("\n\n\n")  # Splitting by three newlines to separate individual games
    return games

# Example usage:
# games = fetch_lichess_games(lichess_username, max_games=max_games, save_to_file="games.pgn")

