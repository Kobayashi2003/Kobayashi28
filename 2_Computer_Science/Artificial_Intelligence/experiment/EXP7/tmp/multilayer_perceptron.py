import numpy as np
import matplotlib.pyplot as plt

class Multilayer_Perceptron:

    def __init__(self, input_size, hidden_size, output_size):
        self.weights1 = np.random.randn(input_size + 1, hidden_size)
        self.weights2 = np.random.randn(hidden_size + 1, output_size)
        
    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))
    
    def sigmoid_derivative(self, x):
        return x * (1 - x)

    def loss(self, y_true, y_pred):
        return 0.5 * np.power(y_pred - y_true, 2)

    def loss_derivative(self, y_true, y_pred):
        return y_pred - y_true

    def fit(self, X, y, learning_rate=0.01, epochs=1000):
        X = np.column_stack((X, np.ones(X.shape[0])))
        for _ in range(epochs):
            # forward pass
            hidden_layer_input = np.dot(X, self.weights1)
            hidden_layer_output = self.sigmoid(hidden_layer_input)
            hidden_layer_output = np.column_stack((hidden_layer_output, np.ones(hidden_layer_output.shape[0])))
            output_layer_input = np.dot(hidden_layer_output, self.weights2)
            output_layer_output = self.sigmoid(output_layer_input)
            # backward pass (output layer)
            weights2_update = np.dot(hidden_layer_output.T, self.loss_derivative(y, output_layer_output) * self.sigmoid_derivative(output_layer_output))
            self.weights2 -= learning_rate * weights2_update
            # backward pass (hidden layer)
            weights1_update = np.dot(X.T, np.dot(self.loss_derivative(y, output_layer_output) * self.sigmoid_derivative(output_layer_output), self.weights2[:-1].T) * self.sigmoid_derivative(hidden_layer_output[:, :-1]))
            self.weights1 -= learning_rate * weights1_update

    def predict(self, X):
        X = np.column_stack((X, np.ones(X.shape[0])))
        hidden_layer_input = np.dot(X, self.weights1)
        hidden_layer_output = self.sigmoid(hidden_layer_input)
        hidden_layer_output = np.column_stack((hidden_layer_output, np.ones(hidden_layer_output.shape[0])))
        output_layer_input = np.dot(hidden_layer_output, self.weights2)
        output_layer_output = self.sigmoid(output_layer_input)
        return output_layer_output


if __name__ == '__main__':
    # read data from ../data/data.csv
    data = np.genfromtxt('../data/data.csv', delimiter=',', skip_header=1)
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
        if y_pred[i] > 0.5 and y_test[i] == 1 or y_pred[i] <= 0.5 and y_test[i] == 0:
            print(f'\033[92mPredicted: {y_pred[i][0]:.2f}, Actual: {y_test[i]}')
        else :
            print(f'\033[91mPredicted: {y_pred[i][0]:.2f}, Actual: {y_test[i]}')

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