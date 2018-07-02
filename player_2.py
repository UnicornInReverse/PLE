import random
import socket
import RPi.GPIO as gpio  # https://pypi.python.org/pypi/RPi.GPIO more info
import time
from requests import ConnectionError

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

pawn_position = 0
game = "20"

gpio.setmode(gpio.BCM)
gpio.setup(18, gpio.IN, pull_up_down=gpio.PUD_UP)


def start():
    sock.connect(('192.168.43.106', 9050))  # connect to remote server
    sock.sendall(game.encode('utf-8'))
    receive()


def throw_dice():
    global pawn_position

    while True:
        input_state = gpio.input(18)
        if not input_state:
            print('Button Pressed')
            time.sleep(0.2)
            break

    die = random.randint(1, 6)
    45pawn_position += die

    if pawn_position >= int(game):
        win()
    else:
        print("pos" + str(pawn_position))
        return die


def receive():
    while True:
        data = sock.recv(128)  # the buffer in this example is 128 bytes
        if data == "end":
            print("Player 1 wins")
            lose()
            break
        else:
            print(data)
            send(throw_dice())


def send(die):
    print("send" + str(pawn_position))
    data = str(die)
    sock.sendall(data.encode('utf-8'))
    receive()


def win():
    print("Player 2 wins, end")
    data = "end"
    sock.sendall(data.encode('utf-8'))
    sock.close()
    exit(0)


def lose():
    print("lose")
    sock.shutdown(1)
    sock.close()
    exit(0)


try:
    start()
except ConnectionError:
    print("Okdoei")
finally:
    print("BYE")
