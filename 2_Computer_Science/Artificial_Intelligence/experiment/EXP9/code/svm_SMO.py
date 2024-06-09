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
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

class SVM:
    def __init__(self, C=1.0, max_iter=1000, tol=1e-3):
        """
        :param C: 惩罚系数
        :param max_iter: 最大迭代次数
        :param tol: 容忍度
        """
        self.C = C
        self.max_iter = max_iter
        self.tol = tol

        """
        self.alphas: 拉格朗日乘子
        self.w: 权重向量
        self.b: 偏置项
        """
        self.alphas = None
        self.w = None
        self.b = None

    def fit(self, X, y): # SMO
        n_samples, n_features = X.shape
        self.alphas = np.zeros(n_samples)
        self.w = np.zeros(n_features)
        self.b = 0

        for _ in range(self.max_iter):
            alpha_prev = np.copy(self.alphas)

            for j in range(n_samples):
                i = np.random.randint(0, n_samples)
                while i == j:
                    i = np.random.randint(0, n_samples)

                xi, xj, yi, yj = X[i], X[j], y[i], y[j]
                # kii, kjj, kij = np.dot(xi, xi), np.dot(xj, xj), np.dot(xi, xj)
                kii, kjj, kij = self._kernel(xi, xi), self._kernel(xj, xj), self._kernel(xi, xj)
                eta = 2 * kij - kii - kjj

                Ei = self._decision_function(xi) - yi
                Ej = self._decision_function(xj) - yj

                if eta == 0:
                    continue

                alpha_j_old = self.alphas[j]

                # 计算L和H (L <= alpha_j_new <= H)
                if yi != yj:
                    L = max(0, self.alphas[j] - self.alphas[i])
                    H = min(self.C, self.C + self.alphas[j] - self.alphas[i])
                else:
                    L = max(0, self.alphas[j] + self.alphas[i] - self.C)
                    H = min(self.C, self.alphas[j] + self.alphas[i])
                
                if L == H:
                    continue

                # 计算新的alpha值
                alpha_j_new = np.clip(alpha_j_old - yj * (Ei - Ej) / eta, L, H)
                alpha_i_new = self.alphas[i] + yi * yj * (alpha_j_old - alpha_j_new)

                self.alphas[j] = alpha_j_new
                self.alphas[i] = alpha_i_new

            # 检查alpha是否有足够的变化
            diff = np.linalg.norm(self.alphas - alpha_prev)
            if diff < self.tol:
                break

        # 计算权重向量w: w = Σ (alpha_i * y_i * x_i)
        self.w = np.sum(self.alphas[:, None] * y[:, None] * X, axis=0)

        # 计算偏置项b: b = 1/n_samples * Σ (y_i - w^T x_i)
        self.b = np.mean([yi - np.dot(self.w, xi) for xi, yi in zip(X, y)])

    def _decision_function(self, x):
        # f(x) = w^T x + b
        return np.dot(x, self.w) + self.b

    def _kernel(self, x1, x2):
        return np.dot(x1, x2)

    def predict(self, X):
        return np.sign(self._decision_function(X))

# 创建SVM实例并训练
model = SVM()
model.fit(X_train, y_train)

# 在测试集上进行预测并计算准确率
predictions = model.predict(X_test)
accuracy = np.mean(predictions == y_test)
print(f"Model accuracy: {accuracy * 100:.2f}%")

def plot_decision_boundary(X, y, model):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.01), np.arange(y_min, y_max, 0.01))

    Z = model.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, alpha=0.3)
    plt.scatter(X[y == -1][:, 0], X[y == -1][:, 1], c='blue', label='Setosa')
    plt.scatter(X[y == 1][:, 0], X[y == 1][:, 1], c='red', label='Versicolor')

    plt.xlabel('Sepal length')
    plt.ylabel('Sepal width')
    plt.legend()
    plt.show() 

plot_decision_boundary(X_test, y_test, model)