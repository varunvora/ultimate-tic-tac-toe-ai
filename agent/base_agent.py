from game.board import Board
from trueskill import Rating


class Agent:
    """
    Template for all agents to implement
    """

    def __init__(self, agent_name=""):
        self.agent_name = agent_name
        self.current_piece = None
        self.current_board = None
        self.opponent_piece = None
        self.rating = Rating()

    def play_move(self, board: Board):
        """
        Should be overloaded by child agent classes to add the needed functionality for their
        implementation. Makes a move on the board.
        @return: None
        """
        pass

    def set_current_piece(self, new_piece):
        """
        Sets the current player piece to the new given one.
        @param new_piece: An int representing the new piece the player will be using (1 for x and -1
        for 0)
        @return:
        """
        self.current_piece = new_piece

    def set_current_board(self, new_board):
        """
        Sets the current board the agent is playing to the given one.
        @param new_board: A reference to the board object the agent will be playing on
        @return: None
        """
        self.current_board = new_board

    def set_opponent_piece(self, player_piece):
        """
        Use the current piece to determine the opponent's piece
        @param player_piece: The piece this agent will be playing with
        @return: None
        """
        if player_piece == 1:
            self.opponent_piece = -1
        else:
            self.opponent_piece = 1

    def start_game(self, board, piece):
        """
        When the games starts the agent will receive a reference to the board object that it is
        playing on and the piece that it will be using. This function can be used by child agent
        classes as is or can be overloaded.
        @param board: A Board object containing the board that the player will be playing on
        @param piece: An int representing the piece the agent will be playing with
        @return: None
        """
        self.set_current_piece(piece)
        self.set_current_board(board)
        self.set_opponent_piece(piece)

    def end_game(self):
        """
        Once the game is over the agent will set it's current piece and board back to none to get
        ready for its next game. This function can be used by child agent classes as is or can be
        overloaded and change or add to what it does.
        @return: None
        """
        self.set_current_piece(None)
        self.set_current_board(None)

    def get_available_spaces(self):
        """
        Should be overloaded by child agent classes to add the needed functionality for their
        implementation
        @return: None
        """
        pass
