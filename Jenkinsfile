pipeline {
    agent any

    environment {
        ECR_REPO = '409784048198.dkr.ecr.eu-north-1.amazonaws.com/vetri'
        IMAGE_TAG = 'latest'
        AWS_REGION = 'eu-north-1'
        // Extend the PATH so sonar-scanner can be found during the pipeline execution
        PATH = "${PATH}:/opt/sonar-scanner/bin"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/VETRI9876/KNN-Flask-App.git'
            }
        }

        stage('SonarQube Analysis') {
            steps {
                withSonarQubeEnv('MySonarQube') {
                    sh 'sonar-scanner'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t vetri .'
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}
                docker tag vetri:latest ${ECR_REPO}:${IMAGE_TAG}
                docker push ${ECR_REPO}:${IMAGE_TAG}
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                kubectl apply -f deployment.yaml
                kubectl apply -f service.yaml
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh 'kubectl get svc'
            }
        }
    }
}
