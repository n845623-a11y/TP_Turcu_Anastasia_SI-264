# Modul reutilizabil pentru laboratorul Python
# Student: Numele Prenumele

import hashlib
import json
import re
import socket
import ssl
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from urllib.parse import urljoin, urlparse

import requests

TIMEOUT = 10
DEFAULT_HEADERS = {"User-Agent": "WebLab-Student"}
SECURITY_HEADER_NAMES = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
    "Referrer-Policy",
]


def fetch(url: str, timeout: int = TIMEOUT) -> requests.Response:
    """Descarcă o pagină cu GET și returnează răspunsul."""
    return requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Extrage titlul din HTML fără să facă o cerere web."""
    lower_html = html.lower()
    start = lower_html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = lower_html.find("</title>", start)
    return html[start:end].strip() if end != -1 else ""


def security_headers(url: str) -> dict[str, bool]:
    """Verifică prezența celor cinci antete de securitate."""
    response = fetch(url)
    return {name: name in response.headers for name in SECURITY_HEADER_NAMES}


def score_headers(results: dict[str, bool]) -> str:
    """Returnează numărul antetelor prezente din total."""
    return f"{sum(results.values())}/{len(results)}"


def check_paths(base: str, paths: list[str]) -> dict[str, int]:
    """Returnează codul de stare pentru fiecare cale din listă."""
    result = {}
    for index, path in enumerate(paths):
        if index:
            time.sleep(1)
        url = urljoin(base.rstrip("/") + "/", path.lstrip("/"))
        try:
            result[path] = get_status(url)
        except requests.RequestException:
            result[path] = 0
    return result


def extract_links(html: str) -> list[str]:
    """Extrage legăturile href fără duplicate, păstrând ordinea."""
    return list(dict.fromkeys(re.findall(r"href=[\"']([^\"']+)[\"']", html, flags=re.I)))


def split_links(links: list[str], domain: str) -> tuple[list[str], list[str]]:
    """Împarte legăturile în liste interne și externe."""
    internal, external = [], []
    base = domain if "://" in domain else "https://" + domain
    expected = urlparse(base).netloc.lower()
    for link in links:
        full = urljoin(base.rstrip("/") + "/", link)
        netloc = urlparse(full).netloc.lower()
        if netloc == expected or netloc.endswith("." + expected):
            internal.append(full)
        elif netloc:
            external.append(full)
    return internal, external


def fetch_robots(base: str) -> str | None:
    """Returnează conținutul robots.txt sau None dacă lipsește."""
    try:
        response = fetch(urljoin(base.rstrip("/") + "/", "robots.txt"))
        return response.text if response.status_code == 200 else None
    except requests.RequestException:
        return None


def disallowed_paths(robots_text: str | None) -> list[str]:
    """Extrage valorile Disallow din textul robots.txt."""
    if not robots_text:
        return []
    result = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()
            if value:
                result.append(value)
    return result


def resolve(hostname: str) -> str:
    """Rezolvă domeniul într-o adresă IPv4."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Returnează numărul de zile până la expirarea certificatului TLS."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            cert = secure_sock.getpeercert()
    expiry_seconds = ssl.cert_time_to_seconds(cert["notAfter"])
    expiry = datetime.fromtimestamp(expiry_seconds, tz=timezone.utc)
    return (expiry - datetime.now(timezone.utc)).days


def page_fingerprint(url: str) -> str:
    """Calculează amprenta SHA-256 a conținutului paginii."""
    response = fetch(url)
    response.raise_for_status()
    return hashlib.sha256(response.content).hexdigest()


def site_report(url: str) -> dict:
    """Colectează informațiile cerute și salvează raportul în report.json."""
    report = {
        "url_requested": url,
        "status_code": None,
        "final_url": None,
        "title": "",
        "ip_address": None,
        "redirect_chain": [],
        "security_headers": {},
        "security_score": "0/5",
        "certificate_days_left": None,
        "internal_links": 0,
        "external_links": 0,
        "disallowed_paths": [],
        "errors": [],
        "checked_at": datetime.now().isoformat(),
    }

    try:
        response = fetch(url)
        response.raise_for_status()
        report["status_code"] = response.status_code
        report["final_url"] = response.url
        report["title"] = get_title(response.text)
        for item in response.history:
            report["redirect_chain"].append({
                "status_code": item.status_code,
                "url": item.url,
                "location": item.headers.get("Location", ""),
            })
        report["security_headers"] = security_headers(url)
        report["security_score"] = score_headers(report["security_headers"])
        links = extract_links(response.text)
        internal, external = split_links(links, response.url)
        report["internal_links"] = len(internal)
        report["external_links"] = len(external)
    except requests.RequestException as error:
        report["errors"].append(f"HTTP: {error}")

    hostname = urlparse(url).hostname
    if hostname:
        try:
            report["ip_address"] = resolve(hostname)
        except OSError as error:
            report["errors"].append(f"DNS: {error}")
        try:
            report["certificate_days_left"] = cert_days_left(hostname)
        except (OSError, ssl.SSLError, ValueError, KeyError) as error:
            report["errors"].append(f"TLS: {error}")

    robots = fetch_robots(url)
    report["disallowed_paths"] = disallowed_paths(robots)

    with open("report.json", "w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    print(f"=== Raport site: {url} ===")
    print("Cod de stare:", report["status_code"])
    print("URL final:", report["final_url"])
    print("Titlu:", report["title"] or "nu a fost găsit")
    print("Adresă IP:", report["ip_address"] or "indisponibilă")
    if report["redirect_chain"]:
        print("Redirecționări:", " -> ".join(
            f'{item["status_code"]} {item["url"]}' for item in report["redirect_chain"]
        ))
    else:
        print("Redirecționări: niciuna observată")
    print("Scor antete de securitate:", report["security_score"])
    print("Zile până la expirarea certificatului:", report["certificate_days_left"])
    print("Legături:", report["internal_links"], "interne,", report["external_links"], "externe")
    print("Căi Disallow:", report["disallowed_paths"] or "niciuna găsită")
    if report["errors"]:
        print("Observații:", "; ".join(report["errors"]))
    print("Salvat în report.json")
    return report


if __name__ == "__main__":
    # Ex. 46: acest bloc rulează numai când fișierul este executat direct.
    print("Autotest:", get_status("https://cybercor.org"))
