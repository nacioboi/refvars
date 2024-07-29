// Constants and includes...
typedef char bool;

#define START_MMF_SERVICE__NAME_MAX_LEN 256

#define ERR__SAFE_MEMORY_ACCESS__FAILED_ALLOC 1
#define ERR__DEALLOCATE__NULL_PTR 2
#define ERR__START_MMF_SERVICE__NULL_PTR 3
#define ERR__START_MMF_SERVICE__INVALID_NAME 4
#define ERR__WRITE__NULL_PTR 5
#define ERR__START_MMF_SERVICE__FAILED_CREATE_FILE_MAPPING 6
#define ERR__START_MMF_SERVICE__FAILED_MAP_VIEW_OF_FILE 7
#define ERR__START_MMF_SERVICE__INVALID_SIZE 8
#define ERR__START_MMF_SERVICE__INVALID_OFFSET 9
#define ERR__START_MMF_SERVICE__FAILED_SHM_OPEN 10
#define ERR__START_MMF_SERVICE__FAILED_FTRUNCATE 11
#define ERR__START_MMF_SERVICE__FAILED_MMAP 12
#define ERR__GROW_MMF_SERVICE__INVALID_SIZE 13
#define ERR__GROW_MMF_SERVICE__NULL_PTR 14
#define ERR__SHRINK_MMF_SERVICE__INVALID_NAME 15
#define ERR__SHRINK_MMF_SERVICE__INVALID_SIZE 16
#define ERR__SHRINK_MMF_SERVICE__TRUNCATES_DATA 17
#define ERR__SHRINK_MMF_SERVICE__FAILED_FTRUNCATE 18
#define ERR__SHRINK_MMF_SERVICE__FAILED_MUNMAP 19
#define ERR__SHRINK_MMF_SERVICE__FAILED_MMAP 20
#define ERR__SHRINK_MMF_SERVICE__FAILED_CREATE_FILE_MAPPING 21
#define ERR__SHRINK_MMF_SERVICE__FAILED_MAP_VIEW_OF_FILE 22

#define SUCCESS 0

#ifdef _WIN32
#define DECLARE_EXPORT __declspec(dllexport)
#else
#define DECLARE_EXPORT __attribute__((visibility("default")))
#endif

#include <stdlib.h>
#include <string.h>
#include <stdio.h>
#include <stdint.h>
#ifdef _WIN32
#include <windows.h>
#include <synchapi.h>
#else
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>
#include <pthread.h>
#endif
#include <stdarg.h>
#define DEBUG_PREFIX "[[ `memlib.c` DEBUG ]] "

void debug_write(bool b_enabled_, const char *format, ...) {
	if (!b_enabled_) {
		return;
	}
	
	va_list args;
	va_start(args, format);
	
	printf(DEBUG_PREFIX);

	char buffer[1024];
	vsprintf(buffer, format, args);

	printf("%s", buffer);
	
	va_end(args);
}






///////////////////////////////////
// Memory-mapped file service... //
///////////////////////////////////







void* mmf_ptr = NULL;
void* temp_mmf_ptr = NULL;
int64_t mmf_size = 0;
int64_t last_regrow_size = 0;







#ifdef _WIN32
static HANDLE mmf_handle = NULL;
static CRITICAL_SECTION mmf_critical_section;
void InitializeCriticalSectionExample() {
	// Initialize the critical section with a spin count of 1024
	if (!InitializeCriticalSectionAndSpinCount(&mmf_critical_section, 0x00000400)) {
		printf("Failed to initialize critical section.\n");
	}
}
BOOL APIENTRY DllMain(HMODULE hModule,
                      DWORD  ul_reason_for_call,
                      LPVOID lpReserved)
{
	switch (ul_reason_for_call)
	{
	case DLL_PROCESS_ATTACH:
		// A process is loading the DLL.
		InitializeCriticalSection(&mmf_critical_section);
		break;
	case DLL_THREAD_ATTACH:
		// A process is creating a new thread.
		break;
	case DLL_THREAD_DETACH:
		// A thread exits normally.
		break;
	case DLL_PROCESS_DETACH:
		// A process unloads the DLL.
		break;
	}
	return TRUE;
}
#else
static int mmf_fd = -1;
static pthread_mutex_t mmf_mutex = PTHREAD_MUTEX_INITIALIZER;
#endif







