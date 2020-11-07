# a program to play red vs blue
# It's played on a board. Each side gets to choose an open
# square per side. Selecting a square turns each adjacent square
# your color. The game ends when all squares are filled.
# the winner is the side with the most squares

# created from this idea
# https://red-blue.herokuapp.com/
# https://github.com/akulchhillar/Red-Blue
# https://www.reddit.com/r/flask/comments/jkdxh0/hi_all_here_is_a_board_game_for_two_players_made/

# Flow:
# Display Status
# Wait for turn
# Evaluate/Update Board
# Check for win
# Save Game

from random import choice
from enum import Enum

class Cell_Value(Enum):
    RED = -1
    BLUE = 1
    NEUTRAL = 0


class Red_Blue():

    def __init__(self, width = 8, height = 8,
        display_status = True,
        red_player = 'human', 
        blue_player = 'human'):

        player_type = {
            'human': self.get_human_move,
            'random': self.get_random_computer_move
        }

        self.board_width = 8
        self.board = [Cell_Value.NEUTRAL] * width * height
        self.game_over = False

        self.player = {
            Cell_Value.BLUE: player_type[blue_player],
            Cell_Value.RED: player_type[red_player]
        }

        # self.red_player = red_player
        # self.blue_player = blue_player
        self.display_status = display_status
        self.history = []
        self.turn = Cell_Value.RED
    
    def get_available_moves(self):
        available_moves = []
        for i in range(len(self.board)):
            if self.board[i].name == 'NEUTRAL':
                available_moves.append(i)
        return available_moves
    
    def get_random_move(self):
        available_moves = self.get_available_moves()
        random_selection = choice(available_moves)
        return random_selection
    
    def check_if_move_is_valid(self,move):
        if int(move) in self.get_available_moves():
            return True
        return False
    
    def get_adjacent_cells(self, cell):
        adjacent_cells = []
        
        # Above
        if cell - self.board_width >= 0:
            adjacent_cells.append(cell-self.board_width)
        # Below
        if cell + self.board_width < len(self.board):
            adjacent_cells.append(cell+self.board_width)
        # Left
        if cell % self.board_width != 0:
            adjacent_cells.append(cell-1)
        # Right
        if (cell+1)%self.board_width !=0:
            adjacent_cells.append(cell+1)
        return adjacent_cells
    
    def get_center_cell(self, data):
        # used if we only get the data of cells flipped
        # but not selected cell
        for cell in data:
            cell_adjacents = self.get_adjacent_cells(cell)
            cell_overlap = [c for c in cell_adjacents if c in data]
            if len(cell_overlap) > 1:
                return cell
        return None

    def player_action(self):
        self.player[self.turn]()

    def get_human_move(self):
        move = None
        while move not in self.get_available_moves():
            move = input("Select cell: ")
            if move == 'q':
                break
            try:
                move = int(move)
            except:
                print('Selection must be an integer.')
            if move  not in self.get_available_moves():
                print('Invalid move... please select again')
        
        self.move(move)
    
    def get_random_computer_move(self):
        move = self.get_random_move()
        self.move(move)

    def change_player(self):
        if self.turn == Cell_Value.RED:
            self.turn = Cell_Value.BLUE
        else:
            self.turn = Cell_Value.RED

    def show_status(self):
        r,b = self.red_blue_score()
        print(f'Turn: {self.turn.name} -- Score RED: {r}, BLUE: {b}')
    
    def show_board(self):
        row = ''
        for i, cell in enumerate(self.board):
            if cell == Cell_Value.RED:
                row += ' RR '
            elif cell == Cell_Value.BLUE:
                row += ' BB '
            else:
                row += f' {i:2d} '
            if (i+1) % self.board_width == 0:
                # we've reached the end of the row.
                print(row)
                print()
                row = ''

    def move(self, move):
        all_cells = self.get_adjacent_cells(move)
        all_cells.append(move)
        for cell in all_cells:
            self.board[cell] = self.turn
        board = [cell.value for cell in self.board]
        self.history.append([self.turn.value, move, board])

    def red_blue_score(self):
        red = len([cell for cell in self.board if cell.name == Cell_Value.RED.name])
        blue = len([cell for cell in self.board if cell.name == Cell_Value.BLUE.name])
        return red, blue

    def check_game_status(self):
        if len(self.get_available_moves()) == 0:
            # game is over,
            # so append the winner of the game to the game history

            self.game_over = True
            print('Winner!!!')

            red_cells = [cell for cell in self.board if cell.name == Cell_Value.RED.name]
            blue_cells = [cell for cell in self.board if cell.name == Cell_Value.BLUE.name]
            winner = 0
            if len(red_cells) > len(blue_cells):
                winner = Cell_Value.RED.value
            elif len(blue_cells) > len(red_cells):
                winner = Cell_Value.BLUE.value
            else:
                winner = Cell_Value.NEUTRAL.value
            for item in self.history:
                item.insert(0,winner)
    def play_game(self):
        while self.game_over is False:
            if self.display_status:
                self.show_status()
                self.show_board()
            self.player_action()
            
            self.change_player()
            self.check_game_status()
        print(self.history)
        print(self.show_status())


if __name__=='__main__':
    game = Red_Blue(display_status=False, red_player='random', blue_player='random')
    game.play_game()
