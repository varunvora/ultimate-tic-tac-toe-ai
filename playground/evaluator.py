from typing import Optional
from agent.base_agent import Agent
from agent.simple_minimax_agent import SimpleMinimaxAgent
from agent.genetic_agent import GeneticAgent
from GeneticProgram.genetic import GeneticProgram
from game.board import Board


def play(x_player: Agent, o_player: Agent) -> Optional[Agent]:
    """
    Takes 2 agents and plays a game. Returns the winner.
    :param x_player: Agent playing X (plays first)
    :param o_player: Agent playing O (plays second)
    :return: The winner if an agent has won, else None in case of draw.
    """
    b = Board()
    current_player = x_player
    while not b.is_terminal():
        current_player.play_move(board=b)
        current_player = o_player if current_player == x_player else x_player
    assert b.winner is not None  # must be +1, 0, -1
    return None if b.winner == 0 else (x_player if b.winner == 1 else o_player)


def evaluate(a: Agent, b: Agent, num_games: int = 100) -> float:
    """
    Takes 2 agents :a and :b and plays :num_games games. Evaluates a's play against b.
    :param a: Agent a
    :param b: Agent b
    :param num_games: Number of games both agents play
    :return: Score for agent a
    """
    a_points = 0  # number of points A has. +1 for win, +0.5 for draw.
    x_player, o_player = a, b
    for i in range(num_games):
        winner = play(x_player, o_player)
        a_points = a_points + 1 if winner == a else (a_points + 0.5 if winner is None else a_points)
        x_player, o_player = o_player, x_player  # swap agents for the next game
    return a_points / num_games


if __name__ == '__main__':
    # Testing the evaluator. Score should be around 0.5 for random agents.
    from agent.random_agent import RandomAgent

    p, q = RandomAgent(), RandomAgent()
    print(evaluate(p, q))

    # simple minimax agent should be better, may take some time to finish
    p = SimpleMinimaxAgent(max_depth=4)
    print(evaluate(p, q, num_games=8))

    # Deeper minimax agent must outperform shallower minimax agent? Nope, it's 0.5
    q = SimpleMinimaxAgent(max_depth=2)
    print(evaluate(p, q, num_games=16))

    # Let's go 1 step deeper. Wins 75% !
    p = SimpleMinimaxAgent(max_depth=5)
    print(evaluate(p, q, num_games=16))

    gp = GeneticProgram()
    g = gp.generate_random_agent()
    print(evaluate(g, p, num_games=8))

