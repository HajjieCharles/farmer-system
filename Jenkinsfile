pipeline {
    agent any

    environment {
        EC2_USER = "ubuntu"
        EC2_HOST = "18.224.180.36"
        PROJECT_DIR = "/home/ubuntu/farmer-system"
    }

    stages {
        stage('Update Code on EC2') {
            steps {
                script {
                    sshagent(credentials: ['ec2-ssh-private-key']) {
                        sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} '
                            cd ${PROJECT_DIR}
                            git pull origin main
                            python3 -m venv comp314
                            . comp314/bin/activate
                            python3 -m pip install --upgrade pip
                            python3 -m pip install django
                            python manage.py migrate
                            pkill -f "manage.py runserver 0.0.0.0:8000" || true
                            nohup python manage.py runserver 0.0.0.0:8000 > django.log 2>&1 &
                        '
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "Code updated and app restarted successfully on EC2!"
        }
        failure {
            echo "Deployment failed."
        }
    }
}