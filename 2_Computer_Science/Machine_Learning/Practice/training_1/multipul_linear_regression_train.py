import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
import plotly
import plotly.graph_objs as go

from multipul_linear_regression import LinearRegression

data = pd.read_csv('./data/world-happiness-report-2017.csv')
train_data = data.sample(frac=0.8)
test_data = data.drop(train_data.index)

input_param_name_1 = 'Economy..GDP.per.Capita.'
input_param_name_2 = 'Freedom'
output_param_name = 'Happiness.Score'

x_train = train_data[[input_param_name_1, input_param_name_2]].values
y_train = train_data[[output_param_name]].values

x_test = test_data[[input_param_name_1, input_param_name_2]].values
y_test = test_data[[output_param_name]].values

plot_training_trace = go.Scatter3d(
    x = x_train[:, 0].flatten(),
    y = x_train[:, 1].flatten(),
    z = y_train.flatten(),
    name = 'Training Set',
    mode = 'markers',
    marker = {
        'size': 10,
        'opacity': 0.8,
        'line': {
            'color': 'rgba(255, 255, 255, 1)',
            'width': 1
        }
    },
)

plot_test_trace = go.Scatter3d(
    x = x_test[:, 0].flatten(),
    y = x_test[:, 1].flatten(),
    z = y_test.flatten(),
    name = 'Test Set',
    mode = 'markers',
    marker = {
        'size': 10,
        'opacity': 1,
        'line': {
            'color': 'rgba(255, 255, 255, 1)',
            'width': 1
        }
    },
)

plot_layout = go.Layout(
    title = 'Date Sets',
    scene = {
        'xaxis': {'title': input_param_name_1},
        'yaxis': {'title': input_param_name_2},
        'zaxis': {'title': output_param_name}
    },
    margin = { 'l': 0, 'r': 0, 'b': 0, 't': 0 }
)

plot_data = [plot_training_trace, plot_test_trace]
plot_figure = go.Figure(data=plot_data, layout=plot_layout)
plotly.offline.plot(plot_figure, filename='DateSets.html')




num_iterations = 500
learning_rate = 0.01

model = LinearRegression(x_train, y_train)
(theta, cost_history) = model.train(learning_rate, num_iterations)

print('begin cost', cost_history[0])
print('last cost', cost_history[-1])

predictions_num = 100

x_min = x_train[:, 0].min()
x_max = x_train[:, 0].max()

y_min = x_train[:, 1].min()
y_max = x_train[:, 1].max()

x_axis = np.linspace(x_min, x_max, predictions_num)
y_axis = np.linspace(y_min, y_max, predictions_num)

x_predictions = np.zeros((predictions_num * predictions_num, 1))
y_predictions = np.zeros((predictions_num * predictions_num, 1))

x_y_index = 0
for x_index, x_value in enumerate(x_axis):
    for y_index, y_value in enumerate(y_axis):
        x_predictions[x_y_index] = x_value
        y_predictions[x_y_index] = y_value
        x_y_index += 1

z_predictions = model.predict(np.hstack((x_predictions, y_predictions)))

plot_predictions_trace = go.Scatter3d(
    x = x_predictions.flatten(),
    y = y_predictions.flatten(),
    z = z_predictions.flatten(),
    name = 'Predictions Plane',
    mode = 'markers',
    marker = {
        'size': 1,
    },
    opacity = 0.8,
    surfaceaxis=2,
)

plot_data = [plot_training_trace, plot_test_trace, plot_predictions_trace]
plot_figure = go.Figure(data=plot_data, layout=plot_layout)
plotly.offline.plot(plot_figure, filename='Predictions.html')