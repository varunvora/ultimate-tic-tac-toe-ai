from typing import Optional, Tuple, List

from subboard import SubBoard


class Board:
    """
    The main board of the game
    """

    def __init__(self, n):
        self.n: int = n
        self.grid: List[List[SubBoard]] = [[SubBoard(n) for _ in range(n)] for __ in range(n)]
        self.winner: Optional[int] = None
        self.last_move: Optional[Tuple[Tuple[int, int], Tuple[int, int]]] = None
        self.turn: int = 1  # X always starts

    def __repr__(self):
        # todo figure out a way to make it visually better
        return f'{self.grid}'

    def is_board_full(self) -> bool:
        return all(x.is_board_full() for x in sum(self.grid, []))

    def play(self, player: int, board_position: Tuple[int, int], sub_board_position: Tuple[int, int]):
        x, y = board_position
        assert self.winner is None
        assert self.turn == player
        sub_board_winner = self.grid[x][y].play(player, sub_board_position)
        self.last_move = (board_position, sub_board_position)
        self.turn *= -1  # change turns from +1 -> -1 and -1 -> +1
        if sub_board_winner is not None:
            if self.is_winner(player, board_position):
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
        while self.is_valid_position((i, j)) and self.grid[i][j].winner == player:
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
        return sum([self.grid[x][y].get_legal_moves() for x in range(self.n) for y in range(self.n)], [])

    def is_terminal(self):
        return self.winner is not None or self.is_board_full()
