pipeline {
    agent any

    environment {
        EC2_USER = "ubuntu"
        EC2_HOST = "3.22.178.160"
        CRED_ID  = "ec2-ssh-private-key"
        PROJECT_DIR = "/home/ubuntu/farmer-system"
    }

    stages {

        stage('Deploy Django with Docker') {
            steps {
                script {
                    sshagent([CRED_ID]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                            
                            cd ${PROJECT_DIR}

                            git pull

                            sudo docker stop farmer-container || true
                            sudo docker rm farmer-container || true

                            sudo docker build -t farmer-system .

                            sudo docker run -d -p 8000:8000 --name farmer-container farmer-system
                        '
                        """
                    }
                }
            }
        }
    }
}
