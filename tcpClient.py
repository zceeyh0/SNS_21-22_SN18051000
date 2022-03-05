# Student Number: 18051000
# This file builds a client for the chatbot to interact with the user.
# In the main function, the chatbot will ask for a sentence ending with the
# form YYYY-MM. The client sends the sentence to the server, receives and
# prints out a result predicted by the MLP predictor in the server.


import socket


def main():
    host = '127.0.0.1'  # local host
    port = 100
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # connect to server on local computer
    sock.connect((host, port))
    # message of chosen date
    print('Hello, I\'m the Oracle. I can predict the number of '
          'sunspots on the sun in any month in the future.')
    message = input('Please input any sentence ending with the form '
                    'YYYY-MM\nFor example: Please tell me how many '
                    'sunspots will be on the sun in 2025-06\n')
    while True:
        # message sent to server
        sock.send(message.encode('ascii'))
        print('Predicting... (It takes longer for the first time)')
        # message received from server
        data = sock.recv(1024)
        # print the received message
        # here it would be a reverse of sent message
        print('Received from the server:\n', str(data.decode('ascii')))
        # ask the client whether he wants to continue
        ans = input('\nDo you wish to predict again?(y/n) :')
        if ans == 'y':
            message = input('Please input another month (YYYY-MM):\n')
            continue
        else:
            print('Thanks for using me. Bye!')
            break
    # close the connection
    sock.close()


if __name__ == '__main__':
    main()

