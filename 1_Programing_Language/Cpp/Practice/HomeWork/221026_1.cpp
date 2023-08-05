#include <cmath>
#include <iostream>
using namespace std;

class Point {
private:
	int _x;         //点的横坐标
	int _y;         //点的纵坐标
public:
	//外部接口：可参考第7次实验第3题
	Point();
	Point(int x, int y);
	int get_x();
	int get_y();
	double get_r();
};

class Point_set {
private:
	int    _N;                         //点数组的长度
	Point* _set;                       //点数组指针
	bool* _is_valid;                   //点数组的N个位置是否已经输入，已输入置“1”，未输入置“0”
public:
	//外部接口：可参考第7次实验第3题
	Point_set(int N);
	Point_set(const Point_set& src);   //复制构造函数一定要定义！！！
	~Point_set();
	bool  set(int n_index, Point src);
	int   get_N();
	Point get(int n_index);
	bool  has_point(Point src);
	void  sort();
	void  show();

	//以上为部分成员函数，同学们根据实际情况还需添加部分函数: 重点参考3.4.2节的“常成员函数”！！！
    int get_N() const;
    Point get(int n_index) const;
    bool has_point(Point src) const;
};

/* Point Function */
Point::Point() = default;

Point::Point(int x, int y):_x(x), _y(y){}

int Point::get_x() { return _x; }

int Point::get_y() { return _y; }

double Point::get_r() { return sqrt(_x*_x + _y*_y); }
/*Point Function End*/


/* Point_set Function */
Point_set::Point_set(int N) : _N(N) {
    _set = new Point[_N];
    _is_valid = new bool[_N];
    for (int i = 0; i < _N; i++) {
        _is_valid[i] = false;
    }
}

Point_set::Point_set(const Point_set& src) {
    _N = src._N;
    // deep clone
    _set = new Point[_N];
    _is_valid = new bool[_N];
    for (int i = 0; i < _N; i++) {
        _set[i] = src._set[i];
        _is_valid[i] = src._is_valid[i];
    }
}

Point_set::~Point_set() {
    delete[] _set;
    delete[] _is_valid;
}

bool Point_set::set(int n_index, Point src) {
    if (n_index < 0 || n_index >= _N || has_point(src)) { return false; }
    _set[n_index] = src;
    _is_valid[n_index] = true;
    return true;
}

int Point_set::get_N() { return _N; }

Point Point_set::get(int n_index) { return _set[n_index]; }

bool Point_set::has_point(Point src) {
    for (int i = 0; i < _N; i++) {
        if (_is_valid[i] && _set[i].get_x() == src.get_x() && _set[i].get_y() == src.get_y()) {
            return true;
        }
    }
    return false;
}

void Point_set::sort() {
    for (int i = 0; i < _N && _is_valid[i]; i++) {
        for (int j = i + 1; j < _N && _is_valid[j]; j++) {
            if (_set[i].get_r() < _set[j].get_r()) {
                Point tmp = _set[i];
                _set[i] = _set[j];
                _set[j] = tmp;
            }
        }
    }
}

void Point_set::show() {
    cout << "{";
    for (int i = 0; i < _N && _is_valid[i]; i++) {
        cout << "(" << _set[i].get_x() << "," << _set[i].get_y() << ")";
        if (i != _N - 1 && _is_valid[i + 1]) {
            cout << ",";
        }
    }
    cout << "}" << endl;
}

int Point_set::get_N() const { return _N; }

Point Point_set::get(int n_index) const { return _set[n_index]; }

bool Point_set::has_point(Point src) const {
    for (int i = 0; i < _N; i++) {
        if (_is_valid[i] && _set[i].get_x() == src.get_x() && _set[i].get_y() == src.get_y()) {
            return true;
        }
    }
    return false;
}

/* Point_set Function End */

Point_set sysmmetric_difference(const Point_set & Ps1, const Point_set & Ps2) {
    Point_set new_Ps(Ps1.get_N() + Ps2.get_N());
    int cont = 0;
    for (int i = 0; i < Ps1.get_N(); i++) {
        if (!Ps2.has_point(Ps1.get(i))) {
            new_Ps.set(cont, Ps1.get(i));
            cont++;
        }
    }

    for (int i = 0; i < Ps2.get_N(); i++) {
        if (!Ps1.has_point(Ps2.get(i))) {
            new_Ps.set(cont, Ps2.get(i));
            cont++;
        }
    }

    return new_Ps;
}

Point_set Union(const Point_set &a, const Point_set &b)
{
    int N = a.get_N();
    bool *is_union = new bool[b.get_N()]; //判断b中的元素是否存在于a中
    for (int i = 0; i < b.get_N(); i++)
    {
        if (a.has_point(b.get(i)) == true)
        { // b中的元素存在于a中,认为b的当前元素无需再纳入并集
            is_union[i] = false;
        }
        else
        { // b中的元素不存在于a中,认为b的当前元素“可以”再纳入并集
            is_union[i] = true;
            N++;
        }
    }
    Point_set c(N);
    for (int i = 0; i < a.get_N(); i++)
    { // a和b的并集必然包含a的全部元素，存入c中
        c.set(i, a.get(i));
    }
    int j = 0;
    for (int i = 0; i < b.get_N(); i++)
    { //将b中可以纳入并集的元素依次存入c中
        if (is_union[i] == true)
        {
            c.set(j + a.get_N(), b.get(i));
            j++;
        }
    }
    return c;
}

int main()
{
    //输入第一个点集合
    int N1;
    cin >> N1;
    Point_set point_set1(N1);
    for (int i = 0; i < N1; i++)
    {
        int x, y;
        std::cin >> x >> y;
        bool success = point_set1.set(i, Point(x, y));
        if (success != true)
            return 0;
    }
    //输入第二个点集合
    int N2;
    cin >> N2;
    Point_set point_set2(N2);
    for (int i = 0; i < N2; i++)
    {
        int x, y;
        std::cin >> x >> y;
        bool success = point_set2.set(i, Point(x, y));
        if (success != true)
            return 0;
    }
    //集合运算
    Point_set point_set3 = Union(point_set1, point_set2); //求并集，并打印
    Point_set point_set4 =
        sysmmetric_difference(point_set1, point_set2); //求对称差集，并打印
    //按输入顺序打印a和b
    point_set1.show();
    point_set2.show();
    //按离原点欧式距离从大到小打印a和b
    point_set3.sort();
    point_set3.show();
    point_set4.sort();
    point_set4.show();

    return 0;
}