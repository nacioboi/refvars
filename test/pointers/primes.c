#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <windows.h>

bool is_prime(int num) {
	if (num <= 1) return false;
	for (int i = 2; i * i <= num; ++i) {
		if (num % i == 0) return false;
	}
	return true;
}

void generate_primes(int* ptr, size_t size, int num_primes) {
	int count = 0;
	int candidate = 2;
	while (count < num_primes) {
		if (is_prime(candidate)) {
			if (count * sizeof(int) >= size) {
				fprintf(stderr, "Memory block size is not sufficient.\n");
				return;
			}
			ptr[count] = candidate;
			count++;
		}
		candidate++;
	}
	ptr[count] = -1;  // Null terminator for end of primes
}

int main(int argc, char* argv[]) {
	if (argc != 4) {
		fprintf(stderr, "Usage: %s <memory_address> <size> <num_primes>\n", argv[0]);
		return 1;
	}

	void* memory_address = (void*)strtoull(argv[1], NULL, 0);
	size_t size = (size_t)strtoull(argv[2], NULL, 0);
	int num_primes = atoi(argv[3]);

	if (memory_address == NULL) {
		fprintf(stderr, "Invalid memory address.\n");
		return 1;
	}

	int* ptr = (int*)memory_address;
	printf("Memory address: %p\n", ptr);
	printf("Memory size: %zu bytes\n", size);
	printf("Number of primes to generate: %d\n", num_primes);

	generate_primes(ptr, size, num_primes);

	printf("Primes generated and stored in memory.\n");
	return 0;
}
