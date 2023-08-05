#include "myExceptions.h"
#include "linearList.h"
#include <iostream>
#include <sstream>
#include <algorithm>
#include <iterator>

#include <initializer_list>

/// @brief change the length of the array
/// @tparam T 
/// @param a 
/// @param oldLength 
/// @param newLength 
template <typename T>
void changeLength1D(T*& a, int oldLength, int newLength) {
    if (newLength < 0) throw illegalParameterValue("new length must be >= 0");
    T* temp = new T[newLength];
    int number = min(oldLength, newLength);
    copy(a, a + number, temp);
    delete [] a;
    a = temp;
}


template <typename T>
class arrayList : public linearList<T> {
public:
    /// constructor and destructor ///
    arrayList(int initialCapacity = 10);
    arrayList(const arrayList<T>&);
    ~arrayList() { delete [] element; } 


    arrayList(initializer_list<T> list) : arrayList(list.size()) {
        for (auto i = list.begin(); i != list.end(); ++i) {
            insert(listSize, *i);
        }
    }


    /// ADT method ///
    bool empty() const { return listSize == 0; }
    int size() const { return listSize; }
    T& get(int theIndex) const;
    int indexOf(const T& theElement) const;
    void erase(int theIndex);
    void insert(int theIndex, const T& theElement);
    void output(ostream& out) const;

    /// additional method ///
    int capacity() const { return arrayLength; }

protected:
    void checkIndex(int theIndex) const;
    T* element;
    int arrayLength;
    int listSize;   
};

/// @brief  constructor
/// @tparam T 
/// @param initialCapacity 
template <typename T>
arrayList <T>::arrayList(int initialCapacity) {
    if (initialCapacity < 1) {
        ostringstream s;
        s << "Initial capacity = " << initialCapacity << " Must be > 0";        
        throw illegalParameterValue(s.str());
    }
    arrayLength = initialCapacity;
    element = new T[arrayLength];
    listSize = 0;
}


/// @brief  copy constructor
/// @tparam T 
/// @param theList 
template <typename T>
arrayList <T>::arrayList(const arrayList<T>& theList) {
    arrayLength = theList.arrayLength;
    listSize = theList.listSize;
    element = new T[arrayLength];
    copy(theList.element, theList.element + listSize, element);
}

/// @brief  check whether theIndex is valid
/// @tparam T 
/// @param theIndex 
template <typename T>
void arrayList <T>::checkIndex(int theIndex) const {
    if (theIndex < 0 || theIndex >= listSize) {
        ostringstream s;
        s << "index = " << theIndex << " size = " << listSize;
        throw illegalIndex(s.str());
    }
}

/// @brief  get the element at the position of theIndex
/// @tparam T 
/// @param theIndex 
/// @return T&
template <typename T>
T& arrayList <T>::get(int theIndex) const {
    checkIndex(theIndex);
    return element[theIndex];
}


/// @brief  find theElement in the arrayList, return the index of the first occurrence
/// @tparam T 
/// @param theElement 
/// @return if theElement is not in the arrayList, return -1
///         else return the index of theElement(first occurrence)
template <typename T>
int arrayList <T>::indexOf(const T& theElement) const {
    int theIndex = (int) (find(element, element + listSize, theElement) - element);
    if (theIndex == listSize) {
        return -1;
    }
    else {
        return theIndex;
    }
}


/// @brief  erease the element at the position of theIndex
/// @tparam T 
/// @param theIndex 
template <typename T>
void arrayList <T>::erase(int theIndex) {
    checkIndex(theIndex);
    copy(element + theIndex + 1, element + listSize, element + theIndex);
    element[--listSize].~T();
}


/// @brief  insert theElement at the position of theIndex
/// @tparam T 
/// @param theIndex 
/// @param theElement 
template <typename T>
void arrayList<T>::insert(int theIndex, const T& theElement) {
    if (theIndex < 0 || theIndex > listSize) {
        ostringstream s;
        s << "index = " << theIndex << " size = " << listSize;
        throw illegalIndex(s.str());
    }
    if (listSize == arrayLength) {
        changeLength1D(element, arrayLength, 2 * arrayLength);
        arrayLength *= 2;
    }
    copy_backward(element + theIndex, element + listSize, element + listSize + 1);
    element[theIndex] = theElement;
    listSize++;
}


/// @brief  insert the arrayList to the ostream
/// @tparam T 
/// @param out 
template <typename T>
void arrayList<T>::output(ostream& out) const {
    copy(element, element + listSize, ostream_iterator<T>(cout, " "));
}

/// @brief  overload the operator<<
/// @tparam T 
/// @param out 
/// @param x 
/// @return ostream&
template <typename T>
ostream& operator<<(ostream& out, const arrayList<T>& x) {
    x.output(out);
    return out;
}