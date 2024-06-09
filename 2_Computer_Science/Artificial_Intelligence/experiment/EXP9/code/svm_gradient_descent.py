import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# 加载数据集
iris = datasets.load_iris()
X = iris.data
y = iris.target
y[y == 0] = -1  # 将类别标签从0变为-1，以适应SVM的标准形式

# 选择Setosa和Versicolor两类
X = X[y < 2]
y = y[y < 2]

# 选择前两个特征以便于可视化
X = X[:, :2]

# 标准化
scaler = StandardScaler()
X = scaler.fit_transform(X)

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=45)

class LinearSVM:
    def __init__(self, learning_rate=0.01, lambda_param=0.01, n_iters=1000):
        """
        :param learning_rate: 学习率
        :param lambda_param: 正则化参数
        :param n_iters: 迭代次数
        """
        self.lr = learning_rate
        self.lambda_param = lambda_param
        self.n_iters = n_iters

        """
        self.w: 权重向量
        self.b: 偏置项
        """
        self.w = None
        self.b = None

    def fit(self, X, y): # gradient descent
        n_samples, n_features = X.shape
        y_ = np.where(y <= 0, -1, 1)
        
        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(self.n_iters):
            for idx, x_i in enumerate(X):
                condition = y_[idx] * (np.dot(x_i, self.w) - self.b) >= 1
                if condition: # 正确分类的情况
                    self.w -= self.lr * (2 * self.lambda_param * self.w)
                else: 
                    self.w -= self.lr * (2 * self.lambda_param * self.w - np.dot(x_i, y_[idx]))
                    self.b -= self.lr * y_[idx]

    def predict(self, X):
        linear_output = np.dot(X, self.w) - self.b
        return np.sign(linear_output)

# 创建SVM分类器实例
svm = LinearSVM()
svm.fit(X_train, y_train)

# 预测测试集
predictions = svm.predict(X_test)
accuracy = np.mean(predictions == y_test)
print(f"Model accuracy: {accuracy * 100:.2f}%")


def plot_decision_boundary(X, y, model):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.linspace(x_min, x_max, 100), np.linspace(y_min, y_max, 100))

    points = np.c_[xx.ravel(), yy.ravel()]
    z = model.predict(points)
    z = z.reshape(xx.shape)

    plt.contourf(xx, yy, z, alpha=0.1)
    plt.scatter(X[:, 0], X[:, 1], c=y, s=40, cmap=plt.cm.Paired)
    plt.xlabel("Sepal length")
    plt.ylabel("Sepal width")
    plt.show()

plot_decision_boundary(X_test, y_test, svm)

