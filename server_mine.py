from concurrent import futures
import random
import mine_grpc_pb2_grpc
import hashlib

class challengeArgs:
    def __init__(self, transactionId, clientId, solution):
        self.transactionId = transactionId
        self.clientId = clientId
        self.solution = solution

class MineServer(mine_grpc_pb2_grpc.apiServicer):
    def __init__(self):
        self.transactions = {}
        self.transactions[0] = {'challenge': random.randint(1, 6), 'solution': None, 'winner': -1}

    def _validTrId(self,id):
        if(id <= max(self.transactions.keys())):
            return True
        return False

    def getTransactionId(self):
        return max(self.transactions.keys())
    
    def getChallenge(self, transactionId):
        if(self._validTrId(transactionId)):
            return self.transactions[transactionId]['challenge']
        return -1
    
    def getTransactionStatus(self, transactionId):
        if(self._validTrId(transactionId)):
            if(self.transactions[transactionId]['solution'] != None):
                return 0
            return 1
        return -1
    
    def submitChallenge(self, challengeArgs):
        if self.getTransactionStatus(challengeArgs.transactionId) == 0:
            return 2
        if self.getTransactionStatus(challengeArgs.transactionId) == -1:
            return -1
        
        sha1 = hashlib.sha1()
        sha1.update(challengeArgs.solution.encode('utf-8'))

        hash_digest = sha1.hexdigest()
        binary_hash = bin(int(hash_digest, 16))[2:]
        print(binary_hash[:10])

        if binary_hash[:self.getChallenge(challengeArgs.transactionId)['challenge']] == '0' * self.getChallenge(challengeArgs.transactionId):
            self.transactions[challengeArgs.transactionId]['winner'] = challengeArgs.clientId
            self.transactions[challengeArgs.transactionId]['solution'] = challengeArgs.solution
            return 1
        else:
            return 0
    
    def getWinner(self,transactionId):
        if self._validTrId(transactionId):
            if self.transactions[transactionId]['solution'] == None:
                return 0
            return 1
        
        return -1
    
    def getSolution(self, transactionId):
        if self._validTrId(transactionId):
            return {'status': self.getTransactionStatus(transactionId), 'solution': self.transactions[transactionId]['solution'], 'challenge': self.getChallenge(transactionId)}
        return 'Invalid transactionId!'


if __name__ == '__main__':
    server = MineServer()
    ch = challengeArgs(solution = "test", clientId = 0, transactionId = 0)
    print(server.getSolution(0))

    # while(1):
