// 设计⼀个程序，定义⼀个矩形类，包括数据成员和函数
// 成员。要求有构造函数、析构函数，完成赋值、修改、
// 显示等功能的接⼝，并编写 main 函数测试，要求⽤⼀
// 个对象初始化另⼀对象。

// 要确定⼀个矩形（四边都是⽔平或垂直⽅向，不能倾
// 斜），只要确定其左上⻆坐标和宽度⾼度即可，因此
// 应包括四个数据成员，x, y, width, height。

#include<iostream>

using namespace std;

class rectangle {
    private :
        double x, y, width, height;
    public :
        rectangle(double tx, double ty, double tw, double th) { // 构造函数
            x = tx; y = ty; width = tw; height = th;
            cout << "Constructor Work" << endl;
        }
        rectangle(const rectangle & REC) { // 复制构造函数
            x = REC.x; y = REC.y; width = REC.width; height = REC.height;
            cout << "Copy Constructor Work" << endl;
        }
        ~rectangle (){ // 析构函数
            cout << "Desturctor Work" << endl;
        }
        void set(double tx, double ty, double tw, double th) {
            x = tx; y = ty; width = tw; height = th;
        }
        void show () {
            cout << "Coordinate: " << x << ", " << y << endl << "Width: " << width << endl << "Height: " << height << endl;
        }
};

int main() {
    rectangle REC(1.0, 2.0, 10.0, 10.0);
    rectangle Rec = REC;
    Rec.show();
    return 0;
}