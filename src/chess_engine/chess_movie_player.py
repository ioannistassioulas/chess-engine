import io
import os

import cairosvg
import chess
import chess.pgn
import chess.svg
from PIL import Image, ImageFile


def read_game_from_pgn(filename: str) -> chess.pgn.Game:
    """"""
    directory = os.path.join(os.getcwd(), "..", "chess-games")
    game_location = os.path.join(directory, filename)
    with open(game_location) as pgn:
        game = chess.pgn.read_game(pgn)

    if game is None:
        raise ValueError("No game found!")

    return game


def chess_movie(
    game: chess.pgn.Game,
    framerate: int = 2,
) -> list[ImageFile.ImageFile]:
    """Take file of chess notation and produce gif showing game."""
    board = chess.Board(chess.Board.starting_fen)  # define the board

    png_bytes = cairosvg.svg2png(bytestring=chess.svg.board(board))
    starting_position_frame = Image.open(io.BytesIO(png_bytes))
    frames = []
    frames.append(starting_position_frame)

    for move in game.mainline_moves():
        # push the board for each move
        board.push(move)

    return frames
