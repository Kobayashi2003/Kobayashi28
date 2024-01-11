import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from single_linear_regression import LinearRegression

data = pd.read_csv('./data/world-happiness-report-2017.csv')
train_data = data.sample(frac=0.8)
test_data = data.drop(train_data.index)

input_param_name = 'Economy..GDP.per.Capita.'
output_param_name = 'Happiness.Score'

x_train = train_data[[input_param_name]].values
y_train = train_data[[output_param_name]].values

x_test = test_data[[input_param_name]].values
y_test = test_data[[output_param_name]].values

plt.scatter(x_train, y_train, color='red', label='Train data')
plt.scatter(x_test, y_test, color='blue', label='Test data')
plt.xlabel(input_param_name)
plt.ylabel(output_param_name)

plt.title('World happiness report 2017')
# plt.legend()
# plt.show()

num_iterations = 500
learning_rate = 0.01

model = LinearRegression(x_train, y_train)
(theta, cost_history) = model.train(learning_rate, num_iterations)


# print('begin cost', cost_history[0])
# print('last cost', cost_history[-1])

predictions_num = 100
x_predictions = np.linspace(x_train.min(), x_train.max(), predictions_num).reshape(predictions_num, 1)
y_predictions = model.predict(x_predictions)

plt.plot(x_predictions, y_predictions, color='green', label='Linear regression')
plt.legend()
plt.show()

plt.plot(cost_history, color='blue', label='Cost function')
plt.xlabel('Iteration')
plt.ylabel('Cost')
plt.title('Cost function')
plt.show()