#include "Point.h"

Point::Point(int r, int c) {
    row = r;
    col = c;
}

Point::Point() : Point(0, 0) {}