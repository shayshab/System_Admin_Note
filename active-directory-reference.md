# Active Directory and Windows Server Administration Guide

## 1. Active Directory Management

### User Management
```powershell
# List Users
Get-ADUser -Filter *

# Create User
New-ADUser -Name "John Doe" `
    -GivenName "John" `
    -Surname "Doe" `
    -SamAccountName "jdoe" `
    -UserPrincipalName "jdoe@domain.com" `
    -AccountPassword (ConvertTo-SecureString "P@ssw0rd" -AsPlainText -Force) `
    -Enabled $true

# Modify User
Set-ADUser -Identity "jdoe" -Department "IT" -Title "System Administrator"

# Disable User
Disable-ADAccount -Identity "jdoe"

# Delete User
Remove-ADUser -Identity "jdoe" -Confirm:$false
```

### Group Management
```powershell
# List Groups
Get-ADGroup -Filter *

# Create Group
New-ADGroup -Name "IT Staff" `
    -GroupCategory Security `
    -GroupScope Global `
    -Path "OU=Groups,DC=domain,DC=com"

# Add User to Group
Add-ADGroupMember -Identity "IT Staff" -Members "jdoe"

# Remove User from Group
Remove-ADGroupMember -Identity "IT Staff" -Members "jdoe"

# List Group Members
Get-ADGroupMember -Identity "IT Staff"
```

### Organizational Units (OUs)
```powershell
# List OUs
Get-ADOrganizationalUnit -Filter *

# Create OU
New-ADOrganizationalUnit -Name "IT Department" `
    -Path "DC=domain,DC=com"

# Move User to OU
Move-ADObject -Identity "CN=John Doe,CN=Users,DC=domain,DC=com" `
    -TargetPath "OU=IT Department,DC=domain,DC=com"

# Delete OU
Remove-ADOrganizationalUnit -Identity "OU=IT Department,DC=domain,DC=com" `
    -Recursive -Confirm:$false
```

## 2. Group Policy Management

### GPO Creation and Management
```powershell
# List GPOs
Get-GPO -All

# Create GPO
New-GPO -Name "IT Security Policy"

# Link GPO to OU
New-GPLink -Name "IT Security Policy" `
    -Target "OU=IT Department,DC=domain,DC=com"

# Edit GPO
Set-GPRegistryValue -Name "IT Security Policy" `
    -Key "HKLM\Software\Policies\Microsoft\Windows\System" `
    -ValueName "DisableCMD" `
    -Type DWord `
    -Value 1

# Remove GPO
Remove-GPO -Name "IT Security Policy"
```

### GPO Backup and Restore
```powershell
# Backup GPO
Backup-GPO -Name "IT Security Policy" -Path "C:\GPOBackup"

# Restore GPO
Restore-GPO -Name "IT Security Policy" -Path "C:\GPOBackup"

# Import GPO
Import-GPO -BackupId "GUID" -Path "C:\GPOBackup" -TargetName "New GPO Name"
```

## 3. DNS Management

### DNS Records
```powershell
# List DNS Records
Get-DnsServerResourceRecord -ZoneName "domain.com"

# Add A Record
Add-DnsServerResourceRecordA -Name "server" `
    -ZoneName "domain.com" `
    -IPv4Address "192.168.1.100"

# Add CNAME Record
Add-DnsServerResourceRecordCName -Name "www" `
    -ZoneName "domain.com" `
    -HostNameAlias "server.domain.com"

# Add MX Record
Add-DnsServerResourceRecordMX -Name "@" `
    -ZoneName "domain.com" `
    -MailExchange "mail.domain.com" `
    -Preference 10

# Remove Record
Remove-DnsServerResourceRecord -ZoneName "domain.com" `
    -Name "server" `
    -RecordType "A"
```

### DNS Zones
```powershell
# List Zones
Get-DnsServerZone

# Create Zone
Add-DnsServerPrimaryZone -Name "domain.com" `
    -ZoneFile "domain.com.dns"

