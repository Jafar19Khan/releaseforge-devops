# Security Policy

## Reporting a concern

Do not publish passwords, access tokens, private keys, cloud service-account keys, Jenkins agent secrets, or sensitive logs in issues or pull requests. If a secret is exposed, revoke or rotate it first, then remove the exposed value from the repository and related logs where possible.

## Operational safeguards

- Store Jenkins secrets in Jenkins Credentials and scope them to the minimum required jobs.
- Use dedicated, trusted build agents. Docker daemon access is effectively privileged.
- Do not make `/var/run/docker.sock` world-writable.
- Keep SSH host-key verification enabled for Ansible deployment.
- Restrict cloud firewall rules to the required ports and intended VM targets.
- Do not expose the Jenkins controller directly to the public internet without access controls.
- Pin and review base-image and dependency updates before production use.
- Review evidence screenshots for credentials, public IPs, project identifiers, and personal data before publication.

## Scope

This repository is a deployment example. It does not provide a security guarantee or substitute for an environment-specific security review.
