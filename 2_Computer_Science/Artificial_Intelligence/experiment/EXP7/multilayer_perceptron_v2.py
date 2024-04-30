import numpy as np
import matplotlib.pyplot as plt

class Multilayer_Perceptron:

    def __init__(self, input_size, hidden_size, output_size):
        self.weights1 = np.random.randn(input_size, hidden_size)
        self.weights2 = np.random.randn(hidden_size, output_size)
        self.bias1 = np.random.randn(1, hidden_size)
        self.bias2 = np.random.randn(1, output_size)
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def loss(self, y_true, y_pred):
        return 0.5 * np.power(y_pred - y_true, 2)

    def loss_derivative(self, y_true, y_pred):
        return y_pred - y_true

    def fit(self, X, y, learning_rate=0.01, epochs=10000):
        w1 = np.vstack((self.weights1, self.bias1))
        w2 = np.vstack((self.weights2, self.bias2))
        bias = np.ones((X.shape[0], 1))

        for _ in range(epochs):
            # forward pass
            hidden_layer_input = np.dot(np.column_stack((X, bias)), w1)
            hidden_layer_output = self.sigmoid(hidden_layer_input)

            output_layer_input = np.dot(np.column_stack((hidden_layer_output, bias)), w2)
            output_layer_output = self.sigmoid(output_layer_input)

            # backward pass (output layer)
            # delta(E_total) /  delta(output_o)
            gradient_cal1 = self.loss_derivative(y, output_layer_output) # data_size x output_layer_size
            # delta(output_o) / delta(net_o)
            gradient_cal2 = self.sigmoid_derivative(output_layer_output) # data_size x output_layer_size
            # delta(net_o) / delta(w2)
            gradient_cal3 = np.column_stack((hidden_layer_output, bias)) # data_size x (hidden_layer_size + 1)
            # delta(E_total) / delta(w2)
            gradient_cal4 = np.dot(gradient_cal3.T, gradient_cal1 * gradient_cal2) # (hidden_layer_size + 1) x output_layer_size
            # update w2
            weights2_update = gradient_cal4 * learning_rate 
            w2 -= weights2_update

            # backward pass (hidden layer)
            # delta(E_total) / delta(output_h)
            gradient_cal5 = np.dot(gradient_cal1 * gradient_cal2, w2[:-1].T) # data_size x hidden_layer_size
            # delta(output_h) / delta(net_h)
            gradient_cal6 = self.sigmoid_derivative(hidden_layer_output) # data_size x hidden_layer_size
            # delta(net_h) / delta(w1)
            gradient_cal7 = np.column_stack((X, bias)) # data_size x (input_size + 1)
            # delta(E_total) / delta(w1)
            gradient_cal8 = np.dot(gradient_cal7.T, gradient_cal5 * gradient_cal6) # (input_size + 1) x hidden_layer_size
            # update w1
            weights1_update = gradient_cal8 * learning_rate
            w1 -= weights1_update

        self.weights1 = w1[:-1]
        self.weights2 = w2[:-1]
        self.bias1 = w1[-1]
        self.bias2 = w2[-1]

    def predict(self, X):
        hidden_layer_input = np.dot(X, self.weights1) + self.bias1
        hidden_layer_output = self.sigmoid(hidden_layer_input)
        output_layer_input = np.dot(hidden_layer_output, self.weights2) + self.bias2
        output_layer_output = self.sigmoid(output_layer_input)
        return output_layer_output

if __name__ == '__main__':
    # read data from data/data.csv
    data = np.genfromtxt('data/data.csv', delimiter=',', skip_header=1)
    # z-score normalization
    data[:, 0] = (data[:, 0] - data[:, 0].mean()) / data[:, 0].std()
    data[:, 1] = (data[:, 1] - data[:, 1].mean()) / data[:, 1].std()
    # shuffle data
    np.random.shuffle(data)
    # split data into training and testing sets
    data_train, data_test = data[:int(0.8 * len(data))], data[:]
    age, estimated_salary, purchased = data_train[:, 0], data_train[:, 1], data_train[:, 2]
    age_test, estimated_salary_test, purchased_test = data_test[:, 0], data_test[:, 1], data_test[:, 2]

    mlp = Multilayer_Perceptron(2, 4, 1)

    X_train = np.column_stack((age, estimated_salary))
    y_train = np.expand_dims(purchased, axis=1) 
    mlp.fit(X_train, y_train)

    X_test = np.column_stack((age_test, estimated_salary_test))
    y_test = np.expand_dims(purchased_test, axis=1) 
    y_pred = mlp.predict(X_test)

    for i in range(len(y_pred)):
        if y_pred[i] > 0 and y_test[i] == 1 or y_pred[i] <= 0 and y_test[i] == 0:
            print(f'\033[92mPredicted: {y_pred[i][0]:.2f}, Actual: {y_test[i]}\033[0m')
        else :
            print(f'\033[91mPredicted: {y_pred[i][0]:.2f}, Actual: {y_test[i]}\033[0m')

    for i in range(len(y_test)):
        if y_test[i] == 1:
            plt.scatter(age_test[i], estimated_salary_test[i], color='red')
        else:
            plt.scatter(age_test[i], estimated_salary_test[i], color='blue')
    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')
    
    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = mlp.predict(np.column_stack((X.ravel(), Y.ravel()))).reshape(X.shape)
    plt.contourf(X, Y, Z, levels=1, alpha=0.5)
    plt.show()