DECLARE_EXPORT void* get_mmf_ptr(bool b_debug_) {
	debug_write(b_debug_, "Entering critical section...\n");
#ifdef _WIN32
	EnterCriticalSection(&mmf_critical_section);
#else
	pthread_mutex_lock(&mmf_mutex);
#endif

	void* ptr = mmf_ptr;

	debug_write(b_debug_, "Leaving critical section...\n");
#ifdef _WIN32
	LeaveCriticalSection(&mmf_critical_section);
#else
	pthread_mutex_unlock(&mmf_mutex);
#endif

	debug_write(b_debug_, "Returning memory-mapped file pointer @[%p]...\n", ptr);
	return ptr;
}







int _start_mmf_service(
		bool b_debug_,
		const char* name_,
		int size_low_, int size_high_,
		void **ptr_,
		int offset_low_, int offset_high_
) {
	if (!name_) {
		debug_write(b_debug_, "ERROR: `name_` is NULL!\n");
		return ERR__START_MMF_SERVICE__INVALID_NAME;
	}

	if (!ptr_) {
		debug_write(b_debug_, "ERROR: `ptr_` is NULL!\n");
		return ERR__START_MMF_SERVICE__NULL_PTR;
	}

	// Add bounds checking for the name length
	if (strlen(name_) >= START_MMF_SERVICE__NAME_MAX_LEN) {
		debug_write(b_debug_, "ERROR: `name_`:[%s] too long!\n", name_);
		return ERR__START_MMF_SERVICE__INVALID_NAME;
	}

	// Ensure size is not negative
	int64_t total_size = ((int64_t)size_high_ << 32) | (int64_t)size_low_;
	debug_write(b_debug_, "Total size: [%ld]\n", total_size);
	if (total_size <= 0) {
		debug_write(b_debug_, "ERROR: Invalid size!\n");
		return ERR__START_MMF_SERVICE__INVALID_SIZE;
	}

#ifdef _WIN32
	debug_write(b_debug_, "Entering critical section...\n");
	EnterCriticalSection(&mmf_critical_section);

	debug_write(b_debug_, "Creating file mapping object...\n");
	mmf_handle = CreateFileMapping(
		INVALID_HANDLE_VALUE,    // Use paging file
		NULL,                    // Default security attributes
		PAGE_READWRITE,
		size_high_,
		size_low_,
		name_
	);
	if (mmf_handle == NULL) {
		debug_write(b_debug_, "ERROR: Could not create file mapping object! WinError:[%lu].\n", GetLastError());
		debug_write(b_debug_, "Leaving critical section...\n");
		LeaveCriticalSection(&mmf_critical_section);
		return ERR__START_MMF_SERVICE__FAILED_CREATE_FILE_MAPPING;
	}

	debug_write(b_debug_, "Mapping view of file...\n");
	int64_t offset_size = ((int64_t)offset_high_ << 32) | (int64_t)offset_low_;
	int64_t offset_accounted_size = total_size - offset_size;
	debug_write(b_debug_, "Offset size: [%ld]\n", offset_size);
	debug_write(b_debug_, "Offset accounted size: [%ld]\n", offset_accounted_size);
	if (offset_accounted_size <= 0) {
		debug_write(b_debug_, "ERROR: Invalid offset!\n");
		CloseHandle(mmf_handle);
		mmf_handle = NULL;
		debug_write(b_debug_, "Leaving critical section...\n");
		LeaveCriticalSection(&mmf_critical_section);
		return ERR__START_MMF_SERVICE__INVALID_OFFSET;
	}
	*ptr_ = MapViewOfFile(
		mmf_handle,           // Handle to map object
		FILE_MAP_ALL_ACCESS,  // Read/write permission
		offset_high_,
		offset_low_,
		offset_accounted_size
	);
	if (*ptr_ == NULL) {
		debug_write(b_debug_, "ERROR: Could not map view of file! WinError:[%lu].\n", GetLastError());
		CloseHandle(mmf_handle);
		mmf_handle = NULL;
		debug_write(b_debug_, "Leaving critical section...\n");
		LeaveCriticalSection(&mmf_critical_section);
		return ERR__START_MMF_SERVICE__FAILED_MAP_VIEW_OF_FILE;
	}

	debug_write(b_debug_, "Leaving critical section...\n");
	LeaveCriticalSection(&mmf_critical_section);
#else
	pthread_mutex_lock(&mmf_mutex);

	char full_name[START_MMF_SERVICE__NAME_MAX_LEN + 2];
	if (snprintf(full_name, sizeof(full_name), "/%s", name) >= sizeof(full_name)) {
		fprintf(stderr, "Formatted name too long\n");
		pthread_mutex_unlock(&mmf_mutex);
		return ERR__START_MMF_SERVICE__INVALID_NAME;
	}

	mmf_fd = shm_open(full_name, O_RDWR | O_CREAT, 0666);
	if (mmf_fd == -1) {
		perror("shm_open");
		pthread_mutex_unlock(&mmf_mutex);
		return ERR__START_MMF_SERVICE__FAILED_SHM_OPEN;
	}

	if (ftruncate(mmf_fd, total_size) == -1) {
		perror("ftruncate");
		close(mmf_fd);
		mmf_fd = -1;
		pthread_mutex_unlock(&mmf_mutex);
		return ERR__START_MMF_SERVICE__FAILED_FTRUNCATE;
	}

	int64_t offset_accounted_size = total_size - (((int64_t)offset_high << 32) | (int64_t)offset_low);
	if (offset_accounted_size <= 0) {
		close(mmf_fd);
		mmf_fd = -1;
		pthread_mutex_unlock(&mmf_mutex);
		return ERR__START_MMF_SERVICE__INVALID_OFFSET;
	}

	*ptr = mmap(NULL, offset_accounted_size, PROT_READ | PROT_WRITE, MAP_SHARED, mmf_fd, (((int64_t)offset_high << 32) | (int64_t)offset_low));
	if (*ptr == MAP_FAILED) {
		perror("mmap");
		close(mmf_fd);
		mmf_fd = -1;
		pthread_mutex_unlock(&mmf_mutex);
		return ERR__START_MMF_SERVICE__FAILED_MMAP;
	}

	pthread_mutex_unlock(&mmf_mutex);
#endif

	return SUCCESS;
}







