template <typename T>
struct binaryTreeNode {
    T element;
    binaryTreeNode<T> *leftChild, *rightChild;

    binaryTreeNode() { leftChild = rightChild = nullptr; }
    binaryTreeNode(const T& theElement) {
        element(theElement);
        leftChild = rightChild = nullptr;
    } 
    binaryTreeNode(const T& theElement,
                   binaryTreeNode<T> *theLeftChild,
                   binaryTreeNode<T> *theRightChild) 
    {
        element = theElement;
        leftChild = theLeftChild;
        rightChild = theRightChild;
    }
};


// preOrder traverse //
template <typename T>
void preOrder(binaryTreeNode<T> *t) {
    if (t != nullptr) {
        visit(t->element);
        preOrder(t->leftChild);
        preOrder(t->rightChild);
    }
}


// inOrder traverse //
template <typename T>
void inOrder(binaryTreeNode<T> *t) {
    if (t != nullptr) {
        inOrder(t->leftChild);
        visit(t->element);
        inOrder(t->rightChild);
    }
}


// postOrder traverse //
template <typename T>
void postOrder(binaryTreeNode<T> *t) {
    if (t != nullptr) {
        postOrder(t->leftChild);
        postOrder(t->rightChild);
        visit(t->element);
    }
}


template <typename T>
void visit(binaryTreeNode<T> *x) {
    cout << x->element << " ";
}


// levelOrder traverse //
template <typename T>
void levelOrder(binaryTreeNode<T> *t) {
    arrayQueue<binaryTreeNode<T>*> q;
    while (t != nullptr) {
        visit(t);

        if (t->leftChild != nullptr)
            q.push(t->leftChild);
        if (t->rightChild != nullptr)
            q.push(t->rightChild);

        try { t = q.front(); }
        catch (queueEmpty) { return; }
        q.pop();
    }
}
