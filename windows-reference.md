# Windows Server Administration Reference

## 1. System Information

### Hardware Information
```powershell
# System Information
systeminfo
Get-WmiObject Win32_ComputerSystem
Get-WmiObject Win32_Processor
Get-WmiObject Win32_PhysicalMemory

# Disk Information
Get-WmiObject Win32_LogicalDisk
Get-WmiObject Win32_DiskDrive
Get-PSDrive
```

### System Status
```powershell
# System Uptime
Get-CimInstance -ClassName Win32_OperatingSystem | Select-Object LastBootUpTime
net statistics server

# Process Information
Get-Process
Get-Service
tasklist
```

## 2. Disk Management

### Disk Operations
```powershell
# List Disks
Get-Disk
Get-Partition
Get-Volume

# Initialize Disk
Initialize-Disk -Number 1
New-Partition -DiskNumber 1 -Size 100GB -AssignDriveLetter
Format-Volume -DriveLetter D -FileSystem NTFS -NewFileSystemLabel "Data"
```

### Storage Spaces
```powershell
# Create Storage Pool
New-StoragePool -FriendlyName "StoragePool1" -StorageSubsystemFriendlyName "Storage Spaces*" -PhysicalDisks (Get-PhysicalDisk)

# Create Virtual Disk
New-VirtualDisk -StoragePoolFriendlyName "StoragePool1" -FriendlyName "VirtualDisk1" -Size 100GB -ResiliencySettingName Simple
```

## 3. User and Group Management

### User Operations
```powershell
# Create User
New-LocalUser -Name "username" -Password (ConvertTo-SecureString "password" -AsPlainText -Force)
Add-LocalGroupMember -Group "Users" -Member "username"

# Modify User
Set-LocalUser -Name "username" -Password (ConvertTo-SecureString "newpassword" -AsPlainText -Force)
Disable-LocalUser -Name "username"
Enable-LocalUser -Name "username"

# Delete User
Remove-LocalUser -Name "username"
```

### Group Operations
```powershell
# Create Group
New-LocalGroup -Name "groupname"

# Add User to Group
Add-LocalGroupMember -Group "groupname" -Member "username"

# Remove User from Group
Remove-LocalGroupMember -Group "groupname" -Member "username"
```

## 4. Active Directory

### User Management
```powershell
# Create AD User
New-ADUser -Name "username" -AccountPassword (ConvertTo-SecureString "password" -AsPlainText -Force) -Enabled $true

# Modify AD User
Set-ADUser -Identity "username" -Department "IT"
Enable-ADAccount -Identity "username"
Disable-ADAccount -Identity "username"

# Delete AD User
Remove-ADUser -Identity "username"
```

### Group Management
```powershell
# Create AD Group
New-ADGroup -Name "groupname" -GroupScope Global -GroupCategory Security

# Add User to AD Group
Add-ADGroupMember -Identity "groupname" -Members "username"

# Remove User from AD Group
Remove-ADGroupMember -Identity "groupname" -Members "username"
```

## 5. Service Management

### Windows Services
```powershell
# Service Status
Get-Service
Get-Service -Name "servicename"

# Service Control
Start-Service -Name "servicename"
Stop-Service -Name "servicename"
Restart-Service -Name "servicename"

# Service Configuration
Set-Service -Name "servicename" -StartupType Automatic
Set-Service -Name "servicename" -StartupType Manual
```

### Service Dependencies
```powershell
# View Dependencies
Get-Service -Name "servicename" -DependentServices
Get-Service -Name "servicename" -RequiredServices
```

## 6. Network Configuration

### Network Interfaces
```powershell
# Interface Status
Get-NetAdapter
Get-NetIPAddress
Get-NetRoute

# Configure Interface
New-NetIPAddress -InterfaceIndex 12 -IPAddress 192.168.1.100 -PrefixLength 24 -DefaultGateway 192.168.1.1
Set-DnsClientServerAddress -InterfaceIndex 12 -ServerAddresses ("8.8.8.8","8.8.4.4")
```

### Network Services
```powershell
# DNS Configuration
Get-DnsClientServerAddress
Set-DnsClientServerAddress -InterfaceIndex 12 -ServerAddresses ("8.8.8.8","8.8.4.4")

# DHCP Configuration
Get-DhcpServerv4Scope
Add-DhcpServerv4Scope -Name "Scope1" -StartRange 192.168.1.100 -EndRange 192.168.1.200 -SubnetMask 255.255.255.0
```

## 7. Security

### Windows Firewall
```powershell
# Firewall Status
Get-NetFirewallProfile
Get-NetFirewallRule

# Configure Firewall
New-NetFirewallRule -DisplayName "Allow Port 80" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow
Remove-NetFirewallRule -DisplayName "Allow Port 80"
```

