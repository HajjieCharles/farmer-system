pipeline {
    agent any

    environment {
        DOCKER_IMAGE = "hajjiecharles/farmer-system"
        EC2_USER = "ubuntu"
        EC2_HOST = "3.22.178.160"
        EC2_CRED_ID = "ec2-ssh-private-key"
        DOCKERHUB_CRED_ID = "dockerhub-creds"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                sh "docker build -t ${DOCKER_IMAGE}:latest ."
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: "${DOCKERHUB_CRED_ID}",
                    usernameVariable: "DOCKER_USER",
                    passwordVariable: "DOCKER_PASS"
                )]) {
                    sh """
                    echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                    docker push ${DOCKER_IMAGE}:latest
                    docker logout
                    """
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent([EC2_CRED_ID]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                        sudo docker pull ${DOCKER_IMAGE}:latest

                        sudo docker stop farmer-container || true
                        sudo docker rm farmer-container || true

                        sudo docker run -d \
                        -p 8000:8000 \
                        --restart always \
                        --name farmer-container \
                        ${DOCKER_IMAGE}:latest

                        sudo systemctl restart nginx
                    '
                    """
                }
            }
        }
    }

    post {
        success {
            echo "SUCCESS: Site deployed at http://${EC2_HOST}"
        }
        failure {
            echo "FAILED: Deployment did not complete."
        }
    }
}
