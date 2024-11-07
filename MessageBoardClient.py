#Ryan Dyson Darmawan - 57883349

from socket import *
import sys
import signal

clientSocket = None #initialize clientSocket to None

def signal_handler(sig, frame):  #handles when client force quites via terminal (CTRL + C)
    clientSocket.send("QUIT".encode())
    isOk = clientSocket.recv(1024).decode()
    if clientSocket and isOk == "OK":
        clientSocket.close()
        print("\nClient: Socket forcefully closed. Exiting program.")
        sys.exit(0)


def main(ipAddress, serverPortNum):
    global clientSocket #access nonlocal variable

    def handleCommand(Command): #helper function to handle commands
        clientSocket.send(Command.encode()) #send command to server

        if (Command == "POST"):
            isDone = False
            while not isDone: #loops while user still want to post
                newMsg = input("Client, enter a message: ").strip() #get user input
                clientSocket.send(newMsg.encode()) #set user input that is encoded
                if (newMsg == "#"): #if input == #, break the loop
                    isDone = True
                    break
            isOk = clientSocket.recv(1024).decode() #check response from server
            if (isOk == "OK"):
                print("Server: OK, Message added successfully")
            else: 
                print("Server: ERROR - Message was not received")

        elif (Command == "GET"):
            happySocket = clientSocket.recv(1024).decode() #get the "happy socket programming" response from server
            print("Server: ", happySocket)
            isDone = False
            while not isDone: #while there is still messages to get
                currMessage = clientSocket.recv(1024).decode() #first response is the ID and date
                if (currMessage == "#"): #break if response is #
                    isDone = True
                    break

                print("server: ", currMessage)

        elif (Command == "DELETE"):
            isDone = False
            while not isDone:
                messageID = input("Client, enter a message ID: ").strip() #get the IDs to delete
                clientSocket.send(messageID.encode()) #send the ID to server
                if (messageID == "#"): #break if user is done
                    isDone = True
                    break

            isOk = clientSocket.recv(1024).decode() #get response from server
            if (isOk != "OK"): #check the response
                print("Server: ERROR - Wrong ID")
            else:
                print("Server: Message(s) deleted successfully")

        elif (Command == "QUIT"):
            isOk = clientSocket.recv(1024).decode() #get response from server
            if (isOk == "OK"):
                clientSocket.close()
                sys.exit(0)

        else: #if command is not reconized
            serverRes = clientSocket.recv(1024).decode() #server will send our error message
            print("Server: ", serverRes)

    serverName = ipAddress
    serverPort = serverPortNum

    clientSocket = socket(AF_INET, SOCK_STREAM) #initialize TCP socket
    try:
        clientSocket.connect((serverName, serverPort)) #try to connect to server of specified IP and Port num
    except ConnectionRefusedError:
        print("Client: Failed connecting to server. Exiting program.") #if cannot find server, close the program
        if (clientSocket):
            clientSocket.close()
        sys.exit(1)

    while True: 
        command = input("Client, enter a command: ").strip().upper() #get command from user
        handleCommand(command)
        

if __name__ == "__main__": #dunder method to execute main func
    if (len(sys.argv) < 2): #if .py is executed with less than 2 arguments, exits
        print("Arguments required: Server IP Address, Server Port Number")
        sys.exit(1)
    
    serverIp = sys.argv[1]
    serverPort = int(sys.argv[2])

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    main(serverIp, serverPort) #calls main func to handle ther client