# Create Reverse Zone
Add-DnsServerPrimaryZone -NetworkID "192.168.1.0/24" `
    -ZoneFile "1.168.192.in-addr.arpa.dns"

# Remove Zone
Remove-DnsServerZone -Name "domain.com" -Force
```

## 4. DHCP Management

### DHCP Scopes
```powershell
# List Scopes
Get-DhcpServerv4Scope

# Create Scope
Add-DhcpServerv4Scope -Name "Main Network" `
    -StartRange "192.168.1.100" `
    -EndRange "192.168.1.200" `
    -SubnetMask "255.255.255.0"

# Set Scope Options
Set-DhcpServerv4OptionValue -ScopeId "192.168.1.0" `
    -DnsServer "192.168.1.1" `
    -Router "192.168.1.1"

# Remove Scope
Remove-DhcpServerv4Scope -ScopeId "192.168.1.0" -Force
```

### DHCP Reservations
```powershell
# List Reservations
Get-DhcpServerv4Reservation -ScopeId "192.168.1.0"

# Add Reservation
Add-DhcpServerv4Reservation -ScopeId "192.168.1.0" `
    -IPAddress "192.168.1.50" `
    -ClientId "00-11-22-33-44-55" `
    -Description "Printer"

# Remove Reservation
Remove-DhcpServerv4Reservation -ScopeId "192.168.1.0" `
    -IPAddress "192.168.1.50"
```

## 5. Certificate Services

### Certificate Management
```powershell
# List Certificates
Get-ChildItem -Path Cert:\LocalMachine\My

# Request Certificate
$cert = New-SelfSignedCertificate `
    -DnsName "server.domain.com" `
    -CertStoreLocation "cert:\LocalMachine\My" `
    -NotAfter (Get-Date).AddYears(1)

# Export Certificate
Export-Certificate -Cert $cert `
    -FilePath "C:\Certificates\server.cer"

# Import Certificate
Import-Certificate -FilePath "C:\Certificates\server.cer" `
    -CertStoreLocation "Cert:\LocalMachine\Root"
```

### Certificate Authority
```powershell
# Install Certificate Authority
Install-WindowsFeature -Name AD-Certificate `
    -IncludeManagementTools

# Configure CA
Install-AdcsCertificationAuthority `
    -CAType EnterpriseRootCA `
    -CryptoProviderName "RSA#Microsoft Software Key Storage Provider" `
    -KeyLength 2048 `
    -HashAlgorithmName SHA256 `
    -ValidityPeriod Years `
    -ValidityPeriodUnits 5
```

## 6. File Services

### File Shares
```powershell
# List Shares
Get-SmbShare

# Create Share
New-SmbShare -Name "Data" `
    -Path "C:\Data" `
    -FullAccess "Domain Admins" `
    -ChangeAccess "IT Staff" `
    -ReadAccess "Domain Users"

# Set Share Permissions
Grant-SmbShareAccess -Name "Data" `
    -AccountName "IT Staff" `
    -AccessRight Full

# Remove Share
Remove-SmbShare -Name "Data" -Force
```

### NTFS Permissions
```powershell
# Get NTFS Permissions
Get-Acl -Path "C:\Data" | Format-List

# Set NTFS Permissions
$acl = Get-Acl -Path "C:\Data"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("IT Staff","FullControl","Allow")
$acl.SetAccessRule($accessRule)
Set-Acl -Path "C:\Data" -AclObject $acl
```

## 7. Windows Server Roles

### Role Management
```powershell
# List Installed Roles
Get-WindowsFeature | Where-Object {$_.Installed -eq $true}

# Install Role
Install-WindowsFeature -Name Web-Server `
    -IncludeManagementTools

# Remove Role
Uninstall-WindowsFeature -Name Web-Server
```

### IIS Management
```powershell
# List Websites
Get-Website

# Create Website
New-Website -Name "MySite" `
    -PhysicalPath "C:\inetpub\wwwroot\mysite" `
    -Port 80

# Start/Stop Website
Start-Website -Name "MySite"
Stop-Website -Name "MySite"

# Remove Website
Remove-Website -Name "MySite"
```

