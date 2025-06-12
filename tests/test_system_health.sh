#!/bin/bash

# Test file for system_health.sh

# Load test utilities
source "$(dirname "$0")/../scripts/test_utils.sh"

# Test configuration
TEST_LOG_FILE="/tmp/system_health_test.log"
TEST_THRESHOLD_CPU=80
TEST_THRESHOLD_MEMORY=85
TEST_THRESHOLD_DISK=90

# Setup test environment
setup_test() {
    # Create temporary log file
    touch "$TEST_LOG_FILE"
    
    # Backup original config
    if [ -f "config/config.sh" ]; then
        cp "config/config.sh" "config/config.sh.bak"
    fi
    
    # Create test config
    cat > "config/config.sh" << EOF
LOG_FILE="$TEST_LOG_FILE"
THRESHOLD_CPU=$TEST_THRESHOLD_CPU
THRESHOLD_MEMORY=$TEST_THRESHOLD_MEMORY
THRESHOLD_DISK=$TEST_THRESHOLD_DISK
CHECK_INTERVAL=1
EOF
}

# Cleanup test environment
cleanup_test() {
    # Remove test log file
    rm -f "$TEST_LOG_FILE"
    
    # Restore original config
    if [ -f "config/config.sh.bak" ]; then
        mv "config/config.sh.bak" "config/config.sh"
    fi
}

# Test CPU check
test_cpu_check() {
    echo "Testing CPU check..."
    
    # Simulate high CPU usage
    local high_cpu=90
    local result=$(check_cpu $high_cpu)
    
    if grep -q "High CPU usage" "$TEST_LOG_FILE"; then
        echo "✅ CPU check passed"
    else
        echo "❌ CPU check failed"
        return 1
    fi
}

# Test memory check
test_memory_check() {
    echo "Testing memory check..."
    
    # Simulate high memory usage
    local high_memory=90
    local result=$(check_memory $high_memory)
    
    if grep -q "High memory usage" "$TEST_LOG_FILE"; then
        echo "✅ Memory check passed"
    else
        echo "❌ Memory check failed"
        return 1
    fi
}

# Test disk check
test_disk_check() {
    echo "Testing disk check..."
    
    # Simulate high disk usage
    local high_disk=95
    local result=$(check_disk $high_disk)
    
    if grep -q "High disk usage" "$TEST_LOG_FILE"; then
        echo "✅ Disk check passed"
    else
        echo "❌ Disk check failed"
        return 1
    fi
}

# Test log message function
test_log_message() {
    echo "Testing log message function..."
    
    local test_message="Test log message"
    log_message "$test_message"
    
    if grep -q "$test_message" "$TEST_LOG_FILE"; then
        echo "✅ Log message function passed"
    else
        echo "❌ Log message function failed"
        return 1
    fi
}

# Run all tests
run_tests() {
    echo "Starting system health monitor tests..."
    
    setup_test
    
    # Run individual tests
    test_log_message
    test_cpu_check
    test_memory_check
    test_disk_check
    
    cleanup_test
    
    echo "All tests completed"
}

# Main execution
if [ "${BASH_SOURCE[0]}" = "$0" ]; then
    run_tests
fi 