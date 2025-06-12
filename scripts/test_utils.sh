#!/bin/bash

# Test utilities for system administration scripts

# Function to assert equality
assert_equal() {
    local expected="$1"
    local actual="$2"
    local message="${3:-Test failed}"
    
    if [ "$expected" = "$actual" ]; then
        echo "✅ $message"
        return 0
    else
        echo "❌ $message"
        echo "Expected: $expected"
        echo "Actual: $actual"
        return 1
    fi
}

# Function to assert file exists
assert_file_exists() {
    local file="$1"
    local message="${2:-File should exist}"
    
    if [ -f "$file" ]; then
        echo "✅ $message"
        return 0
    else
        echo "❌ $message"
        return 1
    fi
}

# Function to assert directory exists
assert_dir_exists() {
    local dir="$1"
    local message="${2:-Directory should exist}"
    
    if [ -d "$dir" ]; then
        echo "✅ $message"
        return 0
    else
        echo "❌ $message"
        return 1
    fi
}

# Function to assert command exists
assert_command_exists() {
    local command="$1"
    local message="${2:-Command should exist}"
    
    if command -v "$command" >/dev/null 2>&1; then
        echo "✅ $message"
        return 0
    else
        echo "❌ $message"
        return 1
    fi
}

# Function to assert file contains text
assert_file_contains() {
    local file="$1"
    local text="$2"
    local message="${3:-File should contain text}"
    
    if grep -q "$text" "$file"; then
        echo "✅ $message"
        return 0
    else
        echo "❌ $message"
        return 1
    fi
}

# Function to run a test
run_test() {
    local test_name="$1"
    local test_function="$2"
    
    echo "Running test: $test_name"
    if $test_function; then
        echo "✅ $test_name passed"
        return 0
    else
        echo "❌ $test_name failed"
        return 1
    fi
}

# Function to clean up test files
cleanup_test_files() {
    local files=("$@")
    for file in "${files[@]}"; do
        rm -f "$file"
    done
} 