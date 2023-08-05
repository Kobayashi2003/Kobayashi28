// Make sure public inheritance models "is-a"
// 确定你的 public 继承塑模出 is-a 关系

// Attention: “public 继承” 意味着 is-a。适用于 base classes 身上的每一件事一定也适用于 derived classes 身上，
// 因为每一个 derived classes 对象也都是一个 base classes 对象。

#include <iostream>

using namespace std;

class Pet
{
public:
    Pet() { cout << "Pet()" << endl; }
    ~Pet() { cout << "~Pet()" << endl; }
};

class Dog : public Pet // public inheritance: Dog "is a" Pet
{
public:
    Dog() { cout << "Dog()" << endl; }
    ~Dog() { cout << "~Dog()" << endl; }
};

int main()
{
    Dog d;
    return 0;
}