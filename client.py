import sys
import grpc
import mine_grpc_pb2
import mine_grpc_pb2_grpc
import pybreaker
import threading
import aux
import random

breaker = pybreaker.CircuitBreaker(fail_max=2, reset_timeout=2)
@breaker

def runOperation(client, operation, clientId):
    def validTransaction(transactionId):
        if transactionId == -1:
            print("Transaction Not Found!\n")
            return False
        return True
    


    if operation == 1:
        print(f"The current transaction is: {client.getTransactionId(mine_grpc_pb2.void()).result}\n")

    elif operation == 2:
        transactionId = input("Enter with one transactionId: ")
        ch = client.getChallenge(mine_grpc_pb2.transactionId(transactionId = int(transactionId))).result

        if validTransaction(ch):
            print(f"The challenge of that transaction is: {ch}\n")

    elif operation == 3:
        transactionId = input("Enter with one transactionId: ")
        status = client.getTransactionStatus(mine_grpc_pb2.transactionId(transactionId = int(transactionId))).result

        if validTransaction(status):
            if status == 1:
                print("No solution yet!\n")
            else:
                print("Transaction already settled!\n")

    elif operation == 4:
        transactionId = input("Enter with one transactionId: ")
        winnerId = client.getWinner(mine_grpc_pb2.transactionId(transactionId = int(transactionId))).result

        if validTransaction(winnerId):
            if winnerId == 0:
                print("No winner yet!")
            else:
                print(f"The winner is: {winnerId}")

    elif operation == 5:
        transactionId = input("Enter with one transactionId: ")
        solutions = client.getSolution(mine_grpc_pb2.transactionId(transactionId = int(transactionId)))

        if validTransaction(solutions.status):
            print(f"Status: {solutions.status} / Solution: {solutions.solution} / Challenge {solutions.challenge}\n")

    elif operation == 6:
        transactionId = client.getTransactionId(mine_grpc_pb2.void()).result
        ch = client.getChallenge(mine_grpc_pb2.transactionId(transactionId = int(transactionId))).result

        if validTransaction(ch):
            solution = aux.lookForAnswer(ch)

            result = client.submitChallenge(mine_grpc_pb2.challengeArgs(transactionId = int(transactionId), clientId=(clientId), solution=(solution))).result
            print(f"Local Solution: {solution}")
            if result == 1:
                print(f"Solution worked $$$")
            elif result == 0:
                print("Denied Solution by Server! :(")
            elif result == 2:
                print("This Challenge has been Solved!")
    
    else:
        print("Invalid Operation!")


@breaker
def connect():
    clientId = random.randint(1, (2**31)-1)

    try:
        serverAddress = sys.argv[1]
    except IOError:
        print("Missing argument! Server Address...")
        exit()

    channel = grpc.insecure_channel(serverAddress)
    client = mine_grpc_pb2_grpc.apiStub(channel)

    while True:
        print('Menu Options:')
        print('1 - getTransactionId')
        print('2 - getChallenge')
        print('3 - getTransactionStatus')
        print('4 - getWinner')
        print('5 - getSolution')
        print('6 - Mine')
        print('7 - Exit')

        try:
            operation = int(input('Enter your choice: '))
        except ValueError:
            print("Invalid Operation!\n")
            input("Press Enter to continue...")
            continue
    
        if operation == 7:
            exit()

        try:
            runOperation(client, operation, clientId)
            input("Press Enter to continue...")
            print()
        except pybreaker.CircuitBreakerError:
            print(pybreaker.CircuitBreakerError)


if __name__ == "__main__":
    connect()
