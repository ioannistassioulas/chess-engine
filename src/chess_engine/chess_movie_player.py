import io
import os

import cairosvg
import chess
import chess.pgn
import chess.svg
from PIL import Image


def read_game_from_pgn(filename: str) -> chess.pgn.Game:
    """"""
    directory = os.path.join(os.getcwd(), "chess-games")
    game_location = os.path.join(directory, filename)
    with open(game_location) as pgn:
        game = chess.pgn.read_game(pgn)

    if game is None:
        raise ValueError("No game found!")

    return game


def chess_movie(
    game: chess.pgn.Game,
    framerate: int = 2,
) -> bytes:
    """Take file of chess notation and produce gif showing game."""
    board = chess.Board(chess.Board.starting_fen)  # define the board

    png_bytes = cairosvg.svg2png(bytestring=chess.svg.board(board))
    if png_bytes is None:
        raise ValueError("Unable to render starting chess board")

    # create a list of frames for the gif
    starting_position_frame = Image.open(io.BytesIO(png_bytes))
    frames = []
    frames.append(starting_position_frame)

    for move in game.mainline_moves():
        # push the board for each move
        board.push(move)

        png_bytes = cairosvg.svg2png(bytestring=chess.svg.board(board))
        if png_bytes is None:
            raise ValueError("Unable to render starting chess board")
        current_position_frame = Image.open(io.BytesIO(png_bytes))
        frames.append(current_position_frame)

    # create a gif
    buffer = io.BytesIO()
    frames[0].save(
        buffer,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=1000 / framerate,
        loop=0,
    )
    buffer.seek(0)
    return buffer.getvalue()
