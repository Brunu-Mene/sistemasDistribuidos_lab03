import time
import random
import string
import hashlib

class challengeArgs:
    def __init__(self, transactionId, clientId, solution):
        self.transactionId = transactionId
        self.clientId = clientId
        self.solution = solution

def sleepFive(server):
    while True:
        server._printTransactions()
        time.sleep(5)

def lookForAnswer(challenger):
    hash_object = hashlib.sha1()

    while True:
        solution = ''.join(random.choices(string.ascii_letters + string.digits, k=15))

        hash_object.update(solution.encode('utf-8'))
        hash_str = hash_object.hexdigest()
        hash_bin = bin(int(hash_str, 16))[2:]
        nBits = hash_bin[1:challenger+1]

        if nBits == '0'* challenger:
            print(nBits)
            return solution
