import mlpPredictor
# import socket programming library
import socket
# import thread module
from _thread import *
import threading
import pandas as pd


print_lock = threading.Lock()

# read the training dataset
df = pd.read_csv('D:\Study\MLNotebook\AMLS_21-22_SN18051000\Sunspots.csv')
# convert string (each month) into datetime (first day of each month)
df['Month'] = pd.to_datetime(df['Month'], infer_datetime_format=True)
# 200 samples in each training group
mlp = mlpPredictor.MLP(df, 200)
sunspots = df['Sunspots'].to_list()
X_train, Y_train = mlp.create_training_set(sunspots)


# calculate the difference of months between two dates
def diff_month(date1, date2):
    return (date1.year - date2.year) * 12 + (date1.month - date2.month)


# thread function for a connected client
def threaded(conn):
    while True:
        # data received from the client
        data = conn.recv(1024).decode()
        if not data:
            print('Client disconnected')
            # lock released on exit
            print_lock.release()
            break

        date_str = data[-7:]  # read the input month
        # Check if the input string is in the correct form and
        # can be converted to int.
        try:
            year_int = int(date_str[0:4])
            month_int = int(date_str[5:])
        except ValueError:
            msg = 'The input date is not in the correct form!'
            conn.send(msg.encode('ascii'))
            continue
        # check for the corner cases of the input date
        if year_int < 1678:
            msg = 'The input year ' + str(year_int) + ' is too early!'
            conn.send(msg.encode('ascii'))
            continue
        elif year_int > 2262:
            msg = 'The input year ' + str(year_int) + ' is too late!'
            conn.send(msg.encode('ascii'))
            continue
        if month_int < 1 or month_int > 12:
            msg = 'The input month is incorrect! Should be 1-12.'
            conn.send(msg.encode('ascii'))
            continue
        # convert the input string into datetime variable
        # infer_datetime_format is set as True to speed up the conversion
        date = pd.to_datetime(date_str, infer_datetime_format=True)

        if mlp.predictions:  # if there are previous predictions
            # Calculate the number of months between the input month
            # and the last month in the prediction history.
            diff = diff_month(date, mlp.future_months[-1])
            if diff > 0:  # if the input month is in the future
                # predict number of sunspots in the input month in the future
                ans = mlp.mlp_predict(X_train, Y_train, diff)
                mlp.plot_predictions()
                msg = 'The predicted number of sunspots in ' + date_str + \
                      ' is: ' + str(ans)
                conn.send(msg.encode('ascii'))
                continue
            else:
                diff = diff_month(date, mlp.future_months[0])
                if diff >= 0:  # if the input month has its prediction record
                    msg = 'The prediction has been recorded, ' \
                          'the number of sunspots in ' + \
                          date_str + ': ' + str(mlp.predictions[diff])
                    conn.send(msg.encode('ascii'))
                    continue
        else:  # if no prediction has been made
            # Calculate the number of months between the input month
            # and the last month in the training dataset.
            diff = diff_month(date, mlp.df['Month'].to_list()[-1])
            if diff > 0:  # if the input month is in the future
                # predict number of sunspots in the input month in the future
                ans = mlp.mlp_predict(X_train, Y_train, diff)
                mlp.plot_predictions()
                msg = 'The predicted number of sunspots in ' + date_str + \
                      ' is: ' + str(ans)
                conn.send(msg.encode('ascii'))
                continue
        # if no message was sent, the input month is not in the future
        diff = diff_month(date, mlp.df['Month'].to_list()[0])
        if diff >= 0:  # if the input month is in the training dataset
            msg = 'The date is not in the future, but I can ' \
                  'show you the recorded number of sunspots in ' + \
                  date_str + ': ' + str(mlp.df['Sunspots'].to_list()[diff])
        else:  # if the input month is even earlier
            msg = 'The date is not in the future, please try again.'
        conn.send(msg.encode('ascii'))
    # connection closed
    conn.close()


def server_main():
    host = ''
    port = 100
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((host, port))
    print("Socket binded to port", port)
    # put the socket into listening mode
    # 5 means the maximum number of unaccepted connections being allowed
    sock.listen(5)
    print("Socket is listening")
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        conn, addr = sock.accept()
        # if the connected client is already closed, break the loop
        if getattr(conn, '_closed'):
            break
        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])
        # Start a new thread and return its identifier
        start_new_thread(threaded, (conn,))
    sock.close()


if __name__ == '__main__':
    server_main()
