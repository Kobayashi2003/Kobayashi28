#include<iostream>
#include<cmath>
using namespace std;

class Point {
private:
	int _x;         //点的横坐标
	int _y;         //点的纵坐标
public:
	//外部接口
	Point();
	Point(int x, int y);
	int get_x();           //获取横坐标
	int get_y();           //获取纵坐标
	double get_r();        //获取该点到原点的欧式距离
};

class Point_set {
private:
	int    _N;                         //点数组的长度
	Point* _set;                       //点数组指针
	bool* _is_valid;                   //点数组的N个位置是否已经输入，已输入置“1”，未输入置“0”
public:
	//外部接口
	Point_set(int N);
	~Point_set();
	bool  set(int n_index, Point src); //如果“src”与“_set”中的已输入元素互异，将“src”的值赋值给“_set”数组中下标为“n_index”的Point元素，且返回true
									   //                                   否则，返回false。
	int   get_N();                     //获取点集合的长度
	Point get(int n_index);            //获取“_set”数组中下标为“n_index”的Point元素。
	bool  has_point(Point src);        //检查“_set”数组中的已输入值中是否有和“src”相同坐标的点，有返回true，无返回false。
	void  sort();                      //按与原点的欧式距离从大到小进行排序。
	void  show();
};

const int BADNUMBER = (int)(~((~0u)>>1));
Point ENDPOINT(BADNUMBER, BADNUMBER);

Point::Point() {
    _x = 0;
    _y = 0;
}

Point::Point(int x, int y) {
    _x = x;
    _y = y;
}

int Point::get_x() {
    return _x;
}

int Point::get_y() {
    return _y;
}

double Point::get_r() {
    return sqrt(_x * _x + _y * _y);
}

Point_set::Point_set(int N) {
    _N = N;
    _set = new Point[N];
    _is_valid = new bool[N];
    for (int i = 0; i < N; i++) {
        _is_valid[i] = false;
    }
}

Point_set::~Point_set() {
    delete[] _set;
    delete[] _is_valid;
}

Point Point_set::get(int n_index) {
    return _set[n_index];
}

int Point_set::get_N() {
    return _N;
}

bool Point_set::has_point(Point src) {
    for (int i = 0; i < _N && _is_valid[i]; ++i) {
        if (_set[i].get_x() == src.get_x() && _set[i].get_y() == src.get_y()) {
            return true;
        }
    }
    return false;
}

bool Point_set::set(int n_index, Point src) {
    if (src.get_x() == BADNUMBER) {
        _set[n_index] = src;
        _is_valid[n_index] = true;
        return true;
    }

    if (has_point(src)) {
        return false;
    }
    _set[n_index] = src;
    _is_valid[n_index] = true;

    return true;
}

void Point_set::sort() {
    for (int i = 0; i < _N - 1; ++i) {

        if (_set[i].get_x() == BADNUMBER) {
            break;
        }

        for (int j = i + 1; j < _N; ++j) {
            if (_set[i].get_r() < _set[j].get_r()) {
                Point temp = _set[i];
                _set[i] = _set[j];
                _set[j] = temp;
            }
        }
    }
}

void Point_set::show() {
    cout << "{";
    for (int i = 0; i < _N; ++i) {

        if (_set[i].get_x() == BADNUMBER) {
            break;
        }

        cout << "(" << _set[i].get_x() << "," << _set[i].get_y() << ")";

        if (i != _N-1 && _set[i+1].get_x() != BADNUMBER) {
            cout << ",";
        }
    }
    cout << "}" << endl;
}


// void Intersection(Point_set& a, Point_set& b);  //求点集合a与点集合b的交集c，并打印c
// void Union(Point_set& a, Point_set& b);         //求点集合a与点集合b的并集c，并打印c
// void Relative(Point_set& a, Point_set& b);      //求点集合a与点集合b的差集c，并打印c

// //你的代码会从这里插入

void Intersection(Point_set& a, Point_set& b) {
    Point_set c(a.get_N());
    int count = 0;
    for (int i = 0; i < a.get_N(); ++i) {
        if (b.has_point(a.get(i))) {
            c.set(count++, a.get(i));
        }
    }
    if (count != a.get_N()) {
        c.set(count, ENDPOINT);
    }
    c.sort();
    c.show();
}

void Union(Point_set& a, Point_set& b) {
    Point_set c(a.get_N() + b.get_N());
    int count = 0;
    for (int i = 0; i < a.get_N(); ++i) {
        c.set(count++, a.get(i));
    }
    for (int i = 0; i < b.get_N(); ++i) {
        if (!a.has_point(b.get(i))) {
            c.set(count++, b.get(i));
        }
    }
    if (count != a.get_N() + b.get_N()) {
        c.set(count, ENDPOINT);
    }
    c.sort();
    c.show();
}

void Relative(Point_set& a, Point_set& b) {
    Point_set c(a.get_N());
    int count = 0;
    for (int i = 0; i < a.get_N(); ++i) {
        if (!b.has_point(a.get(i))) {
            c.set(count++, a.get(i));
        }
    }
    if (count != a.get_N()) {
        c.set(count, ENDPOINT);
    }
    c.sort();
    c.show();
}

int main() {
	//输入第一个点集合
	int N1;
	cin >> N1;
	Point_set point_set1(N1);
	for (int i = 0; i < N1; i++) {
		int x, y;
		std::cin >> x >> y;
		bool success = point_set1.set(i, Point(x, y));
		if (success != true) return 0;
	}
	point_set1.show();
	//输入第二个点集合
	int N2;
	cin >> N2;
	Point_set point_set2(N2);
	for (int i = 0; i < N2; i++) {
		int x, y;
		std::cin >> x >> y;
		bool success = point_set2.set(i, Point(x, y));
		if (success != true) return 0;
	}
	point_set2.show();
	//集合运算
	Intersection(point_set1, point_set2);
	Union(point_set1, point_set2);
	Relative(point_set1, point_set2);
	return 0;
}
