from typing import Optional, Tuple, List

import numpy as np

from subboard import SubBoard


class Board:
    """
    The main board of the game
    The methods named with _single_leading_underscore are for internal use.
    They can be ignored unless you intend to modify this class.
    https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe
    """

    def __init__(self, n):
        self.n: int = n
        self.grid: List[List[SubBoard]] = [[SubBoard(n) for _ in range(n)] for __ in range(n)]
        self.winner: Optional[int] = None  # set only after game is over. +1 for X, -1 for O, 0 for draw.
        # Keep a track of last move because the next legal move depends on it.
        self.last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
        self.turn: int = 1  # X always starts

    def __repr__(self):
        """
        :return: String representation of the board. Kinda readable.
        """
        t = [[self.grid[i][j].get_grid() for j in range(self.n)] for i in range(self.n)]
        return str(np.array(t).reshape((self.n*self.n, self.n*self.n)))

    def get_grid(self):
        """
        :return: The entire board. Can be used for tests.
        """
        return self.grid

    def is_board_full(self) -> bool:
        """
        Checks if the board is full by checking if all the sub-boards are full.
        :return: True if all sub-boards are full
        """
        return all(x.is_board_full() for x in sum(self.grid, []))

    def play(self, player: int, board_position: Tuple[int, int], sub_board_position: Tuple[int, int]) -> Optional[int]:
        """
        Makes player's move at the given position and returns the outcome if the game ended.
        Throws an error for an illegal move.

        :param player: 1 for X, -1 for O
        :param board_position: Co-ordinates of the main board
        :param sub_board_position: Co-ordinates of the position in the sub-board for the given main board.
        :return: 1 if X wins, -1 if O wins, 0 for draw, None if the game is not yet completed.
        """
        x, y = board_position
        assert self.winner is None  # can not make a move after the game is ended
        assert self.turn == player
        sub_board_winner = self.grid[x][y].play(player, sub_board_position)
        self.last_move = (board_position, sub_board_position)
        self.turn *= -1  # change turns from +1 -> -1 and -1 -> +1
        if sub_board_winner is not None:  # sub-board has a result! check if board has a result.
            if self._is_winner(player, board_position):
                self.winner = player
                return self.winner
            if self.is_board_full():
                self.winner = 0
                return 0  # draw

    def _process_count(self, player: int, position: Tuple[int, int]) -> int:
        i, j = position
        configs = [[(i, j - 1), '←', (i, j + 1), '→'],
                   [(i - 1, j), '↑', (i + 1, j), '↓'],
                   [(i - 1, j - 1), '↖', (i + 1, j + 1), '↘'],
                   [(i + 1, j - 1), '↙', (i - 1, j + 1), '↗']]
        return 1 + max([self._count(player, p1, d1) + self._count(player, p2, d2) for p1, d1, p2, d2 in configs])

    def _is_winner(self, player: int, position: Tuple[int, int]) -> bool:
        return self._process_count(player, position) >= self.n

    def _is_valid_position(self, position: Tuple[int, int]) -> bool:
        i, j = position
        return 0 <= i < self.n and 0 <= j < self.n

    def _count(self, player: int, position: Tuple[int, int], direction: str) -> int:
        """
        Counts the number of times :param player appears consecutively in a given :param direction.
        """
        i, j = position
        result = 0
        while self._is_valid_position((i, j)) and self.grid[i][j].winner == player:
            i = i - int(direction in {'↑', '↖', '↗'})
            i = i + int(direction in {'↓', '↘', '↙'})
            j = j - int(direction in {'←', '↖', '↙'})
            j = j + int(direction in {'→', '↗', '↘'})
            result += 1
        return result

    def get_legal_moves(self) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        (_, _), (x, y) = self.last_move  # get the position in the sub-board for the last move
        if not self.grid[x][y].is_terminal():
            return [((x, y), (i, j)) for (i, j) in self.grid[x][y].get_legal_moves()]

        # If a player is sent to play on a terminal board, then that player may play in any other board.
        return sum([self.grid[x][y].get_legal_moves() for x in range(self.n) for y in range(self.n)], [])

    def is_terminal(self):
        """
        Checks if the game has ended by checking if there is a winner or the board is full
        :return: True if the game has ended
        """
        return self.winner is not None or self.is_board_full()
