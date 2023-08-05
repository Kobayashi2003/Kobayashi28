# 参考 https://blog.csdn.net/wcc15256945095/article/details/123297392

CC_c = gcc
CC_cpp = g++

# 通过 wildcard 搜索当前目录下所有以 .c .cpp 结尾的文件，分别生成一个以空格间隔的文件名列表，并赋值给 SRC_c，SRC_cpp
SRC_c = $(wildcard *.c)
SRC_cpp = $(wildcard *.cpp)

# 通过使用 makefile中的替换规则，将两个 SRC变量中所有以 .c .cpp 结尾的文件名替换为没有后缀的文件名，然后赋回给对应变量
# 注意，这将意味着你的 c与 cpp不能够出现同名的文件，否则将会导致编译失败
BIN_c = $(SRC_c:%.c=%)
BIN_cpp = $(SRC_cpp:%.cpp=%)

all : ${BIN_c} ${BIN_cpp}

# 使用 makefile 的静态模式规则（规则中存在有多个目标，并且不同的目标文件可以根据目标的名字来自动构造处自己的依赖文件）
${BIN_c}:%:%.c
	${CC_c} -g $^ -o $@

${BIN_cpp}:%:%.cpp
	${CC_cpp} -g $^ -o $@

clean:
	rm -rf ${BIN_c} ${BIN_cpp}

.PHONY: all clean