#include "NDvector.h"

NDvector::NDvector(int dim)
{
    this->_dim = dim;
    this->_data = new int[dim];
}

NDvector::~NDvector()
{
    delete[] this->_data;
}

std::istream& operator>>(std::istream &in, NDvector &vec)
{
    for (int i = 0; i < vec._dim; ++i) {
        in >> vec._data[i];
    }
    return in;
}

std::ostream& operator<<(std::ostream &out, const NDvector &vec)
{
    std::cout << "("; 
    for (int i = 0; i < vec._dim; ++i) {
        out << vec._data[i];
        if (i != vec._dim - 1) {
            out << ",";
        }
    }
    out << ")";
    return out;
}

NDvector NDvector::operator+(const NDvector &vec)
{
    if (this->_dim != vec._dim) {
        // throw "Error: The dimensions of the two vectors are different.";
        std::string message = "error in operator+";
        throw message;
    }
    NDvector result(this->_dim);
    for (int i = 0; i < this->_dim; ++i) {
        result._data[i] = this->_data[i] + vec._data[i];
    }
    return result;
}

NDvector NDvector::operator-(const NDvector &vec)
{
    if (this->_dim != vec._dim) {
        // throw "Error: The dimensions of the two vectors are different.";
        std::string message = "error in operator-";
        throw message; 
    }
    NDvector result(this->_dim);
    for (int i = 0; i < this->_dim; ++i) {
        result._data[i] = this->_data[i] - vec._data[i];
    }
    return result;
}

int NDvector::operator*(const NDvector &vec)
{
    if (this->_dim != vec._dim) {
        // throw "Error: The dimensions of the two vectors are different.";
        std::string message = "error in operator*";
        throw message;
    }
    int result = 0;
    for (int i = 0; i < this->_dim; ++i) {
        result += this->_data[i] * vec._data[i];
    }
    return result;
}

bool NDvector::operator=(const NDvector &vec)
{
    delete [] this->_data;
    this->_dim = vec._dim;
    this->_data = new int[this->_dim];
    for (int i = 0; i < this->_dim; ++i) {
        this->_data[i] = vec._data[i];
    }

    return true;
}