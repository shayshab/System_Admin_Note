# Top 10 Essential Bash Programs for System Administrators

## 1. System Health Monitor
```bash
#!/bin/bash
# system_health.sh - Monitors system resources and logs issues

# Configuration
LOG_FILE="/var/log/system_health.log"
THRESHOLD_CPU=80
THRESHOLD_MEMORY=85
THRESHOLD_DISK=90

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Check CPU usage
check_cpu() {
    CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d. -f1)
    if [ "$CPU_USAGE" -gt "$THRESHOLD_CPU" ]; then
        log_message "WARNING: High CPU usage detected: ${CPU_USAGE}%"
    fi
}

# Check memory usage
check_memory() {
    MEMORY_USAGE=$(free | grep Mem | awk '{print $3/$2 * 100.0}' | cut -d. -f1)
    if [ "$MEMORY_USAGE" -gt "$THRESHOLD_MEMORY" ]; then
        log_message "WARNING: High memory usage detected: ${MEMORY_USAGE}%"
    fi
}

# Check disk usage
check_disk() {
    DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | cut -d% -f1)
    if [ "$DISK_USAGE" -gt "$THRESHOLD_DISK" ]; then
        log_message "WARNING: High disk usage detected: ${DISK_USAGE}%"
    fi
}

# Main monitoring loop
while true; do
    check_cpu
    check_memory
    check_disk
    sleep 300  # Check every 5 minutes
done
```

## 2. Log File Analyzer
```bash
#!/bin/bash
# log_analyzer.sh - Analyzes log files for patterns and generates reports

# Configuration
LOG_DIR="/var/log"
REPORT_DIR="/var/log/reports"
PATTERNS=("ERROR" "WARNING" "CRITICAL" "Failed")

# Create report directory if it doesn't exist
mkdir -p "$REPORT_DIR"

# Function to analyze a single log file
analyze_log() {
    local log_file="$1"
    local report_file="$REPORT_DIR/$(basename "$log_file").report"
    
    echo "=== Analysis Report for $(basename "$log_file") ===" > "$report_file"
    echo "Generated on: $(date)" >> "$report_file"
    echo "" >> "$report_file"
    
    for pattern in "${PATTERNS[@]}"; do
        count=$(grep -c "$pattern" "$log_file")
        echo "Occurrences of $pattern: $count" >> "$report_file"
        if [ "$count" -gt 0 ]; then
            echo "Last 5 occurrences:" >> "$report_file"
            grep "$pattern" "$log_file" | tail -n 5 >> "$report_file"
            echo "" >> "$report_file"
        fi
    done
}

# Main analysis loop
for log_file in "$LOG_DIR"/*.log; do
    if [ -f "$log_file" ]; then
        analyze_log "$log_file"
    fi
done
```

## 3. Backup Automation Script
```bash
#!/bin/bash
# backup_automation.sh - Automated backup script with rotation

# Configuration
BACKUP_DIR="/backup"
SOURCE_DIRS=("/etc" "/home" "/var/www")
RETENTION_DAYS=7
DATE=$(date +%Y%m%d)

# Function to create backup
create_backup() {
    local source="$1"
    local backup_name="backup_$(basename "$source")_${DATE}.tar.gz"
    
    tar -czf "$BACKUP_DIR/$backup_name" "$source"
    if [ $? -eq 0 ]; then
        echo "Backup created: $backup_name"
    else
        echo "Error creating backup: $backup_name"
    fi
}

# Function to clean old backups
clean_old_backups() {
    find "$BACKUP_DIR" -name "backup_*.tar.gz" -mtime +$RETENTION_DAYS -delete
}

# Main backup process
for dir in "${SOURCE_DIRS[@]}"; do
    if [ -d "$dir" ]; then
        create_backup "$dir"
    fi
done

clean_old_backups
```

