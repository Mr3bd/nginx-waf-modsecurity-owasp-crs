import requests

tests = [
    ("SQL Injection", "http://localhost:8080/echo?q=' OR 1=1--", 403),
    ("XSS", "http://localhost:8080/echo?q=<script>alert(1)</script>", 403),
    ("Scanner UA", "http://localhost:8080/", 403, {"User-Agent": "sqlmap/1.0"}),
]

for name, url, expected, headers in [(t[0], t[1], t[2], t[3] if len(t) == 4 else {}) for t in tests]:
    r = requests.get(url, headers=headers)
    print(f"{name} → {r.status_code} (expected {expected})")