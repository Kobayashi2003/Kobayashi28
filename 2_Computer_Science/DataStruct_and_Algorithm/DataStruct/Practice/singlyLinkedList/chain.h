#include "linearList.h"
#include "chainNode.h"
#include "myExceptions.h"
#include <iostream>
#include <sstream>

using namespace std;

template <typename T>
class chain : public linearList<T> {
public:
    /// constructors and destructor ///
    chain(int initialCapacity = 10);
    chain(const chain<T>&);
    ~chain();

    /// ADT methods ///
    bool empty() const { return listSize == 0; }
    int size() const { return listSize; }
    T& get(int theIndex) const;
    int indexOf(const T& theElement) const;
    void erase(int theIndex);
    void insert(int theIndex, const T& theElement);
    void output(ostream& out) const;

protected:
    void checkIndex(int theIndex) const;

    chainNode<T>* firstNode; // pointer to first node in chain 
    int listSize; // number of elements in list
};


/// constructor ///
template <typename T>
chain<T>::chain(int initialCapacity) {
    if (initialCapacity < 1) {
        ostringstream s;
        s << "Initial capacity = " << initialCapacity << " Must be > 0";
        throw illegalParameterValue(s.str());
    }
    firstNode = nullptr;
    listSize = 0;
}

/// copy constructor ///
template <typename T>
chain<T>::chain(const chain<T>& theList) {
    listSize = theList.listSize;

    if (listSize == 0) { // theList is empty
        firstNode = nullptr;
        return;
    }

    // theList is not empty
    chainNode<T>* sourceNode = theList.firstNode; // node in theList to copy from
    firstNode = new chainNode<T>(sourceNode->element); // copy first element of theList
    sourceNode = sourceNode->next; // move to next node
    chainNode<T>* targetNode = firstNode; // current last node in *this
    while (sourceNode != nullptr) {
        // copy from theList
        targetNode->next = new chainNode<T>(sourceNode->element);
        targetNode = targetNode->next;
        sourceNode = sourceNode->next;
    }
    targetNode->next = nullptr; // end the chain
}

/// destructor ///
template <typename T>
chain<T>::~chain() { // delete all nodes in chain
    while (firstNode != nullptr) {
        chainNode<T>* nextNode = firstNode->next;
        delete firstNode;
        firstNode = nextNode;
    }
}


/// ADT methods ///

/// get the k-th element of the list ///
template <typename T>
T& chain<T>::get(int theIndex) const { // return element whose index is theIndex
    // throw illegalIndex if theIndex invalid
    checkIndex(theIndex);

    // move to theIndex-th node
    chainNode<T>* currentNode = firstNode;
    for (int i = 0; i < theIndex; i++) {
        currentNode = currentNode->next;
    }
    return currentNode->element;
}


/// return index of first occurrence of theElement ///
template <typename T>
int chain<T>::indexOf(const T& theElement) const {
    // search the chain for theElement
    // if not found, return -1

    chainNode<T>* currentNode = firstNode;
    int index = 0; // index of currentNode
    while (currentNode != nullptr && currentNode->element != theElement) {
        // move to next node
        currentNode = currentNode->next;
        index++;
    }
    if (currentNode == nullptr) {
        return -1;
    } else {
        return index;
    }
}


/// erase the k-th element of the list ///
template <typename T>
void chain<T>::erase(int theIndex) {
    checkIndex(theIndex);

    chainNode<T>* deleteNode;
    if (theIndex == 0) {
        deleteNode = firstNode;
        firstNode = firstNode->next;
    } else {
        chainNode<T>* p = firstNode; // p is the node before the one to delete
        for (int i = 0; i < theIndex - 1; i++) {
            p = p->next;
        }
        deleteNode = p->next;
        p->next = p->next->next;
    }
    listSize--;
    delete deleteNode;
}


/// insert theELement so that its index is theIndex ///
template <typename T>
void chain<T>::insert(int theIndex, const T& theElement) {
    if (theIndex < 0 || theIndex > listSize) {
        ostringstream s;
        s << "index = " << theIndex << " size = " << listSize;
        throw illegalIndex(s.str());
    }

    if (theIndex == 0) {
        firstNode = new chainNode<T>(theElement, firstNode);
    } else {
        chainNode<T>* p = firstNode;
        for (int i = 0; i < theIndex - 1; i++) {
            p = p->next;
        }
        p->next = new chainNode<T>(theElement, p->next);
    }
    listSize++;
}


/// output the list ///
template <typename T>
void chain<T>::output(ostream& out) const {
    for (chainNode<T>* currentNode = firstNode; currentNode != nullptr; currentNode = currentNode->next) {
        out << currentNode->element << " ";
    }
}

/// overload << ///
template <typename T>
ostream& operator<<(ostream& out, const chain<T>& x) {
    x.output(out);
    return out;
}