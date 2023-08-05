# 绘制简单的折线图

import matplotlib.pyplot as plt

input_values = [1, 2, 3, 4, 5]
squares = [1, 4, 9, 16, 25]

plt.style.use('seaborn')

fig, ax = plt.subplots() # 调用函数 subplots()。这个函数可以在一张图片中绘制一个或多个图标。变量 fig 表示整张图片。变量 ax 表示图片中的各个图表
ax.plot(input_values, squares, linewidth=3) # 方法 plot() ，它尝试根据给定的数据以有意义的方式绘制图表。

# 设置图表标题并给坐标轴加上标签（标签最好用英文）
ax.set_title("Square number", fontsize=24)
ax.set_xlabel("Value", fontsize=14)
ax.set_ylabel("Square", fontsize=14)

# 设置刻度标记的大小
ax.tick_params(axis='both', labelsize=14)

plt.show() # 方法 show() 打开 Matplotlib 查看器并显示绘制的图表