## 4. Network Port Scanner
```bash
#!/bin/bash
# port_scanner.sh - Scans network ports and services

# Configuration
TARGET_HOST="$1"
START_PORT=1
END_PORT=1024
TIMEOUT=1

# Function to scan a single port
scan_port() {
    local host="$1"
    local port="$2"
    
    (echo >/dev/tcp/$host/$port) >/dev/null 2>&1
    if [ $? -eq 0 ]; then
        echo "Port $port is open"
        # Try to get service name
        service=$(grep -w "$port/tcp" /etc/services | head -n1 | awk '{print $1}')
        if [ ! -z "$service" ]; then
            echo "Service: $service"
        fi
    fi
}

# Main scanning loop
if [ -z "$TARGET_HOST" ]; then
    echo "Usage: $0 <host>"
    exit 1
fi

echo "Scanning $TARGET_HOST from port $START_PORT to $END_PORT"
for port in $(seq $START_PORT $END_PORT); do
    scan_port "$TARGET_HOST" "$port" &
    sleep $TIMEOUT
done
wait
```

## 5. User Management Tool
```bash
#!/bin/bash
# user_management.sh - User account management tool

# Function to create user
create_user() {
    local username="$1"
    local password="$2"
    
    if id "$username" &>/dev/null; then
        echo "User $username already exists"
        return 1
    fi
    
    useradd -m -s /bin/bash "$username"
    echo "$username:$password" | chpasswd
    
    # Set up user directory
    mkdir -p "/home/$username/.ssh"
    chmod 700 "/home/$username/.ssh"
    chown -R "$username:$username" "/home/$username"
    
    echo "User $username created successfully"
}

# Function to delete user
delete_user() {
    local username="$1"
    
    if ! id "$username" &>/dev/null; then
        echo "User $username does not exist"
        return 1
    fi
    
    userdel -r "$username"
    echo "User $username deleted successfully"
}

# Function to list users
list_users() {
    echo "System Users:"
    awk -F: '$3 >= 1000 && $3 != 65534 {print $1}' /etc/passwd
}

# Main menu
case "$1" in
    "create")
        create_user "$2" "$3"
        ;;
    "delete")
        delete_user "$2"
        ;;
    "list")
        list_users
        ;;
    *)
        echo "Usage: $0 {create|delete|list} [username] [password]"
        exit 1
        ;;
esac
```

## 6. Process Manager
```bash
#!/bin/bash
# process_manager.sh - Process management and monitoring tool

# Function to list processes
list_processes() {
    echo "Running Processes:"
    ps aux | grep -v grep | grep -v "$0"
}

# Function to kill process
kill_process() {
    local pid="$1"
    if ps -p "$pid" > /dev/null; then
        kill -15 "$pid"
        echo "Process $pid terminated"
    else
        echo "Process $pid not found"
    fi
}

# Function to monitor process
monitor_process() {
    local pid="$1"
    local interval="$2"
    
    while ps -p "$pid" > /dev/null; do
        echo "Process $pid status:"
        ps -p "$pid" -o pid,ppid,cmd,%cpu,%mem
        sleep "$interval"
    done
}

# Main menu
case "$1" in
    "list")
        list_processes
        ;;
    "kill")
        kill_process "$2"
        ;;
    "monitor")
        monitor_process "$2" "${3:-5}"
        ;;
    *)
        echo "Usage: $0 {list|kill|monitor} [pid] [interval]"
        exit 1
        ;;
esac
```

