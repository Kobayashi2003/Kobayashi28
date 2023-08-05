#include "leftistHeap.hpp"
#include <iostream>

using namespace std;

int main() {
    LeftistHeap<int> h1;

    LeftistHeap<int> left;
    LeftistHeap<int> mid;
    LeftistHeap<int> right;
    LeftistHeap<int> tmp_l;
    LeftistHeap<int> tmp_r;

    left.insert(12);
    mid.insert(11);
    mid.merge(left);
    tmp_l = mid;

    left.makeEmpty();
    mid.makeEmpty();
    right.makeEmpty();

    left.insert(18);
    mid.insert(17);
    mid.merge(left);
    right = mid;
    tmp_l.merge(right);

    left.makeEmpty();
    mid.makeEmpty();
    right.makeEmpty();

    mid.insert(2);
    left = tmp_l;
    mid.merge(left);
    tmp_l = mid;

    left.makeEmpty();
    mid.makeEmpty();
    right.makeEmpty();

    mid.insert(8);
    left.insert(15);
    mid.merge(left);
    tmp_r = mid;
    
    left.makeEmpty();
    mid.makeEmpty();
    right.makeEmpty();

    mid.insert(5);
    left = tmp_r;
    mid.merge(left);
    tmp_r = mid;

    left.makeEmpty();
    mid.makeEmpty();
    right.makeEmpty();

    mid = tmp_l;
    right = tmp_r;

    mid.merge(right);
    h1 = mid;


    cout << "h1: " << endl;
    h1.show();

    cout << endl;

    LeftistHeap<int> h2;
    
    left.makeEmpty();
    mid.makeEmpty();
    right.makeEmpty();
    tmp_l.makeEmpty();
    tmp_r.makeEmpty();

    left.insert(31);
    mid.insert(18);
    mid.merge(left);
    tmp_l = mid;

    left.makeEmpty();
    mid.makeEmpty();
    right.makeEmpty();

    mid.insert(9);
    left = tmp_l;
    mid.merge(left);
    tmp_l = mid;

    left.makeEmpty();
    mid.makeEmpty();
    right.makeEmpty();

    mid.insert(10);
    right = mid;
    tmp_l.merge(right);

    left.makeEmpty();
    mid.makeEmpty();
    right.makeEmpty();

    mid.insert(4);
    left = tmp_l;
    mid.merge(left);
    tmp_l = mid;

    left.makeEmpty();
    mid.makeEmpty();
    right.makeEmpty();

    mid.insert(11);
    left.insert(21);
    mid.merge(left);
    tmp_r = mid;

    left.makeEmpty();
    mid.makeEmpty();
    right.makeEmpty();

    mid.insert(6);
    left = tmp_r;
    mid.merge(left);
    tmp_r = mid;

    tmp_l.merge(tmp_r);
    h2 = tmp_l;

    cout << "h2: " << endl;
    h2.show();

    cout << endl;

    cout << "h1.merge(h2): " << endl;
    h1.merge(h2);
    h1.show();

    return 0;
}