## 8. Windows Server Security

### Security Policies
```powershell
# Get Security Policy
Get-SecurityPolicy

# Set Password Policy
Set-ADDefaultDomainPasswordPolicy `
    -Identity "domain.com" `
    -MinPasswordLength 12 `
    -MaxPasswordAge 90 `
    -MinPasswordAge 1 `
    -PasswordHistoryCount 24

# Set Account Lockout Policy
Set-ADDefaultDomainPasswordPolicy `
    -Identity "domain.com" `
    -LockoutThreshold 5 `
    -LockoutDuration "00:30:00" `
    -LockoutObservationWindow "00:30:00"
```

### Windows Firewall
```powershell
# List Firewall Rules
Get-NetFirewallRule

# Create Firewall Rule
New-NetFirewallRule `
    -DisplayName "Allow Web Traffic" `
    -Direction Inbound `
    -Protocol TCP `
    -LocalPort 80,443 `
    -Action Allow

# Remove Firewall Rule
Remove-NetFirewallRule -DisplayName "Allow Web Traffic"
```

## 9. Windows Server Monitoring

### Event Logs
```powershell
# Get Event Logs
Get-EventLog -LogName System -Newest 10
Get-EventLog -LogName Application -EntryType Error

# Create Custom Event Log
New-EventLog -LogName "CustomLog" -Source "MyApp"

# Write to Event Log
Write-EventLog -LogName "CustomLog" `
    -Source "MyApp" `
    -EventId 1000 `
    -EntryType Information `
    -Message "Application started successfully"
```

### Performance Monitoring
```powershell
# Get Performance Counters
Get-Counter -Counter "\Processor(_Total)\% Processor Time"
Get-Counter -Counter "\Memory\Available MBytes"

# Create Performance Monitor Data Collector
New-DataCollectorSet -Name "ServerPerformance" `
    -Type Performance `
    -PerformanceCounter @("\Processor(_Total)\% Processor Time", "\Memory\Available MBytes")

# Start/Stop Data Collection
Start-DataCollectorSet -Name "ServerPerformance"
Stop-DataCollectorSet -Name "ServerPerformance"
```

## 10. Windows Server Backup

### Backup Management
```powershell
# List Backup Jobs
Get-WBJob

# Create Backup Job
$policy = New-WBPolicy
$volume = Get-WBVolume -VolumePath "C:"
Add-WBVolume -Policy $policy -Volume $volume
Add-WBSystemState -Policy $policy
Add-WBBareMetalRecovery -Policy $policy
Set-WBSchedule -Policy $policy -Schedule "01:00"

# Start Backup
Start-WBBackup -Policy $policy

# Restore from Backup
Start-WBSystemStateRecovery -BackupSet $backupSet
```

### System State Backup
```powershell
# Backup System State
wbadmin start systemstatebackup -backuptarget:E:

# Restore System State
wbadmin start systemstaterecovery -version:MM/DD/YYYY-HH:MM
```

## 11. Windows Server Maintenance

### Windows Updates
```powershell
# Check for Updates
Get-WindowsUpdate

# Install Updates
Install-WindowsUpdate -AcceptAll -AutoReboot

# Remove Updates
Remove-WindowsUpdate -KBArticleID "KB1234567"
```

### Disk Management
```powershell
# List Disks
Get-Disk

# Initialize Disk
Initialize-Disk -Number 1 -PartitionStyle GPT

# Create Partition
New-Partition -DiskNumber 1 -Size 100GB -AssignDriveLetter

# Format Partition
Format-Volume -DriveLetter D -FileSystem NTFS -NewFileSystemLabel "Data"
```

## 12. Windows Server Best Practices

### Security
- Regular security updates
- Strong password policies
- Least privilege access
- Network segmentation
- Regular security audits

### Performance
- Regular maintenance
- Resource monitoring
- Capacity planning
- Regular backups
- Disaster recovery planning

### Documentation
- System documentation
- Change management
- Incident response
- Standard operating procedures
- Regular reviews and updates 