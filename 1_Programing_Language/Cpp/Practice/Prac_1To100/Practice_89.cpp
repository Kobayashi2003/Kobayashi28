// strategy method

#include <iostream>
#include <string>

using namespace std;

class character {

    typedef int (*skill)(void);

public:
    enum {normal, skill1, skill2};
    character() = default;
    ~character() = default;

    void set_skill_1(int (*skill)(void)) {
        skill_1 = skill;
    }

    void set_skill_2(int (*skill)(void)) {
        skill_2 = skill;
    }

    void attack(int pattern = normal) {
        switch (pattern) {
        case normal:
            cout << "normal attack" << endl;
            break;
        case skill1:
            mp -= skill_1();
            break;
        case skill2:
            mp -= skill_2();
            break;
        }
        show_status();
    }

    void show_status() {
        cout << "hp: " << hp << endl;
        cout << "mp: " << mp << endl;
    }

private:

    skill skill_1 = nullptr;
    skill skill_2 = nullptr;

    string name = "kobayashi";
    string job = "magician";
    int hp = 100;
    int mp = 100;
};

int fire_ball() {
    cout << "fire ball!" << endl;
    return 10;
} 

int thunder() {
    cout << "thunder!" << endl;
    return 20;
}

int main() {
    character kobayashi;
    kobayashi.set_skill_1(fire_ball);
    kobayashi.set_skill_2(thunder);

    kobayashi.attack();
    kobayashi.attack(character::skill1);
    kobayashi.attack(character::skill2);

    return 0;
}