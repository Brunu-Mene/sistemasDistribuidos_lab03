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
    while True:
        solution = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        hash = hashlib.sha1(solution.encode('utf-8')).digest()

        binary_hash = bin(int.from_bytes(hash, byteorder='big'))[2:]

        if binary_hash[1:challenger+1] == '0' * challenger:
            return solution
