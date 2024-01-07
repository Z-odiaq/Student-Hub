pipeline {
    agent any
    triggers {
       githubPush()
    }
    environment {
        EC2_HOST = '3.90.187.145'
        REMOTE_USER = 'ec2-user'
    }

    stages {
        stage('Clone Repository') {
            steps {
                echo 'Cloning the repository...'
                git branch: 'main', changelog: false, poll: false, url: 'https://github.com/Z-odiaq/Student-Hub.git'
            }
        }

        stage('Build') {
            steps {
                script {
                    echo 'Adding secrets'
                    withCredentials([string(credentialsId: 'DB_NAME', variable: 'DB_NAME'), 
                    string(credentialsId: 'DB_PASS', variable: 'DB_PASS'), 
                    string(credentialsId: 'DB_USER', variable: 'DB_USER'), 
                    string(credentialsId: 'DB_HOST', variable: 'DB_HOST'), 
                    string(credentialsId: 'DB_PORT', variable: 'DB_PORT')]) {
                        
                    sh 'sed -i "s/env(\'DB_PASS\')/\'${DB_PASS}\'/g" django_proj/settings.py'
                    sh 'sed -i "s/env(\'DB_NAME\')/\'${DB_NAME}\'/g" django_proj/settings.py'
                    sh 'sed -i "s/env(\'DB_USER\')/\'${DB_USER}\'/g" django_proj/settings.py'
                    sh 'sed -i "s/env(\'DB_HOST\')/\'${DB_HOST}\'/g" django_proj/settings.py'
                    sh 'sed -i "s/env(\'DB_PORT\')/\'${DB_PORT}\'/g" django_proj/settings.py'
                    sh 'sed -i "/import environ/d" django_proj/settings.py'
                    sh 'sed -i "/environ.Env.read_env()/d" django_proj/settings.py'
                    sh 'sed -i "/env = environ.Env()/d" django_proj/settings.py'
                }
                    echo 'Building the application...'
                    sh 'pip install -r requirements.txt --break-system-packages'
                    sh 'python3 manage.py makemigrations'
                    sh 'python3 manage.py migrate'


                }
            }
        }
        
        stage('Test') {
            steps {
                script {
                    echo 'Testing the application...'
                    //sh 'python3 manage.py test'
                }
            }
        }
        
        stage('Transferring the app over SSH') {
            steps {
                
                withCredentials([sshUserPrivateKey(credentialsId: 'cc3b3f83-5b53-4aec-b089-92c2b96ca564', keyFileVariable: 'SSH_KEY')]) {
                script {
                    sh 'ssh -o StrictHostKeyChecking=no -i $SSH_KEY ec2-user@${EC2_HOST} "pwd"'
                    sh 'tar -czf app.tar.gz .'
                    sh 'scp -o StrictHostKeyChecking=no -i $SSH_KEY app.tar.gz ec2-user@${EC2_HOST}:/home/ec2-user'
                    sh 'ssh -o StrictHostKeyChecking=no -i $SSH_KEY ec2-user@${EC2_HOST} "tar -xzf /home/ec2-user/app.tar.gz"'
                    //sh 'ssh -o StrictHostKeyChecking=no -i $SSH_KEY ec2-user@${EC2_HOST} "rm /home/ec2-user/app.tar.gz"'
                    }
                }
            }
        }
        
        stage('Deploying the app') {
            steps {
                
                withCredentials([sshUserPrivateKey(credentialsId: 'cc3b3f83-5b53-4aec-b089-92c2b96ca564', keyFileVariable: 'SSH_KEY')]) {
                script {
                    sh 'ssh -o StrictHostKeyChecking=no -i $SSH_KEY ec2-user@${EC2_HOST} "sudo docker stop studenthub || true"'
                    sh 'ssh -o StrictHostKeyChecking=no -i $SSH_KEY ec2-user@${EC2_HOST} "sudo docker rm studenthub || true"'
                    sh 'ssh -o StrictHostKeyChecking=no -i $SSH_KEY ec2-user@${EC2_HOST} "sudo docker build -t studenthub /home/ec2-user/"'
                    sh 'ssh -o StrictHostKeyChecking=no -i $SSH_KEY ec2-user@${EC2_HOST} "sudo docker run -d -p 80:8000 --name studenthub studenthub"'
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                echo 'Done.'
            }
        }
    }
}
