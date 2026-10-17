# Contributing

## Development workflow

1. Create a branch for a focused change.
2. Keep application, container, CI, and documentation changes consistent.
3. Run the source checks and container smoke test locally.
4. Include troubleshooting notes for any new configuration or operational behavior.
5. Never include credentials, local environment files, or unredacted logs.

## Validation

```bash
python3 -m py_compile tests/smoke_test.py
docker build --pull -t releaseforge:local .
docker compose up -d
python3 tests/smoke_test.py http://127.0.0.1:8082/
docker compose down
```

## Pull requests

Explain the reason for the change, the files affected, validation performed, and any remaining limitations. Avoid claiming checks that were not run.
