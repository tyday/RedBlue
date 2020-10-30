import socketio

sio = socketio.Client(logger=True, engineio_logger=True)

@sio.event(namespace='/seek')
def connect():
    print('connection established')
    print('my sid is', sio.sid)
    sio.emit('message','speedy-cow',namespace='/seek')
    sio.emit('message','speedy-cow',namespace='/hide')
    
# @sio.event(namespace='/seek')
@sio.on('rs', namespace='/seek')
def rs(data):
    print('rs', data)

@sio.on('rh', namespace='/hide')
def rh_thing(data):
    print('rh', data)

@sio.event(namespace='/seek')
def message(data):
    print(data)

@sio.event(namespace='/seek')
def sttcr(data):
    print(data)


@sio.event
def disconnect():
    print('disconnected from server')

sio.connect('http://127.0.0.1:5000/')
sio.wait()