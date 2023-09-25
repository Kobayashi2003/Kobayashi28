#include<iostream>

using namespace std;

class Content {
private :
    int _data2;
public :
    Content(int data2 = 2) : _data2(data2) {
        cout << "Content created" << endl;
    }
    ~Content() {
        cout << "Content deleted" << endl;
    }
    void show2 () {
        cout << "data2: " << _data2 << endl;
    }
};

class Container {
private :
    int _data1;
public :
    Content *_content;
    Container(Content * content = nullptr, int data1 = 1) : _data1(data1),  _content(content) {
        cout << "Container created" << endl;
    }
    ~Container() {
        cout << "Container deleted" << endl;
    }
    void show1 () {
        cout << "data1: " << _data1 << endl;
        if(_content) {
            _content -> show2(); // 提供方法，但不提供接口
        } else {
            cout << "no content" << endl;
        }
    }
};


int main() {
    Content * content = new Content();
    Container container(content);
    container.show1();
    delete content;
    return 0;
}