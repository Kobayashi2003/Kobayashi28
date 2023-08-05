#include <iostream>
#include <string>

using namespace std;

class Birthday {
public:
	int Year, Month, Day;
	Birthday(int y, int m, int d) : Year(y), Month(m), Day(d) {}
	void SetBirthday(int ny, int nm, int nd) {
		Year = ny; Month = nm; Day = nd;
	}
};

class Teacher {
protected:
	int num;
	string name;
	string sex;
public:
	Teacher(int _num, string _name, string _sex) : num(_num), name(_name), sex(_sex) {}
};

class Professor : public Teacher {
private:
	Birthday birthday;
public:
	Professor(int Num, string Name, string Sex, Birthday b) : Teacher(Num, Name, Sex), birthday(b) {}
	void setBirthday(int nYear, int nMonth, int nDay) {
		birthday.SetBirthday(nYear, nMonth, nDay);
	}
	void display() {
		// cout << num << " " << name << " " << birthday.Year << " " << birthday.Month << " " << birthday.Day << endl;
		cout << "id:" << num << endl;
		cout << "name:" << name << endl;;
		cout << "sex:" << sex << endl;
		cout << "birthday:" << birthday.Year << "/" << birthday.Month << "/" << birthday.Day << endl;
	}
};

int main() {
	int Num;
	string Mame;
	string Sex;
	int Year, Month, Day, nYear, nMonth, nDay;
	cin >> Num >> Mame >> Sex >> Year >> Month >> Day;
	Professor p(Num, Mame, Sex, Birthday(Year, Month, Day));
	cin >> nYear >> nMonth >> nDay;
	p.setBirthday(nYear, nMonth, nDay);
	p.display();
	return 0;
}