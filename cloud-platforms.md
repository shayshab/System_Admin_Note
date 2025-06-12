# Cloud Platforms Reference Guide

## 1. AWS (Amazon Web Services)

### EC2 Management
```bash
# List Instances
aws ec2 describe-instances
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running"

# Create Instance
aws ec2 run-instances \
    --image-id ami-0c55b159cbfafe1f0 \
    --instance-type t2.micro \
    --key-name my-key-pair \
    --security-group-ids sg-xxxxxxxx \
    --subnet-id subnet-xxxxxxxx

# Stop/Start Instance
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
aws ec2 start-instances --instance-ids i-1234567890abcdef0
```

### S3 Storage
```bash
# List Buckets
aws s3 ls
aws s3 ls s3://my-bucket

# Upload/Download
aws s3 cp file.txt s3://my-bucket/
aws s3 cp s3://my-bucket/file.txt ./

# Sync Directory
aws s3 sync ./local-folder s3://my-bucket/
```

### IAM Management
```bash
# List Users
aws iam list-users

# Create User
aws iam create-user --user-name MyUser

# Attach Policy
aws iam attach-user-policy \
    --user-name MyUser \
    --policy-arn arn:aws:iam::aws:policy/AmazonS3ReadOnlyAccess
```

### RDS Database
```bash
# List Databases
aws rds describe-db-instances

# Create Database
aws rds create-db-instance \
    --db-instance-identifier mydb \
    --db-instance-class db.t3.micro \
    --engine mysql \
    --master-username admin \
    --master-user-password mypassword
```

## 2. Google Cloud Platform (GCP)

### Compute Engine
```bash
# List Instances
gcloud compute instances list

# Create Instance
gcloud compute instances create my-instance \
    --zone=us-central1-a \
    --machine-type=e2-micro \
    --image-family=debian-10 \
    --image-project=debian-cloud

# Stop/Start Instance
gcloud compute instances stop my-instance --zone=us-central1-a
gcloud compute instances start my-instance --zone=us-central1-a
```

### Cloud Storage
```bash
# List Buckets
gsutil ls
gsutil ls gs://my-bucket

# Upload/Download
gsutil cp file.txt gs://my-bucket/
gsutil cp gs://my-bucket/file.txt ./

# Sync Directory
gsutil rsync -r ./local-folder gs://my-bucket/
```

### IAM Management
```bash
# List Service Accounts
gcloud iam service-accounts list

# Create Service Account
gcloud iam service-accounts create my-service-account

# Grant Role
gcloud projects add-iam-policy-binding my-project \
    --member="serviceAccount:my-service-account@my-project.iam.gserviceaccount.com" \
    --role="roles/storage.objectViewer"
```

### Cloud SQL
```bash
# List Instances
gcloud sql instances list

# Create Instance
gcloud sql instances create my-instance \
    --database-version=MYSQL_8_0 \
    --tier=db-f1-micro \
    --region=us-central1
```

## 3. Microsoft Azure

### Virtual Machines
```powershell
# List VMs
Get-AzVM
Get-AzVM -ResourceGroupName myResourceGroup

# Create VM
New-AzVM `
    -ResourceGroupName myResourceGroup `
    -Name myVM `
    -Location eastus `
    -Image UbuntuLTS `
    -Size Standard_DS1_v2

# Stop/Start VM
Stop-AzVM -ResourceGroupName myResourceGroup -Name myVM
Start-AzVM -ResourceGroupName myResourceGroup -Name myVM
```

### Blob Storage
```powershell
# List Containers
Get-AzStorageContainer

# Upload/Download
Set-AzStorageBlobContent -File "file.txt" -Container "mycontainer" -Blob "file.txt"
Get-AzStorageBlobContent -Container "mycontainer" -Blob "file.txt" -Destination "."

# Sync Directory
az storage blob sync -c mycontainer -s ./local-folder
```

### Azure AD
```powershell
# List Users
Get-AzADUser

# Create User
New-AzADUser `
    -DisplayName "John Doe" `
    -UserPrincipalName "john@domain.com" `
    -Password (ConvertTo-SecureString "password" -AsPlainText -Force)

# Assign Role
New-AzRoleAssignment `
    -ObjectId $user.Id `
    -RoleDefinitionName "Contributor" `
    -Scope "/subscriptions/$subscriptionId"
```

### Azure SQL
```powershell
# List Databases
Get-AzSqlServer
Get-AzSqlDatabase -ServerName myserver -ResourceGroupName myResourceGroup

# Create Database
New-AzSqlDatabase `
    -ResourceGroupName myResourceGroup `
    -ServerName myserver `
    -DatabaseName mydatabase `
    -Edition Basic
```

## 4. Cloud Security

### AWS Security
```bash
# Security Groups
aws ec2 describe-security-groups
aws ec2 create-security-group --group-name my-sg --description "My security group"

