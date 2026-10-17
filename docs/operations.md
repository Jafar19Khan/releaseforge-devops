# Operations runbook

## Start locally
```bash
docker compose up --build -d
docker compose ps
python3 tests/smoke_test.py http://127.0.0.1:8082/
```

## Health and logs
```bash
curl --fail http://127.0.0.1:8082/healthz
curl --fail http://127.0.0.1:8082/
docker inspect --format '{{.State.Health.Status}}' releaseforge-website
docker compose logs --tail=100 website
```

## Port conflict
```bash
WEB_PORT=8090 docker compose up --build -d
python3 tests/smoke_test.py http://127.0.0.1:8090/
```

## Stop
```bash
docker compose down
```

## Jenkins prerequisites
- Linux agent with Git, Docker CLI/daemon access, Python 3, curl, and a POSIX shell.
- Jenkins Pipeline job configured from this repository.
- Agent able to bind test port `18082`.
- Review logs before rerunning a failed release.

## Security checklist
- Never place agent secrets, access tokens, passwords, or private keys in source, screenshots, build logs, or README examples.
- Keep Docker socket access restricted to trusted users and jobs.
- Limit cloud firewall rules to required ports and targets.
- Remove temporary cloud resources after testing.
- Rotate any credential that may have been exposed in a public screenshot or log.
