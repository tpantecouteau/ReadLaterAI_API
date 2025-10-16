from urllib.parse import urlparse

def detect_source(url: str) -> str:
    host = urlparse(url).hostname or ""
    host = host.replace("www.", "")
    return host