// 事实上，vector本身的功能就相当于一个顺序表的数据结构

#include<iostream>
#include<vector>

#define Per_Capacity 5

using namespace std;

typedef int DataType;

struct SeqList {
    vector <DataType> Data;
    int size; // 线性表中的有效数据
    int capacity; // 线性表的总容量
    /*
    int n; // 线性表容量相当于Per_Capacity扩增的倍数
    */
};

int main() {
    vector <DataType> testData(20,1);

    // 制造并初始化顺序表
    SeqList list;
    list.capacity = Per_Capacity;
    list.size = 0;
    list.Data.resize(list.capacity);
    // list.n = 1;

    // 装载数据
    for(auto p = testData.begin(); p != testData.end(); p ++) {
        // 首先需要测试顺序表是否已满
        if(list.size == list.capacity) {
            // list.n ++;
            list.capacity += Per_Capacity;
            list.Data.resize(list.capacity); //扩充
        }
        list.Data[list.size++] = *p;
    }


    return 0;
}