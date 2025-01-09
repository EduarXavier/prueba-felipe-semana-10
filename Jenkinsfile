pipeline {
    agent any

    environment {
     GIT_TAG_NAME = gitTagName()
     USER_DOCKEHUB = 'danielsanchez18'
    }

    stages {
        stage('Generar tag para imagen de docker') {
            steps {
                script {
                    env.GIT_TAG_NAME = gitTagName()
                }
            }
        }

        stage('Construir imagen') {
            steps {
                script {
                    sh '''
                    docker build -t gopenux/prueba-sem-ene8:$GIT_TAG_NAME -f Dockerfile.python ./app
                    '''
                }
            }
        }

        stage('Generar tag de la imagen') {
            steps {
                script {
                    sh '''
                    docker tag gopenux/prueba-sem-ene8:$GIT_TAG_NAME $USER_DOCKEHUB/gopenux-prueba-sem-ene8:$GIT_TAG_NAME
                    '''
                }
            }
        }

        stage('Subir imagen a Docker Hub'){
            steps{
                script{
                    sh'''
                    docker push $USER_DOCKEHUB/gopenux-prueba-sem-ene8:$GIT_TAG_NAME
                    '''
                }
            }
        }
        stage('Actualizar imagen en el Swarm Manager') {
            steps {
                script {
                    sh '''
                    docker service update --image $USER_DOCKEHUB/gopenux-sistemas-formacion:$GIT_TAG_NAME gopenux_backoffice 
                    '''
                }
            }
        }
    }
}