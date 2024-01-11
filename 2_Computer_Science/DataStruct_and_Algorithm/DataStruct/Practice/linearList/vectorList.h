#include "linearList.h"
#include "myExceptions.h"
#include <vector>
#include <iostream>
#include <sstream>

using namespace std;

template <typename T>
class vectorList : public linearList<T> {
public:
    /// Constructor and Destructor ///
    vectorList(int initialCapacity = 10);
    vectorList(const vectorList<T>&);
    ~vectorList() { delete[] element; }

    /// ADT ///
    bool empty() const { return element->empty(); }
    int size() const { return (int) element->size(); }
    T& get(int theIndex) const;
    int indexOf(const T& theElement) const;
    void erase(int theIndex);
    void insert(int theIndex, const T& theElement);
    void output(ostream& out) const;

    /// Additional ///
    int capacity() const { return (int) element->capacity(); }

    /// iterator ///
    typedef typename vector<T>::iterator iterator;
    iterator begin() { return element->begin(); }
    iterator end() { return element->end(); }

protected:
    void checkIndex(int theIndex) const;
    vector<T>* element;
};


template <typename T>
vectorList<T>::vectorList(int initialCapacity) {
    if (initialCapacity < 1) {
        ostringstream s;
        s << "Initial capacity = " << initialCapacity << " Must be > 0";
        throw illegalParameterValue(s.str());        
    }

    element = new vector<T>;
    element->reserve(initialCapacity);
}

template <typename T>
vectorList<T> :: vectorList(const vectorList<T>& theList) {
    element = new vector<T>(*theList.element);
}

template <typename T>
void vectorList<T>::erase(int theIndex) {
    checkIndex(theIndex);
    element->erase(element->begin() + theIndex);
}

template <typename T>
void vectorList<T>::insert(int theIndex, const T& theElement) {
    if (theIndex < 0 || theIndex > size()) {
        ostringstream s;
        s << "index = " << theIndex << " size = " << size();
        throw illegalIndex(s.str());
    }
    element->insert(element->begin() + theIndex, theElement);
}