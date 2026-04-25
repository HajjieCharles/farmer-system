pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "hajjiecharles/farmer-system:latest"
        EC2_HOST = "3.22.178.160"
        EC2_USER = "ubuntu"
        SSH_CRED = "ec2-ssh-private-key"
        DOCKER_CRED = "dockerhub-creds"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git 'https://github.com/HajjieCharles/farmer-system.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t farmer-system .'
            }
        }

        stage('Tag Image') {
            steps {
                sh 'docker tag farmer-system hajjiecharles/farmer-system:latest'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKER_CRED}",
                    usernameVariable: 'USER',
                    passwordVariable: 'PASS'
                )]) {
                    sh '''
                    echo $PASS | docker login -u $USER --password-stdin
                    docker push hajjiecharles/farmer-system:latest
                    '''
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent(["${SSH_CRED}"]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                    
                    sudo docker stop farmer-container || true
                    sudo docker rm farmer-container || true
                    
                    sudo docker pull ${DOCKER_IMAGE}
                    
                    sudo docker run -d -p 8000:8000 --name farmer-container ${DOCKER_IMAGE}
                    
                    '
                    """
                }
            }
        }
    }
}
