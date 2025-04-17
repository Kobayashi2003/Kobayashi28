#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include <time.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

int total_points;
int points_in_circle = 0;
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;

typedef struct {
    int thread_id;
    int num_threads;
    unsigned int seed;
} ThreadArgs;

unsigned int rand_r(unsigned int* seed) {
    unsigned int next = *seed;
    next = next * 1103515245 + 12345;
    *seed = next;
    return next % ((unsigned int)RAND_MAX + 1);
}

void* monte_carlo_worker(void* arg) {
    ThreadArgs* args = (ThreadArgs*)arg;
    int local_points_in_circle = 0;
    unsigned int seed = args->seed;
    
    int points_per_thread = total_points / args->num_threads;
    int points = (args->thread_id == args->num_threads - 1) ? 
                 points_per_thread + (total_points % args->num_threads) : 
                 points_per_thread;
    
    for (int i = 0; i < points; i++) {
        double x = (double)rand_r(&seed) / RAND_MAX;
        double y = (double)rand_r(&seed) / RAND_MAX;
        
        if (x * x + y * y <= 1.0) {
            local_points_in_circle++;
        }
    }
    
    pthread_mutex_lock(&mutex);
    points_in_circle += local_points_in_circle;
    pthread_mutex_unlock(&mutex);
    
    return NULL;
}

int main() {
    printf("Please enter the number of random points to generate (range [1024, 65536]): ");
    scanf("%d", &total_points);
    
    if (total_points < 1024 || total_points > 65536) {
        printf("Number of points must be in range [1024, 65536]\n");
        return 1;
    }
    
    int num_threads;
    printf("Please enter the number of threads: ");
    scanf("%d", &num_threads);
    
    if (num_threads <= 0) {
        printf("Thread count must be greater than 0\n");
        return 1;
    }
    
    if (num_threads > total_points) {
        printf("Thread count cannot exceed number of points, adjusted to %d\n", total_points);
        num_threads = total_points;
    }
    
    pthread_t* threads = (pthread_t*)malloc(num_threads * sizeof(pthread_t));
    ThreadArgs* thread_args = (ThreadArgs*)malloc(num_threads * sizeof(ThreadArgs));
    
    if (!threads || !thread_args) {
        printf("Memory allocation failed\n");
        free(threads);
        free(thread_args);
        return 1;
    }
    
    srand(time(NULL));
    
    struct timeval start_time, end_time;
    mingw_gettimeofday(&start_time, NULL);
    
    for (int i = 0; i < num_threads; i++) {
        thread_args[i].thread_id = i;
        thread_args[i].num_threads = num_threads;
        thread_args[i].seed = rand() + i;
        
        if (pthread_create(&threads[i], NULL, monte_carlo_worker, &thread_args[i]) != 0) {
            printf("Failed to create thread %d\n", i);
            free(threads);
            free(thread_args);
            return 1;
        }
    }
    
    for (int i = 0; i < num_threads; i++) {
        pthread_join(threads[i], NULL);
    }
    
    mingw_gettimeofday(&end_time, NULL);
    double time_spent = (end_time.tv_sec - start_time.tv_sec) + 
                      (end_time.tv_usec - start_time.tv_usec) / 1e6;
    
    double pi_approximation = 4.0 * points_in_circle / total_points;
    
    printf("\nResults:\n");
    printf("Total points: %d\n", total_points);
    printf("Points inside circle: %d\n", points_in_circle);
    printf("Pi approximation: %.10lf\n", pi_approximation);
    printf("Time spent: %.6lf seconds\n", time_spent);
    printf("Number of threads: %d\n", num_threads);
    printf("Difference from standard Pi: %.10lf\n", fabs(pi_approximation - M_PI));
    
    free(threads);
    free(thread_args);
    pthread_mutex_destroy(&mutex);
    
    return 0;
} 