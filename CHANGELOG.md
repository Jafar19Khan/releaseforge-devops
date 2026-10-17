# Changelog

## Unreleased

- Reorganized the application, container configuration, CI workflows, deployment automation, and operational documentation.
- Replaced the original page with a responsive, accessible ReleaseForge interface.
- Added health endpoint checks, container health checks, security headers, and a Python HTTP smoke test.
- Added GitHub Actions and Azure Pipelines validation workflows alongside the Jenkins deployment pipeline.
- Updated Ansible deployment to use the root URL and `/healthz` endpoint.
- Added a step-by-step evidence guide with headings, expected outcomes, and troubleshooting notes.
- Redacted the known Jenkins agent secret from the copied evidence image.
