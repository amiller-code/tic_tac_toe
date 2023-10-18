from random import randint

# Global dictionary with the setup of the initial board
BLANK_BOARD = {'v1': '   |   |   ',
               'h1': '___ ___ ___',
               'v2': '   |   |   ',
               'h2': '___ ___ ___',
               'v3': '   |   |   ', }
ROW_CONVERSION = {
    'a': 1,
    'b': 5,
    'c': 9,
}

keep_playing = 'y'
turn = ''
winner = ''
played_turns = []
board = BLANK_BOARD.copy()
x_score = 0
o_score = 0


# Function to print the board in it's current state
def print_board(current_board):
    print('   A   B   C ')
    print(f'1 {current_board["v1"]}')
    print(f'  {current_board["h1"]}')
    print(f'2 {current_board["v2"]}')
    print(f'  {current_board["h2"]}')
    print(f'3 {current_board["v3"]}')


# Function to randomly decide if X or O will start first
def decide_first():
    first_player = 'X'
    if x_score == o_score:
        i = randint(0, 1)
        if i == 0:
            first_player = 'X'
        else:
            first_player = 'O'
    elif x_score < o_score:
        first_player = 'X'
    elif o_score < x_score:
        first_player = 'O'
    return first_player


# Function to change whose turn it is
def flip_turn(previous_turn):
    if previous_turn == 'X':
        next_turn = 'O'
    else:
        next_turn = 'X'
    return next_turn


# Function to ask the current player to submit their move and check whether it is legal
def ask_for_move(this_turn):
    move = input(f'Player {this_turn}, pick your next move: ').lower()
    while len(move) != 2 or move[0] not in ROW_CONVERSION.keys() or move[1] not in ['1', '2', '3'] \
            or move in played_turns or len(move) != 2:
        move = input(f'That move is not possible. Either it is not on the board or has already been played,'
                     f' please try again: ').lower()
    return move


# Function to transfer the chosen move to the current board
def place_move(move, this_turn):
    row = 'v' + move[1]
    col = ROW_CONVERSION[move[0]]
    board[row] = board[row][:col] + this_turn + board[row][col + 1:]
    played_turns.append(move)


# Function to check all possibilities for a win
def check_for_win():
    win_checks = {
        'row1': f'{board["v1"][1]}{board["v1"][5]}{board["v1"][9]}',
        'row2': f'{board["v2"][1]}{board["v2"][5]}{board["v2"][9]}',
        'row3': f'{board["v3"][1]}{board["v3"][5]}{board["v3"][9]}',
        'col1': f'{board["v1"][1]}{board["v2"][1]}{board["v3"][1]}',
        'col2': f'{board["v1"][5]}{board["v2"][5]}{board["v3"][5]}',
        'col3': f'{board["v1"][9]}{board["v2"][9]}{board["v3"][9]}',
        'dia1': f'{board["v1"][1]}{board["v2"][5]}{board["v3"][9]}',
        'dia2': f'{board["v1"][9]}{board["v2"][5]}{board["v3"][1]}',
    }
    winner_after_turn = ''
    # If there was a winner, check which player won
    for condition in win_checks.values():
        if condition == 'XXX' or condition == 'OOO':
            winner_after_turn = condition[0]
    # If game is complete and no one has won, the game ends in a tie
    if len(played_turns) == 9 and winner_after_turn == '':
        winner_after_turn = 'tie'
    return winner_after_turn


if __name__ == '__main__':
   # Initiate game
    print('TIC TAC TOE!\nFind a friend and decide who will be "X"s and who will be "O"s\nWhen prompted, type the '
          'location where you want to play in by the column first (letter) then row (number). E.g. "B3"\n')
    keep_playing = 'y'

    while keep_playing == 'y':
        winner = ''
        turn = decide_first()
        played_turns = []
        # Copy the blank board to a new variable to be able to track the game
        board = BLANK_BOARD.copy()
        while winner == '':
            print_board(board)
            chosen_move = ask_for_move(turn)
            place_move(chosen_move, turn)
            winner = check_for_win()
            if winner != '':
                print_board(board)
                # If either player won, declare it and change the score
                if winner == 'X':
                    x_score += 1
                    print(f'Game over! {winner} wins!')
                elif winner == 'O':
                    o_score += 1
                    print(f'Game over! {winner} wins!')
                elif winner == 'tie':
                    print(f'Tie game! No winner this round :(')
                print(f'Current score: X-{x_score}, O-{o_score}')
            else:
                # If neither player won this round, change whose turn it is and repeat
                turn = flip_turn(turn)
        keep_playing = input('Would you like to play again? (Y/N): ').lower()
        # Error handling for incorrect input
        while keep_playing != 'y' and keep_playing != 'n':
            keep_playing = input('Please type either "Y" to play again or "N" to stop playing: ').lower()
