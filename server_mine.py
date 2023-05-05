from concurrent import futures
import random
import mine_grpc_pb2_grpc
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
        # print(binary_hash[1:6])

        #fugindo do primerio bit sempre == 1
        if binary_hash[1:self.getChallenge(challengeArgs.transactionId)+1] == '0' * self.getChallenge(challengeArgs.transactionId):
            self.transactions[challengeArgs.transactionId]['winner'] = challengeArgs.clientId
            self.transactions[challengeArgs.transactionId]['solution'] = challengeArgs.solution

            #com duvida se esta criando da maneira correta
            self.transactions[challengeArgs.transactionId+1] = {'challenge': random.randint(1, 6), 'solution': None, 'winner': -1} # criando novo desafio
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
    
    def _printTransactions(self):
        print("-------------------------------- Transactions Table --------------------------------")
        for i in self.transactions:
            print(self.getSolution(i))
        print()

    #test
    def _insertCh(self, tam):
        self.transactions[tam+1] = {'challenge': random.randint(1, 6), 'solution': None, 'winner': -1} # criando novo desafio


if __name__ == '__main__':
    server = MineServer()
    grpc_server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    mine_grpc_pb2_grpc.add_apiServicer_to_server(server, grpc_server)

    grpc_server.add_insecure_port('[::]:8080')
    grpc_server.start()

    ## test
    thread_print = threading.Thread(target=aux.sleepFive, args=(server, ))
    thread_answer = threading.Thread(target=aux.lookForAnswer, args=(server, ))
    thread_answer.start()
    thread_print.start()
    ##

    grpc_server.wait_for_termination()
