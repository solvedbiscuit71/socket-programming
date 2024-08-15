from pickle import *
from socket import *
from os import system
from time import sleep

serverAddress = ('localhost', 12000)
clientSocket = socket(AF_INET, SOCK_DGRAM)

tag = None
game = None

def sendto(obj):
    clientSocket.sendto(dumps(obj), serverAddress)

def recvfrom():
    data, _ = clientSocket.recvfrom(2048)
    return loads(data)

def draw():
    system('clear')
    print(f"You're {tag} ({game['turn']}'s Turn)")
    print(f"State: {game['state']}")
    print()
    
    print("Broad:")
    print("======")
    for r in range(3):
        for c in range(3):
            print(game['board'][r][c], end=' ')
        print()
    print("======")

try:
    while True:
        sendto(('NEW',))
        print("Waiting for opponent...")
        res = recvfrom()
        if res[0] == 'WAIT':
            res = recvfrom()

        _, tag, game = res
        
        while True:
            sleep(1)
            draw()
            if game['state'] == 'GOING':
                if game['turn'] == tag:
                    r, c = map(int, input('Enter your move: ').split(' '))
                    sendto(('MOVE', game['id'], (r, c)))
                    _, update, updateGame = recvfrom()
                    if update:
                        game = updateGame
                    else:
                        print('Invalid Move')
                elif game['turn'] != tag:
                    print("Waiting for opponent...")
                    sendto(('GET', game['id']))
                    _, game = recvfrom()
            else:
                break
            
        choice = input("Play Again (Y/N)? ")
        if choice == 'N':
            break

except KeyboardInterrupt:
    clientSocket.close()