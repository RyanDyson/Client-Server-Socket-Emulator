from socket import *
import sys

def main(ipAddress, serverPortNum):
    def handleCommand(Command):
        clientSocket.send(Command.encode())

        if (Command[0] == "POST"):
            exited = False
            while not exited:
                newMsg = input("Client, enter a message: ").strip()
                if (input == "#\n"):
                    exited = True
                    break
                clientSocket.send(newMsg.encode())

        elif (Command[0] == "GET"):
            happySocket = clientSocket.recv(1024).decode()
            print("Server: ", happySocket)
            isDone = False
            while not isDone:
                currMessage = clientSocket.recv(1024).decode()
                if (currMessage == "#\n"):
                    isDone = True
                    break

                print("server: ", currMessage)

        elif (Command[0] == "DELETE"):
            isDone = False
            while not isDone:
                messageID = input("Client, enter a message ID: ").strip()
                if (messageID == "#\n"):
                    isDone = True
                    break
                clientSocket.send(messageID.encode())

        elif (Command == "QUIT"):
            clientSocket.close()
            sys.exit(0)

        else:
            serverRes = clientSocket.recv(1024).decode()
            print("Server: ", serverRes)

    serverName = ipAddress
    serverPort = serverPortNum

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverName, serverPort))

    while True:
        command = input("Client, enter a command: ").strip().upper().split(" ")
        handleCommand(command)
        

if __name__ == "__main__": #dunder method to execute main func
    if (len(sys.argv) < 2): #if .py is executed with less than 2 arguments, exits
        print("Arguments required: Server IP Address, Server Port Number")
        sys.exit(1)
    
    serverIp = sys.argv[1]
    serverPort = int(sys.argv[2])
    main(serverIp, serverPort) #calls main func to handle ther client