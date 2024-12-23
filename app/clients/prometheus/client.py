from prometheus_client import Counter, generate_latest, CollectorRegistry

REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP Requests', ['method', 'endpoint'])

