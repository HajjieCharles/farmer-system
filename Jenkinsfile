pipeline {
    agent any

    environment {
        EC2_USER    = "ubuntu"
        EC2_HOST    = "3.22.99.35"
        CRED_ID     = "ec2-ssh-private-key"
        PROJECT_DIR = "/home/ubuntu/farmer-system"
        REPO_URL    = "https://github.com/HajjieCharles/farmer-system.git"
    }

    stages {
        stage('Deploy Django with Docker') {
            steps {
                script {
                    sshagent([CRED_ID]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
                            sudo apt-get update
                            sudo apt-get install -y git docker.io docker-compose-plugin

                            sudo systemctl start docker
                            sudo systemctl enable docker

                            sudo rm -rf ${PROJECT_DIR}
                            cd /home/ubuntu
                            git clone ${REPO_URL} farmer-system

                            cd ${PROJECT_DIR}

                            sudo docker compose down || true
                            sudo docker compose up -d --build

                            sudo docker ps
                            echo 'Site started at http://${EC2_HOST}'
                        "
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "SUCCESS: Your site is live at http://3.22.99.35"
        }

        failure {
            echo "FAILURE: Check Jenkins console output for errors."
        }
    }
}
