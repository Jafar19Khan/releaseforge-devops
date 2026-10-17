# Architecture and design decisions

## Request path

1. Source changes are committed to Git.
2. GitHub Actions or Azure Pipelines validates required files, builds the image, starts a temporary container, and runs HTTP checks.
3. The Jenkins declarative pipeline validates source, builds the same image, and deploys locally or remotely.
4. Remote deployment uses Ansible and the `community.docker` collection to recreate the named service on a Linux host.
5. Nginx serves static assets and exposes `/healthz`.
6. The Python smoke test verifies the homepage response, expected page markers, and health response.

## Design decisions

- **Static application:** keeps runtime requirements small and makes deployment behavior easy to inspect.
- **Nginx container:** serves static assets without a Node.js runtime or package installation in the production container.
- **Dedicated health route:** separates runtime checks from homepage content.
- **Scoped container operations:** automation targets `releaseforge-website`; it does not delete unrelated containers.
- **Layered validation:** source checks, image build, health check, and HTTP content checks catch different classes of failure.
- **Secrets outside source:** credentials are referenced through Jenkins Credentials; no cloud provisioning keys are stored in this repository.
- **Historical evidence:** screenshots document the earlier Google Cloud VM/Jenkins/Docker workflow. The original VM was removed after the run.

## Scope and production considerations

This repository provides application packaging, CI validation, and deployment examples. It does not claim active uptime, automated cloud provisioning, TLS/domain configuration, a managed registry, centralized monitoring, or production certification. Before public production use, add a managed TLS/domain setup, a reviewed image-publishing policy, vulnerability scanning, monitoring/alerting, and an environment-specific rollback plan.
