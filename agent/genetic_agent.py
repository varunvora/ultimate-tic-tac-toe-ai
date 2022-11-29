from time import time
from copy import deepcopy
from typing import Optional, Tuple, List
from agent.base_agent import Agent
from game.board import Board
from game.subboard import SubBoard


class GeneticAgent(Agent):

    def __init__(self, agent_name="", existing_traits=None):
        super().__init__(agent_name)
        if existing_traits is None:
            existing_traits = []
        self.traits = existing_traits
        self.win_count = 0
        self.lose_count = 0
        self.total_win_score = 0
        self.total_genetic_rounds = 0
        self.total_turns = 0
        self.move_scores = []
        self.average_time = 0

    def set_traits(self, new_traits: List[float]) -> None:
        """
        Sets the traits list of the agent to the new traits list given.

        @param new_traits: A list of traits representing traits for the genetic agent
        @return: None
        """
        self.traits = new_traits

    def set_specific_trait(self, trait_pos: int, new_trait: float) -> None:
        """
        Will set the value of a specific trait in the agent's trait list to the given value.

        @param trait_pos: The int index of the trait will be set
        @param new_trait: The float representing the trait that will replace the existing trait
        at trait_pos
        @return: None
        """

        self.traits[trait_pos] = new_trait

    def play_move(self, board: Board) -> None:
        """
        Run alpha-beta search on the current game board and find the best move for the agent to
        make. Will also calculate the new average time to find a move.
        @param board: The current board that the agent will play on
        @return: None
        """
        # If you can play on any board then choose the best one using minimax
        # Then for the board find the best move using minimax
        # Then choose the best move from the list and set the current board to be the space's
        #     corresponding subboard
        # Play the move on the board

        self.current_piece = board.turn
        self.set_opponent_piece(self.current_piece)

        start_time = round(time() * 1000)
        self.total_turns += 1

        # Find and play move
        val, global_move, sub_move = self.alpha_beta(board, 0, True)
        board.play(self.current_piece, global_move, sub_move)

        # Calculate new average time
        end_time = round(time() * 1000)
        duration = end_time - start_time # in milliseconds
        #total_games = (self.win_count + self.lose_count)
        self.average_time = ((self.average_time * self.total_turns) + duration) / self.total_turns

    def start_game(self, board: Board, piece: int) -> None:
        """
        When the games starts the agent will receive a reference to the board object that it is
        playing on and the piece that it will be using. This function can be used by child agent
        classes as is or can be overloaded.
        @param board: A Board object containing the board that the player will be playing on
        @param piece: An int representing the piece the agent will be playing with
        @return: None
        """
        Agent.start_game(self, board, piece)

    def alpha_beta(self, board: Board, current_board: int, max_player: bool) -> Tuple[float, Tuple[int, int],
                                                                                      Tuple[int, int]]:
        """
        Kicks of the alpha-beta search on the game board
        @param board: A board object the player will bbe using to decide their next move
        @param current_board: The 1D index where the current subboard would be located in an array
        @param max_player: A boolean representing if the maxplayer is evaluted first
        @return: A tuple that contains the value of the returned move(s),
        the 2D coordinates of the subboard the move is played on, the 2D coordinates of the
        square in the subboard where the move is played
        """

        depth = 3
        if self.current_piece == 1:
            val, global_move, sub_move = self.maximize_value(board, current_board, depth, float("-inf"), float("inf"))
        else:
            val, global_move, sub_move = self.minimize_value(board, current_board, depth, float("-inf"), float("inf"))

        return val, global_move, sub_move

    def maximize_value(self, board: Board, current_board_index: int, depth: int, alpha: float,
                       beta: float) -> Tuple[float, Tuple[int, int], Tuple[int, int]]:
        """
        The maximize side of alpha-beta search. Will evaluate the prospective moves as the
        maximizing player. When the max search depth is reached then the current board will be
        evaluted to determine how valuable it is to the player.
        @param board: The Board object where the player will be making their moves and will be
        used to look at all the available moves.
        @param current_board_index: The 1D index of the current subboard
        @param depth: An int presenting the current search depth
        @param alpha: An int representing the alpha value in alpha-beta search
        @param beta: An in representing the beta value in alpha-beta search
        @return: A tuple that contains the value of the returned move(s),
        the 2D coordinates of the subboard the move is played on, the 2D coordinates of the
        square in the subboard where the move is played
        """

        v = float('-inf')
        best_board_move = (-1, -1)
        best_subboard_move = (-1, -1)

        if board.is_terminal():
            return board.winner, best_board_move, best_subboard_move

        # perform depth check
        if depth <= 0:
            # Evaluate current board
            curr_eval = self.eval_game(board, current_board_index)
            return curr_eval, best_board_move, best_subboard_move

        # This variable is here in case we want to add a heuristic to sort the successors before
        # evaluation
        available = board.get_legal_moves()

        # For each available space (limited to specific or all available space depending on last
        # move)
        for brd, subs in board.get_legal_moves():
            # Play piece
            temp_board = deepcopy(board)
            temp_board.play(1, brd, subs)
            sub_index = brd[1] + 3 * brd[0] # Convert the 2D coordinates of the subboard to a 1D index
            possible_v, global_move, sub_move = self.minimize_value(temp_board, sub_index,
                                                                    depth-1, alpha, beta)
            # Remove piece

            if possible_v > v:
                v = possible_v
                best_board_move = brd
                best_subboard_move = subs

            if v >= beta:
                return v, best_board_move, best_subboard_move
            alpha = max(v, alpha)
        return v, best_board_move, best_subboard_move

    def minimize_value(self, board: Board, current_board_index: int, depth: int, alpha: float,
                       beta: float) -> Tuple[float, Tuple[int, int], Tuple[int, int]]:
        """
        The minimize side of alpha-beta search. Will evaluate the prospective moves as the
        minimizing player. When the max search depth is reached then the current board will be
        evaluated to determine how valuable it is to the player.
        @param board: The Board object where the player will be making their moves and will be
        used to look at all the available moves.
        @param current_board_index: The 1D index of the current subboard
        @param depth: An int presenting the current search depth
        @param alpha: An int representing the alpha value in alpha-beta search
        @param beta: An in representing the beta value in alpha-beta search
        @return: A tuple that contains the value of the returned move(s),
        the 2D coordinates of the subboard the move is played on, the 2D coordinates of the
        square in the subboard where the move is played
        """

        v = float('inf')
        best_board_move = (-1, -1)
        best_subboard_move = (-1, -1)

        if board.is_terminal():
            return board.winner, best_board_move, best_subboard_move

        # perform depth check
        if depth <= 0:
            # Evaluate current board
            curr_eval = self.eval_game(board, current_board_index)
            return curr_eval, best_board_move, best_subboard_move

        # This variable is here in case we want to add a heuristic to sort the successors before
        # evaluation
        available = board.get_legal_moves()

        # For each available space (limited to specific or all available space depending on last
        # move)
        for brd, subs in board.get_legal_moves():
            # Play piece
            temp_board = deepcopy(board)
            temp_board.play(-1, brd, subs)
            sub_index = brd[1] + 3 * brd[0] # Convert the 2D coordinates of the subboard to a 1D index
            possible_v, global_move, sub_move = self.maximize_value(temp_board, sub_index,
                                                                    depth - 1, alpha, beta)
            # Remove piece

            if possible_v < v:
                v = possible_v
                best_board_move = brd
                best_subboard_move = subs

            if v <= alpha:
                return v, best_board_move, best_subboard_move
            beta = min(v, beta)
        return v, best_board_move, best_subboard_move

    def eval_game(self, board: Board, current_board: int) -> float:
        """
        The base evaluation function that will be used to determine the value of the specific
        board state. Will iterate through all of its subboards and determine their values before determining
        the overall global board state's worth
        @param board: The current board object to evaluate
        @param current_board: The 1D index of the current subboard
        @return: A float representing the global board state's value
        """

        def convert_to_list(grid: List[List[SubBoard]]) -> List[SubBoard]:
            """
            Converts the 2D array of subboards to a 1D list
            @param grid: 2D array of subboards
            @return: 1D list of subboards
            """
            array = []
            for row in range(0, 3):
                for col in range(0, 3):
                    array.append(grid[row][col])
            return array

        evaluation = 0
        global_board = []
        sub_list = convert_to_list(board.get_grid())
        board_win = board.winner
        if board_win is None:
            board_win = 0

        for num, sub in enumerate(sub_list):
            sub_list = convert_to_list(sub.get_grid())
            sub_win = sub.winner
            if sub_win is None:
                sub_win = 0
            eval_val = self.evaluate_board(sub_list, sub_win)
            evaluation += eval_val * 1.5 * self.traits[num]
            if current_board == num:
                evaluation += eval_val * self.traits[num]
            temp_eval = sub_win
            evaluation -= temp_eval * self.traits[num]
            global_board.append(temp_eval)

        evaluation -= board_win * 5000
        evaluation += self.evaluate_board(global_board, board_win) * 150

        return evaluation

    def evaluate_board(self, sub_board: List[int], winner: int) -> float:
        """
        Evaluate the individual value of a specific subboard. Will look at horizontal, vertical,
        and diagonals to determine how many matches the player is close to or has and how many
        matches the opponent is close to or has.
        @param sub_board: A 1D array of all the spaces in the specific subboard
        @param winner: The winner value of the specific subboard
        @return: A float representing the value of the subboard
        """

        def check_doubles(triple: List[int], piece_val: int) -> bool:
            """
            Will check if pairs of space will match up based on the given triple of indices.
            @param triple: A list of 3 indices representing the set to look at
            @param piece_val: An int representing the specific player's piece (may need to be
            changed if the board isn't properly evaluated
            @return: A boolean saying if any 2 in a row pairs exist
            """
            return ((triple[0] + triple[1] == -2 * self.current_piece and triple[2] == -1 * piece_val)
                    or (triple[1] + triple[2] == -2 * self.current_piece and triple[0] == -1 * piece_val)
                    or (triple[0] + triple[2] == -2 * self.current_piece and triple[1] == -1 * piece_val))

        def eval_player(piece_val: int, eval_num: float, sub: bool = True) -> float:
            """
            Performs an evaluation of the spaces for each player's pieces. First checks each row, then
            the columns, and then the diagonal triples. It will then look at pairs on the
            rows, columns, and diagonals.
            @param piece_val: An int representing the player's piece
            @param eval_num: A float representing the current evaluation value
            @param sub: A boolean representing if subtration should be used in the evaluation
            calculations
            @return: A float representing the current evaluated value of the subboard
            """

            # Look at all horizontal "triples"
            if sub_board[0] + sub_board[1] + sub_board[2] == 2 * piece_val \
                    or sub_board[3] + sub_board[4] + sub_board[5] == 2 * piece_val \
                    or sub_board[6] + sub_board[7] + sub_board[8] == 2 * piece_val:
                eval_num = eval_num - 6 if sub else eval_num + 6

            # Look at all vertical "triples"
            if sub_board[0] + sub_board[3] + sub_board[6] == 2 * piece_val \
                    or sub_board[1] + sub_board[4] + sub_board[7] == 2 * piece_val \
                    or sub_board[2] + sub_board[5] + sub_board[8] == 2 * piece_val:
                eval_num = eval_num - 6 if sub else eval_num + 6

            # Look at all diagonal "triples"
            if sub_board[0] + sub_board[4] + sub_board[8] == 2 * piece_val \
                    or sub_board[2] + sub_board[4] + sub_board[6] == 2 * piece_val:
                eval_num = eval_num - 7 if sub else eval_num + 7

            # Look at all possible doubles (horizontal, vertical, and diagonal)
            if check_doubles([0, 1, 2], piece_val) or check_doubles([3, 4, 5], piece_val) \
                    or check_doubles([6, 7, 8], piece_val):
                eval_num = eval_num - 9 if sub else eval_num + 9
            elif check_doubles([0, 3, 6], piece_val) or check_doubles([1, 4, 7], piece_val) \
                    or check_doubles([2, 5, 9], piece_val):
                eval_num = eval_num - 9 if sub else eval_num + 9
            elif check_doubles([0, 4, 8], self.opponent_piece) or check_doubles([2, 4, 6], piece_val):
                eval_num = eval_num - 9 if sub else eval_num + 9
            return eval_num

        evaluation = 0

        # Score the specific position based on it's placement alone
        for num, val in enumerate(self.traits):
            evaluation -= sub_board[num] * val

        # For one player
        evaluation = eval_player(self.current_piece, evaluation)

        # For the other player
        evaluation = eval_player(self.opponent_piece, evaluation, False)

        # Check if the board has already been won
        evaluation -= winner

        return evaluation / 12
