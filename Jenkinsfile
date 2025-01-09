pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS = 'docker-hub-credentials' 
        DOCKER_REPO = 'danielsanchez18/gopenux-prueba-sem-ene8' 
        IMAGE_NAME = 'gopenux/prueba-sem-ene8:latest' 
        TAG = "latest-${BUILD_NUMBER}" 
        DOCKER_HOST = 'tcp://localhost:5000'          
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("${DOCKER_REPO}:${TAG}", ".")
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    docker.withRegistry('https://registry.hub.docker.com', DOCKER_CREDENTIALS) {
                        docker.image("${DOCKER_REPO}:${TAG}").push()
                    }
                }
            }
        }

        stage('Update Docker Swarm Service') {
            steps {
                script {
                    sh """
                        docker --host=${DOCKER_HOST} service update --image ${DOCKER_REPO}:${TAG} ${SERVICE_NAME}
                    """
                }
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}
