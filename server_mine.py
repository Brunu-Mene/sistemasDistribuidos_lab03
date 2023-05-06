from concurrent import futures
import random
import mine_grpc_pb2_grpc
import mine_grpc_pb2
import hashlib
import grpc
import threading
import aux



class MineServer(mine_grpc_pb2_grpc.apiServicer):
    def __init__(self):
        self.transactions = {}
        self.transactions[0] = {'challenge': random.randint(1, 6), 'solution': None, 'winner': -1}

    def _validTrId(self,id):
        if(id <= max(self.transactions.keys())):
            return True
        return False
    def _getLocalStatus(self, id):
        if(self._validTrId(id)):
            if(self.transactions[id]['solution'] != None):
                return 0
            return 1
        return -1

    def getTransactionId(self, request, context):
        return mine_grpc_pb2.intResult(result=(max(self.transactions.keys())))
    
    def getChallenge(self, request, context):
        transactionId = request.transactionId
        if(self._validTrId(transactionId)):
            return mine_grpc_pb2.intResult(result=(self.transactions[transactionId]['challenge']))
        return mine_grpc_pb2.intResult(result=(-1))
    
    def getTransactionStatus(self, request, context):
        transactionId = request.transactionId
        if(self._validTrId(transactionId)):
            if(self.transactions[transactionId]['solution'] != None):
                return mine_grpc_pb2.intResult(result=(0))
            return mine_grpc_pb2.intResult(result=(1))
        return mine_grpc_pb2.intResult(result=(-1))
    
    def submitChallenge(self, request, context):
        transactionId = request.transactionId
        if self._getLocalStatus(transactionId) == 0:
            return mine_grpc_pb2.intResult(result=(2))
        if self._getLocalStatus(transactionId) == -1:
            return mine_grpc_pb2.intResult(result=(-1))
        
        hash = hashlib.sha1(request.solution.encode('utf-8')).digest()
        binary_hash = bin(int.from_bytes(hash, byteorder='big'))[2:]

        if binary_hash[1:self.transactions[transactionId]['challenge']+1] == '0' * self.transactions[transactionId]['challenge']:
            self.transactions[transactionId]['winner'] = request.clientId
            self.transactions[transactionId]['solution'] = request.solution

            self.transactions[transactionId+1] = {'challenge': random.randint(1, 6), 'solution': None, 'winner': -1} # criando novo desafio
            return mine_grpc_pb2.intResult(result=(1))
        else:
            return mine_grpc_pb2.intResult(result=(0))
    
    def getWinner(self, request, context):
        transactionId = request.transactionId
        if self._validTrId(transactionId):
            if self.transactions[transactionId]['winner'] == -1:
                return mine_grpc_pb2.intResult(result=(0))
            return mine_grpc_pb2.intResult(result=(self.transactions[transactionId]['winner']))
        
        return mine_grpc_pb2.intResult(result=(-1))
    
    def getSolution(self, request, context):
        transactionId = request.transactionId

        if self._validTrId(transactionId):
            return mine_grpc_pb2.structResult(status=(self._getLocalStatus(transactionId)), solution=(str(self.transactions[transactionId]['solution'])), challenge=(self.transactions[transactionId]['challenge']))
        
        return mine_grpc_pb2.structResult(status=(-1), solution=("-1"), challenge=(-1)) 
    
    def _printTransactions(self):
        print("-------------------------------- Transactions Table --------------------------------")
        for i in self.transactions:
            print(f"Challenge: {self.transactions[i]['challenge']} | Solution: {self.transactions[i]['solution']} | Winner: {self.transactions[i]['winner']}")
        print()


if __name__ == '__main__':
    server = MineServer()
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mine_grpc_pb2_grpc.add_apiServicer_to_server(server, grpc_server)

    grpc_server.add_insecure_port('[::]:8080')
    grpc_server.start()

    thread_print = threading.Thread(target=aux.sleepFive, args=(server, ))
    thread_print.start()

    grpc_server.wait_for_termination()
