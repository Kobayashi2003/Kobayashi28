#include <iostream>
using namespace std;

class Array
{

private:
    int *data; // 定义整形数据data保存数据

    int count;

    int n;

public:
    // 构造函数

    Array(int nums)
    {

        data = new int[nums];

        n = nums;

        count = 0;
    }

    void adddata(int x)
    {
        data[count++] = x;
    }

    void PrintAll()
    {
        for (int i = 0; i < count; i++) {
            if (i == count - 1) {
                cout << data[i] << endl;
                return;
            }
            cout << data[i] << " ";
        }
    }

    void FindMax()
    {
        int max = data[0];
        for (int i = 0; i < count; i++)
            if (data[i] >= max)
                max = data[i];
        cout << max << endl;
    }

    void FindMin()
    {
        int min = data[0];
        for (int i = 0; i < count; i++)
            if (data[i] <= min)
                min = data[i];
        cout << min << endl;
    }

    void Exchange(int index1, int index2)
    {
        data[index1] += data[index2];
        data[index2] = data[index1] - data[index2];
        data[index1] -= data[index2];
    }

    bool Contains(int x)
    {
        for (int i = 0; i < count; i++)
            if (data[i] == x)
                return true;
        return false;
    }
};

int main()
{


    int n, e, index1, index2;
    cin >> n;
    Array array(n);
    for (int i = 0; i < n; i++)
    {
        int data; cin >> data;
        array.adddata(data);
    }
    cin >> index1 >> index2;
    cin >> e;


    array.PrintAll(); // 打印数组

    array.FindMax(); // 找出最大值

    array.FindMin(); // 找出最小值

    array.Exchange(index1, index2); // 交换两个元素位置

    array.PrintAll(); // 打印数组

    cout << array.Contains(e) << endl; // 某个元素是否存在

    return 0;
}