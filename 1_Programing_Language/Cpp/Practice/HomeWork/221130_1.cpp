#include <iostream>
#include <limits>
#include <string>

using namespace std;

class Journey_Card {
protected:
    int j_card_number;
    int j_points;
public:
    Journey_Card(int number) : j_card_number(number), j_points(0) {};
    virtual void order(float m) {
        j_points += (int)m;
    }
    virtual void show() const {
        cout << j_card_number << " " << j_points << endl;
    }
};

class Credit_Card {
protected:
    int c_card_number;
    string c_name;
    int c_limit;
    float c_bill;
    int c_points;
public:
    Credit_Card(int number, string name, int limit) : c_card_number(number), c_name(name), c_limit(limit), c_bill(0), c_points(0) {};
    void consume(float m) {
        if (c_bill + m > c_limit) { return; }
        c_bill += m; c_points += (int)m;
    }
    void refund(float m) {
        if (c_bill - m < 0) { return; }
        c_bill -= m;
        c_points -= (int)m;
        if (c_points < 0) { c_points = 0; }
    }
    virtual void show() const {
        cout << c_card_number << " " << c_name << " " << c_bill << " " << c_points << endl;
    }
};

class JourneyCreditCard : public Journey_Card, public Credit_Card {
public:
    JourneyCreditCard(int j_number, int c_number, string name, int limit) :
        Journey_Card(j_number), Credit_Card(c_number, name, limit) {};

    virtual void order(float m) {
        Journey_Card::order(m);
        Credit_Card::consume(m);
    }

    void change_points(int m) {
        if (c_points - m < 0) { return; }
        c_points -= m;
        j_points += m/2;
    }

    virtual void show () const {
        Journey_Card::show();
        Credit_Card::show();
    }
};


int main() {

    int j_number, c_number; cin >> j_number >> c_number;
    string name; cin >> name;
    int limit; cin >> limit;
    JourneyCreditCard card(j_number, c_number, name, limit);

    int N; cin >> N;
    char command;
    float m;
    while (N--) {
        cin >> command >> m;
        cin.ignore(numeric_limits<streamsize>::max(), '\n');
        switch (command) {
            case 'o':
                card.order(m);
                break;
            case 'c':
                card.consume(m);
                break;
            case 'q':
                card.refund(m);
                break;
            case 't':
                card.change_points(m);
                break;
            default:
                cout << "Unknown command" << endl;
        }
    }
    card.show();
    return 0;
}