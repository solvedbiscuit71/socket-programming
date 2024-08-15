from socket import *
from pickle import *
from datetime import datetime

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('', 12000))

lobby = []

gameStateTracker = {}
nextGameId = 1

def nextState(board):
    # row
    for r in range(3):
        if board[r][0] == board[r][1] == board[r][2] != '-':
            return 'WIN'
    
    # column
    for c in range(3):
        if board[0][c] == board[1][c] == board[2][c] != '-':
            return 'WIN'

    # diagonal
    if board[0][0] == board[1][1] == board[2][2] != '-':
        return 'WIN'
    
    if board[0][2] == board[1][1] == board[2][0] != '-':
        return 'WIN'
    
    # tie?
    for r in range(3):
        for c in range(3):
            if board[r][c] == '-':
                return 'GOING'
    else:
        return 'TIE'

def updateGame(game, move):
    r, c = move
    if 0 <= r < 3 and 0 <= c < 3 and game['board'][r][c] == '-' and game['state'] == 'GOING':
        game['board'][r][c] = game['turn']
        game['state'] = nextState(game['board'])
        if game['state'] == 'GOING':
            game['turn'] = 'O' if game['turn'] == 'X' else 'X'
        return True
    else:
        return False
    
def timestamp():
    t = datetime.now()
    return t.strftime('%H:%M:%S')

def sendto(obj, address):
    print(f"[{timestamp()}] send {obj} to {address}")
    serverSocket.sendto(dumps(obj), address)

print(f"Server listening at port {12000}")
try:
    while True:
        data, clientAddress = serverSocket.recvfrom(2048)
        TYPE, *args = loads(data)
        print(f"[{timestamp()}] receive {TYPE} {args} from {clientAddress}")
        
        # [TYPE, ARGS..]
        match TYPE:
            case 'NEW':
                if lobby:
                    peerAddress = lobby.pop(0)
                    gameId = nextGameId
                    nextGameId += 1
                    gameStateTracker[gameId] = {
                        'id': gameId,
                        'X': peerAddress,
                        'O': clientAddress,
                        'board': [['-'] * 3 for _ in range(3)],
                        'turn': 'X',
                        'state': 'GOING'
                    }
                    
                    sendto(( 'CREATED', 'X',  gameStateTracker[gameId] ), peerAddress)
                    sendto(( 'CREATED', 'O',  gameStateTracker[gameId] ), clientAddress)
                else:
                    lobby.append(clientAddress)
                    sendto(('WAIT',), clientAddress)
            case 'GET':
                gameId = args[0]
                game = gameStateTracker[gameId]
                if game['X'] != clientAddress and game['O'] != clientAddress:
                    continue
                sendto(( 'STATE', game ), clientAddress)
            case 'MOVE':
                gameId, move = args
                game = gameStateTracker[gameId]               
                if game[game['turn']] != clientAddress:
                    continue
                if updateGame(game, move):
                    payload = ( 'UPDATED', True, game )
                else:
                    payload = ( 'UPDATED', False, None )
                sendto(payload, clientAddress)


except KeyboardInterrupt:
    serverSocket.close()
