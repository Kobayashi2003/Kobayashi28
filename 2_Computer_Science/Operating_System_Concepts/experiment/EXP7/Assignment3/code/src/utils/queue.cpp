#include "queue.h"
#include "stdlib.h"

Queue::Queue()
{
}

void Queue::initialize(int *queue, const int length)
{
    this->queue = queue;
    this->length = length;
    this->head = 0;
    this->tail = 0;

    for (int i = 0; i < length; ++i)
    {
        queue[i] = 0;
    }
}

bool Queue::empty() const
{
    return head == tail;
}

bool Queue::full() const
{
    return (tail + 1) % length == head;
}

void Queue::push(const int item)
{
    if (full())
    {
        return;
    }

    queue[tail] = item;
    tail = (tail + 1) % length;
}

int Queue::pop()
{
    if (empty())
    {
        return -1;
    }

    int item = queue[head];
    head = (head + 1) % length;

    return item;
}

int Queue::front() const
{
    if (empty())
    {
        return -1;
    }

    return queue[head];
}

int Queue::back() const
{
    if (empty())
    {
        return -1;
    }

    return queue[(tail - 1 + length) % length];
}

int Queue::size() const
{
    return (tail - head + length) % length;
}

int Queue::capacity() const
{
    return length;
}

void Queue::earse(int item) {
    int i = head;
    while (i != tail) {
        if (queue[i] == item) {
            for (int j = i; j != tail; j = (j + 1) % length) {
                queue[j] = queue[(j + 1) % length];
            }
            tail = (tail - 1 + length) % length;
            return;
        }
        i = (i + 1) % length;
    }
}

void Queue::clear() {
    head = 0;
    tail = 0;
}
