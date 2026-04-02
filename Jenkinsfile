pipeline {
    agent any

    environment {
        REGISTRY = 'registry.cloudforyour.work/forgeplatform'
        IMAGE_NAME = 'forge-assistant'
        VERSION = sh(script: "cat VERSION 2>/dev/null || echo 'dev'", returnStdout: true).trim()
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    python3.12 -m venv .venv
                    . .venv/bin/activate
                    pip install --quiet ruff
                    ruff check app/ tests/
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    . .venv/bin/activate
                    pip install --quiet -r requirements-dev.txt
                    python -m pytest tests/ -v --tb=short --junitxml=test-results.xml
                '''
            }
            post {
                always {
                    junit allowEmptyResults: true, testResults: 'test-results.xml'
                }
            }
        }

        stage('Build Image') {
            steps {
                sh """
                    docker build \
                        -t ${REGISTRY}/${IMAGE_NAME}:${VERSION} \
                        -t ${REGISTRY}/${IMAGE_NAME}:latest \
                        .
                """
            }
        }

        stage('Scan Image') {
            steps {
                sh """
                    docker run --rm \
                        -v /var/run/docker.sock:/var/run/docker.sock \
                        aquasec/trivy:latest image \
                        --severity CRITICAL,HIGH \
                        --exit-code 1 \
                        ${REGISTRY}/${IMAGE_NAME}:${VERSION} || true
                """
            }
        }

        stage('Push Image') {
            when {
                anyOf {
                    branch 'main'
                    buildingTag()
                }
            }
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'harbor-registry',
                    usernameVariable: 'REGISTRY_USER',
                    passwordVariable: 'REGISTRY_PASS'
                )]) {
                    sh """
                        echo \$REGISTRY_PASS | docker login ${REGISTRY} -u \$REGISTRY_USER --password-stdin
                        docker push ${REGISTRY}/${IMAGE_NAME}:${VERSION}
                        docker push ${REGISTRY}/${IMAGE_NAME}:latest
                    """
                }
            }
        }

        stage('Deploy') {
            when {
                anyOf {
                    branch 'main'
                    buildingTag()
                }
            }
            steps {
                sh """
                    echo "Deploying forge-assistant ${VERSION}..."
                    ssh deploy@forge-prod "cd /opt/forge && \
                        docker compose -f docker-compose.yml \
                            -f docker-compose.assistant.yml pull forge-assistant && \
                        docker compose -f docker-compose.yml \
                            -f docker-compose.assistant.yml up -d forge-assistant"
                """
            }
        }
    }

    post {
        always {
            sh 'rm -rf .venv'
            cleanWs()
        }
        failure {
            echo "Build failed for forge-assistant ${VERSION}"
        }
        success {
            echo "Build succeeded for forge-assistant ${VERSION}"
        }
    }
}
