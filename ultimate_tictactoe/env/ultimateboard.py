import numpy as np

'''
ub = UltimateBoard()
while True:
    print(ub)
    symbol = 'X' if ub.turn % 2 else 'O'
    if ub.is_game_over:
        winner = ub.winner
        if winner is not None:
            print(f'{winner} wins!')
        else:
            print('Draw!')
        break
    print(f'Turn {ub.turn}')
    while True:
        print(f'{symbol}: ', end='')
        board_x, board_y, tile_x, tile_y = map(int, input().split())
        if ub.mark(board_x - 1, board_y - 1, tile_x - 1, tile_y - 1):
            break
        print('Invalid input.')
'''
class UltimateBoard:
    def __init__(self):
        self._ultimate_board = np.full((81,), ' ')
        self._boards = np.full((9,), ' ')
        self._turn = 1
        self._prev_move = None
        self._is_game_over = False
        self._winner = None

    def __str__(self):
        return (
            f"               │               │\n"
            f"   {self.ultimate_board[ 0]} │ {self.ultimate_board[ 1]} │ {self.ultimate_board[ 2]}   │   {self.ultimate_board[ 3]} │ {self.ultimate_board[ 4]} │ {self.ultimate_board[ 5]}   │   {self.ultimate_board[ 6]} │ {self.ultimate_board[ 7]} │ {self.ultimate_board[ 8]}\n"
            f"  ───┼───┼───  │  ───┼───┼───  │  ───┼───┼───\n"
            f"   {self.ultimate_board[ 9]} │ {self.ultimate_board[10]} │ {self.ultimate_board[11]}   │   {self.ultimate_board[12]} │ {self.ultimate_board[13]} │ {self.ultimate_board[14]}   │   {self.ultimate_board[15]} │ {self.ultimate_board[16]} │ {self.ultimate_board[17]}\n"
            f"  ───┼───┼───  │  ───┼───┼───  │  ───┼───┼───\n"
            f"   {self.ultimate_board[18]} │ {self.ultimate_board[19]} │ {self.ultimate_board[20]}   │   {self.ultimate_board[21]} │ {self.ultimate_board[22]} │ {self.ultimate_board[23]}   │   {self.ultimate_board[24]} │ {self.ultimate_board[25]} │ {self.ultimate_board[26]}\n"
            f"               │               │\n"
            f"───────────────┼───────────────┼───────────────\n"
            f"               │               │\n"
            f"   {self.ultimate_board[27]} │ {self.ultimate_board[28]} │ {self.ultimate_board[29]}   │   {self.ultimate_board[30]} │ {self.ultimate_board[31]} │ {self.ultimate_board[32]}   │   {self.ultimate_board[33]} │ {self.ultimate_board[34]} │ {self.ultimate_board[35]}\n"
            f"  ───┼───┼───  │  ───┼───┼───  │  ───┼───┼───\n"
            f"   {self.ultimate_board[36]} │ {self.ultimate_board[37]} │ {self.ultimate_board[38]}   │   {self.ultimate_board[39]} │ {self.ultimate_board[40]} │ {self.ultimate_board[41]}   │   {self.ultimate_board[42]} │ {self.ultimate_board[43]} │ {self.ultimate_board[44]}\n"
            f"  ───┼───┼───  │  ───┼───┼───  │  ───┼───┼───\n"
            f"   {self.ultimate_board[45]} │ {self.ultimate_board[46]} │ {self.ultimate_board[47]}   │   {self.ultimate_board[48]} │ {self.ultimate_board[49]} │ {self.ultimate_board[50]}   │   {self.ultimate_board[51]} │ {self.ultimate_board[52]} │ {self.ultimate_board[53]}\n"
            f"               │               │\n"
            f"───────────────┼───────────────┼───────────────\n"
            f"               │               │\n"
            f"   {self.ultimate_board[54]} │ {self.ultimate_board[55]} │ {self.ultimate_board[56]}   │   {self.ultimate_board[57]} │ {self.ultimate_board[58]} │ {self.ultimate_board[59]}   │   {self.ultimate_board[60]} │ {self.ultimate_board[61]} │ {self.ultimate_board[62]}\n"
            f"  ───┼───┼───  │  ───┼───┼───  │  ───┼───┼───\n"
            f"   {self.ultimate_board[63]} │ {self.ultimate_board[64]} │ {self.ultimate_board[65]}   │   {self.ultimate_board[66]} │ {self.ultimate_board[67]} │ {self.ultimate_board[68]}   │   {self.ultimate_board[69]} │ {self.ultimate_board[70]} │ {self.ultimate_board[71]}\n"
            f"  ───┼───┼───  │  ───┼───┼───  │  ───┼───┼───\n"
            f"   {self.ultimate_board[72]} │ {self.ultimate_board[73]} │ {self.ultimate_board[74]}   │   {self.ultimate_board[75]} │ {self.ultimate_board[76]} │ {self.ultimate_board[77]}   │   {self.ultimate_board[78]} │ {self.ultimate_board[79]} │ {self.ultimate_board[80]}\n"
            f"               │               │"
        )

    @property
    def ultimate_board(self):
        return self._ultimate_board

    @property
    def boards(self):
        return self._boards

    @property
    def turn(self):
        return self._turn

    @property
    def prev_move(self):
        return self._prev_move

    @property
    def is_game_over(self):
        return self._is_game_over

    @property
    def winner(self):
        return self._winner

    def mark(self, board_x, board_y, tile_x, tile_y):
        board_index = 3 * board_y + board_x
        cell_index = 27 * board_y + 3 * board_x + 9 * tile_y + tile_x

        is_legal = all(0 <= coord <= 2 for coord in (board_x, board_y, tile_x, tile_y)) and (
            self.turn == 1 or (
                self.boards[board_index] == ' ' and
                self.ultimate_board[cell_index] == ' ' and (
                    (board_x, board_y) == (self.prev_move[2], self.prev_move[3]) or
                    self.boards[3 * self.prev_move[3] + self.prev_move[2]] != ' '
                )
            )
        )
        if is_legal:
            symbol = 'X' if self.turn % 2 else 'O'
            self._ultimate_board[cell_index] = symbol
            self._prev_move = (board_x, board_y, tile_x, tile_y)

            row_start_index = cell_index - tile_x
            col_start_index = cell_index - 9 * tile_y
            top_left_start_index = col_start_index - tile_x
            top_right_start_index = top_left_start_index + 2
            if (
                all(cell == symbol for cell in self.ultimate_board[row_start_index:row_start_index + 3]) or
                all(cell == symbol for cell in self.ultimate_board[col_start_index:col_start_index + 27:9]) or
                all(cell == symbol for cell in self.ultimate_board[top_left_start_index:top_left_start_index + 30:10]) or
                all(cell == symbol for cell in self.ultimate_board[top_right_start_index:top_right_start_index + 24:8])
            ):
                self._boards[board_index] = symbol

                row_start_index = board_index - board_x
                col_start_index = board_index - 3 * board_y
                top_left_start_index = col_start_index - board_x
                top_right_start_index = top_left_start_index + 2
                if (
                    all(board == symbol for board in self.boards[row_start_index:row_start_index + 3]) or
                    all(board == symbol for board in self.boards[col_start_index:col_start_index + 9:3]) or
                    all(board == symbol for board in self.boards[top_left_start_index:top_left_start_index + 12:4]) or
                    all(board == symbol for board in self.boards[top_right_start_index:top_right_start_index + 6:2])
                ):
                    self._winner = symbol
                    self._is_game_over = True

        if not self.is_game_over:
            if any(board == ' ' for board in self.boards):
                self._turn += 1
            else:
                self._is_game_over = True

        return is_legal

    def reset(self):
        self.__init__()