int _stop_mmf_service(bool b_debug_, void *ptr_) {
	debug_write(b_debug_, "Stopping memory-mapped file service...\n");
	debug_write(b_debug_, "Entering critical section...\n");
#ifdef _WIN32
	EnterCriticalSection(&mmf_critical_section);
	if (mmf_ptr) {
		UnmapViewOfFile(mmf_ptr);
		mmf_ptr = NULL;
		debug_write(b_debug_, "`mmf_ptr` should be NULL --> Schizophrenia:[%p]...\n", mmf_ptr);
	}
	if (mmf_handle) {
		CloseHandle(mmf_handle);
		mmf_handle = NULL;
		debug_write(b_debug_, "`mmf_handle` should be NULL --> Schizophrenia:[%p]...\n", mmf_handle);
	}
	LeaveCriticalSection(&mmf_critical_section);
#else
	pthread_mutex_lock(&mmf_mutex);
	if (mmf_ptr && mmf_ptr != MAP_FAILED) {
		munmap(mmf_ptr, mmf_size);
		mmf_ptr = NULL;
	}
	if (mmf_fd != -1) {
		close(mmf_fd);
		mmf_fd = -1;
	}
	pthread_mutex_unlock(&mmf_mutex);
#endif
	debug_write(b_debug_, "Leaving critical section...\n");

	return SUCCESS;
}







DECLARE_EXPORT int start_mmf_service(bool b_debug_, const char* name_, int size_low_, int size_high_) {
	return _start_mmf_service(b_debug_, name_, size_low_, size_high_, &mmf_ptr, 0, 0);
}







DECLARE_EXPORT int stop_mmf_service(bool b_debug_) {
	return _stop_mmf_service(b_debug_, mmf_ptr);
}







