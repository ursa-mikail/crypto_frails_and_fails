# Makefile for timesafe_memcmp benchmark

# Compiler and flags
CC := gcc
CFLAGS := -Wall -Wextra -pedantic -std=c99 -D_POSIX_C_SOURCE=199309L
OPTFLAGS := -O3 -march=native -flto
DEBUGFLAGS := -g -O0

# Target
TARGET := memcmp_benchmark
SRC := mem_compare_timing_test.c # main.c

# Default build mode
MODE ?= release

# Output binary depends on mode
ifeq ($(MODE),debug)
    BIN := $(TARGET)_debug
    ALL_CFLAGS := $(CFLAGS) $(DEBUGFLAGS)
else
    BIN := $(TARGET)
    ALL_CFLAGS := $(CFLAGS) $(OPTFLAGS)
endif

# Default target
.PHONY: all
all: $(BIN)

# Build rule
$(BIN): $(SRC)
	@echo "🔧 Compiling in $(MODE) mode..."
	$(CC) $(ALL_CFLAGS) -o $@ $^

# Run target
.PHONY: run
run: $(BIN)
	@echo "🚀 Running $(BIN)..."
	@./$(BIN)

# Benchmark using hyperfine if available
.PHONY: benchmark
benchmark: $(BIN)
	@command -v hyperfine >/dev/null 2>&1 || { echo "⚠️  'hyperfine' not found. Install it for benchmarking."; exit 1; }
	@echo "📊 Benchmarking safe vs standard memcmp with hyperfine..."
	@hyperfine --warmup 3 './$(BIN)'

# Clean build artifacts
.PHONY: clean
clean:
	@echo "🧹 Cleaning up..."
	@rm -f $(TARGET) $(TARGET)_debug

# Help
.PHONY: help
help:
	@echo "Available targets:"
	@echo "  make             - Build in release mode (default)"
	@echo "  make MODE=debug  - Build in debug mode"
	@echo "  make run         - Build and run"
	@echo "  make benchmark   - Run performance comparison using hyperfine"
	@echo "  make clean       - Remove binaries"

# make               # Build in release mode
# make MODE=debug    # Build in debug mode
# make run           # Build and run
# make benchmark     # Compare using hyperfine (if installed)
# make clean         # Clean all binaries
