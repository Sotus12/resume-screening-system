pipeline {

    agent any

    stages {

        stage('Clone Repository') {

            steps {
                git branch: 'main', url: 'https://github.com/Sotus12/resume-screening-system.git'
            }
        }

        stage('Install Dependencies') {

            steps {

                bat 'pip install -r requirements.txt'
            }
        }

        stage('Train Model') {

            steps {

                bat 'python train.py'
            }
        }

        stage('Build Docker Image') {

            steps {

                bat 'docker build -t resume-screening .'
            }
        }

        stage('Stop Old Container') {

            steps {

                bat 'docker stop resume-container || exit 0'
                bat 'docker rm resume-container || exit 0'
            }
        }

        stage('Run Docker Container') {

            steps {

                bat 'docker run -d --name resume-container -p 5000:5000 resume-screening'
            }
        }
    }
}