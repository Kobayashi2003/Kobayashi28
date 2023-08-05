#include <iostream>
#include <string>


using namespace std;

class Residents {
private:
	size_t _id;
	string _name;
	string _sex;
	size_t _birthday;
public:
	Residents() = default;

	void input_R() {
		size_t id; string name; string sex; size_t birthday;
		cin >> id; cin.get();
		cin >> name; cin.get();
		cin >> sex; cin.get();
		cin >> birthday;

		_id = id; _name = name; _sex = sex; _birthday = birthday;
	}

	void output_R() {
		cout << _id << " " << _name << " " << _sex << " " << _birthday << endl;
	}
};

class Adult : public Residents {
private:
	string _acbg;
	string _career;
public:
	Adult() = default;

	void input_A() {

		input_R();

		string acbg, career;
		cin >> acbg; cin.get();
		cin >> career;

		_acbg = acbg; _career = career;
	}

	void output_A() {
		output_R();
		cout << _acbg << " " << _career << endl;
	}
};

class Party : public Adult {
private:
	string _class;
public:
	Party() = default;

	void input_P() {

		input_A();

		string c;
		cin >> c; cin.get();
		_class = c;
	}

	void output_P() {
		output_A();
		cout << _class << endl;
	}
};


int main() {
	Residents R;
	R.input_R();
	R.output_R();

	Adult A;
	A.input_A();
	A.output_A();
	Party P;
	P.input_P();
	P.output_P();
	return 0;
}