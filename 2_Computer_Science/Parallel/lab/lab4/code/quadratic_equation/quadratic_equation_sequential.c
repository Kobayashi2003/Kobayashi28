#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

// Global variables
double discriminant = 0;
double roots[4] = {0}; // x1_real, x1_imag, x2_real, x2_imag

void quadratic_equation(double a, double b, double c) {
    // Sequential calculation
    
    // Step 1: Calculate discriminant
    discriminant = b * b - 4 * a * c;
    
    // Step 2 & 3: Calculate both roots
    if (discriminant < 0) {
        // Complex roots (represented as real and imaginary parts)
        double realPart = -b / (2 * a);
        double imagPart = sqrt(-discriminant) / (2 * a);
        
        // First root: realPart + imagPart*i
        roots[0] = realPart;
        roots[1] = imagPart;
        
        // Second root: realPart - imagPart*i
        roots[2] = realPart;
        roots[3] = -imagPart;
    } else {
        // Real roots
        // First root: (-b + sqrt(discriminant)) / (2*a)
        roots[0] = (-b + sqrt(discriminant)) / (2 * a);
        roots[1] = 0; // Imaginary part is zero
        
        // Second root: (-b - sqrt(discriminant)) / (2*a)
        roots[2] = (-b - sqrt(discriminant)) / (2 * a);
        roots[3] = 0; // Imaginary part is zero
    }
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
    double a, b, c;
    printf("Please enter the coefficients a, b, c of the quadratic equation (range [-100, 100]): ");
    scanf("%lf %lf %lf", &a, &b, &c);
    
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
    
    return 0;
}