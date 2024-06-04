#ifndef QUEUE_H
#define QUEUE_H

#include "os_type.h"

class Queue {
public:
    int head;
    int tail;
    int length;
    int *queue;
public:
    Queue();
    void initialize(int *queue, const int length);
    bool empty() const;
    bool full() const;
    void push(const int item);
    int pop();
    int front() const;
    int back() const;
    int size() const;
    int capacity() const;

    void earse(const int item);
    void clear();
private:
    Queue(const Queue &) {}
    void operator=(const Queue &) {}
};

#endif