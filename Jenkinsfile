pipeline {
    agent any
    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '15'))
        timeout(time: 20, unit: 'MINUTES')
    }
    parameters {
        choice(name: 'DEPLOY_MODE', choices: ['local', 'remote'], description: 'Deploy on this trusted agent or a configured remote Linux host')
        string(name: 'SERVER_IP', defaultValue: '', description: 'Remote target IP or DNS name; required for remote mode')
        string(name: 'ANSIBLE_USER', defaultValue: 'ubuntu', description: 'SSH user for the remote deployment host')
        booleanParam(name: 'PUSH_IMAGE', defaultValue: false, description: 'Push a tagged image to Docker Hub; configure credentials first')
        string(name: 'DOCKERHUB_NAMESPACE', defaultValue: '', description: 'Docker Hub namespace; required when pushing or remote deploying')
    }
    environment {
        IMAGE_NAME = 'releaseforge'
        CONTAINER_NAME = 'releaseforge-website'
        LOCAL_PORT = '8082'
    }
    stages {
        stage('Checkout') {
            steps { checkout scm }
        }
        stage('Validate source') {
            steps {
                sh '''
                    set -eu
                    test -s app/index.html
                    test -s app/assets/styles.css
                    test -s docker/nginx.conf
                    python3 -m py_compile tests/smoke_test.py
                    grep -q 'ReleaseForge' app/index.html
                    grep -q 'location = /healthz' docker/nginx.conf
                '''
            }
        }
        stage('Build image') {
            steps {
                sh 'docker build --pull -t "${IMAGE_NAME}:${BUILD_NUMBER}" -t "${IMAGE_NAME}:latest" .'
            }
        }
        stage('Push image') {
            when {
                anyOf {
                    expression { return params.PUSH_IMAGE }
                    expression { return params.DEPLOY_MODE == 'remote' }
                }
            }
            steps {
                script {
                    if (!params.DOCKERHUB_NAMESPACE?.trim()) {
                        error('DOCKERHUB_NAMESPACE is required when pushing an image or using remote deployment.')
                    }
                }
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', usernameVariable: 'REGISTRY_USER', passwordVariable: 'REGISTRY_TOKEN')]) {
                    sh '''
                        set -eu
                        set +x
                        printf '%s' "$REGISTRY_TOKEN" | docker login --username "$REGISTRY_USER" --password-stdin
                        docker tag "${IMAGE_NAME}:${BUILD_NUMBER}" "${DOCKERHUB_NAMESPACE}/${IMAGE_NAME}:${BUILD_NUMBER}"
                        docker tag "${IMAGE_NAME}:${BUILD_NUMBER}" "${DOCKERHUB_NAMESPACE}/${IMAGE_NAME}:latest"
                        docker push "${DOCKERHUB_NAMESPACE}/${IMAGE_NAME}:${BUILD_NUMBER}"
                        docker logout
                    '''
                }
            }
        }
        stage('Deploy locally') {
            when { expression { return params.DEPLOY_MODE == 'local' } }
            steps {
                sh '''
                    set -eu
                    docker rm -f "$CONTAINER_NAME" >/dev/null 2>&1 || true
                    docker run -d --name "$CONTAINER_NAME" \
                      --restart unless-stopped \
                      --label app=releaseforge \
                      --read-only \
                      --tmpfs /var/cache/nginx --tmpfs /var/run --tmpfs /tmp \
                      --security-opt no-new-privileges:true \
                      --cap-drop ALL \
                      --cap-add CHOWN --cap-add SETGID --cap-add SETUID --cap-add NET_BIND_SERVICE \
                      -p "${LOCAL_PORT}:80" \
                      "${IMAGE_NAME}:${BUILD_NUMBER}"
                '''
            }
        }
        stage('Deploy remotely with Ansible') {
            when { expression { return params.DEPLOY_MODE == 'remote' } }
            steps {
                script {
                    if (!params.SERVER_IP?.trim()) error('SERVER_IP is required for remote deployment.')
                    if (!params.DOCKERHUB_NAMESPACE?.trim()) error('DOCKERHUB_NAMESPACE is required for remote deployment.')
                }
                sshagent(credentials: ['deployment-ssh-key']) {
                    sh '''
                        set -eu
                        ansible-galaxy collection install -r ansible/requirements.yml
                        ANSIBLE_HOST_KEY_CHECKING=True ansible-playbook \
                          -i "${SERVER_IP}," ansible/deploy.yml \
                          -u "${ANSIBLE_USER}" \
                          -e "image_name=${DOCKERHUB_NAMESPACE}/${IMAGE_NAME}:${BUILD_NUMBER}" \
                          -e "published_port=80"
                    '''
                }
            }
        }
        stage('Verify deployment') {
            steps {
                script {
                    def target = params.DEPLOY_MODE == 'local' ? "http://127.0.0.1:${env.LOCAL_PORT}" : "http://${params.SERVER_IP}"
                    withEnv(["RELEASEFORGE_TARGET=${target}"]) {
                        sh '''
                            set -eu
                            for attempt in $(seq 1 20); do
                              if curl --fail --silent "$RELEASEFORGE_TARGET/healthz" >/dev/null; then break; fi
                              sleep 2
                            done
                            python3 tests/smoke_test.py "$RELEASEFORGE_TARGET"
                        '''
                    }
                }
            }
        }
    }
    post {
        success { echo 'ReleaseForge deployment and post-deployment checks succeeded.' }
        failure { echo 'ReleaseForge pipeline failed. Review the failed stage, logs, and target health before retrying.' }
    }
}
