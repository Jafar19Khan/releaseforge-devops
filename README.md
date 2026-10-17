# ReleaseForge — Jenkins + Docker Assignment

ReleaseForge is an original, lightweight demonstration website for practicing a Jenkins CI/CD workflow, Docker image builds, Ansible deployment, and post-deployment smoke tests. It is an educational assignment project, not a claim of production certification.

## What is included

- A responsive static website served by Nginx in a small Docker image.
- `Jenkinsfile` with checkout, validation, image build, optional registry push, deployment, and HTTP verification stages.
- `docker-compose.yml` for a quick local run.
- Ansible playbook for deploying a named container on a Debian/Ubuntu target.
- A Python HTTP smoke test and optional Selenium browser test.
- Optional Azure Pipelines validation; Jenkins is the main CI/CD path.

## Prerequisites

- Git and Docker Engine with Compose plugin for local validation.
- For Jenkins: a Linux agent labelled `slave2`, with Git, Docker, Python 3 and curl installed. The Jenkins service account must have permission to use Docker.
- For remote deployment: Ansible, the `community.docker` collection, SSH access to the target, and Docker-compatible Debian/Ubuntu host.
- Optional registry push: configure a Jenkins username/password credential named `dockerhub-credentials`.
- Optional remote pipeline: configure an SSH private-key credential named `deployment-ssh-key`; enable the Jenkins SSH Agent plugin. Set `SERVER_IP` and `ANSIBLE_USER` when running the build.

Never commit access tokens, private keys, passwords, or live inventory files.

## Run locally

```bash
docker compose up --build -d
curl --fail http://127.0.0.1:8082/devopsIQ/
docker compose ps
docker compose logs website
```

Open `http://localhost:8082/devopsIQ/`. To use another port, set `WEB_PORT`, for example `WEB_PORT=8090 docker compose up --build -d`.

Stop the local project with `docker compose down`.

## Jenkins pipeline setup

1. Push this repository to a Git server and create a Jenkins Pipeline job using **Pipeline script from SCM**.
2. Ensure the agent label `slave2` exists and has Docker, Git, Python 3 and curl.
3. Install Ansible and the `community.docker` collection if you will use remote deployment:
   `ansible-galaxy collection install -r ansible/requirements.yml`
4. Run with `DEPLOY_MODE=local` to deploy on the Jenkins agent at port 8082.
5. For `DEPLOY_MODE=remote`, configure the Jenkins SSH credential `deployment-ssh-key`, provide `SERVER_IP`, and ensure the target allows inbound web traffic on the selected port. The target should be reachable by the Jenkins agent over SSH. The pushed Docker Hub image must be public for anonymous pulls, or registry authentication must be configured on the target host.
6. Set `PUSH_IMAGE=true` only after creating the `dockerhub-credentials` Jenkins credential and deciding the Docker Hub namespace. Update the repository/image naming convention to match your account before enabling the push.

The pipeline never deletes all Docker containers on a machine. Its local deploy stage only replaces the container named `releaseforge-website`.

## Smoke test

The HTTP check requires only Python's standard library:

```bash
python3 selenium_test.py http://127.0.0.1:8082/devopsIQ/
```

For an optional browser test, install a supported Chrome/Chromium browser and run:

```bash
python3 -m pip install -r requirements-test.txt
python3 selenium_test.py http://127.0.0.1:8082/devopsIQ/
```

Recent Selenium versions use Selenium Manager to resolve a compatible driver; avoid pinning a stale ChromeDriver version.

## Important notes

- The default local port is `8082`; remote deployment defaults to port `80`.
- The included Azure Pipeline is an optional validation workflow and does not replace Jenkins.
- `docker.yaml` and `chrome.yaml` are retained as compatibility/reference playbooks; `ansible/deploy.yml` is the preferred deployment playbook.
- This assignment does not create AWS infrastructure automatically. Configure cloud resources and firewall rules separately if deploying to a public server.
- For production use, add TLS/domain management, registry image digest pinning, automated vulnerability policy, backups and monitoring appropriate to the environment.

## Troubleshooting

- **Port already in use:** run `WEB_PORT=8090 docker compose up --build -d` or stop the conflicting service.
- **Permission denied for Docker:** configure the agent service account's Docker access using your administrator's approved policy; do not solve this by making the Docker socket world-writable.
- **SSH host-key failure:** verify the target host key and add it to the Jenkins agent's known hosts. Do not disable host-key checking for convenience.
- **Remote image pull fails:** verify the image name, registry namespace and registry authentication on the target host.
- **Selenium browser failure:** verify browser installation and network access; the HTTP smoke test is still useful without Selenium.

## Assignment checklist

- [ ] Docker image builds successfully.
- [ ] Local website responds with HTTP 200.
- [ ] Jenkins validation and build stages pass.
- [ ] Remote deployment passes, if a target host is configured.
- [ ] Smoke test verifies the ReleaseForge page.
- [ ] Screenshots of Jenkins stages and the running website are captured for submission.
