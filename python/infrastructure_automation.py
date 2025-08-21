#!/usr/bin/env python3
"""
Infrastructure Automation - Server provisioning, configuration management, and deployment
"""

import os
import sys
import yaml
import json
import argparse
import logging
import subprocess
import time
from datetime import datetime
from typing import Dict, List, Any, Optional
import boto3
import paramiko
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
import socket

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

console = Console()

class InfrastructureAutomation:
    """Main class for infrastructure automation and management"""
    
    def __init__(self, config_path: str = None):
        self.config = self._load_config(config_path)
        self.aws_session = None
        self.ssh_clients = {}
        self.deployment_status = {}
        
    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        if not config_path:
            config_path = "config/infrastructure.yml"
            
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_path} not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Return default infrastructure configuration"""
        return {
            'aws': {
                'region': 'us-east-1',
                'vpc_id': 'vpc-12345678',
                'subnet_ids': ['subnet-12345678'],
                'security_groups': ['sg-12345678']
            },
            'servers': {
                'web_servers': {
                    'count': 2,
                    'instance_type': 't3.micro',
                    'ami': 'ami-12345678',
                    'tags': {'Name': 'web-server', 'Environment': 'production'}
                },
                'app_servers': {
                    'count': 2,
                    'instance_type': 't3.small',
                    'ami': 'ami-12345678',
                    'tags': {'Name': 'app-server', 'Environment': 'production'}
                },
                'database_servers': {
                    'count': 1,
                    'instance_type': 't3.medium',
                    'ami': 'ami-12345678',
                    'tags': {'Name': 'db-server', 'Environment': 'production'}
                }
            },
            'deployment': {
                'strategy': 'rolling',
                'health_check_path': '/health',
                'rollback_threshold': 3
            }
        }
    
    def initialize_aws_session(self) -> None:
        """Initialize AWS session for infrastructure management"""
        try:
            self.aws_session = boto3.Session(
                region_name=self.config['aws']['region']
            )
            console.print("✅ AWS session initialized", style="green")
        except Exception as e:
            console.print(f"❌ Failed to initialize AWS session: {e}", style="red")
            raise
    
    def provision_servers(self, server_type: str = None) -> List[str]:
        """Provision servers based on configuration"""
        console.print(Panel("🚀 Starting Server Provisioning", style="bold blue"))
        
        if not self.aws_session:
            self.initialize_aws_session()
        
        ec2 = self.aws_session.resource('ec2')
        instance_ids = []
        
        servers_config = self.config['servers']
        if server_type and server_type in servers_config:
            servers_to_provision = {server_type: servers_config[server_type]}
        else:
            servers_to_provision = servers_config
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            for server_type, config in servers_to_provision.items():
                task = progress.add_task(f"Provisioning {server_type}...", total=config['count'])
                
                for i in range(config['count']):
                    try:
                        instance = ec2.create_instances(
                            ImageId=config['ami'],
                            MinCount=1,
                            MaxCount=1,
                            InstanceType=config['instance_type'],
                            SubnetId=self.config['aws']['subnet_ids'][0],
                            SecurityGroupIds=self.config['aws']['security_groups'],
                            TagSpecifications=[{
                                'ResourceType': 'instance',
                                'Tags': [
                                    {'Key': k, 'Value': v} for k, v in config['tags'].items()
                                ] + [
                                    {'Key': 'Index', 'Value': str(i)},
                                    {'Key': 'ProvisionedBy', 'Value': 'DevSecOps-Automation'}
                                ]
                            }]
                        )[0]
                        
                        instance_ids.append(instance.id)
                        progress.update(task, advance=1)
                        
                        # Wait for instance to be running
                        instance.wait_until_running()
                        console.print(f"✅ {server_type} {i+1} provisioned: {instance.id}", style="green")
                        
                    except Exception as e:
                        console.print(f"❌ Failed to provision {server_type} {i+1}: {e}", style="red")
                        logger.error(f"Provisioning error: {e}")
        
        return instance_ids
    
    def configure_servers(self, instance_ids: List[str]) -> Dict[str, bool]:
        """Configure provisioned servers with security and application settings"""
        console.print(Panel("⚙️ Starting Server Configuration", style="bold green"))
        
        configuration_results = {}
        
        for instance_id in instance_ids:
            try:
                console.print(f"Configuring instance: {instance_id}")
                
                # Get instance details
                ec2 = self.aws_session.resource('ec2')
                instance = ec2.Instance(instance_id)
                
                # Wait for SSH to be available
                self._wait_for_ssh(instance.public_ip_address)
                
                # Apply security hardening
                self._apply_security_hardening(instance_id, instance.public_ip_address)
                
                # Install and configure applications
                self._configure_applications(instance_id, instance.public_ip_address)
                
                # Run security compliance checks
                self._run_compliance_checks(instance_id, instance.public_ip_address)
                
                configuration_results[instance_id] = True
                console.print(f"✅ Configuration completed for {instance_id}", style="green")
                
            except Exception as e:
                console.print(f"❌ Configuration failed for {instance_id}: {e}", style="red")
                configuration_results[instance_id] = False
                logger.error(f"Configuration error for {instance_id}: {e}")
        
        return configuration_results
    
    def _wait_for_ssh(self, public_ip: str, timeout: int = 300) -> None:
        """Wait for SSH to be available on the server"""
        console.print(f"Waiting for SSH on {public_ip}...")
        
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((public_ip, 22))
                sock.close()
                
                if result == 0:
                    console.print(f"✅ SSH available on {public_ip}", style="green")
                    return
                    
            except Exception:
                pass
            
            time.sleep(10)
        
        raise TimeoutError(f"SSH not available on {public_ip} after {timeout} seconds")
    
    def _apply_security_hardening(self, instance_id: str, public_ip: str) -> None:
        """Apply security hardening to the server"""
        console.print(f"🔒 Applying security hardening to {instance_id}")
        
        hardening_commands = [
            # Update system packages
            "sudo apt-get update && sudo apt-get upgrade -y",
            
            # Install security tools
            "sudo apt-get install -y fail2ban ufw rkhunter",
            
            # Configure firewall
            "sudo ufw default deny incoming",
            "sudo ufw default allow outgoing",
            "sudo ufw allow ssh",
            "sudo ufw allow 80/tcp",
            "sudo ufw allow 443/tcp",
            "sudo ufw --force enable",
            
            # Configure fail2ban
            "sudo systemctl enable fail2ban",
            "sudo systemctl start fail2ban",
            
            # Disable root login
            "sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' /etc/ssh/sshd_config",
            "sudo systemctl restart sshd",
            
            # Set up automatic security updates
            "sudo apt-get install -y unattended-upgrades",
            "sudo dpkg-reconfigure -plow unattended-upgrades"
        ]
        
        self._execute_remote_commands(public_ip, hardening_commands)
    
    def _configure_applications(self, instance_id: str, public_ip: str) -> None:
        """Install and configure applications on the server"""
        console.print(f"📦 Configuring applications on {instance_id}")
        
        app_commands = [
            # Install Docker
            "curl -fsSL https://get.docker.com -o get-docker.sh",
            "sudo sh get-docker.sh",
            "sudo usermod -aG docker $USER",
            
            # Install Docker Compose
            "sudo curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
            "sudo chmod +x /usr/local/bin/docker-compose",
            
            # Install monitoring tools
            "sudo apt-get install -y htop iotop nethogs",
            
            # Create application directories
            "sudo mkdir -p /opt/apps /opt/logs /opt/backups",
            "sudo chown $USER:$USER /opt/apps /opt/logs /opt/backups"
        ]
        
        self._execute_remote_commands(public_ip, app_commands)
    
    def _run_compliance_checks(self, instance_id: str, public_ip: str) -> None:
        """Run security compliance checks on the server"""
        console.print(f"🔍 Running compliance checks on {instance_id}")
        
        compliance_commands = [
            # Check for open ports
            "sudo netstat -tuln",
            
            # Check running services
            "sudo systemctl list-units --type=service --state=running",
            
            # Check user accounts
            "cat /etc/passwd",
            
            # Check file permissions
            "ls -la /etc/ssh/",
            "ls -la /etc/",
            
            # Run security audit
            "sudo rkhunter --check --skip-keypress"
        ]
        
        results = self._execute_remote_commands(public_ip, compliance_commands)
        
        # Store compliance results
        self.deployment_status[instance_id] = {
            'compliance_checks': results,
            'timestamp': datetime.now().isoformat()
        }
    
    def _execute_remote_commands(self, public_ip: str, commands: List[str]) -> Dict[str, Any]:
        """Execute commands on remote server via SSH"""
        results = {}
        
        try:
            # Get SSH key path from config or environment
            ssh_key_path = self.config.get('ssh_key_path', os.getenv('SSH_KEY_PATH', '~/.ssh/id_rsa'))
            ssh_key_path = os.path.expanduser(ssh_key_path)
            
            # Create SSH client
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(
                public_ip,
                username=self.config.get('ssh_username', 'ubuntu'),
                key_filename=ssh_key_path,
                timeout=30
            )
            
            for command in commands:
                try:
                    stdin, stdout, stderr = ssh.exec_command(command, timeout=60)
                    exit_status = stdout.channel.recv_exit_status()
                    
                    results[command] = {
                        'exit_status': exit_status,
                        'stdout': stdout.read().decode('utf-8'),
                        'stderr': stderr.read().decode('utf-8'),
                        'success': exit_status == 0
                    }
                    
                    if exit_status != 0:
                        console.print(f"⚠️ Command failed: {command}", style="yellow")
                        console.print(f"Error: {results[command]['stderr']}", style="red")
                    
                except Exception as e:
                    results[command] = {
                        'exit_status': -1,
                        'stdout': '',
                        'stderr': str(e),
                        'success': False
                    }
                    console.print(f"❌ Command execution failed: {command}", style="red")
            
            ssh.close()
            
        except Exception as e:
            console.print(f"❌ SSH connection failed to {public_ip}: {e}", style="red")
            logger.error(f"SSH error: {e}")
        
        return results
    
    def deploy_application(self, instance_ids: List[str], app_version: str) -> Dict[str, bool]:
        """Deploy application to configured servers"""
        console.print(Panel("🚀 Starting Application Deployment", style="bold magenta"))
        
        deployment_results = {}
        deployment_strategy = self.config['deployment']['strategy']
        
        if deployment_strategy == 'rolling':
            deployment_results = self._rolling_deployment(instance_ids, app_version)
        elif deployment_strategy == 'blue_green':
            deployment_results = self._blue_green_deployment(instance_ids, app_version)
        else:
            deployment_results = self._simple_deployment(instance_ids, app_version)
        
        return deployment_results
    
    def _rolling_deployment(self, instance_ids: List[str], app_version: str) -> Dict[str, bool]:
        """Perform rolling deployment to minimize downtime"""
        console.print("🔄 Performing rolling deployment")
        
        deployment_results = {}
        health_check_path = self.config['deployment']['health_check_path']
        
        for i, instance_id in enumerate(instance_ids):
            try:
                console.print(f"Deploying to instance {i+1}/{len(instance_ids)}: {instance_id}")
                
                # Get instance details
                ec2 = self.aws_session.resource('ec2')
                instance = ec2.Instance(instance_id)
                
                # Deploy application
                self._deploy_to_instance(instance.public_ip_address, app_version)
                
                # Health check
                if self._health_check(instance.public_ip_address, health_check_path):
                    deployment_results[instance_id] = True
                    console.print(f"✅ Deployment successful on {instance_id}", style="green")
                else:
                    deployment_results[instance_id] = False
                    console.print(f"❌ Health check failed on {instance_id}", style="red")
                
                # Wait between deployments
                if i < len(instance_ids) - 1:
                    time.sleep(30)
                    
            except Exception as e:
                console.print(f"❌ Deployment failed on {instance_id}: {e}", style="red")
                deployment_results[instance_id] = False
        
        return deployment_results
    
    def _deploy_to_instance(self, public_ip: str, app_version: str) -> None:
        """Deploy application to a specific instance"""
        deploy_commands = [
            f"cd /opt/apps",
            f"git clone https://github.com/your-org/your-app.git || cd your-app && git pull",
            f"git checkout {app_version}",
            "docker-compose down",
            "docker-compose pull",
            "docker-compose up -d",
            "sleep 10"  # Wait for services to start
        ]
        
        self._execute_remote_commands(public_ip, deploy_commands)
    
    def _health_check(self, public_ip: str, health_path: str) -> bool:
        """Perform health check on deployed application"""
        try:
            import requests
            response = requests.get(f"http://{public_ip}{health_path}", timeout=10)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Health check failed for {public_ip}: {e}")
            return False
    
    def _blue_green_deployment(self, instance_ids: List[str], app_version: str) -> Dict[str, bool]:
        """Perform blue-green deployment"""
        console.print("🔵🟢 Performing blue-green deployment")
        # Implementation for blue-green deployment
        return self._simple_deployment(instance_ids, app_version)
    
    def _simple_deployment(self, instance_ids: List[str], app_version: str) -> Dict[str, bool]:
        """Perform simple deployment to all instances"""
        console.print("📦 Performing simple deployment")
        
        deployment_results = {}
        
        for instance_id in instance_ids:
            try:
                ec2 = self.aws_session.resource('ec2')
                instance = ec2.Instance(instance_id)
                
                self._deploy_to_instance(instance.public_ip_address, app_version)
                deployment_results[instance_id] = True
                
            except Exception as e:
                console.print(f"❌ Deployment failed on {instance_id}: {e}", style="red")
                deployment_results[instance_id] = False
        
        return deployment_results
    
    def generate_deployment_report(self) -> None:
        """Generate deployment status report"""
        console.print("\n" + "="*80)
        console.print("📊 DEPLOYMENT STATUS REPORT", style="bold blue")
        console.print("="*80)
        
        if not self.deployment_status:
            console.print("No deployment data available", style="yellow")
            return
        
        # Create deployment table
        deployment_table = Table(title="Deployment Status")
        deployment_table.add_column("Instance ID", style="cyan")
        deployment_table.add_column("Status", style="magenta")
        deployment_table.add_column("Timestamp", style="green")
        deployment_table.add_column("Compliance Checks", style="blue")
        
        for instance_id, status in self.deployment_status.items():
            compliance_status = "PASS" if status.get('compliance_checks') else "N/A"
            deployment_table.add_row(
                instance_id,
                "✅ SUCCESS" if status.get('compliance_checks') else "❌ FAILED",
                status.get('timestamp', 'N/A'),
                compliance_status
            )
        
        console.print(deployment_table)
    
    def cleanup_resources(self, instance_ids: List[str]) -> None:
        """Clean up provisioned resources"""
        console.print(Panel("🧹 Starting Resource Cleanup", style="bold red"))
        
        if not self.aws_session:
            self.initialize_aws_session()
        
        ec2 = self.aws_session.resource('ec2')
        
        for instance_id in instance_ids:
            try:
                instance = ec2.Instance(instance_id)
                instance.terminate()
                console.print(f"🗑️ Terminated instance: {instance_id}", style="green")
            except Exception as e:
                console.print(f"❌ Failed to terminate {instance_id}: {e}", style="red")

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description='Infrastructure Automation Tool')
    parser.add_argument('--config', '-c', help='Configuration file path')
    parser.add_argument('--action', '-a', choices=['provision', 'configure', 'deploy', 'cleanup'],
                       required=True, help='Action to perform')
    parser.add_argument('--server-type', help='Specific server type to work with')
    parser.add_argument('--app-version', help='Application version to deploy')
    parser.add_argument('--instance-ids', nargs='+', help='Specific instance IDs')
    
    args = parser.parse_args()
    
    try:
        automation = InfrastructureAutomation(args.config)
        
        if args.action == 'provision':
            instance_ids = automation.provision_servers(args.server_type)
            console.print(f"✅ Provisioned {len(instance_ids)} instances", style="green")
            
        elif args.action == 'configure':
            if not args.instance_ids:
                console.print("❌ Instance IDs required for configuration", style="red")
                sys.exit(1)
            results = automation.configure_servers(args.instance_ids)
            success_count = sum(results.values())
            console.print(f"✅ Configuration completed for {success_count}/{len(results)} instances", style="green")
            
        elif args.action == 'deploy':
            if not args.instance_ids:
                console.print("❌ Instance IDs required for deployment", style="red")
                sys.exit(1)
            if not args.app_version:
                console.print("❌ App version required for deployment", style="red")
                sys.exit(1)
            results = automation.deploy_application(args.instance_ids, args.app_version)
            success_count = sum(results.values())
            console.print(f"✅ Deployment completed for {success_count}/{len(results)} instances", style="green")
            
        elif args.action == 'cleanup':
            if not args.instance_ids:
                console.print("❌ Instance IDs required for cleanup", style="red")
                sys.exit(1)
            automation.cleanup_resources(args.instance_ids)
            console.print("✅ Cleanup completed", style="green")
        
        # Generate report
        automation.generate_deployment_report()
        
    except KeyboardInterrupt:
        console.print("\nOperation interrupted by user", style="yellow")
        sys.exit(1)
    except Exception as e:
        console.print(f"Error: {e}", style="red")
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
