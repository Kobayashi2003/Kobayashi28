# 使用 scatter() 绘制散点图并设置阳台是

import matplotlib.pyplot as plt

# x_values = [1, 2, 3, 4, 5]
# y_values = [1, 4, 9, 16, 25]

x_values = range(1, 1001)
y_values = [x**2 for x in x_values] # 也可以让 python 自己生成数据

plt.style.use('seaborn')
fig, ax = plt.subplots()
# ax.scatter(2, 4, s=200) # 方法 scatter(), 向它传递一对 x坐标 和 y坐标，它将在指定位置绘制一个点
ax.scatter(x_values, y_values, c=y_values, cmap=plt.cm.Blues, s=10)
# 要绘制一系列的点，可向 scatter() 传递两个分别包含 x值 和 y值 的列表
# 要修改数据点的颜色，可向 scatter() 传递参数 c（c='#2b80c4'）
# 要使用颜色映射（colormap）可以将参数 c 设置为一个 y值列表，并使用参数 cmap告诉 pyplot 使用哪个颜色映射。

# 设置图表标题并给坐标轴加上标签
ax.set_title('squares'.title(), fontsize=24)
ax.set_xlabel("values", fontsize=14)
ax.set_ylabel("squares", fontsize=14)

# 设置刻度标记的大小
ax.tick_params(axis='both', which='major', labelsize=14)

# 设置每个坐标轴的取值范围
ax.axis([0, 1100, 0, 1100000])

plt.show()

# 要让程序自动将图标保存到文件中，可使用 plt.saveifg('filename', bbox_inches='tight') 第二个参数可以指定将图表多余的空白区域裁剪掉。这个文件将存储到当前文件所在的目录