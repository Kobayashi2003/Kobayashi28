#include<iostream>


using namespace std;

class Student {
private:
	string _name;   //姓名
	int    _scores; //成绩
public:
	//外部接口
	Student();
	Student(string name, int scores);
	int    get_scores();                 //获取分数
	string get_name();                   //获取名字
	void   set_scores(int scores);       //更改分数
	void   set_name(string name);        //更改名字
	void   show();                       //打印学生信息
};

class Student_list {
private:
	int _N;         //学生个数
	Student* _list; //学生列表
public:
	//外部接口
	Student_list(int N);
	~Student_list();
	void set(int n_index, Student student);//更改“_list”中下标为“n_index”的学生的信息
	void sort();                           //按照分数高低给“_list”排序
	void show();                           //打印整个班的学生信息
};

//你的代码会从这里插入

Student::Student() {
	_name = "NULL";
	_scores = 0;
}

Student::Student(string name, int scores) {
	_name = name;
	_scores = scores;
}

void Student::set_scores(int scoers) {
    _scores = scoers;
}

void Student::set_name(string name) {
    _name = name;
}

int Student::get_scores() {
    return _scores;
}

string Student::get_name() {
	return _name;
}

void Student::show() {
    cout << _name << " " << _scores << endl;
}

Student_list::Student_list(int N) {
    _N = N;
    _list = new Student[N];
}

Student_list::~Student_list() {
    delete[] _list;
}

void Student_list::set(int n_index, Student student) {
    _list[n_index] = student;
}

void Student_list::sort() {
    // sort the list acroding to the scoers
    for (int i = 0; i < _N - 1; i++) {
        for (int j = i + 1; j < _N; j++) {
            if (_list[i].get_scores() < _list[j].get_scores() ||
			    (_list[i].get_scores() == _list[j].get_scores() && _list[i].get_name() > _list[j].get_name())) {
                Student temp = _list[i];
                _list[i] = _list[j];
                _list[j] = temp;
            }
		}
    }
}

void Student_list::show() {
    for (int i = 0; i < _N; ++i) {
        _list[i].show();
    }
}

int main() {
	int N;
	cin >> N;
	Student_list list(N);
	Student temp;
	for (int i = 0; i < N; i++) {
		string name;
		int scores;
		cin >> name >> scores;
		temp.set_name(name);
		temp.set_scores(scores);
		list.set(i, temp);
	}
	cout << "List sorted by scores: " << endl;
	list.sort();
	list.show();
	return 0;
}