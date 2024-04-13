#include<iostream>

#include<pthread.h>

#define NUM_THREADS 5

using namespace std;

void * sayHello(void *args) {
    cout << "Hello World!" << endl;
    return nullptr;
}

int main() {
    pthread_t tid[NUM_THREADS];
    for (int i = 0; i < NUM_THREADS; i++) {
        int ret = pthread_create(&tid[i], nullptr, sayHello, nullptr);
        if (ret != 0) {
            cout << "Error: pthread_create " <<  "error code:" << ret << endl;
        }
    }
    pthread_exit(nullptr);
}