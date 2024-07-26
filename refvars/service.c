#include <windows.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

typedef char* (*cb__str__void__t)(int);
typedef bool (*cb__bool__str__t)(const char*);

__declspec(dllexport) void service(
		cb__str__void__t request_callback,
		cb__bool__str__t result_callback
) {
	int i = 0;
	while (1) {
		// Get the request from Python
		char* request = (char*)request_callback(i++);
		if (request[0] == '\0') {
			free(request);
			break;
		}
		
		// Perform the computation (example: reverse the string)...
		size_t len = strlen(request);
		char* response = (char*)malloc(len + 1);
		for (size_t i = 0; i < len; ++i) {
			response[i] = request[len - i - 1];
		}
		response[len] = '\0';
		
		// Send the result back to Python.
		bool b = result_callback(response);
		if (!b) {
			printf("Failed to send response\n");
			break;
		}

		// Free the allocated memory.
		//free(request);  // Python frees the request.
		//free(response); // For some reason, having this uncommented causes a crash.
		//printf("response: [%s].\n", response);
		
		Sleep(25);
	}
}
