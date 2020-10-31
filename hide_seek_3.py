import socketio
from urllib.parse import urlparse
from enum import Enum
from random import choice

class Cell_Value(Enum):
    RED = -1
    BLUE = 1
    NEUTRAL = 0

BOARD_WIDTH = 8

# sio = socketio.Client(logger=True, engineio_logger=True)
sio = socketio.Client()

# Player is either hide or seek
# seek is the Red Player
# hide is the Blue Player
player = None

room = None
board = []


def initialize_connection(site_address):
    # web address is like this: http://127.0.0.1:5001/seek/silent-hawk
    # first part of the path is the player side (hide or seek)
    # second part of the path is the name of the game room (silent-hawk)

    site_address = urlparse(site_address)
    game_info = site_address.path.strip('/').split('/')
    url = f'{site_address.scheme}://{site_address.netloc}'

    global board, player, room, sio
    player = game_info[0]
    room = game_info[1]
    board = [Cell_Value.NEUTRAL] * 64

    # sio = socketio.Client(logger=True, engineio_logger=True)

    sio.connect(url)
    sio.wait()

    # Red makes the first move
    if player == 'seek':
        pass
        # run the select square method

def get_available_moves():
    available_moves = []
    for i in range(len(board)):
        if board[i].name == 'NEUTRAL':
            available_moves.append(i)
    return available_moves

def select_move_random():
    available_moves = get_available_moves()
    random_selection = choice(available_moves)
    
    return random_selection

def generate_move_cells():
    move = select_move_random()
    all_cells = get_adjacent_cells(move)
    all_cells.append(move)
    all_cells = convert_board_index_to_web_index(all_cells)
    print('66 ->', all_cells)
    return all_cells

def convert_web_index_to_board_index(values):
    # the web board array starts at 1 and goes to 64
    # we need to convert to 0-63
    return  [int(i)-1 for i in values]

def convert_board_index_to_web_index(values):
    # the board array starts at 0 and goes to 63
    # we need to convert to 1-64
    return [str(int(i)+1) for i in values]

def update_the_board_with_moves_by(player_color,data):
    adjusted_data = convert_web_index_to_board_index(data)
    for i in adjusted_data:
        board[i] = player_color

def get_adjacent_cells(cell):
    adjacent_cells = []
    
    # Above
    if cell - BOARD_WIDTH >= 0:
        adjacent_cells.append(cell-BOARD_WIDTH)
    # Below
    if cell + BOARD_WIDTH < len(board):
        adjacent_cells.append(cell+BOARD_WIDTH)
    # Left
    if cell % BOARD_WIDTH != 0:
        adjacent_cells.append(cell-1)
    # Right
    if (cell+1)%BOARD_WIDTH !=0:
        adjacent_cells.append(cell+1)
    return adjacent_cells

def get_center_cell(data):
    for cell in data:
        cell_adjacents = get_adjacent_cells(cell)
        cell_overlap = [c for c in cell_adjacents if c in data]
        if len(cell_overlap) > 1:
            return cell
    return None

def try_to_determine_what_square_selected_by(player_color,data):
    adjusted_data = convert_web_index_to_board_index(data)

    if len(adjusted_data) == 1:
        # We only changed one square so selected square must be adjusted_data
        return adjusted_data[0]
    elif len(adjusted_data) == 2:
        # We can't determine which square was selected, so we select randomly
        return choice(adjusted_data)
    elif len(adjusted_data) > 2:
        return get_center_cell(adjusted_data)


# Socket IO functions
# @sio.on('connect',namespace=f'/{player}')
@sio.on('connect',namespace=f'/hide')
def connect_to_server():
    print('connection established to seek')
    print('my sid is', sio.sid)
    sio.emit('message', room, namespace=f'/hide')
    sio.emit('message', room, namespace=f'/seek')


# This message receives Blues move -- Player is seek/Red
@sio.on('rs', namespace='/seek')
def rs(data):

    # update the board with moves by (blue,data)
    update_the_board_with_moves_by(Cell_Value.BLUE,data)

    # try to determine what square selected by (blue,data)
    selected_cell = try_to_determine_what_square_selected_by(Cell_Value.BLUE, data)
    print(f'Blue selected cell: {selected_cell}')

    # If i'm playing and it's my turn, get a move and send it in
    if player == 'seek':
        print("I'm red and I should make a move")

# This message receives Red's move -- Player is hide/Blue
@sio.on('rh', namespace='/hide')
def rh_thing(data):
    # print(data)
    # update the board with moves by (blue,data)
    update_the_board_with_moves_by(Cell_Value.RED,data)

    # try to determine what square selected by (blue,data)
    selected_cell = try_to_determine_what_square_selected_by(Cell_Value.RED, data)
    print(f'Red selected cell: {selected_cell}')

    # If i'm playing and it's my turn, get a move and send it in
    if player == 'hide':
        send_hideBlue_to_server()
        print("I'm blue and I should make a move")


# These functions send moves to the server

def send_hideBlue_to_server():

    # create move
    move = generate_move_cells()
    print('Blue move: ', move)
    # todo send move data to server
    sio.emit('sh', [move,room],namespace='/hide')
    # Send turn to server from blue
    sio.emit('sttsb',['red', room],namespace='/hide')

def send_seekRed_to_server():
    # todo send move data to server
    pass

if __name__ == '__main__':
    initialize_connection('http://127.0.0.1:5001/hide/silent-hawk')
    # print(player)
    # print(room)
    # print(get_available_moves())
    # print(select_move_random(get_available_moves()))