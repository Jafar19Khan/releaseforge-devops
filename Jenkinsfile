pipeline {
    agent { label 'slave2' }
    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }
    parameters {
        choice(name: 'DEPLOY_MODE', choices: ['local', 'remote'], description: 'Deploy on the Jenkins agent or a remote Ansible host')
        string(name: 'SERVER_IP', defaultValue: '', description: 'Remote target IP; required for remote deployment')
        string(name: 'ANSIBLE_USER', defaultValue: 'ubuntu', description: 'SSH user configured for the deployment host')
        booleanParam(name: 'PUSH_IMAGE', defaultValue: false, description: 'Push image to Docker Hub; required for remote deployment')
    }
    environment {
        IMAGE_NAME = 'releaseforge-demo'
        CONTAINER_NAME = 'releaseforge-website'
        LOCAL_PORT = '8082'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Validate project') {
            steps {
                sh '''set -eu
                    test -f Dockerfile
                    test -f devopsIQ/index.html
                    grep -q 'ReleaseForge' devopsIQ/index.html
                    python3 -m py_compile selenium_test.py
                '''
            }
        }
        stage('Build image') {
            steps {
                sh '''set -eu
                    docker build --pull -t ${IMAGE_NAME}:${BUILD_NUMBER} -t ${IMAGE_NAME}:latest .
                '''
            }
        }
        stage('Optional image push') {
            when { anyOf { expression { return params.PUSH_IMAGE }; expression { return params.DEPLOY_MODE == 'remote' } } }
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'REGISTRY_USER', passwordVariable: 'REGISTRY_TOKEN')]) {
                    sh '''set +x
                        echo "$REGISTRY_TOKEN" | docker login --username "$REGISTRY_USER" --password-stdin
                        docker tag ${IMAGE_NAME}:${BUILD_NUMBER} "$REGISTRY_USER/${IMAGE_NAME}:${BUILD_NUMBER}"
                        docker tag ${IMAGE_NAME}:${BUILD_NUMBER} "$REGISTRY_USER/${IMAGE_NAME}:latest"
                        docker push "$REGISTRY_USER/${IMAGE_NAME}:${BUILD_NUMBER}"
                        docker push "$REGISTRY_USER/${IMAGE_NAME}:latest"
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy locally') {
            when { expression { return params.DEPLOY_MODE == 'local' } }
            steps {
                sh '''set -eu
                    docker rm -f "$CONTAINER_NAME" 2>/dev/null || true
                    docker run -d --name "$CONTAINER_NAME" --restart unless-stopped \
                      -p ${LOCAL_PORT}:80 --label project=releaseforge \
                      ${IMAGE_NAME}:${BUILD_NUMBER}
                    for attempt in $(seq 1 15); do
                      if curl --fail --silent http://127.0.0.1:${LOCAL_PORT}/devopsIQ/ >/dev/null; then exit 0; fi
                      sleep 2
                    done
                    docker logs "$CONTAINER_NAME"
                    exit 1
                '''
            }
        }
        stage('Deploy remotely with Ansible') {
            when { expression { return params.DEPLOY_MODE == 'remote' } }
            steps {
                script {
                    if (!params.SERVER_IP?.trim()) error('SERVER_IP is required when DEPLOY_MODE=remote')
                }
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'REGISTRY_USER', passwordVariable: 'REGISTRY_TOKEN')]) {
                    sshagent(credentials: ['deployment-ssh-key']) {
                        sh '''set -eu
                            test -f ansible/deploy.yml
                            ANSIBLE_HOST_KEY_CHECKING=True ansible-playbook -i "${SERVER_IP}," ansible/deploy.yml \
                              -u "${ANSIBLE_USER}" \
                              -e "image_name=${REGISTRY_USER}/${IMAGE_NAME}:${BUILD_NUMBER}" \
                              -e "published_port=80"
                        '''
                    }
                }
            }
        }
        stage('Smoke test') {
            steps {
                script {
                    def target = params.DEPLOY_MODE == 'local' ? 'http://127.0.0.1:8082/devopsIQ/' : "http://${params.SERVER_IP}/devopsIQ/"
                    sh "curl --fail --show-error --silent '${target}' | grep -q 'ReleaseForge'"
                }
            }
        }
    }
    post {
        success { echo 'ReleaseForge pipeline completed successfully.' }
        failure { echo 'Pipeline failed. Review the stage logs before retrying.' }
    }
}
