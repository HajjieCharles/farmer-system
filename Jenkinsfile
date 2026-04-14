pipeline {
    agent any

    environment {
        // --- YOUR CONFIGURATION ---
        EC2_USER    = "ubuntu"
        EC2_HOST    = "3.16.154.24"
        CRED_ID     = "ec2-ssh-private-key"
        PROJECT_DIR = "/home/ubuntu/farmer-system"
        REPO_URL    = "https://github.com/HajjieCharles/farmer-system.git"
    }

    stages {
        stage('Clean Deploy & Start Server') {
            steps {
                script {
                    sshagent([CRED_ID]) {
                        sh """
                        ssh -o StrictHostKeyChecking=no ${EC2_USER}@${EC2_HOST} "
                            
                            # 1. Update system and install tools
                            sudo apt-get update && sudo apt-get install -y python3-venv python3-pip git

                            # 2. Kill old Django server
                            sudo fuser -k 8000/tcp || true

                            # 3. Fresh Clone
                            sudo rm -rf ${PROJECT_DIR}
                            cd /home/ubuntu
                            git clone ${REPO_URL} farmer-system

                            # 4. Setup Environment
                            cd ${PROJECT_DIR}
                            python3 -m venv comp314
                            source comp314/bin/activate

                            # 5. Install Dependencies
                            pip install --upgrade pip
                            pip install django

                            # 6. Run Migrations
                            python3 manage.py migrate --noinput

                            # 7. Start Server
                            BUILD_ID=dontKillMe nohup python3 manage.py runserver 0.0.0.0:8000 > django.log 2>&1 &

                            sleep 2
                            echo 'Server started at http://${EC2_HOST}:8000'
                        "
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo "SUCCESS: Your site is live at http://3.16.154.24/:8000"
        }
        failure {
            echo "FAILURE: Check Jenkins console output for errors."
        }
    }
}
