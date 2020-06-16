from MCTS.uct.algorithm.enums import GamePhase


class Board:
    '''Class for the board, it cointans the players'''

    def __init__(self, n_rows, n_cols, n_to_win, player_1=None,
                 player_2=None, player_1_starts=True, is_graphics_on=True):
        '''
        :param n_rows: how many rows
        :param n_cols: how many columns
        :param n_to_win: how many tokens need to be in line to win
        :param player_1_starts: is player 1 starting.
        :param is_graphics_on: is the graphics on
        :param player_1: Agent than inherits Player class if None then human player
        :param player_2: Agent than inherits Player class if None then human player
        '''
        self.players = [player_1, player_2]
        self.is_graphics_on = is_graphics_on
        self.whos_turn_is_now = 1 if player_1_starts else 2
        self.player_1_starts = player_1_starts
        self.n_to_win = n_to_win
        self.n_cols = n_cols
        self.n_rows = n_rows
        self.last_move = None
        # row 0 is at the bottom
        # 0  - empty field, 1 - player_1's token, 2 - player_2's token
        self.board = [[0 for col in range(self.n_cols)] for row in range(self.n_rows)]
        self.result = 0
        self.phase = GamePhase.IN_PROGRESS

    def field_content(self, row, col):
        '''
        Returns the field content
        :param row: which row (indexing from 0)
        :param col: which column (indexing from 0)
        :return: 0 if empty or number of player
        '''
        return self.board[row][col]

    def find_row(self, col):
        for row in range(self.n_rows):
            if self.field_content(row, col) == 0:
                return row
        else:
            return self.n_rows

    def put_token(self, col):
        '''
        Puts the token of player player_id on the field row,col
        :param col: column
        :return: True if the field was empty
        '''
        row = self.find_row(col)
        if row < self.n_rows:
            self.last_move = (row, col)
            self.board[row][col] = self.whos_turn_is_now
            return True
        return False

    def give_possible_moves(self):
        '''
        Gives all possible moves.
        :return: List of all the columns that are not full yet.
        '''
        return [i for i, content in enumerate(self.board[-1]) if content == 0]

    def opposite_player(self, player_id):
        if player_id == 1:
            return 2
        else:
            return 1

    def play(self):
        '''
        Makes the player move.
        :return: False if game is still on, True if game is over
        '''
        possible_moves = self.give_possible_moves()
        move = (self.active_player()).move(self, possible_moves)
        if not self.put_token(move):
            raise Exception('move not possible!')
        self.whos_turn_is_now = self.opposite_player(self.whos_turn_is_now)
        return self.is_game_over()

    def play_human(self, move):
        '''
        Makes the player move.
        :return: False if game is still on, True if game is over
        '''
        if not self.put_token(move):
            raise Exception('move not possible!')
        self.whos_turn_is_now = self.opposite_player(self.whos_turn_is_now)
        return self.is_game_over()

    def active_player(self):
        return self.players[self.whos_turn_is_now - 1]

    def is_game_over(self):
        '''
        Checks if game is over
        :return: True if is over, False if is on
        '''
        if self.check_rows() or self.check_columns() or self.check_diagonals():
            self.phase = GamePhase.PLAYER1_WON if self.whos_turn_is_now == 2 else GamePhase.PLAYER2_WON
            return True
        if self.give_possible_moves() == []:
            self.phase = GamePhase.DRAW
            return True
        return False

    def check_rows(self):
        '''
        Checks if in any row is a sequence. sets the result if some player wins.
        :return: True if there is, False if isnt
        '''
        length = 1
        last = 0
        for row in self.board:
            for field in row:
                if field == last:
                    length += 1
                else:
                    last = field
                    length = 1
                if last != 0 and length == self.n_to_win:
                    self.result = last
                    return True
            last = 0
            length = 1
        return False

    def check_columns(self):
        '''
        Checks if in any column is a sequence. sets the result if some player wins.
        :return: True if there is, False if isn't
        '''
        length = 1
        last = 0
        for col_i in range(self.n_cols):
            for row_i in range(self.n_rows):
                if self.field_content(row_i, col_i) == last:
                    length += 1
                else:
                    last = self.field_content(row_i, col_i)
                    length = 1
                if last != 0 and length == self.n_to_win:
                    self.result = last
                    return True
            last = 0
            length = 1
        return False

    def check_diagonals(self):
        '''
        Checks if in any diagonal is a sequence. sets the result if some player wins.
        :return: True if there is, False if issnt
        '''
        length = 1
        last = 0
        for k in range(self.n_rows + self.n_cols - 1):
            for col_i in range(k + 1):
                row_i = k - col_i
                if row_i < self.n_rows and col_i < self.n_cols:
                    if self.field_content(row_i, col_i) == last:
                        length += 1
                    else:
                        last = self.field_content(row_i, col_i)
                        length = 1
                    if last != 0 and length == self.n_to_win:
                        self.result = last
                        return True
            last = 0
            length = 1
        for p in range(self.n_rows + self.n_cols - 1):
            for q in range(p + 1):
                x = self.n_cols - 1 - q
                y = p - q
                if y < self.n_rows and x < self.n_cols and x >= 0 and y >= 0:
                    if self.field_content(y, x) == last:
                        length += 1
                    else:
                        last = self.field_content(y, x)
                        length = 1
                    if last != 0 and length == self.n_to_win:
                        self.result = last
                        return True
            last = 0
            length = 1
        return False

    def count_rows(self, player_num):
        '''
        Counts the longest sequence in rows of player_num
        :return: number, free spots netxt to the line
        '''
        max_len_free_spots = (0, 0)
        free_before = False
        length = 1
        last = 0
        for row in self.board:
            for field in row:
                if field == last and field == player_num:
                    length += 1
                elif field == player_num:
                    length = 1
                elif field == 0:
                    if max_len_free_spots[0] < length:
                        max_len_free_spots = (length, 2 if free_before else 1)
                    elif max_len_free_spots[1] < 2 and max_len_free_spots[0] == length:
                        # if free is 1 it  wont be worse, cannot be 0
                        max_len_free_spots = (length, 2 if free_before else 1)
                    length = 0
                    free_before = True
                else:
                    # if the token is opponent's
                    if free_before and max_len_free_spots[0] < length:
                        max_len_free_spots = (length, 1)
                    length = 0
                    free_before = False
                if field==player_num and length == self.n_to_win:
                    return self.n_to_win, 0
                last = field

            if max_len_free_spots[0] < length:
                if free_before:
                    max_len_free_spots = (length, 1)

            last = 0
            length = 1
            free_before = False
        return max_len_free_spots


    def count_columns(self, player_num):
        '''
        Counts the longest sequence in columns of player_num
        :return: number, free spots around the sequence
        '''
        max_len_free_spots = (0, 0)
        free_before = False
        length = 1
        last = 0
        for col_i in range(self.n_cols):
            for row_i in range(self.n_rows):
                current_field = self.field_content(row_i, col_i)
                if current_field == last and current_field == player_num:
                    length += 1
                elif current_field == player_num:
                    length = 1
                elif current_field==0:
                    if max_len_free_spots[0] < length:
                        max_len_free_spots = (length, 2 if free_before else 1)
                    elif max_len_free_spots[1] < 2 and max_len_free_spots[0] == length:
                        # if free is 1 it  wont be worse, cannot be 0
                        max_len_free_spots = (length, 2 if free_before else 1)
                    length = 0
                    free_before = True
                else:
                    # if the token is opponent's
                    if free_before and max_len_free_spots[0] < length:
                        max_len_free_spots = (length, 1)
                    length=0
                    free_before =False
                if current_field==player_num and length == self.n_to_win:
                    return self.n_to_win,0
                last = current_field

            if max_len_free_spots[0] < length:
                if free_before:
                    max_len_free_spots = (length, 1)
            last = 0
            length = 1
            free_before=False
        return max_len_free_spots

    def count_diagonals(self, player_num):
        '''
        Counts the longest sequence in diagonals of player_num
        :return: number
        '''
        max_len_free_spots = (0, 0)
        free_before = False
        length = 1
        last = 0
        for k in range(self.n_rows + self.n_cols - 1):
            for col_i in range(k + 1):
                row_i = k - col_i
                if row_i < self.n_rows and col_i < self.n_cols:
                    current_field = self.field_content(row_i, col_i)
                    if current_field == last and current_field == player_num:
                        length += 1
                    elif current_field == player_num:
                        length = 1
                    elif current_field==0:
                        if max_len_free_spots[0] < length:
                            max_len_free_spots = (length, 2 if free_before else 1)
                        elif max_len_free_spots[1] < 2 and max_len_free_spots[0] == length:
                            # if free is 1 it  wont be worse, cannot be 0
                            max_len_free_spots = (length, 2 if free_before else 1)

                        length = 0
                        free_before = True
                    else:
                        # if the token is opponent's
                        if free_before and max_len_free_spots[0] < length:
                            max_len_free_spots = (length, 1)
                        length=0
                        free_before =False
                    if current_field == player_num and length == self.n_to_win:
                        return self.n_to_win,0

                    last = current_field
            if max_len_free_spots[0] < length:
                if free_before:
                    max_len_free_spots = (length, 1)
            last = 0
            length = 1
            free_before=False
        for p in range(self.n_rows + self.n_cols - 1):
            for q in range(p + 1):
                x = self.n_cols - 1 - q
                y = p - q
                if y < self.n_rows and x < self.n_cols and x >= 0 and y >= 0:
                    current_field = self.field_content(y, x)
                    if current_field == last and current_field == player_num:
                        length += 1
                    elif current_field == player_num:
                        length = 1
                    elif current_field == 0:
                        if max_len_free_spots[0] < length:
                            max_len_free_spots = (length, 2 if free_before else 1)
                        elif max_len_free_spots[1] < 2 and max_len_free_spots[0] == length:
                            # if free is 1 it  wont be worse, cannot be 0
                            max_len_free_spots = (length, 2 if free_before else 1)

                        length = 0
                        free_before=True
                    else:
                        # if the token is opponent's
                        if free_before and max_len_free_spots[0] < length:
                            max_len_free_spots = (length, 1)
                        length = 0
                        free_before=False
                    if current_field == player_num and length == self.n_to_win:
                        return self.n_to_win,0

                    last = current_field
            if max_len_free_spots[0] < length:
                if free_before:
                    max_len_free_spots = (length, 1)
            last = 0
            length = 1
            free_before=False
        return max_len_free_spots

    def count_the_longest_line(self, player_num):
        max = (0,0)
        seq_len, free = self.count_rows(player_num)
        if seq_len == self.n_to_win:
            return seq_len, free
        elif max[0] < seq_len:
            max = (seq_len, free)
        elif free == 2 and max[0]==seq_len:
            max= (seq_len, free)
        seq_len,free = self.count_columns(player_num)
        if seq_len == self.n_to_win:
            return seq_len, free
        elif max[0] < seq_len:
            max = (seq_len,free)
        elif free == 2 and max[0]==seq_len:
            max= (seq_len, free)
        seq_len,free = self.count_diagonals(player_num)
        if max[0] < seq_len:
            max = (seq_len,free)
        elif free == 2 and max[0]==seq_len:
            max= (seq_len, free)
        return max

    def deep_copy(self):
        rc = Board(8, 8, 4)
        rc.whos_turn_is_now = self.whos_turn_is_now

        rc.n_to_win = self.n_to_win
        rc.n_cols = self.n_cols
        rc.n_rows = self.n_rows
        # row 0 is at the bottom
        # 0  - empty field, 1 - player_1's token, 2 - player_2's token
        # self.board = [[0 for col in range(self.n_cols)] for row in range(self.n_rows)]
        for i in range(self.n_rows):
            for j in range(self.n_cols):
                rc.board[i][j] = self.board[i][j]

        rc.phase = self.phase
        return rc
