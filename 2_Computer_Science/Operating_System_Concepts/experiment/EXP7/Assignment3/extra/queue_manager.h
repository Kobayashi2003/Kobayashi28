#ifndef QUEUE_MANAGER_H
#define QUEUE_MANAGER_H

class QueueManager
{
public:
    int head;
    int tail;
    int length;
    int *queue_pointer; // 32-bit address of the queues
    int *queue_length;  // length of the queues

public:
    void initialize(int *queue_pointer_addr, int *queue_length_addr, const int length);

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

    void expand(int queue_addr, int queue_length);

private:
    QueueManager(const QueueManager &) {}
    void operator=(const QueueManager &) {}
};

#endif
