# Assignment Notes

## Objective
Demonstrate source checkout, automated validation, Docker image creation, deployment using Ansible, and post-deployment verification.

## Architecture
Git repository → Jenkins agent (`slave2`) → Docker image → (optional registry) → local or remote container → HTTP smoke test.

## What changed from the supplied starter repository
- Removed references to the previous author's GitHub and Docker Hub accounts.
- Replaced the old branded page with a new ReleaseForge assignment demo.
- Replaced the old base image and unrelated exposed ports with an Nginx-based image.
- Removed a bundled executable mistakenly named `docker-compose`; supplied a real Compose YAML file.
- Replaced broad Docker container deletion with a project-scoped container name.
- Replaced plaintext password interpolation with Jenkins credentials and `--password-stdin` for optional image push.
- Removed the hardcoded ChromeDriver version; Selenium Manager is preferred for optional browser testing.
- Added setup, validation, and troubleshooting documentation.

## Submission evidence to capture
1. Jenkins pipeline successful stage view.
2. Docker container status (`docker ps`).
3. Browser showing the ReleaseForge page.
4. HTTP smoke-test output.
5. If remote deployment is required, Ansible output and the deployed page URL.
