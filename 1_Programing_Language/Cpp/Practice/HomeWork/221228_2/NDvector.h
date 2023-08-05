#include <iostream>

class NDvector {
public:
    NDvector(int dim=1);
    ~NDvector();

    friend std::istream& operator>>(std::istream &in, NDvector &vec);
    friend std::ostream& operator<<(std::ostream &out, const NDvector &vec);

    NDvector operator+(const NDvector &vec);
    NDvector operator-(const NDvector &vec);
    int operator*(const NDvector &vec);

    bool operator=(const NDvector &vec);

private:
    int _dim;
    int* _data;
};