#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <time.h>

#define ARRAY_SIZE 1000000 * 128
#define THREAD_NUM 16

typedef struct {
    int thread_id;
    uint32_t start_index;
    uint32_t end_index;
    double* array;
    double partial_sum;
} ThreadData;

void* sum_array(void* arg) {
    ThreadData* data = (ThreadData*)arg;
    for (uint32_t i = data->start_index; i < data->end_index; i++) {
        data->partial_sum += data->array[i];
    }
    return NULL;
}

int main() {

    ThreadData thread_data[THREAD_NUM];
    pthread_t threads[THREAD_NUM];

    double* array = (double*)malloc(ARRAY_SIZE * sizeof(double));
    for (uint32_t i = 0; i < ARRAY_SIZE; i++) {
        array[i] = rand() % 100;
    }

    double total_sum = 0;
    uint32_t elements_per_thread = ARRAY_SIZE / THREAD_NUM;
    for (uint32_t i = 0; i < THREAD_NUM; i++) {
        thread_data[i].thread_id = i;
        thread_data[i].start_index = i * elements_per_thread;
        thread_data[i].end_index = (i == THREAD_NUM - 1) ? ARRAY_SIZE : (i + 1) * elements_per_thread;
        thread_data[i].array = array;
        thread_data[i].partial_sum = 0;
    }

    clock_t start_time = clock();

    for (uint32_t i = 0; i < THREAD_NUM; i++) {
        pthread_create(&threads[i], NULL, sum_array, &thread_data[i]);
    }

    for (uint32_t i = 0; i < THREAD_NUM; i++) {
        pthread_join(threads[i], NULL);
        total_sum += thread_data[i].partial_sum;
    }

    clock_t end_time = clock();

    printf("Total sum: %f\n", total_sum);
    printf("Array size: %d\n", ARRAY_SIZE);
    printf("Number of threads: %d\n", THREAD_NUM);
    printf("Time taken: %f seconds\n", (double)(end_time - start_time) / CLOCKS_PER_SEC);
    FILE* file = fopen("array_sum_results.txt", "a");
    fprintf(file, "Array size: %d\n", ARRAY_SIZE);
    fprintf(file, "Number of threads: %d\n", THREAD_NUM);
    fprintf(file, "Time taken: %f seconds\n\n", (double)(end_time - start_time) / CLOCKS_PER_SEC);
    fclose(file);

    free(array);
    return 0;
}
