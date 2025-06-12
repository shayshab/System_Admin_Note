# Linux System Administration Reference

## 1. System Information

### Hardware Information
```bash
# CPU Information
lscpu
cat /proc/cpuinfo
nproc

# Memory Information
free -h
cat /proc/meminfo
vmstat

# Disk Information
lsblk
fdisk -l
df -h
```

### System Status
```bash
# System Uptime
uptime
w
who

# System Load
top
htop
mpstat

# Process Information
ps aux
pstree
pidof process_name
```

## 2. File System Management

### Disk Operations
```bash
# Partition Management
fdisk /dev/sda
parted /dev/sda
gdisk /dev/sda

# Format Partitions
mkfs.ext4 /dev/sda1
mkfs.xfs /dev/sda1
mkfs.btrfs /dev/sda1

# Mount Points
mount /dev/sda1 /mnt
umount /mnt
mount -a
```

### LVM Operations
```bash
# Physical Volume
pvcreate /dev/sda1
pvdisplay
pvremove /dev/sda1

# Volume Group
vgcreate vg_name /dev/sda1
vgdisplay
vgextend vg_name /dev/sdb1

# Logical Volume
lvcreate -L 10G -n lv_name vg_name
lvdisplay
lvextend -L +5G /dev/vg_name/lv_name
```

## 3. User and Group Management

### User Operations
```bash
# Create User
useradd -m username
useradd -m -s /bin/bash username
useradd -m -g groupname username

# Modify User
usermod -aG groupname username
usermod -s /bin/bash username
usermod -L username  # Lock user
usermod -U username  # Unlock user

# Delete User
userdel username
userdel -r username  # Remove home directory
```

### Group Operations
```bash
# Create Group
groupadd groupname

# Modify Group
groupmod -n newname oldname
groupmod -g 1000 groupname

# Delete Group
groupdel groupname
```

## 4. Package Management

### Debian/Ubuntu
```bash
# Update Package Lists
apt update
apt-get update

# Install Packages
apt install package_name
apt-get install package_name

# Remove Packages
apt remove package_name
apt purge package_name

# Search Packages
apt search keyword
apt-cache search keyword
```

### RHEL/CentOS
```bash
# Update Package Lists
yum update
dnf update

# Install Packages
yum install package_name
dnf install package_name

# Remove Packages
yum remove package_name
dnf remove package_name

# Search Packages
yum search keyword
dnf search keyword
```

## 5. Service Management

### Systemd
```bash
# Service Status
systemctl status service_name
systemctl is-active service_name
systemctl is-enabled service_name

# Service Control
systemctl start service_name
systemctl stop service_name
systemctl restart service_name
systemctl reload service_name

# Service Management
systemctl enable service_name
systemctl disable service_name
systemctl mask service_name
systemctl unmask service_name
```

### Service Files
```bash
# Create Service
nano /etc/systemd/system/service_name.service

# Service File Template
[Unit]
Description=Service Description
After=network.target

[Service]
Type=simple
User=username
ExecStart=/path/to/command
Restart=always

[Install]
WantedBy=multi-user.target
```

## 6. Network Configuration

### Network Interfaces
```bash
# Interface Status
ip addr
ip link
nmcli device show

# Configure Interface
ip addr add 192.168.1.100/24 dev eth0
ip link set eth0 up
ip route add default via 192.168.1.1
```

### Network Services
```bash
# DNS Configuration
cat /etc/resolv.conf
nano /etc/resolv.conf

# Host Configuration
cat /etc/hosts
nano /etc/hosts
```

## 7. Security

### Firewall
```bash
# UFW (Ubuntu)
ufw status
ufw allow 22/tcp
ufw deny 23/tcp
ufw enable

# Firewalld (RHEL/CentOS)
firewall-cmd --list-all
firewall-cmd --add-port=80/tcp --permanent
firewall-cmd --remove-port=23/tcp --permanent
firewall-cmd --reload
```

### SELinux
```bash
# SELinux Status
getenforce
sestatus

# SELinux Context
ls -Z
chcon -t httpd_sys_content_t /var/www/html
restorecon -R /var/www/html
```

