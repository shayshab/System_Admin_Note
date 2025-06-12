# System Administration Quick Reference Notes

## 1. Essential Commands

### Linux Commands
```bash
# System Information
uname -a                    # System information
df -h                      # Disk space usage
free -h                    # Memory usage
top                        # Process monitor
htop                       # Interactive process viewer
ps aux                     # List all processes
systemctl status           # Service status
journalctl                 # System logs

# User Management
useradd username           # Add user
passwd username            # Set password
usermod -aG group user     # Add user to group
chown user:group file      # Change ownership
chmod 755 file            # Change permissions

# Network
ip addr                    # Network interfaces
netstat -tulpn            # Network connections
ping host                 # Test connectivity
traceroute host           # Trace network path
ss -tulpn                 # Socket statistics
```

### Windows Commands
```powershell
# System Information
systeminfo                 # System information
tasklist                  # List processes
taskkill /PID pid         # Kill process
netstat -ano              # Network connections
ipconfig /all             # Network configuration

# User Management
net user                  # List users
net user username /add    # Add user
net localgroup            # List groups
net localgroup group user /add  # Add user to group
```

## 2. Common Ports
```
20, 21    - FTP
22        - SSH
23        - Telnet
25        - SMTP
53        - DNS
80        - HTTP
110       - POP3
143       - IMAP
443       - HTTPS
3306      - MySQL
3389      - RDP
5432      - PostgreSQL
```

## 3. File Permissions (Linux)
```
Permission  |  Binary  |  Octal
-----------|----------|--------
---        |  000     |  0
--x        |  001     |  1
-w-        |  010     |  2
-wx        |  011     |  3
r--        |  100     |  4
r-x        |  101     |  5
rw-        |  110     |  6
rwx        |  111     |  7
```

## 4. Common Services

### Web Servers
```bash
# Apache
systemctl start httpd
systemctl status httpd
apache2ctl -t            # Test config
apache2ctl -S            # Virtual hosts

# Nginx
systemctl start nginx
systemctl status nginx
nginx -t                 # Test config
nginx -T                 # Show config
```

### Database Servers
```bash
# MySQL
systemctl start mysqld
mysql -u root -p
SHOW DATABASES;
SHOW TABLES;

# PostgreSQL
systemctl start postgresql
psql -U postgres
\l                      # List databases
\dt                     # List tables
```

## 5. Backup Commands

### Linux
```bash
# Tar
tar -czvf backup.tar.gz /path/to/backup
tar -xzvf backup.tar.gz

# Rsync
rsync -avz /source/ /destination/
rsync -avz -e ssh user@host:/source/ /destination/

# DD
dd if=/dev/sda of=/path/to/backup.img bs=4M
```

### Windows
```powershell
# Robocopy
robocopy C:\source D:\backup /E /Z /R:1 /W:1

# Windows Backup
wbadmin start backup -backupTarget:E: -include:C:,D: -allCritical
```

## 6. Monitoring Commands

### System Resources
```bash
# CPU
mpstat 1                # CPU stats every second
vmstat 1                # Virtual memory stats
iostat 1                # I/O stats

# Memory
free -m                 # Memory in MB
vmstat -s              # Virtual memory stats
cat /proc/meminfo      # Detailed memory info

# Disk
iostat -x 1            # Disk I/O stats
iotop                  # I/O by process
df -i                  # Inode usage
```

### Network Monitoring
```bash
# Bandwidth
iftop                   # Interface bandwidth
nethogs                # Bandwidth by process
iperf3                 # Network performance

# Connections
netstat -tulpn         # Active connections
ss -s                  # Socket statistics
lsof -i               # Open network files
```

## 7. Security Commands

### Firewall
```bash
# UFW (Ubuntu)
ufw status
ufw allow 22/tcp
ufw enable

# Firewalld (RHEL/CentOS)
firewall-cmd --list-all
firewall-cmd --add-port=80/tcp --permanent
firewall-cmd --reload
```

### SSL/TLS
```bash
# Generate CSR
openssl req -new -newkey rsa:2048 -nodes -keyout server.key -out server.csr

# Check Certificate
openssl x509 -in cert.pem -text -noout

# Test SSL
openssl s_client -connect host:443
```

## 8. Log Files

### Linux
```
/var/log/syslog        # System logs
/var/log/auth.log      # Authentication logs
/var/log/nginx/        # Nginx logs
/var/log/apache2/      # Apache logs
/var/log/mysql/        # MySQL logs
/var/log/audit/        # Audit logs
```

### Windows
```
C:\Windows\System32\winevt\Logs\System.evtx
C:\Windows\System32\winevt\Logs\Application.evtx
C:\Windows\System32\winevt\Logs\Security.evtx
```

## 9. Common Issues and Solutions

### High CPU Usage
```bash
# Find process
top
ps aux | sort -nrk 3,3 | head -n 10

# Check load average
uptime
cat /proc/loadavg
```

### High Memory Usage
```bash
# Check memory
free -h
vmstat 1

# Find memory hogs
ps aux | sort -nrk 4,4 | head -n 10
```

### Disk Space Issues
```bash
# Find large files
find / -type f -size +100M
du -sh /* | sort -hr

# Check inode usage
df -i
find / -type f | wc -l
```

## 10. Emergency Procedures

### System Recovery
```bash
# Boot into recovery mode
# Edit GRUB menu, add 'single' or 'init=/bin/bash'

# Check filesystem
fsck /dev/sda1

# Mount filesystem
mount -o remount,rw /
```

### Network Recovery
```bash
# Reset network
systemctl restart NetworkManager
ip link set dev eth0 down
ip link set dev eth0 up

# Check DNS
cat /etc/resolv.conf
dig @8.8.8.8 google.com
```

## 11. Performance Tuning

### System Limits
```bash
# Check limits
ulimit -a
cat /proc/sys/fs/file-max

# Set limits
ulimit -n 65535
sysctl -w fs.file-max=65535
```

### Kernel Parameters
```bash
# View parameters
sysctl -a

# Set parameters
sysctl -w net.core.somaxconn=65535
echo "net.core.somaxconn=65535" >> /etc/sysctl.conf
```

## 12. Useful Scripts

### System Health Check
```bash
#!/bin/bash
echo "=== System Health Check ==="
echo "CPU Load:"
uptime
echo "Memory Usage:"
free -h
echo "Disk Usage:"
df -h
echo "Top Processes:"
ps aux | sort -nrk 3,3 | head -n 5
```

### Backup Script
```bash
#!/bin/bash
BACKUP_DIR="/backup"
DATE=$(date +%Y%m%d)
tar -czf $BACKUP_DIR/backup-$DATE.tar.gz /path/to/backup
find $BACKUP_DIR -type f -mtime +7 -delete
```

## 13. Security Checklist

### Daily Checks
- [ ] Review system logs
- [ ] Check failed login attempts
- [ ] Monitor disk space
- [ ] Review running processes
- [ ] Check network connections
- [ ] Verify backup status

### Weekly Checks
- [ ] Update system packages
- [ ] Review security logs
- [ ] Check user accounts
- [ ] Verify firewall rules
- [ ] Test backup restoration
- [ ] Review performance metrics

### Monthly Checks
- [ ] Security patches
- [ ] Password changes
- [ ] Access review
- [ ] Backup verification
- [ ] Performance tuning
- [ ] Documentation update 