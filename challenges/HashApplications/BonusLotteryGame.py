# Libraries
from pwn import *
from parse import parse
import hashlib

# Connect to remote
rem = remote("35.195.130.106", 17008)

# Values
def receiveLine():
    line = rem.readline().strip().decode()
    print(f"REC {line}")
    return line


def runLottery():
    max = 100000 - 1
    goal = -1

    # Hash of the goal
    (hashGoal,) = parse(
        "Its hash is {}, let's run the players, the closest wins", receiveLine()
    )
    if not hashGoal:
        raise Exception("Problem with parsing the goal hash")

    # 10 players
    hashDict = {}
    for i in range(10):
        (
            _,
            hash,
        ) = parse("Player {} has committed to {}", receiveLine())
        hashDict[hash] = [i]

    # Question
    receiveLine()

    for i in range(max + 1):
        # compute le hash pour i
        hash = hashlib.sha256(str(i).encode()).hexdigest()
        if hash in hashDict:
            hashDict[hash].append(i)
        if hash == hashGoal:
            goal = i

    if goal < 0:
        raise Exception("Pas trouvé le goal")

    # Trouver le plus proche
    distance = max
    bestPlayer = "-1"
    for player in hashDict.values():
        if abs(player[1] - goal) < distance:
            bestPlayer = player[0]
            distance = abs(player[1] - goal)

    if bestPlayer == "-1":
        raise Exception("Not found the best player")

    print(bestPlayer)
    rem.send(f"{bestPlayer}\r\n")

    # Check the results
    for i in range(12):
        receiveLine()


def main():
    # Receive welcome
    receiveLine()

    stop = False

    while not stop:

        line = receiveLine()

        if "random number" in line:
            # Random number is being drawn
            runLottery()
        else:
            stop = True
            print(rem.recvall().strip().decode())


main()
