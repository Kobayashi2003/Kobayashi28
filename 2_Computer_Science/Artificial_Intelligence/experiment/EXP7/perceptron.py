import numpy as np
import matplotlib.pyplot as plt

class Perceptron:

    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(input_size, output_size)
        self.bias = np.random.randn(1, output_size)
        self.losses = []

    def fit(self, X, y, learning_rate=0.01, epochs=100):
        w = np.vstack((self.weights, self.bias))
        bias = np.ones((X.shape[0], 1))
        for _ in range(epochs):
            y_pred = self.predict(X)
            self.losses.append(0.5 * np.power(y_pred - y, 2))
            w -= learning_rate * np.dot(np.column_stack((X, bias)).T, y_pred - y)
        self.weights = w[:-1]
        self.bias = w[-1]

    def predict(self, X):
        bias = np.ones((X.shape[0], 1))
        return np.dot(np.column_stack((X, bias)), np.vstack((self.weights, self.bias)))

if __name__ == '__main__':
    data = np.genfromtxt('data/data.csv', delimiter=',', skip_header=1)
    # z-score normalization
    data[:, 0] = (data[:, 0] - data[:, 0].mean()) / data[:, 0].std()
    data[:, 1] = (data[:, 1] - data[:, 1].mean()) / data[:, 1].std()
    # shuffle data
    np.random.shuffle(data)
    # split data into training and testing sets
    data_train, data_test = data[:int(0.2 * len(data))], data[:]
    age, estimated_salary, purchased = data_train[:, 0], data_train[:, 1], data_train[:, 2]
    age_test, estimated_salary_test, purchased_test = data_test[:, 0], data_test[:, 1], data_test[:, 2]

    perceptron = Perceptron(2, 1)

    X_train = np.column_stack((age, estimated_salary))
    y_train = np.expand_dims(purchased, axis=1)
    perceptron.fit(X_train, y_train)

    X_test = np.column_stack((age_test, estimated_salary_test))
    y_test = np.expand_dims(purchased_test, axis=1)
    y_pred = perceptron.predict(X_test)

    count_correct = 0
    for i in range(len(y_pred)):
        if y_pred[i] >= 0.5 and y_test[i] == 1 or y_pred[i] < 0.5 and y_test[i] == 0:
            print(f'\033[92mPrediction: {y_pred[i][0]:.2f}, Actual: {y_test[i][0]}\033[0m')
            count_correct += 1
        else:
            print(f'\033[91mPrediction: {y_pred[i][0]:.2f}, Actual: {y_test[i][0]}\033[0m')

    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')

    for i, (age, estimated_salary, purchased) in enumerate(data_test):
        if y_test[i] == 1:
            plt.scatter(age, estimated_salary, color='red')
        else:
            plt.scatter(age, estimated_salary, color='blue')
    plt.savefig('perceptron_data.png')

    weights = perceptron.weights
    bias = perceptron.bias
    x = np.linspace(-2, 2, 100)
    y = (-weights[0] * x - bias) / weights[1]
    plt.plot(x, y, color='black')
    plt.savefig('perceptron_prediction.png')
    plt.close()

    plt.plot(perceptron.losses)
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.savefig('perceptron_loss.png')