#include<iostream>
#include<cstdlib>
#include<string>
#include<thread>

#define NUM_THREADS 3

using namespace std;

struct Data {
    int age;
    string name;
};

void *showData(void *d) {
    Data *data = (Data *)d;
    cout << "name:" << data->name << endl << "age:" << data->age << endl;
    return nullptr;
}

int main() {
    int rc;
    pthread_t threads[NUM_THREADS];
    pthread_attr_t attr;
    void *status;

    // 初始化并设置线程的可连接性
    pthread_attr_init(&attr);
    pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);

    Data data[3];
    data[0].age = 18; data[0].name = "xiaoming";
    data[1].age = 19; data[1].name = "xiaowang";
    data[2].age = 16; data[2].name = "xiaohong";

    for (int  i = 0; i < NUM_THREADS; ++i) {
        rc = pthread_create(&threads[i], nullptr, showData, (void *)(&data[i]));
        if (rc != 0) {
            cout << "erro code:" << rc << endl;
            exit(-1);
        }
    }

    pthread_attr_destroy(&attr);
    for (int i = 0; i < NUM_THREADS; ++i) {
        rc = pthread_join(threads[i], &status);
        if (rc) {
            cout << "unable to join," << rc << endl;
            exit(-1);
        }
        cout << "   exiting with status: " << status << endl;
    }
    pthread_exit(nullptr);
}