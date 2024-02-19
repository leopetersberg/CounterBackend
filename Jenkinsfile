pipeline {
    agent any
    environment {
        DOCKER_PATH = "/usr/local/bin/docker"
        DOCKER_USERNAME = 'leopetersberg'
        DOCKER_PASSWORD = credentials('DockerHubPasswortCredentialId')
        IMAGE_NAME = 'leopetersberg/counterbackend'
        // Variable für den Git Commit Hash
        GIT_COMMIT_HASH = '' // Wird später festgelegt
        GITHUB_TOKEN = credentials('GITHUB_TOKEN')
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
                // Git Commit Hash extrahieren und in einer Umgebungsvariablen speichern
                script {
                    GIT_COMMIT_HASH = sh(script: "git rev-parse HEAD", returnStdout: true).trim()
                    echo "Git Commit Hash: ${GIT_COMMIT_HASH}"
                }
            }
        }
        stage('Build Docker Image') {
            steps {
                echo 'Building Docker image...'
                // Verwenden des Git Commit Hashes als Tag für das Docker Image
                sh "${DOCKER_PATH} build -t ${IMAGE_NAME}:${GIT_COMMIT_HASH} ."
            }
        }
        stage('Login to Docker Hub') {
            steps {
                echo 'Logging in to Docker Hub...'
                sh "${DOCKER_PATH} login -u ${DOCKER_USERNAME} -p ${DOCKER_PASSWORD}"
            }
        }
        stage('Push Image') {
            steps {
                echo 'Pushing Docker image to Docker Hub...'
                // Image mit Git Commit Hash tag pushen
                sh "${DOCKER_PATH} push ${IMAGE_NAME}:${GIT_COMMIT_HASH}"
            }
        }
        stage('Logout from Docker Hub') {
            steps {
                echo 'Logging out from Docker Hub...'
                sh "${DOCKER_PATH} logout"
            }
        }
        stage('Update GitOps Repository') {
        steps {
            echo 'Authenticating to GitHub and updating GitOps repository with new Docker image tag...'
            script {
                // Entferne das Verzeichnis, falls es bereits existiert
                sh 'rm -rf CounterGitOps'
                // Klone das GitOps Repository, verwende das Token für die Authentifizierung
                sh "git clone https://leopetersberg:${GITHUB_TOKEN}@github.com/leopetersberg/CounterGitOps.git"
                dir('CounterGitOps') {
                    // Aktualisiere das Docker-Compose-File mit dem neuen Image-Tag
                    sh "sed -i '' 's|leopetersberg/counterbackend:.*|leopetersberg/counterbackend:${GIT_COMMIT_HASH}|' docker-compose.yaml"

                    // Füge Änderungen hinzu und committe sie
                    sh "git add docker-compose.yaml"
                    sh "git config user.email 'jenkins@example.com'"
                    sh "git config user.name 'Jenkins CI'"
                    sh "git commit -m 'Update backend image tag to ${GIT_COMMIT_HASH}'"
                    // Push Änderungen zurück zum Repository unter Verwendung des Tokens
                    sh "git push https://${GITHUB_TOKEN}@github.com/leopetersberg/CounterGitOps.git master"
                }
            }
        }
    }
    }
    post {
        always {
            echo 'Cleaning up...'
        }
        success {
            echo 'Build and push to Docker Hub succeeded with Git Commit Hash: ${GIT_COMMIT_HASH}.'
        }
        failure {
            echo 'Build or push to Docker Hub failed.'
        }
    }
}
