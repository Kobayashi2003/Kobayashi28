#include <iostream>
#include <queue>
// 为了方便，固定有向图的起点为 1——数学科目
#define MAX 10 // 限制最多有10个数学科目

class digraph
{
private:
    int _Vexs[MAX];         // 有向图的顶点
    int _VexNum;            // 顶点的数目
    int _EdgeNum;           // 关系（边）的个数
    bool _Matrix[MAX][MAX]; // 邻接矩阵
public:
    // 创建图(自己输入数据)
    digraph();
    // 销毁图
    ~digraph();
    // 打印矩阵队列次序
    void print();
};

digraph::digraph()
{
    std::cin >> _VexNum;
    // 图初始化（顶点矩阵和邻接矩阵）
    for (int i = 0; i < _VexNum; i++)
    {
        _Vexs[i] = i + 1; // 初始化顶点
    }
    for (int i = 0; i < _VexNum; i++)
    {
        for (int j = 0; j < _VexNum; j++)
        {
            /*============================
                    请在此处完成代码
                 邻接矩阵初始为全false
             ============================*/
            _Matrix[i][j] = false;
        }
    }
    // 课 程 关 系 输 入
    std::cin >> _EdgeNum;
    for (int i = 0; i < _EdgeNum; i++)
    {
        int src, dst;
        std::cin >> src >> dst;
        /*============================
                请在此处完成代码
        将关系对应的邻接矩阵元素设置为true
        ============================*/
        _Matrix[src - 1][dst - 1] = true;
    }
}

digraph::~digraph()
{
}

void digraph::print()
{
    std::queue<int> arrangement;
    bool label[MAX]; // label记录该节点是否被访问过
    for (int i = 0; i < _VexNum; i++)
    {
        /*============================
                请在此处完成代码
        初始化label，全部设置为false
        ============================*/
        label[i] = false;
    }
    // 把起点压入队列
    arrangement.push(_Vexs[0]);
    while (!arrangement.empty())
    {
        int course_id = arrangement.front();
        // 检查当前课程是否已被输出
        if (label[course_id - 1] == true)
        {
            /*============================
                   请在此处完成代码
              该课程已输出，不应存在在队列
                   将其弹出并跳过处理
            ============================*/
            arrangement.pop();
            continue;
        }
        // 当前课程未被输出
        for (int i = 0; i <= _VexNum; i++)
        {
            if (i == _VexNum)
            { // 任意前继节点均被访问的
                /*============================
                       请在此处完成代码
                当前节点可以被访问，对其进行记录
                ============================*/
                label[course_id - 1] = true;
                break;
            }
            if ((_Matrix[i][course_id - 1] == true) && (label[i] == false))
            { // 存在前继节点未被访问
                break;
            }
        }
        arrangement.pop();
        if (label[course_id - 1] == true)
            /*============================
                    请在此处完成代码
                  输出当前节点课程编号
            ============================*/
            std::cout << course_id << " ";
        else
            continue;
        // 将该课程的后继节点入队
        for (int i = 0; i < _VexNum; i++)
        {
            if ((_Matrix[course_id - 1][i] == true) && (label[i] == false))
            { // 存在后继节点 i 未被访问
                arrangement.push(_Vexs[i]);
            }
        }
    }
    std::cout << std::endl;
}

int main()
{
    digraph course;
    course.print();
    return 0;
}