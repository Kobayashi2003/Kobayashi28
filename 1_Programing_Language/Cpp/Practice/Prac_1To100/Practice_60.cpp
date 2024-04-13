#include <iostream>

using namespace std;

class People {
private:
    const char *name = "kobayashi";
public:
    People() {}
    People(const People & p) {
        cout << "clone!" << endl;
        name = p.name;
    }
    ~People() {}
    void tellName() {
        cout << "my name is " << name << endl;
    }
};

int main() {
    People me = People();
    People clone_me_1 = People(me);
    People clone_me_2 = me;
    me.tellName();
    clone_me_1.tellName();
    clone_me_2.tellName();
    return 0;
}