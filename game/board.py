from subboard import SubBoard


class Board:
    """
    The main board of the game
    """

    def __init__(self, n):
        self.n: int = n
        self.grid = [[SubBoard(n) for _ in range(n)] for __ in range(n)]

    def __repr__(self):
        return f'{self.grid}'
