import requests
from bs4 import BeautifulSoup

def scan_url(url):
    results = []
    try:
        response = requests.get(url, timeout=10)
        headers = response.headers

        if "X-Frame-Options" not in headers:
            results.append("Clickjacking protection (X-Frame-Options) header missing.")
        if "Content-Security-Policy" not in headers:
            results.append("Content Security Policy header missing.")
        if "?id=" in url or "&id=" in url:
            results.append("Potential SQL injection parameter found in URL.")
        soup = BeautifulSoup(response.text, 'html.parser')
        if "<script>alert(1)</script>" in response.text:
            results.append("Possible XSS vulnerability detected.")
        if not results:
            results.append("No common vulnerabilities detected.")
    except Exception as e:
        results.append(f"Error scanning URL: {e}")
    return results