## 7. File System Monitor
```bash
#!/bin/bash
# filesystem_monitor.sh - Monitors file system changes

# Configuration
WATCH_DIR="/var/www"
LOG_FILE="/var/log/filesystem_changes.log"
IGNORE_PATTERNS=("*.tmp" "*.log" "*.swp")

# Function to log changes
log_change() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to check if file should be ignored
should_ignore() {
    local file="$1"
    for pattern in "${IGNORE_PATTERNS[@]}"; do
        if [[ "$file" == $pattern ]]; then
            return 0
        fi
    done
    return 1
}

# Main monitoring loop
inotifywait -m -r -e create,modify,delete,move "$WATCH_DIR" | while read path action file; do
    if ! should_ignore "$file"; then
        case "$action" in
            "CREATE")
                log_change "File created: $path$file"
                ;;
            "MODIFY")
                log_change "File modified: $path$file"
                ;;
            "DELETE")
                log_change "File deleted: $path$file"
                ;;
            "MOVED_FROM")
                log_change "File moved from: $path$file"
                ;;
            "MOVED_TO")
                log_change "File moved to: $path$file"
                ;;
        esac
    fi
done
```

## 8. System Update Manager
```bash
#!/bin/bash
# update_manager.sh - Manages system updates and patches

# Configuration
LOG_FILE="/var/log/update_manager.log"
MAIL_RECIPIENT="admin@example.com"

# Function to log updates
log_update() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to send email
send_email() {
    local subject="$1"
    local body="$2"
    echo "$body" | mail -s "$subject" "$MAIL_RECIPIENT"
}

# Check for updates
check_updates() {
    if command -v apt-get &> /dev/null; then
        apt-get update
        updates=$(apt-get -s upgrade | grep -c "^Inst")
    elif command -v yum &> /dev/null; then
        updates=$(yum check-update | grep -c "^[a-zA-Z]")
    else
        echo "Unsupported package manager"
        exit 1
    fi
    
    if [ "$updates" -gt 0 ]; then
        log_update "Updates available: $updates"
        send_email "System Updates Available" "There are $updates updates available for installation."
    fi
}

# Install updates
install_updates() {
    log_update "Starting system update"
    
    if command -v apt-get &> /dev/null; then
        apt-get upgrade -y
    elif command -v yum &> /dev/null; then
        yum update -y
    fi
    
    if [ $? -eq 0 ]; then
        log_update "System update completed successfully"
        send_email "System Update Complete" "System updates have been installed successfully."
    else
        log_update "System update failed"
        send_email "System Update Failed" "There was an error during system update."
    fi
}

# Main menu
case "$1" in
    "check")
        check_updates
        ;;
    "install")
        install_updates
        ;;
    *)
        echo "Usage: $0 {check|install}"
        exit 1
        ;;
esac
```

## 9. Network Traffic Analyzer
```bash
#!/bin/bash
# traffic_analyzer.sh - Analyzes network traffic patterns

# Configuration
INTERFACE="eth0"
LOG_FILE="/var/log/traffic_analysis.log"
THRESHOLD=1000  # KB/s

# Function to get current traffic
get_traffic() {
    local interface="$1"
    rx_bytes=$(cat /sys/class/net/$interface/statistics/rx_bytes)
    tx_bytes=$(cat /sys/class/net/$interface/statistics/tx_bytes)
    echo "$rx_bytes $tx_bytes"
}

# Function to calculate traffic rate
calculate_rate() {
    local old_rx="$1"
    local old_tx="$2"
    local new_rx="$3"
    local new_tx="$4"
    local interval="$5"
    
    rx_rate=$(( (new_rx - old_rx) / interval ))
    tx_rate=$(( (new_tx - old_tx) / interval ))
    echo "$rx_rate $tx_rate"
}

# Main monitoring loop
old_traffic=$(get_traffic "$INTERFACE")
old_time=$(date +%s)

while true; do
    sleep 1
    new_traffic=$(get_traffic "$INTERFACE")
    new_time=$(date +%s)
    
    interval=$((new_time - old_time))
    rates=($(calculate_rate $old_traffic $new_traffic $interval))
    
    rx_rate=${rates[0]}
    tx_rate=${rates[1]}
    
    if [ "$rx_rate" -gt "$THRESHOLD" ] || [ "$tx_rate" -gt "$THRESHOLD" ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - High traffic detected: RX: ${rx_rate}KB/s TX: ${tx_rate}KB/s" >> "$LOG_FILE"
    fi
    
    old_traffic=$new_traffic
    old_time=$new_time
done
```

