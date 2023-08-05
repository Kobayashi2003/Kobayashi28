#include <iostream>
#include <string>
#include <limits>
#include <iomanip>
#include <vector>

using ULL = unsigned long long int;

using Vstring = std::vector<std::string>;

const bool ERROR = false;

/* Class */

class Time {
private:
    enum {year=0, month=1, day=2, hour=3, minute=4};
    ULL *_time;
public:
    Time();
    Time(std::string input);
    Time(const Time &other); // copy constructor
    ~Time();

    bool check() const;
    void show() const;

    static bool check(Time &t);
    static bool compare(const Time & a, const Time & b);

    bool operator=(const Time & other);
};

class Task {
private:
    Time _time;
    std::string _content;
public:
    Task();
    Task(Time time, std::string content);
    Task(Task & other); // copy constructor
    ~Task();

    bool setTask(Time time, std::string content);

    Time getTime() const;
    std::string getContent() const;
    void show() const;

    bool operator=(const Task & other);
};

class TaskList {
private:
    Task *_tasks;
    ULL _capacity;
    ULL _size;

protected:
    void expand();
    void sort_by_time();

public:
    TaskList();
    TaskList(ULL capacity);
    ~TaskList();

    bool addTask(Task & task);

    Task getTask(ULL index) const;
    ULL getSize() const;
    void show() const;
};

/* Class End */


/* Class Function */

/* Time Class Function Definition */
Time::Time() {
    _time = new ULL[5];
    for (int i = 0; i < 5; ++i) {
        _time[i] = 0;
    }
}

Time::Time(std::string input) {
    _time = new ULL[5] {0};
    for (int flg=0, i=0; i < (int)input.length(); ++i) {
        if (input[i] >= '0' && input[i] <= '9') {
            _time[flg] = _time[flg]*10 + input[i] - '0';
        }
        else {
            flg += 1;
        }
    }
}

Time::Time(const Time & other) {
    _time = new ULL[5];
    for (int i = 0; i < 5; ++i) {
        _time[i] = other._time[i];
    }
}

Time::~Time() { delete [] _time; }

bool Time::check() const {
    ULL day_standard[13] = {0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31};

    // check the year
    if (_time[year] < 0) {
        return false;
    }

    if ((_time[year] % 4 == 0 && _time[year] % 100 != 0) ||
        (_time[year] % 400 == 0))
    {
        day_standard[2] += 1;
    }

    // cheak the month
    if (_time[month] < 0 || _time[month] > 12) {
        return false;
    } else { // then check the days in the month
        if (_time[day] < 0 || _time[day] > day_standard[_time[month]]) {
            return false;
        }
    }

    // finally check the hour and minute
    if (_time[hour] < 0 || _time[hour] > 24) {
        return false;
    }
    if (_time[minute] < 0 || _time[minute] > 60) {
        return false;
    }

    return true;
}

void Time::show() const {
    std::cout << _time[year] << "/"
              << _time[month] << "/"
              << _time[day] << " "
              << std::setw(2) << std::setfill('0') << _time[hour] << ":"
              << std::setw(2) << std::setfill('0') << _time[minute]
              << std::endl;
}

bool Time::check(Time & t) {
    return t.check();
}

bool Time::compare(const Time& t1, const Time& t2) {
    for (int i = 0; i < 5; i += 1) {
        if (t1._time[i] < t2._time[i]) {
            return true;
        } else if (t1._time[i] == t2._time[i]) {
            continue;
        }
        break;
    }
    return false;
}

bool Time::operator=(const Time & other) {
    for (int i = 0; i < 5; ++i) {
        _time[i] = other._time[i];
    }
    return true;
}
/* Time Class Function End */


/* Task Class Function Definition */
Task::Task() {
    _time = Time();
    _content = "";
}

Task::Task(Time time, std::string content) {
    if (!time.check()) {
        if (ERROR) {
            std::cout << "Error: Time is not valid." << std::endl;
        }
        _time = Time();
        _content = "";
        return;
    }
    _time = time;
    _content = content;
}