DECLARE_EXPORT int grow_mmf_service(bool b_debug_, const char* name_, int size_low_, int size_high_) {
	int64_t new_size = ((int64_t)size_high_ << 32) | (int64_t)size_low_;
	debug_write(b_debug_, "New size: [%ld]\n", new_size);
	debug_write(b_debug_, "Last regrow size: [%ld]\n", last_regrow_size);
	if (new_size <= last_regrow_size || new_size < 1) {
		debug_write(b_debug_, "ERROR: Invalid size!\n");
		return ERR__GROW_MMF_SERVICE__INVALID_SIZE;
	}

	last_regrow_size = new_size;
	debug_write(b_debug_, "Starting memory-mapped file service...\n");
	int result = _start_mmf_service(b_debug_, name_, size_low_, size_high_, &temp_mmf_ptr, 0, 0);
	if (result != 0) {
		return result;
	}

	// Check for NULL pointer before using it
	if (!temp_mmf_ptr || !mmf_ptr) {
		debug_write(b_debug_, "ERROR: NULL pointer!\n");
		_stop_mmf_service(b_debug_, temp_mmf_ptr);
		return ERR__GROW_MMF_SERVICE__NULL_PTR;
	}

	// Copy the data from the old memory-mapped file to the new one.
	debug_write(b_debug_, "Copying data from old memory-mapped file to new one...\n");
	debug_write(b_debug_, "Entering critical section...\n");
#ifdef _WIN32
	EnterCriticalSection(&mmf_critical_section);
#else
	pthread_mutex_lock(&mmf_mutex);
#endif
	debug_write(b_debug_, "Copying [%ld] bytes...\n", mmf_size);
	memcpy(temp_mmf_ptr, mmf_ptr, mmf_size);

	// Unmap the old memory-mapped file.
	debug_write(b_debug_, "Unmapping old memory-mapped file...\n");
	_stop_mmf_service(b_debug_, mmf_ptr);

	// Update the pointers and size.
	debug_write(b_debug_, "Sanity check, pre: `mmf_ptr`:[%p], `temp_mmf_ptr`:[%p]...\n", mmf_ptr, temp_mmf_ptr);
	mmf_ptr = temp_mmf_ptr;
	mmf_size = new_size;
	temp_mmf_ptr = NULL;
	debug_write(b_debug_, "Sanity check, post: `mmf_ptr`:[%p], `temp_mmf_ptr`:[%p]...\n", mmf_ptr, temp_mmf_ptr);
#ifdef _WIN32
	LeaveCriticalSection(&mmf_critical_section);
#else
	pthread_mutex_unlock(&mmf_mutex);
#endif
	debug_write(b_debug_, "Leaving critical section...\n");

	return SUCCESS;
}







