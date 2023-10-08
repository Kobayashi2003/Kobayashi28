#include <iostream>
#include <string>

using namespace std;

class myString : public string {

    bool operator==(const myString& s) {
        if (this->size() != s.size()) {
            return false;
        }
        for (int i = 0; i < this->size(); i++) {
            if (this->at(i) != s.at(i)) {
                return false;
            }
        }
        return true;        
    }

};

int main() {
    string s1 = "abc";
    string s2 = "abc";
    cout << (s1 == s2) << endl;

    return 0;
}