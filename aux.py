import time
import random
import string

class challengeArgs:
    def __init__(self, transactionId, clientId, solution):
        self.transactionId = transactionId
        self.clientId = clientId
        self.solution = solution

def sleepFive(server):
    while True:
        server._printTransactions()
        time.sleep(5)

def lookForAnswer(server):
    id = 0

    while True:
        time.sleep(0.9)
        solution = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

        chall = challengeArgs(transactionId = id, clientId = 0, solution=solution)
        if server.submitChallenge(chall) == 1:
            id += 1
        elif server.submitChallenge(chall) == -1:
            break