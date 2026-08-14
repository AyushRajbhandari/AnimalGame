class Piece:
    """Base class for game pieces."""
    def __init__(self, player):
        self.__player = player

    def get_player(self):
        return self.__player

class Marmoset(Piece):
    def __init__(self, player):
        super().__init__(player)

    def is_path_clear(self, starting_row, starting_column, ending_row, ending_column, board):
        row = 1 if ending_row > starting_row else -1
        col = 1 if ending_column > starting_column else -1
        curr_r, curr_c = starting_row + row, starting_column + col
        while curr_r != ending_row or curr_c != ending_column:
            if board[curr_r][curr_c] is not None:
                return False
            curr_r += row
            curr_c += col
        return True

    def is_valid_move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos[0], start_pos[1]
        end_row, end_col = end_pos[0], end_pos[1]
        r_diff = abs(end_row - start_row)
        c_diff = abs(end_col - start_col)
        # Alternative move: 1 square orthogonally
        if r_diff + c_diff == 1:
            return True
        # main move: diagonal sliding, up to 3 squares
        if r_diff == c_diff and 0 < r_diff <= 3:
            return self.is_path_clear(start_row, start_col, end_row, end_col, board)

        return False
class Wallaby(Piece):
    def __init__(self, player):
        super().__init__(player)

    def is_valid_move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos[0], start_pos[1]
        end_row, end_col = end_pos[0], end_pos[1]
        r_diff = abs(end_row - start_row)
        c_diff = abs(end_col - start_col)

        # Alternative move: 1 square diagonally
        if r_diff == 1 and c_diff == 1:
            return True

        #Main  move: orthogonal sliding, exactly 1 square (no path to block)
        if (r_diff == 1 and c_diff == 0) or (r_diff == 0 and c_diff == 1):
            return True

        return False
class Axolotl(Piece):
    def __init__(self, player):
        super().__init__(player)

    def is_valid_move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos[0], start_pos[1]
        end_row, end_col = end_pos[0], end_pos[1]
        r_diff = abs(end_row - start_row)
        c_diff = abs(end_col - start_col)

        # Alt move: 1 square orthogonally
        if r_diff + c_diff == 1:
            return True

        # main move: diagonal jumping, exactly 4 squares
        if r_diff == 4 and c_diff == 4:
            return True

        return False

class Pika(Piece):
    def __init__(self, player):
        super().__init__(player)

    def is_valid_move(self, start_pos, end_pos, board):
        start_row, start_col = start_pos[0], start_pos[1]
        end_row, end_col = end_pos[0], end_pos[1]
        r_diff = abs(end_row - start_row)
        c_diff = abs(end_col - start_col)

        # Alt move: 1 square diagonally
        if r_diff == 1 and c_diff == 1:
            return True

        # main move: orthogonal jumping, exactly 2 squares
        if (r_diff == 2 and c_diff == 0) or (r_diff == 0 and c_diff == 2):
            return True

        return False
class AnimalGame:
    """Class representing the AnimalGame board, state, and moves."""

    def __init__(self):
        self.__state = 'UNFINISHED'
        self.__turn = 'tangerine'

        # Make a 7x7 grid
        self.__board = [[None for _ in range(7)] for _ in range(7)]
        self.initialize_board()

    def initialize_board(self):
        """Sets up the board with the initial pieces for both players."""
        setup_order = [Marmoset, Wallaby, Axolotl, Pika, Axolotl, Wallaby, Marmoset]

        # Tangerine starts in row 1
        for col in range(7):
            self.__board[0][col] = setup_order[col]('tangerine')

        # Amethyst starts in row 7
        for col in range(7):
            self.__board[6][col] = setup_order[col]('amethyst')

    def get_game_state(self):
        """Returns the current state of the game."""
        return self.__state
    def square_to_indices(self, square):
        """convert algebraic notation to row and column list."""
        if len(square) != 2:
            return None
        c_char, r_char = square[0].lower(), square[1]
        if not ('a' <= c_char <= 'g' and '1' <= r_char <= '7'):
            return None
        col_idx = ord(c_char) - ord('a')
        row_idx = int(r_char) - 1

        return [row_idx, col_idx]

    def make_move(self, start_square, end_square):
        """
        Attempts to move a piece. Returns True if it works and updates the game state,
        otherwise its False.
        """
        if self.__state != 'UNFINISHED':
            return False

        start_idx = self.square_to_indices(start_square)
        end_idx = self.square_to_indices(end_square)

        if not start_idx or not end_idx:
            return False

        start_row, start_col = start_idx[0], start_idx[1]
        end_row, end_col = end_idx[0], end_idx[1]

        piece = self.__board[start_row][start_col]

        # Check if there is a piece and it belongs to the current player
        if piece is None or piece.get_player() != self.__turn:
            return False

        target = self.__board[end_row][end_col]

        # Check if the target square has a piece of the same player
        if target is not None and target.get_player() == self.__turn:
            return False

       # Checks if the move is legal
        if not piece.is_valid_move([start_row, start_col], [end_row, end_col], self.__board):
            return False

        # If a Pika is captured, update 
        if target is not None and isinstance(target, Pika):
            self.__state = 'TANGERINE_WON' if self.__turn == 'tangerine' else 'AMETHYST_WON'

        # Execute the move
        self.__board[end_row][end_col] = piece
        self.__board[start_row][start_col] = None

        # Update the turn if the game is still going
        if self.__state == 'UNFINISHED':
            self.__turn = 'amethyst' if self.__turn == 'tangerine' else 'tangerine'

        return True
