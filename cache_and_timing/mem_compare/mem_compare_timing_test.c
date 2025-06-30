#define _POSIX_C_SOURCE 199309L
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

typedef unsigned char byte_t;

int timesafe_memcmp(void* source, void* target, int length) {
    byte_t result = 0x00, inter;
    byte_t* s = (byte_t*)source;
    byte_t* t = (byte_t*)target;
    for (int i = 0; i < length; i++) {
        inter = s[i] ^ t[i];    // X-OR operation
        result |= inter;        // OR operation
    }
    return result ? -1 : 0;
}

double elapsed_ns(struct timespec start, struct timespec end) {
    return (end.tv_sec - start.tv_sec) * 1e9 + (end.tv_nsec - start.tv_nsec);
}

int main() {
    const int length = 1024 * 1024; // 1 MB
    byte_t* buf1 = malloc(length);
    byte_t* buf2 = malloc(length);
    memset(buf1, 0xAA, length);
    memset(buf2, 0xAA, length);

    struct timespec start, end;

    // Time safe memcmp
    clock_gettime(CLOCK_MONOTONIC, &start);
    int safe_result = timesafe_memcmp(buf1, buf2, length);
    clock_gettime(CLOCK_MONOTONIC, &end);
    printf("Safe memcmp result: %d, Time: %.0f ns\n", safe_result, elapsed_ns(start, end));

    // Time standard memcmp
    clock_gettime(CLOCK_MONOTONIC, &start);
    int std_result = memcmp(buf1, buf2, length);
    clock_gettime(CLOCK_MONOTONIC, &end);
    printf("Standard memcmp result: %d, Time: %.0f ns\n", std_result, elapsed_ns(start, end));

    free(buf1);
    free(buf2);
    return 0;
}

/*
Safe memcmp result: 0, Time: 2836239 ns
Standard memcmp result: 0, Time: 119770 ns


=== Code Execution Successful ===
timesafe_memcmp avoids short-circuiting, so it always runs through all bytes regardless of early mismatch.

memcmp will exit early on the first differing byte, so it's typically faster, but not constant-time and can be exploited for timing attacks.

This benchmark uses 1 MB of data—adjust the size to test different loads or early mismatch timing behavior.

*/