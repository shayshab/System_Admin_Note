#!/bin/bash

# System Health Monitor Configuration
THRESHOLD_CPU=80
THRESHOLD_MEMORY=85
THRESHOLD_DISK=90
LOG_FILE="/var/log/system_health.log"
CHECK_INTERVAL=300  # 5 minutes

# Log Analyzer Configuration
LOG_DIR="/var/log"
REPORT_DIR="/var/log/reports"
PATTERNS=("ERROR" "WARNING" "CRITICAL" "Failed")

# Backup Configuration
BACKUP_DIR="/backup"
SOURCE_DIRS=("/etc" "/home" "/var/www")
RETENTION_DAYS=7
COMPRESSION_LEVEL=9

# Network Scanner Configuration
DEFAULT_START_PORT=1
DEFAULT_END_PORT=1024
SCAN_TIMEOUT=1

# User Management Configuration
DEFAULT_SHELL="/bin/bash"
DEFAULT_GROUPS=("users" "sudo")
SSH_KEY_DIR="/home/%USER%/.ssh"

# Process Manager Configuration
DEFAULT_MONITOR_INTERVAL=5
KILL_TIMEOUT=30

# File System Monitor Configuration
WATCH_DIR="/var/www"
FS_LOG_FILE="/var/log/filesystem_changes.log"
IGNORE_PATTERNS=("*.tmp" "*.log" "*.swp")

# Update Manager Configuration
UPDATE_LOG_FILE="/var/log/update_manager.log"
MAIL_RECIPIENT="admin@example.com"
AUTO_UPDATE=false

# Network Traffic Analyzer Configuration
INTERFACE="eth0"
TRAFFIC_LOG_FILE="/var/log/traffic_analysis.log"
TRAFFIC_THRESHOLD=1000  # KB/s

# System Report Configuration
REPORT_DIR="/var/log/system_reports"
REPORT_RETENTION_DAYS=30

# Email Configuration
SMTP_SERVER="smtp.example.com"
SMTP_PORT=587
SMTP_USER="notifications@example.com"
SMTP_PASS="your-password-here"
EMAIL_FROM="System Admin <notifications@example.com>"

# Security Configuration
ENCRYPT_BACKUPS=true
BACKUP_ENCRYPTION_KEY="your-encryption-key"
LOG_ROTATION=true
MAX_LOG_SIZE=100M
MAX_LOG_FILES=10

# Notification Configuration
ENABLE_EMAIL_NOTIFICATIONS=true
ENABLE_SLACK_NOTIFICATIONS=false
SLACK_WEBHOOK_URL="https://hooks.slack.com/services/your-webhook-url"
ENABLE_TELEGRAM_NOTIFICATIONS=false
TELEGRAM_BOT_TOKEN="your-bot-token"
TELEGRAM_CHAT_ID="your-chat-id" 