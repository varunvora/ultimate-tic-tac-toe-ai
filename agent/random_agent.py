from agent.base_agent import Agent
from game.board import Board
from random import sample


class RandomAgent(Agent):
    """
    Picks a random move from the legal moves.
    """

    def __init__(self, name="Random Sample Agent"):
        super(RandomAgent, self).__init__(agent_name=name)

    def play_move(self, board: Board):
        assert not board.is_terminal()
        legal_moves = board.get_legal_moves()
        move = sample(legal_moves, 1)[0]
        ((x, y), (i, j)) = move
        board.play(board.turn, (x, y), (i, j))
