import random
import socket

from requests import ConnectionError

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('192.168.43.106', 9050))
sock.listen(1)  # allow only 1 connection
connection, client_address = sock.accept()

pawn_position = 0
game = 0


def start():
    while True:
        data = connection.recv(128)  # the buffer in this example is 128 bytes
        if data:
            global game
            game = int(data)
            print(game)
            send(throw_dice())


def throw_dice():
    global pawn_position
    die = random.randint(1, 6)
    pawn_position += die

    if pawn_position >= int(game):
        win()
    else:
        print("pos" + str(pawn_position))
        return die


def receive():
    while True:
        data = connection.recv(128)  # the buffer in this example is 128 bytes
        if data == "end":
            print("Player 2 wins")
            lose()
            break
        else:
            print(data)
            send(throw_dice())


def send(die):
    print("send" + str(pawn_position))
    data = str(die)
    connection.sendall(data.encode('utf-8'))
    receive()


def win():
    print("Player 1 wins, end")
    data = "end"
    connection.sendall(data.encode('utf-8'))
    connection.close()
    exit(0)


def lose():
    print("lose")
    connection.shutdown(1)
    connection.close()
    exit(0)


try:
    start()
except ConnectionError:
    print("Okdoei")
finally:
    print("BYE")
