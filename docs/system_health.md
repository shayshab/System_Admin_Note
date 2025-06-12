# System Health Monitor

## Overview
The System Health Monitor is a Bash script that continuously monitors system resources (CPU, memory, and disk usage) and logs warnings when thresholds are exceeded.

## Features
- Real-time monitoring of CPU usage
- Memory usage tracking
- Disk space monitoring
- Configurable thresholds
- Automatic logging
- Email notifications

## Requirements
- Bash shell
- `top` command
- `free` command
- `df` command
- Mail utilities (for notifications)

## Configuration
Edit `config/config.sh` to modify:
- Threshold values
- Log file location
- Check interval
- Email settings

## Usage
```bash
./scripts/system_health.sh
```

## Output
The script generates logs in the configured log file with the following format:
```
YYYY-MM-DD HH:MM:SS - WARNING: High CPU usage detected: XX%
YYYY-MM-DD HH:MM:SS - WARNING: High memory usage detected: XX%
YYYY-MM-DD HH:MM:SS - WARNING: High disk usage detected: XX%
```

## Examples

### Basic Usage
```bash
./scripts/system_health.sh
```

### Custom Configuration
```bash
# Edit config/config.sh
THRESHOLD_CPU=70
THRESHOLD_MEMORY=80
THRESHOLD_DISK=85
CHECK_INTERVAL=600  # 10 minutes
```

## Troubleshooting

### Common Issues
1. **Script not running**
   - Check if the script has execute permissions
   - Verify that required commands are available
   - Check system logs for errors

2. **No notifications received**
   - Verify email configuration
   - Check mail server settings
   - Ensure thresholds are set correctly

3. **High resource usage**
   - Adjust check interval
   - Review threshold values
   - Check for system issues

## Best Practices
1. Set appropriate thresholds based on your system
2. Regular log rotation
3. Monitor log file size
4. Regular script maintenance
5. Keep configuration updated

## Security Considerations
1. Secure log file permissions
2. Protect configuration file
3. Use secure email settings
4. Regular security audits

## Contributing
Feel free to submit issues and enhancement requests! 