## 10. System Report Generator
```bash
#!/bin/bash
# system_report.sh - Generates comprehensive system reports

# Configuration
REPORT_DIR="/var/log/system_reports"
DATE=$(date +%Y%m%d)

# Function to generate report
generate_report() {
    local report_file="$REPORT_DIR/system_report_${DATE}.txt"
    
    echo "=== System Report Generated on $(date) ===" > "$report_file"
    echo "" >> "$report_file"
    
    # System Information
    echo "=== System Information ===" >> "$report_file"
    uname -a >> "$report_file"
    echo "" >> "$report_file"
    
    # CPU Information
    echo "=== CPU Information ===" >> "$report_file"
    lscpu >> "$report_file"
    echo "" >> "$report_file"
    
    # Memory Information
    echo "=== Memory Information ===" >> "$report_file"
    free -h >> "$report_file"
    echo "" >> "$report_file"
    
    # Disk Usage
    echo "=== Disk Usage ===" >> "$report_file"
    df -h >> "$report_file"
    echo "" >> "$report_file"
    
    # Network Information
    echo "=== Network Information ===" >> "$report_file"
    ip addr >> "$report_file"
    echo "" >> "$report_file"
    
    # Running Services
    echo "=== Running Services ===" >> "$report_file"
    systemctl list-units --type=service --state=running >> "$report_file"
    echo "" >> "$report_file"
    
    # Recent Log Entries
    echo "=== Recent System Logs ===" >> "$report_file"
    journalctl -n 50 >> "$report_file"
    echo "" >> "$report_file"
    
    # Security Information
    echo "=== Security Information ===" >> "$report_file"
    last -n 10 >> "$report_file"
    echo "" >> "$report_file"
    
    echo "Report generated successfully: $report_file"
}

# Create report directory if it doesn't exist
mkdir -p "$REPORT_DIR"

# Generate report
generate_report
```

## Usage Instructions

1. **System Health Monitor**
   - Monitors CPU, memory, and disk usage
   - Logs warnings when thresholds are exceeded
   - Run as: `./system_health.sh`

2. **Log File Analyzer**
   - Analyzes log files for patterns
   - Generates detailed reports
   - Run as: `./log_analyzer.sh`

3. **Backup Automation Script**
   - Automates system backups
   - Implements backup rotation
   - Run as: `./backup_automation.sh`

4. **Network Port Scanner**
   - Scans network ports
   - Identifies running services
   - Run as: `./port_scanner.sh <host>`

5. **User Management Tool**
   - Manages user accounts
   - Handles user creation and deletion
   - Run as: `./user_management.sh {create|delete|list} [username] [password]`

6. **Process Manager**
   - Monitors and manages processes
   - Provides process information
   - Run as: `./process_manager.sh {list|kill|monitor} [pid] [interval]`

7. **File System Monitor**
   - Monitors file system changes
   - Logs file operations
   - Run as: `./filesystem_monitor.sh`

8. **System Update Manager**
   - Manages system updates
   - Sends email notifications
   - Run as: `./update_manager.sh {check|install}`

9. **Network Traffic Analyzer**
   - Monitors network traffic
   - Detects high traffic patterns
   - Run as: `./traffic_analyzer.sh`

10. **System Report Generator**
    - Generates comprehensive system reports
    - Includes system information and logs
    - Run as: `./system_report.sh`

## Best Practices

1. Always review and customize scripts before use
2. Set appropriate permissions: `chmod +x script.sh`
3. Test scripts in a safe environment first
4. Keep scripts updated and maintained
5. Implement proper error handling
6. Use logging for important operations
7. Follow security best practices
8. Document script usage and configuration
9. Implement proper backup procedures
10. Monitor script execution and performance 