from typing import Tuple, Optional, List

import numpy as np


class SubBoard:
    """
    The inner board for ultimate tic-tac-toe. Works like tic-tac-toe board.
    Each cell in the sub-board contains one of the following:
    <ul>
    <li> X is represented by 1 </li>
    <li> O is represented by -1 </li>
    <li> blank is represented by 0 </li>
    </ul>
    """

    def __init__(self, n: int):
        self.n: int = n
        self.grid = np.array([[0 for _ in range(n)] for __ in range(n)], dtype=np.byte)
        self.winner: Optional[int] = None

    def __repr__(self):
        return f'{self.grid}'

    def get_grid(self):
        return self.grid

    def is_board_full(self) -> bool:
        return np.count_nonzero(self.grid) == (self.n ** 2)

    def play(self, player: int, position: Tuple[int, int]) -> Optional[int]:
        i, j = position
        assert self.grid[i][j] == 0  # can play only on blank cells
        assert self.winner is None  # can not play on a board after it's won
        self.grid[i][j] = player
        if self.is_winner(player, position):
            self.winner = player
            return self.winner
        if self.is_board_full():
            self.winner = 0
            return 0  # draw

    def process_count(self, player: int, position: Tuple[int, int]) -> int:
        i, j = position
        configs = [[(i, j - 1), '←', (i, j + 1), '→'],
                   [(i - 1, j), '↑', (i + 1, j), '↓'],
                   [(i - 1, j - 1), '↖', (i + 1, j + 1), '↘'],
                   [(i + 1, j - 1), '↙', (i - 1, j + 1), '↗']]
        return 1 + max([self.count(player, p1, d1) + self.count(player, p2, d2) for p1, d1, p2, d2 in configs])

    def is_winner(self, player: int, position: Tuple[int, int]) -> bool:
        return self.process_count(player, position) >= self.n

    def is_valid_position(self, position: Tuple[int, int]) -> bool:
        i, j = position
        return 0 <= i < self.n and 0 <= j < self.n

    def count(self, player: int, position: Tuple[int, int], direction: str) -> int:
        """
        Counts the number of times :param player appears consecutively in a given :param direction.
        """
        i, j = position
        result = 0
        while self.is_valid_position((i, j)) and self.grid[i][j] == player:
            i = i - int(direction in {'↑', '↖', '↗'})
            i = i + int(direction in {'↓', '↘', '↙'})
            j = j - int(direction in {'←', '↖', '↙'})
            j = j + int(direction in {'→', '↗', '↘'})
            result += 1
        return result

    def get_legal_moves(self) -> List[Tuple[int, int]]:
        if self.winner is None:
            return [(i, j) for i in range(self.n) for j in range(self.n) if self.grid[i][j] == 0]
        return []

    def is_terminal(self):
        return self.winner is not None or self.is_board_full()

    def get_html(self):
        t = lambda x, y: 'X' if self.grid[x][y] == 1 else ('O' if self.grid[x][y] == -1 else '_')
        return f"""<table>
            <tr>
                <td>{t(0, 0)}</td>
                <td>{t(0, 1)}</td>
                <td>{t(0, 2)}</td>
            </tr>
            <tr>
                <td>{t(1, 0)}</td>
                <td>{t(1, 1)}</td>
                <td>{t(1, 2)}</td>
            </tr>
            <tr>
                <td>{t(2, 0)}</td>
                <td>{t(2, 1)}</td>
                <td>{t(2, 2)}</td>
            </tr>
        </table>
        """
