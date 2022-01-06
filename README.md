# SNS_21-22_SN18051000
* This is a repository for the final assignment of ELEC0088, created by student 18051000. <br>
* The program is able to build a machine learning model to perform time-series predictions. <br>
* The dataset being used is the Sunspots dataset which contains the numbers of sunspots in 235 years (1749 to 1983). <br>
* The whole program is written in Python. <br>

## Main tasks that are achieved:
#### 1. MLP model for future predictions: <br>
A Multi-Layer Perceptron model is built to predict the number of sunspots in any month in the future (`mlpPredictor.py`).<br>
#### 2. Chatbot processing of sentences from the user: <br>
A chatbot is able to receive a sentence from the user (`tcpClient.py`). The server (`tcpServer.py`) checks if the input is in the correct form, reads the date in the sentence and builds an MLP model to predict the number of sunspots in the input month.<br>

## Organisation of files and their roles:

#### 1. `README.md`: <br>
Introduction to this repository with instructions on how to run the program.<br>
#### 2. `Sunspots.csv`: <br>
This CSV file contains the dataset of the number of sunspots from 1749 to 1983.<br>
#### 3. `mlpPredictor.py`: <br>
This python file implements the MLP model in a class to return prediction results and plot graphs for the predictions. The performance of the MLP model can be evaluated using the main function in this file.<br>
#### 4. `tcpServer.py`: <br>
This python file builds a server to connect with one client at a time. The connection from a client will be processed in a separate thread.<br>
#### 5. `tcpClient.py`: <br>
This python file builds a client to connect with the server. It asks for a sentence from the user to get the date for a prediction. After the prediction is done, the client will receive the result from the server and display it on the user's terminal.<br>

## The necessary Python packages/modules are: <br>
`numpy 1.20.3`, `pandas 1.3.4`, `matplotlib 3.5.0`, `tensorflow 2.7.0` <br>
When downloading these packages/modules, other essential packages/modules will be downloaded automatically as dependencies.

## To run the code, please follow the steps below: <br>
1. Download the whole repository (either by doing `git clone` or downloading zip). <br>
2. Run the main function of the file `tcpServer.py` to start the server.
3. Run the main function of the file `tcpClient.py` to connect with the server and start the chatbot. Make sure the client has the same port as the server's port.
4. On the client's terminal, the chatbot will ask for a sentence ending with the form YYYY-MM.
5. On the client's terminal, input a sentence ending with the date you want to predict. Wait until the chatbot gives you the predicted number of sunspots in that month.
6. The program will automatically show you a plot of predictions. If you want to evaluate the accuracy and performance of the model, please run the main function of `mlpPredictor.py` after setting the sizes of the training set and test set.
