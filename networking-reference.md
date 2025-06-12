# Networking Reference Guide

## 1. Network Fundamentals

### OSI Model
```
Layer 7 - Application    (HTTP, FTP, SMTP)
Layer 6 - Presentation   (SSL, TLS)
Layer 5 - Session       (NetBIOS, RPC)
Layer 4 - Transport     (TCP, UDP)
Layer 3 - Network       (IP, ICMP)
Layer 2 - Data Link     (Ethernet, MAC)
Layer 1 - Physical      (Cables, Hubs)
```

### TCP/IP Model
```
Application Layer    (HTTP, FTP, SMTP)
Transport Layer     (TCP, UDP)
Internet Layer      (IP, ICMP)
Network Access      (Ethernet, MAC)
```

## 2. IP Addressing

### IPv4
```
Class A: 1.0.0.0 to 126.255.255.255
Class B: 128.0.0.0 to 191.255.255.255
Class C: 192.0.0.0 to 223.255.255.255
Class D: 224.0.0.0 to 239.255.255.255 (Multicast)
Class E: 240.0.0.0 to 255.255.255.255 (Reserved)
```

### Subnetting
```
/24 = 255.255.255.0     (256 addresses)
/25 = 255.255.255.128   (128 addresses)
/26 = 255.255.255.192   (64 addresses)
/27 = 255.255.255.224   (32 addresses)
/28 = 255.255.255.240   (16 addresses)
/29 = 255.255.255.248   (8 addresses)
/30 = 255.255.255.252   (4 addresses)
```

## 3. Common Ports

### Well-Known Ports
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

### Service Ports
```
161, 162  - SNMP
389       - LDAP
636       - LDAPS
1433      - MSSQL
1521      - Oracle
27017     - MongoDB
```

## 4. Network Commands

### Linux
```bash
# Network Interfaces
ip addr
ip link
nmcli device show

# Network Configuration
ip addr add 192.168.1.100/24 dev eth0
ip route add default via 192.168.1.1

# Network Testing
ping host
traceroute host
mtr host
```

### Windows
```powershell
# Network Interfaces
ipconfig /all
netsh interface show interface

# Network Configuration
netsh interface ip set address "Ethernet" static 192.168.1.100 255.255.255.0 192.168.1.1
netsh interface ip set dns "Ethernet" static 8.8.8.8

# Network Testing
ping host
tracert host
pathping host
```

## 5. DNS

### DNS Records
```
A        - IPv4 address
AAAA     - IPv6 address
CNAME    - Canonical name
MX       - Mail exchange
TXT      - Text record
NS       - Name server
PTR      - Pointer record
SOA      - Start of authority
```

### DNS Commands
```bash
# Linux
dig @8.8.8.8 domain.com
nslookup domain.com
host domain.com

# Windows
nslookup domain.com
Resolve-DnsName domain.com
```

## 6. DHCP

### DHCP Configuration
```bash
# Linux (ISC DHCP)
subnet 192.168.1.0 netmask 255.255.255.0 {
    range 192.168.1.100 192.168.1.200;
    option routers 192.168.1.1;
    option domain-name-servers 8.8.8.8, 8.8.4.4;
}

# Windows
Add-DhcpServerv4Scope -Name "Scope1" -StartRange 192.168.1.100 -EndRange 192.168.1.200 -SubnetMask 255.255.255.0
```

## 7. Routing

### Static Routes
```bash
# Linux
ip route add 192.168.2.0/24 via 192.168.1.1
ip route add default via 192.168.1.1

# Windows
route add 192.168.2.0 mask 255.255.255.0 192.168.1.1
route add 0.0.0.0 mask 0.0.0.0 192.168.1.1
```

### Routing Tables
```bash
# Linux
ip route show
netstat -rn

# Windows
route print
Get-NetRoute
```

## 8. Firewall

### Linux (iptables)
```bash
# Allow Port
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Allow IP
iptables -A INPUT -s 192.168.1.100 -j ACCEPT

# Save Rules
iptables-save > /etc/iptables/rules.v4
```

### Windows
```powershell
# Allow Port
New-NetFirewallRule -DisplayName "Allow Port 80" -Direction Inbound -Protocol TCP -LocalPort 80 -Action Allow

# Allow Program
New-NetFirewallRule -DisplayName "Allow Program" -Direction Inbound -Program "C:\Program Files\App\app.exe" -Action Allow
```

## 9. VPN

### OpenVPN
```bash
# Server Configuration
port 1194
proto udp
dev tun
ca ca.crt
cert server.crt
key server.key
dh dh2048.pem
server 10.8.0.0 255.255.255.0
push "redirect-gateway def1"
push "dhcp-option DNS 8.8.8.8"
```

### L2TP/IPsec
```bash
# Server Configuration
ipsec.conf:
conn %default
    ikelifetime=60m
    keylife=20m
    rekeymargin=3m
    keyingtries=1
    keyexchange=ikev2
    authby=secret
    ike=aes256-sha2_256-modp2048!
    esp=aes256-sha2_256!
```

## 10. Network Monitoring

### Bandwidth Monitoring
```bash
# Linux
iftop
nethogs
iperf3

# Windows
netsh interface show interface
Get-NetAdapterStatistics
```

### Connection Monitoring
```bash
# Linux
netstat -tulpn
ss -s
lsof -i

# Windows
netstat -ano
Get-NetTCPConnection
```

## 11. Network Security

### SSL/TLS
```bash
# Generate Certificate
openssl req -new -newkey rsa:2048 -nodes -keyout server.key -out server.csr
openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

# Check Certificate
openssl x509 -in cert.pem -text -noout
openssl s_client -connect host:443
```

### Network Scanning
```bash
# Nmap
nmap -sV host
nmap -p 1-1000 host
nmap -A host

# Security Tools
nmap -sV --script vuln host
nikto -h host
```

## 12. Network Troubleshooting

### Connectivity Issues
```bash
# Check Physical Connection
ip link show
ethtool eth0

# Check IP Configuration
ip addr show
ip route show

# Check DNS
cat /etc/resolv.conf
dig @8.8.8.8 domain.com
```

### Performance Issues
```bash
# Check Bandwidth
iperf3 -c server
iperf3 -s

# Check Latency
ping -c 100 host
mtr host
```

## 13. Network Documentation

### Network Diagrams
```
Physical Topology:
[Router] --- [Switch] --- [Server]
                  |
              [Client]

Logical Topology:
[Internet] --- [Firewall] --- [DMZ] --- [Internal Network]
```

### IP Documentation
```
Network: 192.168.1.0/24
Gateway: 192.168.1.1
DNS: 8.8.8.8, 8.8.4.4
DHCP Range: 192.168.1.100-200
```

## 14. Network Automation

### Configuration Management
```bash
# Ansible
- name: Configure Network
  hosts: network
  tasks:
    - name: Set IP Address
      ios_config:
        lines:
          - ip address 192.168.1.100 255.255.255.0
        parents: interface GigabitEthernet1
```

### Network Scripts
```bash
#!/bin/bash
# Network Health Check
echo "=== Network Health Check ==="
echo "Interface Status:"
ip link show
echo "Routing Table:"
ip route show
echo "DNS Resolution:"
dig @8.8.8.8 google.com
```

## 15. Network Best Practices

### Security
- Use strong passwords
- Enable encryption
- Regular updates
- Access control
- Network segmentation
- Monitoring and logging

### Performance
- Regular maintenance
- Bandwidth monitoring
- QoS implementation
- Load balancing
- Redundancy
- Documentation 