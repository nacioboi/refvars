#pragma once

#include <stdbool.h>

typedef struct {
	int result_code;
	char* response;
	bool needs_free;
} Compute_Result_t;

typedef bool (*cb__bool__int_voidp_int__t)(int,void*,int);
typedef bool (*cb__bool__str__t)(char*);
typedef Compute_Result_t* (*compute_t)(char*);
