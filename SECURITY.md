# Security Notes

- Never commit `.env` files, passwords, SSH private keys, access tokens or cloud credentials.
- Store Jenkins credentials in Jenkins Credentials and scope them to the required job/folder.
- Use least-privilege IAM and SSH identities for cloud deployment.
- Keep SSH host-key verification enabled and verify host fingerprints through a trusted channel.
- Do not expose the Jenkins controller directly to the public internet.
- Do not grant broad Docker socket access to untrusted jobs; Docker access is effectively privileged.
- Review dependency and base-image updates before using this educational starter in a production environment.
