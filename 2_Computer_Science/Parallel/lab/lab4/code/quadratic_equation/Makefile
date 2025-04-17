CC = gcc
CFLAGS = -Wall -g -pthread -lm

all: quadratic_equation_3threads quadratic_equation_sequential

# Compilation rules
quadratic_equation_3threads: quadratic_equation_3threads.c
	$(CC) $(CFLAGS) -o quadratic_equation_3threads.exe quadratic_equation_3threads.c

quadratic_equation_sequential: quadratic_equation_sequential.c
	$(CC) $(CFLAGS) -o quadratic_equation_sequential.exe quadratic_equation_sequential.c -lm

# Test rule with adjustable loop count
# Usage: make test_equation LOOPS=100000
LOOPS ?= 1000000

test_equation: quadratic_equation_3threads quadratic_equation_sequential
	@echo "========== Testing Multiple Cases (Loop $(LOOPS) times) =========="
	
	@echo "\n===== Test Case 1: a=1, b=-3, c=2 ====="
	@echo "\n========== Sequential =========="
	@echo "1 -3 2" | ./quadratic_equation_sequential.exe $(LOOPS)
	@echo "\n========== Parallel =========="
	@echo "1 -3 2" | ./quadratic_equation_3threads.exe $(LOOPS)
	
	@echo "\n===== Test Case 2: a=2, b=4, c=2 ====="
	@echo "\n========== Sequential =========="
	@echo "2 4 2" | ./quadratic_equation_sequential.exe $(LOOPS)
	@echo "\n========== Parallel =========="
	@echo "2 4 2" | ./quadratic_equation_3threads.exe $(LOOPS)
	
	@echo "\n===== Test Case 3: a=1, b=2, c=5 (Complex Roots) ====="
	@echo "\n========== Sequential =========="
	@echo "1 2 5" | ./quadratic_equation_sequential.exe $(LOOPS)
	@echo "\n========== Parallel =========="
	@echo "1 2 5" | ./quadratic_equation_3threads.exe $(LOOPS)

clean:
	rm -f *.exe

.PHONY: all clean test_equation 