Task::Task(Task & other) {
    _time = other._time;
    _content = other._content;
}

Task::~Task() = default;

bool Task::setTask(Time time, std::string content) {
    if (!time.check()) {
        if (ERROR) {
            std::cout << "Error: Time is not valid." << std::endl;
        }
        return false;
    }
    delete &_time;
    _time = time;
    _content = content;
    return true;
}

Time Task::getTime() const { return _time; }

std::string Task::getContent() const { return _content; }

void Task::show() const {
    _time.show();
    std::cout << _content << std::endl;
}

bool Task::operator=(const Task & other) {
    _time = other._time;
    _content = other._content;
    return true;
}
/* Task Class Function End */


/* TaskList Class Function Definition */
TaskList::TaskList() : _tasks(nullptr), _capacity(0), _size(0) {}

TaskList::TaskList(ULL capacity) : _capacity(capacity) {
    _tasks = new Task[capacity];
    _size = 0;
}

TaskList::~TaskList() { delete [] _tasks; }

void TaskList::expand() {
    Task *new_tasks = new Task[_capacity*2];
    for (ULL i = 0; i < _size; ++i) {
        new_tasks[i] = _tasks[i];
    }
    delete [] _tasks;
    _tasks = new_tasks;
    _capacity *= 2;
}

void TaskList::sort_by_time() {
    for (ULL i = 0; i < _size-1; ++i) {
        for (ULL j = i+1; j < _size; ++j) {
            if (!Time::compare(_tasks[i].getTime(), _tasks[j].getTime())) {
                Task tmp = _tasks[i];
                _tasks[i] = _tasks[j];
                _tasks[j] = tmp;
            }
        }
    }
}

bool TaskList::addTask(Task & task) {
    if (_size == _capacity) {
        if (ERROR) {
            std::cout << "Error: TaskList is full." << std::endl;
            std::cout << "Do you want to expand the list? (y/n)" << std::endl;
            char ch; std::cin >> ch;
            if (ch == 'y') {
                expand();
            } else {
                return false;
            }
        }
        return false;
    }

    if (task.getContent() == "") {
        if (ERROR) {
            std::cout << "Error: Task content is empty." << std::endl;
        }
        return false;
    }

    _tasks[_size] = task;
    _size += 1;

    sort_by_time();
    return true;
}

Task TaskList::getTask(ULL index) const {
    if (index >= _size || index < 0) {
        if (ERROR) {
            std::cout << "Error: Index out of range." << std::endl;
        }
        Task _BLANK_TASK;
        return _BLANK_TASK;
    } else if (_size == 0) {
        if (ERROR) {
            std::cout << "Error: TaskList is empty." << std::endl;
        }
        Task _BLANK_TASK;
        return _BLANK_TASK;
    }
    return _tasks[index];
}

ULL TaskList::getSize() const { return _size; }

void TaskList::show() const {
    for (ULL i = 0; i < _size; ++i) {
        _tasks[i].show();
    }
}
/* TaskList Class Function End*/

/* Class Function */

/* Tools */
Vstring & process_input(std::string input) {
    Vstring *result = new Vstring();
    std::string time = "", content = "";
    for (ULL i = 0; i < input.length(); ++i) {
        if ((input[i] >= '0' && input[i] <= '9') || input[i] == ' ' || input[i] == ':' || input[i] == '/') {
            time += input[i];
        } else {
            content = input.substr(i);
            break;
        }
    }
    result->push_back(time); result->push_back(content);
    return *result;
}
/* Tools End */

int main() {
    int N; std::cin >> N;
    TaskList task_list(N);
    std::cin.get();
    while(N--) {
        std::string input; std::getline(std::cin, input);
        Vstring &tmp = process_input(input);

        Time time(tmp[0]); Task task(time, tmp[1]); task_list.addTask(task);
    }
    task_list.show();
    return 0;
}