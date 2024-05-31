#include <stdlib.h>
#include <string.h>
#include <stdio.h>



typedef char bool;

#define ERR_FAILED_ALLOC 1
#define ERR_NULL_PTR 2
#define SUCCESS 0



#ifdef _WIN32
#define DECLARE_EXPORT __declspec(dllexport)
#else
#define DECLARE_EXPORT __attribute__((visibility("default")))
#endif



DECLARE_EXPORT int safe_memory_access(bool b_debug_, size_t size_, void (*callback_)(void* ptr_)) {
	void* ptr = malloc(size_);
	if (!ptr) {
		return ERR_FAILED_ALLOC;
	}
	if (b_debug_) {
		fprintf(stdout, "`memlib.c`: Allocated memory at %p...\n", ptr);
	}
	callback_(ptr);
	free(ptr);
	if (b_debug_) {
		fprintf(stdout, "`memlib.c`: Freed memory at %p...\n", ptr);
	}
	return SUCCESS;
}

DECLARE_EXPORT int write(bool b_debug_, void* ptr_, const char* data_, size_t size_) {
	if (!ptr_) {
		return ERR_NULL_PTR;
	}
	if (b_debug_) {
		fprintf(stdout, "`memlib.c`: Writing %zd bytes to %p...\n", size_, ptr_);
	}
	memcpy(ptr_, data_, size_);
	return SUCCESS;
}

DECLARE_EXPORT char* read(bool b_debug_, void* ptr_, size_t size_) {
	if (!ptr_) {
		return NULL;
	}
	if (b_debug_) {
		fprintf(stdout, "`memlib.c`: Reading %zd bytes from %p...\n", size_, ptr_);
	}
	return (char*)ptr_;
}
