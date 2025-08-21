pipeline {
    agent any
    
    environment {
        // Application configuration
        APP_NAME = 'devsecops-app'
        APP_VERSION = "${env.BUILD_NUMBER}"
        DOCKER_IMAGE = "devsecops/${APP_NAME}:${APP_VERSION}"
        
        // Security scanning tools
        OWASP_ZAP_PATH = '/opt/zap/zap.sh'
        SONARQUBE_URL = 'http://sonarqube:9000'
        TRIVY_PATH = '/usr/local/bin/trivy'
        
        // Compliance frameworks
        COMPLIANCE_FRAMEWORKS = ['pci-dss', 'soc2', 'iso27001']
        
        // Infrastructure
        ANSIBLE_PATH = '/opt/ansible'
        TERRAFORM_PATH = '/opt/terraform'
        
        // Notifications
        SLACK_CHANNEL = '#devsecops-alerts'
        EMAIL_RECIPIENTS = 'devsecops-team@company.com'
    }
    
    options {
        // Security options
        skipDefaultCheckout(false)
        timestamps()
        timeout(time: 2, unit: 'HOURS')
        
        // Build retention
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    
    triggers {
        // Automated triggers
        pollSCM('H/15 * * * *')  // Poll SCM every 15 minutes
        cron('0 2 * * *')        // Daily security scan at 2 AM
    }
    
    stages {
        stage('Security Pre-Check') {
            parallel {
                stage('Code Security Scan') {
                    steps {
                        script {
                            echo "🔒 Starting code security scan..."
                            
                            // Run Bandit for Python security
                            if (fileExists('requirements.txt')) {
                                sh '''
                                    pip install bandit
                                    bandit -r . -f json -o bandit-report.json || true
                                '''
                                publishJSON([
                                    target: [
                                        reportDir: '.',
                                        reportFiles: 'bandit-report.json',
                                        reportName: 'Bandit Security Report'
                                    ]
                                ])
                            }
                            
                            // Run Semgrep for pattern-based security
                            sh '''
                                semgrep ci --config auto --json --output semgrep-report.json || true
                            '''
                            publishJSON([
                                target: [
                                    reportDir: '.',
                                    reportFiles: 'semgrep-report.json',
                                    reportName: 'Semgrep Security Report'
                                ]
                            ])
                            
                            // Run Trivy for dependency vulnerabilities
                            sh '''
                                trivy fs --format json --output trivy-fs-report.json . || true
                            '''
                            publishJSON([
                                target: [
                                    reportDir: '.',
                                    reportFiles: 'trivy-fs-report.json',
                                    reportName: 'Trivy Filesystem Report'
                                ]
                            ])
                        }
                    }
                    post {
                        always {
                            // Archive security reports
                            archiveArtifacts artifacts: '*-report.json', allowEmptyArchive: true
                        }
                    }
                }
                
                stage('Infrastructure Security') {
                    steps {
                        script {
                            echo "🏗️ Checking infrastructure security..."
                            
                            // Validate Terraform configuration
                            if (fileExists('terraform/')) {
                                dir('terraform') {
                                    sh '''
                                        terraform init
                                        terraform validate
                                        terraform plan -out=tfplan
                                    '''
                                    
                                    // Run Checkov for Terraform security
                                    sh '''
                                        checkov -f . --output json --output-file-path checkov-report.json || true
                                    '''
                                    publishJSON([
                                        target: [
                                            reportDir: '.',
                                            reportFiles: 'checkov-report.json',
                                            reportName: 'Checkov Terraform Report'
                                        ]
                                    ])
                                }
                            }
                            
                            // Validate Ansible configuration
                            if (fileExists('ansible/')) {
                                dir('ansible') {
                                    sh '''
                                        ansible-lint *.yml || true
                                        ansible-playbook --syntax-check deploy.yml
                                    '''
                                }
                            }
                        }
                    }
                }
            }
        }
        
        stage('Build & Test') {
            parallel {
                stage('Build Application') {
                    steps {
                        script {
                            echo "🔨 Building application..."
                            
                            // Build Docker image
                            sh '''
                                docker build -t ${DOCKER_IMAGE} .
                                docker tag ${DOCKER_IMAGE} ${DOCKER_IMAGE}:latest
                            '''
                            
                            // Push to registry
                            withCredentials([usernamePassword(credentialsId: 'docker-registry', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                                sh '''
                                    docker login -u ${DOCKER_USER} -p ${DOCKER_PASS} registry.company.com
                                    docker push ${DOCKER_IMAGE}
                                    docker push ${DOCKER_IMAGE}:latest
                                '''
                            }
                        }
                    }
                }
                
                stage('Security Testing') {
                    steps {
                        script {
                            echo "🧪 Running security tests..."
                            
                            // Run OWASP ZAP security scan
                            sh '''
                                ${OWASP_ZAP_PATH} -cmd -quickurl http://localhost:8080 -quickout zap-report.xml || true
                            '''
                            
                            // Run Trivy container scan
                            sh '''
                                ${TRIVY_PATH} image --format json --output trivy-image-report.json ${DOCKER_IMAGE} || true
                            '''
                            
                            // Run container security scan
                            sh '''
                                docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
                                    aquasec/trivy image --format json --output trivy-container-report.json ${DOCKER_IMAGE} || true
                            '''
                        }
                    }
                    post {
                        always {
                            // Archive security test reports
                            archiveArtifacts artifacts: '*-report.*', allowEmptyArchive: true
                        }
                    }
                }
                
                stage('Compliance Check') {
                    steps {
                        script {
                            echo "📋 Running compliance checks..."
                            
                            // Run compliance checks for each framework
                            COMPLIANCE_FRAMEWORKS.split(',').each { framework ->
                                echo "Checking ${framework} compliance..."
                                
                                // Run OpenSCAP compliance scan
                                sh '''
                                    oscap xccdf eval --profile ${framework} \
                                        --results compliance-${framework}-report.xml \
                                        /usr/share/xml/scap/ssg/content/ssg-ubuntu20-ds.xml || true
                                '''
                                
                                // Run custom compliance checks
                                sh '''
                                    python scripts/compliance_checker.py --framework ${framework} \
                                        --output compliance-${framework}-custom.json || true
                                '''
                            }
                        }
                    }
                    post {
                        always {
                            // Archive compliance reports
                            archiveArtifacts artifacts: 'compliance-*-report.*', allowEmptyArchive: true
                        }
                    }
                }
            }
        }
        
        stage('Quality Gate') {
            steps {
                script {
                    echo "🚦 Running quality gates..."
                    
                    // SonarQube quality gate
                    withSonarQubeEnv('SonarQube') {
                        sh '''
                            mvn sonar:sonar \
                                -Dsonar.projectKey=${APP_NAME} \
                                -Dsonar.projectVersion=${APP_VERSION} \
                                -Dsonar.sources=. \
                                -Dsonar.host.url=${SONARQUBE_URL}
                        '''
                    }
                    
                    // Wait for SonarQube analysis
                    timeout(time: 10, unit: 'MINUTES') {
                        waitForQualityGate abortPipeline: true
                    }
                    
                    // Security threshold check
                    def securityIssues = sh(
                        script: "grep -c 'HIGH' bandit-report.json || echo '0'",
                        returnStdout: true
                    ).trim()
                    
                    if (securityIssues.toInteger() > 0) {
                        error "Security quality gate failed: ${securityIssues} high severity issues found"
                    }
                    
                    // Compliance threshold check
                    COMPLIANCE_FRAMEWORKS.split(',').each { framework ->
                        def complianceScore = sh(
                            script: "python scripts/compliance_score.py --framework ${framework}",
                            returnStdout: true
                        ).trim()
                        
                        if (complianceScore.toFloat() < 0.8) {
                            error "Compliance quality gate failed for ${framework}: Score ${complianceScore} < 0.8"
                        }
                    }
                }
            }
        }
        
        stage('Deploy to Staging') {
            when {
                expression { 
                    return env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'develop' 
                }
            }
            steps {
                script {
                    echo "🚀 Deploying to staging environment..."
                    
                    // Deploy using Ansible
                    dir('ansible') {
                        withCredentials([sshUserPrivateKey(credentialsId: 'staging-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                            sh '''
                                export ANSIBLE_HOST_KEY_CHECKING=False
                                ansible-playbook -i staging-inventory.ini deploy.yml \
                                    --private-key=${SSH_KEY} \
                                    --extra-vars="app_version=${APP_VERSION}"
                            '''
                        }
                    }
                    
                    // Run post-deployment tests
                    sh '''
                        python scripts/health_check.py --environment staging
                        python scripts/security_verification.py --environment staging
                    '''
                }
            }
        }
        
        stage('Production Deployment') {
            when {
                expression { 
                    return env.BRANCH_NAME == 'main' && env.BUILD_NUMBER.toInteger() % 5 == 0 
                }
            }
            input {
                message "Deploy to production?"
                ok "Deploy"
                submitter "devsecops-team"
            }
            steps {
                script {
                    echo "🚀 Deploying to production environment..."
                    
                    // Deploy using Ansible with rolling strategy
                    dir('ansible') {
                        withCredentials([sshUserPrivateKey(credentialsId: 'production-ssh-key', keyFileVariable: 'SSH_KEY')]) {
                            sh '''
                                export ANSIBLE_HOST_KEY_CHECKING=False
                                ansible-playbook -i production-inventory.ini deploy.yml \
                                    --private-key=${SSH_KEY} \
                                    --extra-vars="app_version=${APP_VERSION} deployment_strategy=rolling"
                            '''
                        }
                    }
                    
                    // Run production verification
                    sh '''
                        python scripts/health_check.py --environment production
                        python scripts/security_verification.py --environment production
                        python scripts/performance_test.py --environment production
                    '''
                }
            }
        }
        
        stage('Post-Deployment Security') {
            steps {
                script {
                    echo "🔒 Running post-deployment security checks..."
                    
                    // Run runtime security scan
                    sh '''
                        python scripts/runtime_security_scan.py --environment production
                    '''
                    
                    // Run compliance verification
                    COMPLIANCE_FRAMEWORKS.split(',').each { framework ->
                        sh '''
                            python scripts/compliance_verification.py --framework ${framework} --environment production
                        '''
                    }
                    
                    // Generate security report
                    sh '''
                        python scripts/generate_security_report.py \
                            --environment production \
                            --output security-report-${BUILD_NUMBER}.html
                    '''
                }
            }
            post {
                always {
                    // Archive security reports
                    archiveArtifacts artifacts: 'security-report-*.html', allowEmptyArchive: true
                    
                    // Send notifications
                    script {
                        if (currentBuild.result == 'SUCCESS') {
                            slackSend(
                                channel: SLACK_CHANNEL,
                                color: 'good',
                                message: "✅ ${APP_NAME} v${APP_VERSION} deployed successfully to production"
                            )
                        } else {
                            slackSend(
                                channel: SLACK_CHANNEL,
                                color: 'danger',
                                message: "❌ ${APP_NAME} v${APP_VERSION} deployment failed"
                            )
                        }
                    }
                }
            }
        }
    }
    
    post {
        always {
            // Cleanup
            sh '''
                docker system prune -f || true
                rm -rf workspace || true
            '''
            
            // Update deployment metrics
            script {
                if (currentBuild.result == 'SUCCESS') {
                    // Update metrics in monitoring system
                    sh '''
                        curl -X POST "http://monitoring:9090/metrics/job/deployment/instance/${APP_NAME}" \
                            -d "deployment_success_total{app=\"${APP_NAME}\",version=\"${APP_VERSION}\"} 1"
                    '''
                }
            }
        }
        
        success {
            // Success notifications
            emailext (
                subject: "✅ ${APP_NAME} v${APP_VERSION} - Deployment Successful",
                body: "Build ${BUILD_NUMBER} completed successfully. Application deployed to production.",
                to: EMAIL_RECIPIENTS
            )
        }
        
        failure {
            // Failure notifications
            emailext (
                subject: "❌ ${APP_NAME} v${APP_VERSION} - Deployment Failed",
                body: "Build ${BUILD_NUMBER} failed. Please check Jenkins console for details.",
                to: EMAIL_RECIPIENTS
            )
            
            // Rollback if needed
            script {
                if (env.BRANCH_NAME == 'main') {
                    echo "Rolling back to previous version..."
                    sh '''
                        python scripts/rollback.py --environment production --app ${APP_NAME}
                    '''
                }
            }
        }
        
        cleanup {
            // Final cleanup
            sh '''
                docker system prune -f || true
                rm -rf workspace || true
            '''
        }
    }
}
