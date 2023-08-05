#ifndef BINARY_TREE
#define BINARY_TREE

template <typename T>
class binaryTree {
public:
    virtual ~binaryTree() { }
    virtual bool empty() const = 0;
    virtual int size() const = 0;
    virtual int height() const = 0;

    virtual void preOrder(void (*) (T *)) = 0;
    virtual void inOrder(void (*) (T *)) = 0;
    virtual void postOrder(void (*) (T *)) = 0;
};  

#endif