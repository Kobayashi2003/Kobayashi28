#include <iostream>

using namespace std;

class illegalParameterValue {
public:
    illegalParameterValue(string theMessage = "Illegal parameter value") { message = theMessage; }
    void outputMessage() { cout << message << endl; }
private:
    string message;
};


class illegalIndex {
public:
    illegalIndex(string theMessage = "Illegal index") { message = theMessage; }
    void outputMessage() { cout << message << endl; }
private:
    string message;
};


class matrixIndexOutOfBounds {
public:
    matrixIndexOutOfBounds(string theMessage = "Matrix index out of bounds") { message = theMessage; }
    void outputMessage() { cout << message << endl; }
private:
    string message;
};


class matrixSizeMismatch {
public:
    matrixSizeMismatch(string theMessage = "Matrix size mismatch") { message = theMessage; }
    void outputMessage() { cout << message << endl; }
private:
    string message;
};