# KMS Encryption
aws kms create-key
aws kms encrypt --key-id alias/my-key --plaintext fileb://plaintext.txt
```

### GCP Security
```bash
# Firewall Rules
gcloud compute firewall-rules list
gcloud compute firewall-rules create allow-http \
    --allow tcp:80

# Cloud KMS
gcloud kms keys create my-key \
    --keyring my-keyring \
    --location global \
    --purpose encryption
```

### Azure Security
```powershell
# Network Security Groups
Get-AzNetworkSecurityGroup
New-AzNetworkSecurityRuleConfig `
    -Name "allow-http" `
    -Protocol Tcp `
    -Direction Inbound `
    -Priority 1000 `
    -SourceAddressPrefix * `
    -SourcePortRange * `
    -DestinationAddressPrefix * `
    -DestinationPortRange 80 `
    -Access Allow
```

## 5. Cloud Monitoring

### AWS CloudWatch
```bash
# List Metrics
aws cloudwatch list-metrics

# Get Metric Statistics
aws cloudwatch get-metric-statistics \
    --namespace AWS/EC2 \
    --metric-name CPUUtilization \
    --dimensions Name=InstanceId,Value=i-1234567890abcdef0 \
    --start-time 2023-01-01T00:00:00 \
    --end-time 2023-01-02T00:00:00 \
    --period 3600 \
    --statistics Average
```

### GCP Monitoring
```bash
# List Metrics
gcloud monitoring metrics list

# Create Alert Policy
gcloud alpha monitoring policies create \
    --policy-from-file=policy.json
```

### Azure Monitor
```powershell
# Get Metrics
Get-AzMetricDefinition -ResourceId $vm.Id
Get-AzMetric -ResourceId $vm.Id -MetricName "Percentage CPU"

# Create Alert Rule
Add-AzMetricAlertRule `
    -Name "cpu-alert" `
    -Location "East US" `
    -ResourceGroup "myResourceGroup" `
    -TargetResourceId $vm.Id `
    -MetricName "Percentage CPU" `
    -Operator GreaterThan `
    -Threshold 80
```

## 6. Cloud Cost Management

### AWS Cost Management
```bash
# Get Cost Report
aws ce get-cost-and-usage \
    --time-period Start=2023-01-01,End=2023-02-01 \
    --granularity MONTHLY \
    --metrics "UnblendedCost"

# Set Budget
aws budgets create-budget \
    --account-id 123456789012 \
    --budget file://budget.json
```

### GCP Cost Management
```bash
# Export Billing Data
gcloud billing export create \
    --dataset-name billing_data \
    --table-name billing_export

# Set Budget
gcloud billing budgets create \
    --billing-account=XXXXXX-XXXXXX-XXXXXX \
    --display-name="Monthly Budget" \
    --budget-amount=1000USD \
    --threshold-rule=percent=0.5 \
    --threshold-rule=percent=0.9
```

### Azure Cost Management
```powershell
# Get Cost Analysis
Get-AzConsumptionUsageDetail

# Set Budget
New-AzConsumptionBudget `
    -Amount 1000 `
    -Category Cost `
    -TimeGrain Monthly `
    -StartDate 2023-01-01 `
    -EndDate 2023-12-31
```

## 7. Cloud Automation

### Infrastructure as Code

#### AWS CloudFormation
```yaml
Resources:
  MyEC2Instance:
    Type: AWS::EC2::Instance
    Properties:
      ImageId: ami-0c55b159cbfafe1f0
      InstanceType: t2.micro
      KeyName: my-key-pair
```

#### GCP Deployment Manager
```yaml
resources:
- name: my-vm
  type: compute.v1.instance
  properties:
    zone: us-central1-a
    machineType: zones/us-central1-a/machineTypes/e2-micro
    disks:
    - deviceName: boot
      type: PERSISTENT
      boot: true
      autoDelete: true
      initializeParams:
        sourceImage: projects/debian-cloud/global/images/family/debian-10
```

#### Azure ARM Templates
```json
{
  "resources": [
    {
      "type": "Microsoft.Compute/virtualMachines",
      "name": "myVM",
      "apiVersion": "2020-06-01",
      "location": "eastus",
      "properties": {
        "hardwareProfile": {
          "vmSize": "Standard_DS1_v2"
        }
      }
    }
  ]
}
```

## 8. Cloud Best Practices

### Security
- Use IAM roles and least privilege
- Enable encryption at rest and in transit
- Regular security audits
- Network segmentation
- Monitoring and logging

### Cost Optimization
- Right-size resources
- Use reserved instances
- Implement auto-scaling
- Monitor and optimize storage
- Use spot instances when possible

### Performance
- Use appropriate instance types
- Implement caching
- Use CDN for static content
- Optimize database performance
- Regular performance monitoring

### Reliability
- Implement redundancy
- Use multiple availability zones
- Regular backups
- Disaster recovery planning
- Monitoring and alerting 