#include <iostream>
#include <queue>
#include <random>

using namespace std;

enum EventType { ARRIVAL, DEPARTURE };

struct Event {

    int time;
    EventType type;

    Event(int time, EventType type) : time(time), type(type) {}

    bool operator<(const Event& rhs) const {
        return time > rhs.time;
    }
};

class Solution {

    const int tellers = 5;
    int customers_num;
    queue<Event> customers;
    queue<int> require_time;

public:

    Solution(int customers_num) : customers_num(customers_num) {
        random_device rd;
        mt19937 gen(rd());
        uniform_int_distribution<> dis(1, 10);

        for (int i = 0; i < customers_num; ++i) {
            customers.push(Event(dis(gen), ARRIVAL));
        }

        for (int i = 0; i < customers_num; ++i) {
            require_time.push(dis(gen));
        }
    }


    double bank_simulation() {
        double total_wait_time = .0;
        int tellers_available = tellers;

        priority_queue<Event> events;
        queue<Event> waiting_customers;
        queue<int> waiting_customers_require_time;

        while (!customers.empty()) {
            events.push(customers.front());
            customers.pop();
        }

        while (!events.empty()) {
            Event e = events.top();
            events.pop();
            double current_time = e.time;

            if (e.type == ARRIVAL) {
                if (tellers_available > 0) {
                    --tellers_available;
                    events.push(Event(current_time + require_time.front(), DEPARTURE));
                    require_time.pop();
                } else {
                    waiting_customers.push(e);
                    waiting_customers_require_time.push(require_time.front());
                }
            } else {
                if (!waiting_customers.empty()) {
                    Event next_customer = waiting_customers.front();
                    waiting_customers.pop();
                    total_wait_time += current_time - next_customer.time;
                    events.push(Event(current_time + waiting_customers_require_time.front(), DEPARTURE));
                    waiting_customers_require_time.pop();
                } else {
                    ++tellers_available;
                }
            }

        }
        return total_wait_time / customers_num;
    }
};

int main() {

    Solution s(100);
    cout << s.bank_simulation() << endl;

    return 0;
}