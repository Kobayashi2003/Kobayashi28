import numpy as np
import matplotlib.pyplot as plt

class Perceptron:

    def __init__(self, input_size, output_size):
        self.weights = np.random.randn(input_size, output_size)
        self.bias = np.random.randn(1, output_size)
        self.losses = []

    def fit(self, X, y, learning_rate=0.01, epochs=1000):
        for _ in range(epochs):
            y_pred = self.predict(X)
            self.losses.append(np.sum(0.5 * np.power(y_pred - y, 2)))
            gradient = np.dot(X.T, y_pred - y) / len(y)
            self.weights -= learning_rate * gradient
            self.bias -= learning_rate * np.sum(y_pred - y) / len(y)

    def predict(self, X):
        return np.where(np.dot(X, self.weights) + self.bias > 0, 1, 0)


if __name__ == '__main__':
    data = np.genfromtxt('../data/data.csv', delimiter=',', skip_header=1)

    # z-score 
    data[:, 0] = (data[:, 0] - data[:, 0].mean()) / data[:, 0].std()
    data[:, 1] = (data[:, 1] - data[:, 1].mean()) / data[:, 1].std()

    # # normalize (not necessary)
    # data[:, 0] = (data[:, 0] - data[:, 0].min()) / (data[:, 0].max() - data[:, 0].min())
    # data[:, 1] = (data[:, 1] - data[:, 1].min()) / (data[:, 1].max() - data[:, 1].min())

    # shuffle data
    np.random.shuffle(data)

    # split data into training and testing sets
    data_train, data_test = data[:int(0.8 * len(data))], data[:]
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
        if y_pred[i] == y_test[i]:
            print(f'\033[92mPrediction: {y_pred[i][0]:.2f}, Actual: {y_test[i][0]}\033[0m')
            count_correct += 1
        else:
            print(f'\033[91mPrediction: {y_pred[i][0]:.2f}, Actual: {y_test[i][0]}\033[0m')
    print(f'Accuracy: {count_correct / len(y_pred):.2%}')

    plt.xlabel('Age')
    plt.ylabel('Estimated Salary')

    for i, (age, estimated_salary, purchased) in enumerate(data_test):
        if y_test[i] == 1:
            plt.scatter(age, estimated_salary, color='red')
        else:
            plt.scatter(age, estimated_salary, color='blue')
    plt.savefig('../data/img/perceptron_data.png')

    x = np.linspace(-3, 3, 100)
    y = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x, y)
    Z = perceptron.predict(np.column_stack((X.ravel(), Y.ravel()))).reshape(X.shape)
    plt.contourf(X, Y, Z, levels=1, alpha=0.5)
    plt.savefig('../data/img/perceptron_prediction.png')
    
    plt.clf()

    plt.plot(perceptron.losses)
    plt.xlabel('Epochs')
    plt.ylabel('Loss')
    plt.savefig('../data/img/perceptron_loss.png')