## 8. Log Management

### System Logs
```bash
# View Logs
journalctl
journalctl -f
journalctl -u service_name

# Log Rotation
logrotate -d /etc/logrotate.conf
logrotate -f /etc/logrotate.d/service
```

### Log Files
```bash
# Common Log Locations
/var/log/syslog
/var/log/auth.log
/var/log/dmesg
/var/log/secure
```

## 9. Backup and Recovery

### Backup Tools
```bash
# Tar Archives
tar -czvf backup.tar.gz /path/to/backup
tar -xzvf backup.tar.gz

# Rsync
rsync -avz /source/ /destination/
rsync -avz -e ssh user@host:/source/ /destination/

# DD
dd if=/dev/sda of=/path/to/backup.img bs=4M
```

### Recovery Procedures
```bash
# Boot Recovery
# Edit GRUB menu, add 'single' or 'init=/bin/bash'

# Filesystem Check
fsck /dev/sda1
e2fsck /dev/sda1

# Mount Recovery
mount -o remount,rw /
mount -t ext4 /dev/sda1 /mnt
```

## 10. Performance Tuning

### System Limits
```bash
# View Limits
ulimit -a
cat /proc/sys/fs/file-max

# Set Limits
ulimit -n 65535
sysctl -w fs.file-max=65535
```

### Kernel Parameters
```bash
# View Parameters
sysctl -a
cat /proc/sys/net/core/somaxconn

# Set Parameters
sysctl -w net.core.somaxconn=65535
echo "net.core.somaxconn=65535" >> /etc/sysctl.conf
```

## 11. Monitoring

### System Monitoring
```bash
# CPU Monitoring
mpstat 1
vmstat 1
iostat 1

# Memory Monitoring
free -m
vmstat -s
cat /proc/meminfo

# Disk Monitoring
iostat -x 1
iotop
df -i
```

### Network Monitoring
```bash
# Bandwidth
iftop
nethogs
iperf3

# Connections
netstat -tulpn
ss -s
lsof -i
```

## 12. Troubleshooting

### System Issues
```bash
# High CPU Usage
top
ps aux | sort -nrk 3,3 | head -n 10

# High Memory Usage
free -h
ps aux | sort -nrk 4,4 | head -n 10

# Disk Space Issues
df -h
du -sh /* | sort -hr
```

### Network Issues
```bash
# Connectivity
ping host
traceroute host
mtr host

# DNS Issues
dig @8.8.8.8 domain.com
nslookup domain.com
host domain.com
```

## 13. Automation

### Shell Scripts
```bash
#!/bin/bash
# System Health Check
echo "=== System Health Check ==="
echo "CPU Load:"
uptime
echo "Memory Usage:"
free -h
echo "Disk Usage:"
df -h
```

### Cron Jobs
```bash
# Edit Crontab
crontab -e

# Common Cron Patterns
0 * * * *     # Every hour
0 0 * * *     # Every day at midnight
0 0 * * 0     # Every Sunday at midnight
*/15 * * * *  # Every 15 minutes
```

## 14. Security Hardening

### System Hardening
```bash
# Disable Unused Services
systemctl disable service_name
systemctl mask service_name

# Secure SSH
nano /etc/ssh/sshd_config
# Set PermitRootLogin no
# Set PasswordAuthentication no
```

### File Permissions
```bash
# Set Permissions
chmod 755 file
chmod -R 755 directory
chown user:group file
chown -R user:group directory
```

## 15. Documentation

### System Documentation
```bash
# Create Documentation
mkdir -p /var/log/system-docs
nano /var/log/system-docs/system-info.txt

# Document Changes
echo "$(date): Changed configuration" >> /var/log/system-docs/changes.log
```

### Configuration Backups
```bash
# Backup Configs
cp /etc/ssh/sshd_config /etc/ssh/sshd_config.backup
cp /etc/nginx/nginx.conf /etc/nginx/nginx.conf.backup
``` 
 