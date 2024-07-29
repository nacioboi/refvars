#include <windows.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include "service.h"

__declspec(dllexport) int service(
		cb__bool__int_voidp_int__t request_callback,
		cb__bool__str__t result_callback,
		UINT32 buff_size,
		UINT64 sleep_time
) {
	HMODULE hLib = LoadLibrary(TEXT("compute.dll"));
	if (hLib == NULL) {
		return 1;
	}

	compute_t compute = (compute_t)GetProcAddress(hLib, "compute");
	if (compute == NULL) {
		FreeLibrary(hLib);
		return 1;
	}

	// Allocate memory for the request.
	void* request = (void*)malloc(sizeof(char) * buff_size);

	size_t j = 0;
	while (1) {
		// Get the request from Python.
		memset(request, 0, sizeof(char) * buff_size);
		bool keep_going = request_callback(j++, request, buff_size);
		if (!keep_going) {
			FreeLibrary(hLib);
			break;
		}
		
		// Perform the computation using the dynamically loaded compute function.
		Compute_Result_t* result = (Compute_Result_t*)compute(request);
		char* response = result->response;

		// Send the result back to Python.
		bool b = result_callback(response);

		// First, always free the request if required.	
		if (result->needs_free) {
			free(response);
		}

		if (!b) {
			FreeLibrary(hLib);
			free(result);
			free(request);
			return 1;
		}

		if (result->result_code != 0) {
			int res_code = result->result_code;
			FreeLibrary(hLib);
			free(request);
			free(result);
			return res_code;
		}

		free(result);

		Sleep((DWORD)sleep_time);
	}

	FreeLibrary(hLib);
	free(request);
	return 0;
}
