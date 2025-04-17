#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <math.h>
#include <time.h>

// Global variables for sharing data between threads
double discriminant = 0;
double coefficients[3] = {0}; // a, b, c
double roots[4] = {0}; // x1_real, x1_imag, x2_real, x2_imag

// Synchronization variables
pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER;
pthread_cond_t discriminant_calculated = PTHREAD_COND_INITIALIZER;
pthread_cond_t roots_calculated = PTHREAD_COND_INITIALIZER;
int discriminant_done = 0;
int roots_done = 0;

// Thread parameter structure
typedef struct {
    int root_index; // 0 for discriminant, 1 for x1, 2 for x2
} ThreadArgs;

// Thread function to calculate the discriminant
void* calculate_discriminant(void* arg) {
    // Calculate discriminant = b² - 4ac
    double a = coefficients[0];
    double b = coefficients[1];
    double c = coefficients[2];
    
    discriminant = b * b - 4 * a * c;
    
    // Signal that discriminant is calculated
    pthread_mutex_lock(&mutex);
    discriminant_done = 1;
    pthread_cond_broadcast(&discriminant_calculated);
    pthread_mutex_unlock(&mutex);
    
    return NULL;
}

// Thread function to calculate one of the roots
void* calculate_root(void* arg) {
    ThreadArgs* args = (ThreadArgs*)arg;
    int root_index = args->root_index;
    
    // Wait for discriminant to be calculated
    pthread_mutex_lock(&mutex);
    while (!discriminant_done) {
        pthread_cond_wait(&discriminant_calculated, &mutex);
    }
    pthread_mutex_unlock(&mutex);
    
    // Get coefficients
    double a = coefficients[0];
    double b = coefficients[1];
    
    // Calculate root based on discriminant
    if (discriminant < 0) {
        // Complex roots (represented as real and imaginary parts)
        double realPart = -b / (2 * a);
        double imagPart = sqrt(-discriminant) / (2 * a);
        
        if (root_index == 1) {
            // First root: realPart + imagPart*i
            roots[0] = realPart;
            roots[1] = imagPart;
        } else {
            // Second root: realPart - imagPart*i
            roots[2] = realPart;
            roots[3] = -imagPart;
        }
    } else {
        // Real roots
        if (root_index == 1) {
            // First root: (-b + sqrt(discriminant)) / (2*a)
            roots[0] = (-b + sqrt(discriminant)) / (2 * a);
            roots[1] = 0; // Imaginary part is zero
        } else {
            // Second root: (-b - sqrt(discriminant)) / (2*a)
            roots[2] = (-b - sqrt(discriminant)) / (2 * a);
            roots[3] = 0; // Imaginary part is zero
        }
    }
    
    // Signal that a root is calculated
    pthread_mutex_lock(&mutex);
    roots_done++;
    if (roots_done == 2) {
        pthread_cond_signal(&roots_calculated);
    }
    pthread_mutex_unlock(&mutex);
    
    return NULL;
}

void quadratic_equation(double a, double b, double c) {

    // Prepare thread arguments
    ThreadArgs args1 = {1}; // For x1
    ThreadArgs args2 = {2}; // For x2
    
    // Create threads
    pthread_t disc_thread, root1_thread, root2_thread;

    // Launch threads
    pthread_create(&disc_thread, NULL, calculate_discriminant, NULL);
    pthread_create(&root1_thread, NULL, calculate_root, &args1);
    pthread_create(&root2_thread, NULL, calculate_root, &args2);
    
    // Wait for all calculations to complete
    pthread_mutex_lock(&mutex);
    while (roots_done < 2) {
        pthread_cond_wait(&roots_calculated, &mutex);
    }
    pthread_mutex_unlock(&mutex);

    // Wait for threads to finish
    pthread_join(disc_thread, NULL);
    pthread_join(root1_thread, NULL);
    pthread_join(root2_thread, NULL);
}

int main(int argc, char* argv[]) {

    int test_num = 1;
    if (argc > 1) {
        test_num = atoi(argv[1]);
        if (test_num <= 0) {
            printf("Invalid test number\n");
            return 1;
        }
    }

    // Input parameters a, b, c
    printf("Please enter the coefficients a, b, c of the quadratic equation (range [-100, 100]): ");
    scanf("%lf %lf %lf", &coefficients[0], &coefficients[1], &coefficients[2]);
    
    double a = coefficients[0];
    double b = coefficients[1];
    double c = coefficients[2];
    
    // Check parameter range
    if (a < -100 || a > 100 || b < -100 || b > 100 || c < -100 || c > 100) {
        printf("Input coefficients out of range [-100, 100]\n");
        return 1;
    }
    
    // Check if it's a quadratic equation
    if (fabs(a) < 1e-10) {
        printf("Coefficient a is close to zero, not a quadratic equation\n");
        return 1;
    }
    
    // Start timing
    clock_t start = clock();
    
    for (int i = 0; i < test_num; i++) {
        quadratic_equation(a, b, c);
    }

    // End timing
    clock_t end = clock();
    double time_spent = (double)(end - start) / CLOCKS_PER_SEC;
    
    // Output results
    printf("\nSolving equation: %.2lfx^2 + %.2lfx + %.2lf = 0\n", a, b, c);
    printf("Discriminant: %.2lf\n", discriminant);
    
    if (fabs(roots[1]) < 1e-10 && fabs(roots[3]) < 1e-10) {
        // Real roots
        printf("x1 = %.2lf\n", roots[0]);
        printf("x2 = %.2lf\n", roots[2]);
    } else {
        // Complex roots
        printf("x1 = %.2lf + %.2lfi\n", roots[0], roots[1]);
        printf("x2 = %.2lf + %.2lfi\n", roots[2], roots[3]);
    }
    
    printf("Time spent: %.3lf seconds\n", time_spent);
    
    // Destroy mutex and condition variable
    pthread_mutex_destroy(&mutex);
    pthread_cond_destroy(&discriminant_calculated);
    pthread_cond_destroy(&roots_calculated);
    
    return 0;
} 