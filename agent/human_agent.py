from agent.base_agent import Agent
from game.board import Board


class HumanAgent(Agent):
    """
    A Human makes the moves by taking input from CLI
    """
    def __init__(self, agent_name):
        super().__init__(agent_name)

    def play_move(self, board: Board):
        assert not board.is_terminal()
        legal_moves = board.get_legal_moves()
        print('Agent played', board.last_move)
        x, y, i, j = map(int, input('Your move: ').split())
        assert ((x, y), (i, j)) in legal_moves
        board.play(board.turn, (x, y), (i, j))
