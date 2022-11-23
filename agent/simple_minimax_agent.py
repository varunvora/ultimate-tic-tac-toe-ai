from copy import deepcopy
from typing import Optional
from agent import Agent
from game.board import Board


class SimpleMinimaxAgent(Agent):

    def __init__(self, name="Simple Minimax Agent", max_depth=float('inf')):
        super().__init__(name)
        self.max_depth = max_depth

    def play_move(self, board):
        assert not board.is_terminal()
        move = self.minimax_search(board)
        ((x, y), (i, j)) = move
        board.play(board.turn, (x, y), (i, j))

    def minimax_search(self, board: Board) -> tuple[int, int]:
        if board.turn == 1:
            value, move = self.max_value(board)
        else:
            value, move = self.min_value(board)
        return move

    def max_value(self, board: Board, alpha=-float('inf'), beta=float('inf'), depth=0) -> tuple[
        float, Optional[tuple[tuple[int, int], tuple[int, int]]]]:
        if board.is_terminal():
            return board.winner, None
        if depth >= self.max_depth:
            return alpha, board.get_legal_moves()[0]  # todo we can do better here?
        v, move = -float('inf'), None
        for (x, y), (i, j) in board.get_legal_moves():
            board_copy = deepcopy(board)
            board_copy.play(1, (x, y), (i, j))
            v2, a2 = self.min_value(board_copy, alpha, beta, depth + 1)
            if v2 > v:
                v, move = v2, (i, j)
                alpha = max(alpha, v)
            if v >= beta:
                return v, move
        return v, move

    def min_value(self, board: Board, alpha=-float('inf'), beta=float('inf'), depth=0) -> tuple[
        float, Optional[tuple[tuple[int, int], tuple[int, int]]]]:
        if board.is_terminal():
            return board.winner, None
        if depth >= self.max_depth:
            return beta, board.get_legal_moves()[0]  # todo we can do better here?
        v, move = float('inf'), None
        for (x, y), (i, j) in board.get_legal_moves():
            board_copy = deepcopy(board)
            board_copy.play(-1, (x, y), (i, j))
            v2, a2 = self.max_value(board_copy, alpha, beta, depth + 1)
            if v2 < v:
                v, move = v2, ((x, y), (i, j))
                beta = min(beta, v)
            if v <= alpha:
                return v, move
        return v, move
