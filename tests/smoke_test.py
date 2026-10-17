# HTTP smoke test using only Python's standard library.
import sys
from urllib.error import URLError
from urllib.request import Request, urlopen

EXPECTED_TITLE = "ReleaseForge — Ship with confidence"
EXPECTED_MARKERS = ("Ship better.", "DELIVERY FLOW", "POST-DEPLOYMENT CHECKS")

def fetch(url: str) -> tuple[int, str]:
    request = Request(url, headers={"User-Agent": "ReleaseForge-SmokeTest/1.0"})
    with urlopen(request, timeout=8) as response:
        return response.status, response.read().decode("utf-8", errors="replace")

def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <base-url>", file=sys.stderr)
        return 2
    base = sys.argv[1].rstrip("/")
    try:
        status, body = fetch(base + "/")
        health_status, health_body = fetch(base + "/healthz")
    except (URLError, TimeoutError, OSError) as exc:
        print(f"FAIL: endpoint is unreachable: {exc}", file=sys.stderr)
        return 1
    errors = []
    if status != 200:
        errors.append(f"homepage returned HTTP {status}")
    if EXPECTED_TITLE not in body:
        errors.append("expected document title was not found")
    for marker in EXPECTED_MARKERS:
        if marker not in body:
            errors.append(f"expected page marker missing: {marker}")
    if health_status != 200 or health_body.strip() != "ok":
        errors.append(f"health endpoint returned HTTP {health_status} with body {health_body!r}")
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {base}/ returned HTTP 200 and expected page markers")
    print(f"PASS: {base}/healthz returned HTTP 200")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
