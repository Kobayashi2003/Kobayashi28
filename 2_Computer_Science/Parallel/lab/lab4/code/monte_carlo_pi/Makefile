CC = gcc
CFLAGS = -Wall -g -pthread -lm

all: monte_carlo_pi

# Compilation rules
monte_carlo_pi: monte_carlo_pi.c
	$(CC) $(CFLAGS) -o monte_carlo_pi.exe monte_carlo_pi.c

# Test rule
test_monte_carlo: monte_carlo_pi
	@echo "========== Testing Monte Carlo Pi Estimation =========="

	@echo "===== Test with 10000 points and 1 threads ====="
	@(echo 10000 && echo 1) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 10000 points and 4 threads ====="
	@(echo 10000 && echo 4) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 10000 points and 8 threads ====="
	@(echo 10000 && echo 8) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 10000 points and 16 threads ====="
	@(echo 10000 && echo 16) | ./monte_carlo_pi.exe
	@echo ""


	@echo "===== Test with 20000 points and 1 threads ====="
	@(echo 20000 && echo 1) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 20000 points and 4 threads ====="
	@(echo 20000 && echo 4) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 20000 points and 8 threads ====="
	@(echo 20000 && echo 8) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 20000 points and 16 threads ====="
	@(echo 20000 && echo 16) | ./monte_carlo_pi.exe
	@echo ""


	@echo "===== Test with 40000 points and 1 threads ====="
	@(echo 40000 && echo 1) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 40000 points and 4 threads ====="
	@(echo 40000 && echo 4) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 40000 points and 8 threads ====="
	@(echo 40000 && echo 8) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 40000 points and 16 threads ====="
	@(echo 40000 && echo 16) | ./monte_carlo_pi.exe
	@echo ""


	@echo "===== Test with 65536 points and 1 threads ====="
	@(echo 65536 && echo 1) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 65536 points and 4 threads ====="
	@(echo 65536 && echo 4) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 65536 points and 8 threads ====="
	@(echo 65536 && echo 8) | ./monte_carlo_pi.exe
	@echo ""

	@echo "===== Test with 65536 points and 16 threads ====="
	@(echo 65536 && echo 16) | ./monte_carlo_pi.exe
	@echo ""

clean:
	rm -f *.exe

.PHONY: all clean test_monte_carlo