### Windows Defender
```powershell
# Defender Status
Get-MpComputerStatus
Get-MpThreatDetection

# Configure Defender
Set-MpPreference -DisableRealtimeMonitoring $false
Update-MpSignature
```

## 8. Log Management

### Event Logs
```powershell
# View Logs
Get-EventLog -LogName System
Get-EventLog -LogName Application
Get-EventLog -LogName Security

# Filter Logs
Get-EventLog -LogName System -EntryType Error
Get-EventLog -LogName System -After (Get-Date).AddDays(-1)
```

### Log Export
```powershell
# Export Logs
Get-EventLog -LogName System | Export-Csv -Path "C:\logs\system.csv"
Get-EventLog -LogName Security | Export-Csv -Path "C:\logs\security.csv"
```

## 9. Backup and Recovery

### Windows Backup
```powershell
# Configure Backup
wbadmin start backup -backupTarget:E: -include:C:,D: -allCritical
wbadmin get status

# Restore Backup
wbadmin start recovery -version:MM/DD/YYYY-HH:MM -itemType:Volume -items:C: -recursive
```

### System Restore
```powershell
# Create Restore Point
Checkpoint-Computer -Description "Before Update" -RestorePointType "APPLICATION_INSTALL"

# List Restore Points
Get-ComputerRestorePoint
```

## 10. Performance Monitoring

### System Performance
```powershell
# CPU Usage
Get-Counter '\Processor(_Total)\% Processor Time'
Get-Counter '\Processor(_Total)\% User Time'

# Memory Usage
Get-Counter '\Memory\Available MBytes'
Get-Counter '\Memory\% Committed Bytes In Use'

# Disk Usage
Get-Counter '\PhysicalDisk(_Total)\% Disk Time'
Get-Counter '\PhysicalDisk(_Total)\Disk Reads/sec'
```

### Performance Logs
```powershell
# Create Data Collector Set
New-DataCollectorSet -Name "SystemPerformance" -XmlTemplate (Get-Content -Path "C:\perf.xml")

# Start Collection
Start-DataCollectorSet -Name "SystemPerformance"
```

## 11. Troubleshooting

### System Issues
```powershell
# Check System Health
Test-NetConnection
Test-Path
Test-WSMan

# Check Services
Get-Service | Where-Object {$_.Status -eq "Stopped"}
Get-EventLog -LogName System -EntryType Error -Newest 10
```

### Network Issues
```powershell
# Network Diagnostics
Test-NetConnection -ComputerName server
Test-NetConnection -ComputerName server -Port 80
Resolve-DnsName -Name server
```

## 12. Automation

### PowerShell Scripts
```powershell
# System Health Check
$health = @{
    CPU = Get-Counter '\Processor(_Total)\% Processor Time'
    Memory = Get-Counter '\Memory\Available MBytes'
    Disk = Get-Counter '\PhysicalDisk(_Total)\% Disk Time'
}
$health | Format-List
```

### Scheduled Tasks
```powershell
# Create Scheduled Task
$action = New-ScheduledTaskAction -Execute "PowerShell.exe" -Argument "-File C:\Scripts\backup.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 2am
Register-ScheduledTask -TaskName "DailyBackup" -Action $action -Trigger $trigger
```

## 13. Security Hardening

### System Hardening
```powershell
# Disable Unused Services
Get-Service | Where-Object {$_.StartType -eq "Automatic"} | Set-Service -StartupType Manual

# Configure Security Policy
secedit /export /cfg C:\secpol.cfg
notepad C:\secpol.cfg
secedit /configure /db C:\Windows\security\local.sdb /cfg C:\secpol.cfg
```

### User Security
```powershell
# Password Policy
net accounts
net accounts /minpwlen:12
net accounts /maxpwage:90
```

## 14. Documentation

### System Documentation
```powershell
# Create Documentation
New-Item -Path "C:\SystemDocs" -ItemType Directory
Get-Service | Export-Csv -Path "C:\SystemDocs\services.csv"
Get-NetAdapter | Export-Csv -Path "C:\SystemDocs\network.csv"
```

### Configuration Backups
```powershell
# Backup Configurations
Copy-Item "C:\Windows\System32\drivers\etc\hosts" "C:\Backup\hosts"
Copy-Item "C:\Windows\System32\drivers\etc\services" "C:\Backup\services"
```

## 15. Remote Management

### Remote Access
```powershell
# Enable Remote Desktop
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -Name "fDenyTSConnections" -Value 0
Enable-NetFirewallRule -DisplayGroup "Remote Desktop"

# Configure WinRM
Enable-PSRemoting -Force
Set-Item WSMan:\localhost\Client\TrustedHosts -Value "*"
```

### Remote Commands
```powershell
# Execute Remote Command
Invoke-Command -ComputerName server -ScriptBlock { Get-Service }
Enter-PSSession -ComputerName server
``` 