#include <iostream>
#include <vector>
#include <stack>
#include <queue>

using namespace std;

template <typename Comparable>
void merge(vector<Comparable> & v, vector<Comparable> & tmpArray, int leftPos, int rightPos, int rightEnd) {

    int leftEnd = rightPos - 1;
    int tmpPos = leftPos;
    int numElements = rightEnd - leftPos + 1;

    while (leftPos <= leftEnd && rightPos <= rightEnd) {
        if (v[leftPos] < v[rightPos]) {
            tmpArray[tmpPos++] = v[leftPos++];
        } else {
            tmpArray[tmpPos++] = v[rightPos++];
        }
    }

    while (leftPos <= leftEnd) {
        tmpArray[tmpPos++] = v[leftPos++];
    }

    while (rightPos <= rightEnd) {
        tmpArray[tmpPos++] = v[rightPos++];
    }

    for (int i = 0; i < numElements; ++i, --rightEnd) {
        v[rightEnd] = tmpArray[rightEnd];
    }
}

template <typename Comparable>
void mergeSort(vector<Comparable> & v) {

    vector<Comparable> tmpArray(v.size());

    queue<int> start_q, end_q;
    stack<int> start_s, end_s;
    int start = 0, end = v.size() - 1;
    start_q.push(start);
    end_q.push(end);

    while (!start_q.empty() && !end_q.empty()) {
        start = start_q.front();
        end = end_q.front();
        start_q.pop();
        end_q.pop();
        start_s.push(start);
        end_s.push(end);
        if (start < end) {
            int mid = (start + end) / 2;
            start_q.push(start);
            end_q.push(mid);
            start_q.push(mid + 1);
            end_q.push(end);
        }
    }

    while (!start_s.empty() && !end_s.empty()) {
        start = start_s.top();
        end = end_s.top();
        start_s.pop();
        end_s.pop();
        if (start < end) {
            int mid = (start + end) / 2;
            merge(v, tmpArray, start, mid + 1, end);
        }   
    }
}

int main() {

    vector<int> v = { 3, 1, 4, 5, 9, 2, 6, 8, 7 };
    mergeSort(v);

    for (auto & i : v) {
        cout << i << " ";
    }


    return 0;
}