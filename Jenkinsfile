pipeline {
    agent any
    stages {
        stage("Unit test") {
            steps {
                sh "python3 manage.py test"
            }    
        }
    }
}