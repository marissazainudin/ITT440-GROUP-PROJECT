import socket
import errno
import time
import random
from os import system


_ = system('clear')

# Choosing name

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print("|           Hello! Welcome to Snake and Ladder Game                  |")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

print ("Name will show on server")
nickname = input("Please enter your name: ")

# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.56.107', 8888))

# just of effects. add a delay of 1 second before performing any action
WAIT  = 1
MAX_VAL = 50

# snake brings you down
snakes = {
    47: 13,
    36: 18,
    26: 8,
}

# ladder brings you up
ladders = {
    22: 42,
    4: 25,
    30: 49,
}

#message for player
playerTurn = [
    "Your turn to move.",
    "Go.",
    "Please continue.",
    "Keep trying!",
    "All set?",
    "",
]


snakeBite = [
    "Oh man!",
    "uh oh !",
    "you got bite by a snake",
    "oh my god!!! !!",
    "oh nooo :(  "
]


ladderJump = [
    "oh yess",
    "hoorayy",
    "good job!",
    "you are doing great!",
    "amazing!"
]



def welcome_msg():
    msg = """
    Hello! Welcome to Snake and Ladder Game.
    41 42 43 44 45 46 47 48 49 50
       ^              *     ^
    40 39 38 37 36 35 34 33 32 31
       |        *       \     \
    21 22 23 24 25 26 27 28 29 30
            /   ^  *     |
    20 19 18 17 16 15 14 13 12 11
               /        \
    1  2  3  4  5  6  7  8  9  10
    Snake    Ladder
    47->13   22->42
    36->18   4->25
    26->8    30->49
    """
    print(msg)

def get_diceValue():
    time.sleep(WAIT)
    diceValue = random.randint(1,6)
    print("Dice value: " + str(diceValue))
    return diceValue


def got_snakeBite(oldValue, currentValue, playerName):
    print("\n" + random.choice(snakeBite).upper() + " ~~~~>")
    print("\n" + playerName + " was bitten by a snake. Go down from " + str(oldValue)+ " to " + str(currentValue))

def got_ladderJump(oldValue, currentValue, playerName):
    print("\n" + random.choice(ladderJump).upper() + "!!!!!")
    print("\n" + playerName + " went up the ladder from " + str(oldValue) + " to " + str(currentValue))




def snakeLadder(playerName, currentValue, diceValue):
    time.sleep(WAIT)
    oldValue = currentValue
    currentValue = currentValue + diceValue

    if currentValue > MAX_VAL:
        print(" A " + str(MAX_VAL - oldValue) + " is required to win this game. Don't give up !" )
        return oldValue

    print("\n" + playerName + " moved from " + str(oldValue) + " to " + str(currentValue))
    if currentValue in snakes:
        finalValue = snakes.get(currentValue)
        got_snakeBite(currentValue, finalValue, playerName)

    elif currentValue in ladders:
        finalValue = ladders.get(currentValue)
        got_ladderJump(currentValue, finalValue, playerName)

    else:
        finalValue = currentValue

    return finalValue


def checkWin(playerName, position):
    time.sleep(WAIT)
    if MAX_VAL == position:
        print("\n\n\nCongratulation!\n\n" + " The game won by " + playerName)
        print("\nThank you for participating in the game.\n\n")
        again=input("\nPlay again? (y/n) ")

        if again == 'n':
           sys.exit(1)

#gamestart
def startgame():
    while True:
        try:
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                 time.sleep(WAIT)
                 playerName = nickname
                 time.sleep(WAIT)
                 currentPosition = 0
                 round = 0
                 while True:
                      welcome_msg()
                      time.sleep(WAIT)
                      print("Now is round:")
                      print(round)
                      print("\nYour current position :")

                      print(currentPosition)
                      input_1 = input("\n" + playerName + ": " + random.choice(playerTurn) + " Press enter to roll dice: ")
                      print("\nDice is rolling...")
                      diceValue = get_diceValue()
                      time.sleep(WAIT)
                      print(playerName + " is moving....")
                      currentPosition = snakeLadder(playerName, currentPosition, diceValue)
                      time.sleep(3)
                      round=round+1


                      checkWin(playerName, currentPosition)

                      _ = system('clear')

        except socket.error as e:
           print (str(e))
           sys.exit()


startgame()
