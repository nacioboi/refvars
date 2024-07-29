#include <string.h>
#include <stdlib.h>
#include "service.h"

__declspec(dllexport) Compute_Result_t* compute(char* request) {
	Compute_Result_t* my_result = (Compute_Result_t*)malloc(sizeof(Compute_Result_t));
	size_t len = strlen(request);

	char* res = (char*)malloc(len + 1);
	for (size_t i = 0; i < len; ++i) {
		res[i] = request[len - i - 1];
	}
	res[len] = '\0';

	my_result->result_code = 0;
	my_result->response = res;
	my_result->needs_free = true;

	return my_result;
}