DECLARE_EXPORT int shrink_mmf_service(bool b_debug_, const char* name_, int new_size_low_, int new_size_high_) {
	if (!name_) {
		debug_write(b_debug_, "ERROR: Invalid name!\n");
		return ERR__SHRINK_MMF_SERVICE__INVALID_NAME;
	}

	int64_t new_size = ((int64_t)new_size_high_ << 32) | (int64_t)new_size_low_;
	debug_write(b_debug_, "New size: [%ld]\n", new_size);
	if (new_size <= 0 || new_size >= mmf_size) {
		debug_write(b_debug_, "ERROR: Invalid size:[%ld]!\n", new_size);
		return ERR__SHRINK_MMF_SERVICE__INVALID_SIZE;
	}

	// Check for null bytes at the end of the memory-mapped file
	int64_t actual_size = mmf_size;
	debug_write(b_debug_, "Actual size: [%ld]\n", actual_size);
	char *data = (char*)mmf_ptr;

	debug_write(b_debug_, "Checking how many null bytes are at the end of the memory-mapped file...\n");
	while (actual_size > new_size && data[actual_size - 1] == '\0') {
		actual_size--;
	}

	if (actual_size > new_size) {
		// Shrinking is not possible because it would truncate usable data
		debug_write(b_debug_, "ERROR: Shrinking would truncate data!\n");
		return ERR__SHRINK_MMF_SERVICE__TRUNCATES_DATA;
	}

#ifdef _WIN32
	debug_write(b_debug_, "Entering critical section...\n");
	EnterCriticalSection(&mmf_critical_section);
	debug_write(b_debug_, "Unmapping view of file...\n");
	UnmapViewOfFile(mmf_ptr);
	debug_write(b_debug_, "Closing file mapping object...\n");
	CloseHandle(mmf_handle);

	debug_write(b_debug_, "Creating file mapping object...\n");
	mmf_handle = CreateFileMapping(
		INVALID_HANDLE_VALUE,
		NULL,
		PAGE_READWRITE,
		new_size_high_,
		new_size_low_,
		name_
	);

	if (mmf_handle == NULL) {
		debug_write(b_debug_, "ERROR: Could not create file mapping object [%lu].\n", GetLastError());
		debug_write(b_debug_, "Leaving critical section...\n");
		LeaveCriticalSection(&mmf_critical_section);
		return ERR__SHRINK_MMF_SERVICE__FAILED_CREATE_FILE_MAPPING;
	}

	debug_write(b_debug_, "Mapping view of file...\n");
	mmf_ptr = MapViewOfFile(
		mmf_handle,
		FILE_MAP_ALL_ACCESS,
		0,
		0,
		new_size
	);

	if (mmf_ptr == NULL) {
		debug_write(b_debug_, "Could not map view of file (%lu).\n", GetLastError());
		debug_write(b_debug_, "Leaving critical section...\n");
		CloseHandle(mmf_handle);
		mmf_handle = NULL;
		LeaveCriticalSection(&mmf_critical_section);
		return ERR__SHRINK_MMF_SERVICE__FAILED_MAP_VIEW_OF_FILE;
	}
	debug_write(b_debug_, "Leaving critical section...\n");
	LeaveCriticalSection(&mmf_critical_section);
#else
	pthread_mutex_lock(&mmf_mutex);
	if (ftruncate(mmf_fd, new_size) == -1) {
		perror("ftruncate");
		pthread_mutex_unlock(&mmf_mutex);
		return ERR__SHRINK_MMF_SERVICE__FAILED_FTRUNCATE;
	}

	if (munmap(mmf_ptr, mmf_size) == -1) {
		perror("munmap");
		pthread_mutex_unlock(&mmf_mutex);
		return ERR__SHRINK_MMF_SERVICE__FAILED_MUNMAP;
	}

	mmf_ptr = mmap(NULL, new_size, PROT_READ | PROT_WRITE, MAP_SHARED, mmf_fd, 0);
	if (mmf_ptr == MAP_FAILED) {
		perror("mmap");
		pthread_mutex_unlock(&mmf_mutex);
		return ERR__SHRINK_MMF_SERVICE__FAILED_MMAP;
	}

	mmf_size = new_size;
	pthread_mutex_unlock(&mmf_mutex);
#endif

	return SUCCESS;
}







////////////
// API... //
////////////

DECLARE_EXPORT int safe_memory_access(bool b_debug_, size_t size_, void (*callback_)(void* ptr_)) {
	void* ptr = malloc(size_);
	if (!ptr) {
		return ERR__SAFE_MEMORY_ACCESS__FAILED_ALLOC;
	}
	debug_write(b_debug_, "Allocated memory at [%p]...\n", ptr);
	callback_(ptr);
	free(ptr);
	debug_write(b_debug_, "Freed memory at [%p]...\n", ptr);
	return SUCCESS;
}

DECLARE_EXPORT void* allocate(bool b_debug_, size_t size_) {
	void* ptr = malloc(size_);  // Cringe, but the user asked for it :(
	if (!ptr) {
		return NULL;
	}
	debug_write(b_debug_, "Allocated memory at [%p]...\n", ptr);
	return ptr;
}

DECLARE_EXPORT int deallocate(bool b_debug_, void* ptr_) {
	if (!ptr_) {
		return ERR__DEALLOCATE__NULL_PTR;
	}
	debug_write(b_debug_, "Freeing memory at [%p]...\n", ptr_);
	free(ptr_);
	return SUCCESS;
}

DECLARE_EXPORT int write(bool b_debug_, void* ptr_, void* data_, size_t size_) {
	if (!ptr_) {
		return ERR__WRITE__NULL_PTR;
	}
	debug_write(b_debug_, "Writing %zd bytes to %p...\n", size_, ptr_);
	memcpy(ptr_, (char*)data_, size_);
	return SUCCESS;
}

DECLARE_EXPORT int read(bool b_debug_, void* ptr_, size_t size_, void* data_out_) {
	if (!ptr_) {
		return 1;
	}
	debug_write(b_debug_, "Reading %zd bytes from %p...\n", size_, ptr_);
	memcpy(data_out_, ptr_, size_);
	return 0;
}

