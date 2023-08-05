#include <iostream>
#include <vector>
#include <limits>
#include <algorithm>

using namespace std;

struct Point {
    double x;
    double y;
    Point(double x = 0, double y = 0) : x(x), y(y) {}

    // bool operator < (const Point & rhs) const {
    //     if (x != rhs.x)
    //         return x < rhs.x;
    //     else
    //         return y < rhs.y;
    // }

    bool operator == (const Point & rhs) const {
        return x == rhs.x && y == rhs.y;
    }
};

class Line {
private:
    Point p1;
    Point p2;
    double slope;
    double intercept; // when slope is not infinite, use y intercept, otherwise use x intercept
public:
    Line(const Point & p1, const Point & p2) : p1(p1), p2(p2) {
        slope = computeSlope();
        if (slope == numeric_limits<double>::max())
            intercept = p1.x;
        else
            intercept = p1.y - slope * p1.x;
    }  

    double computeSlope() const {
        if (abs(p2.x - p1.x) < numeric_limits<double>::epsilon())
            return numeric_limits<double>::max();
        else
            return (p2.y - p1.y) / (p2.x - p1.x);
    }

    bool operator < (const Line & rhs) const {
        if (abs(slope - rhs.slope) > numeric_limits<double>::epsilon())
            return slope < rhs.slope;
        else
            return intercept < rhs.intercept;
    }

    double getSlope() const { return slope; }
    double getIntercept() const { return intercept; }
    Point getP1() const { return p1; }
    Point getP2() const { return p2; }
};

void printPoints(vector<Point> collinear) {
    vector<Point>::iterator it;
    int count = 0;
    it = unique(collinear.begin(), collinear.end());
    for (auto itr = collinear.begin(); itr != it; ++itr)
        count++;
    if (count > 3)
        for (auto itr = collinear.begin(); itr != it; ++itr)
            cout << "(" << itr->x << ", " << itr->y << ") ";  
}

int main() {

    vector<Point> points;
    vector<Line> lines;
    vector<Point> collinear;

    int numPoints;
    cin >> numPoints;

    points.resize(numPoints);
    for (int i = 0; i < numPoints; ++i)
        cin >> points[i].x >> points[i].y;
    
    for (int i = 0; i < numPoints; ++i) {
        for (int j = i + 1; j < numPoints; ++j) {
            Line line(points[i], points[j]);
            lines.push_back(line);
        }
    } 
    sort(lines.begin(), lines.end());
    for (int i = 0; i < lines.size(); ++i) {
        if (i == 0 || lines[i].getSlope() != lines[i - 1].getSlope() || lines[i].getIntercept() != lines[i - 1].getIntercept()) {
            if (collinear.size() > 3) {
                printPoints(collinear);
                cout << endl;
            }
            collinear.clear();
        }
        collinear.push_back(lines[i].getP1());
        collinear.push_back(lines[i].getP2());
    }

    return 0;
}