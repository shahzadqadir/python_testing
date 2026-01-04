pipeline {
    agent any
    stages {
        stage ("prebuild") {
            steps {
                sh "pip install -r requirements.txt"
            }
        }
        stage ("build") {
            steps {
                sh "python3 main.py"
            }
        }
    }
}