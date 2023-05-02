from concurrent import futures
import random
import mine_grpc_pb2_grpc
import hashlib


class MineServer(mine_grpc_pb2_grpc.apiServicer):
    def __init__(self):
        self.transactions = {}
        self.transactions[0] = {'challenge': random.randint(1, 6), 'solution': None, 'winner': -1}

    def validTrId(self,id):
        if(id <= max(self.transactions.keys())):
            return True
        return False

    def getTransactionId(self):
        return max(self.transactions.keys())
    
    def getChallenge(self, transactionId):
        if(self.validTrId(transactionId)):
            return self.transactions[transactionId]['challenge']
        return -1
    
    def getTransactionStatus(self, transactionId):
        if(self.validTrId(transactionId)):
            if(self.transactions[transactionId]['solution'] != None):
                return 0
            return 1
        return -1
    
    def submitChallenge(self, challengeArgs):
        hash_object = hashlib.sha1(challenge.encode())
        computed_solution = hash_object.hexdigest()

        
        return (intResult)
    
    def getWinner(transactionId):
        return (intResult)
    
    # def getSolution(transactionId):
    #     return (structResult)

class challengeArgs:
    def __init__(transactionId, clientId, solution, self):
        self.transactionId = transactionId
        self.clientId = clientId
        self. solution = solution


if __name__ == '__main__':
    server = MineServer()
    print(server.getChallenge(0))

    # while(1):
