

from urllib.parse import urlparse, urljoin
import re
from html.parser import HTMLParser
import hashlib
import json
import socket
import ssl
from datetime import datetime, timezone
import requests
import time

BASE_URL = "https://cybercor.org"
TIMEOUT = 10


def extract_links(html: str) -> list[str]:
    """Extrage linkurile href fără duplicate, păstrând ordinea."""
    return list(dict.fromkeys(re.findall(r'href="([^"]+)"', html)))


def split_links(links: list[str], domain: str) -> tuple[list[str], list[str]]:
    """Împarte linkurile în interne și externe folosind domeniul URL-ului."""
    internal, external = [], []
    for link in links:
        full_url = urljoin(domain.rstrip("/") + "/", link)
        netloc = urlparse(full_url).netloc.lower()
        expected = urlparse(domain if "://" in domain else "https://" + domain).netloc.lower()
        if netloc == expected or netloc.endswith("." + expected):
            internal.append(full_url)
        else:
            external.append(full_url)
    return internal, external


class ImageFinder(HTMLParser):
    """Parser HTML care colectează atributul src al tagurilor img."""
    def __init__(self):
        super().__init__()
        self.images = []

    def handle_starttag(self, tag, attrs):
        """Este apelată automat de parser la întâlnirea unui tag de început."""
        if tag.lower() == "img":
            src = dict(attrs).get("src")
            if src:
                self.images.append(src)


def page_fingerprint(url: str) -> str:
    """Returnează amprenta SHA-256 a conținutului primit."""
    response = requests.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    return hashlib.sha256(response.content).hexdigest()


def resolve(hostname: str) -> str:
    """Returnează o adresă IPv4 pentru numele de domeniu."""
    return socket.gethostbyname(hostname)


def cert_days_left(hostname: str) -> int:
    """Calculează câte zile întregi rămân până la expirarea certificatului TLS."""
    context = ssl.create_default_context()
    with socket.create_connection((hostname, 443), timeout=TIMEOUT) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
            cert = secure_sock.getpeercert()
    expiry_seconds = ssl.cert_time_to_seconds(cert["notAfter"])
    expiry = datetime.fromtimestamp(expiry_seconds, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    return (expiry - now).days


def main():
    # Ex. 35
    parsed = urlparse("https://cybercor.org/path?x=1#top")
    print("Ex. 35 - scheme:", parsed.scheme)
    print("netloc:", parsed.netloc, "path:", parsed.path,
          "query:", parsed.query, "fragment:", parsed.fragment)

    
    for relative in ("/about", "contact.html", "../index.html"):
        print("Ex. 36 -", relative, "->", urljoin(BASE_URL + "/", relative))

    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        response.raise_for_status()
       
        links = extract_links(response.text)
        print("Ex. 37 - Linkuri unice găsite:", len(links))

        
        internal, external = split_links(links, BASE_URL)
        print("Ex. 38 - Interne:", len(internal), "Externe:", len(external))

        
        test_html = """
        <html><body>
        <img src="/logo.png" alt="Logo">
        <IMG SRC="poza.jpg">
        <img alt="imagine fără src">
        <img src="https://cdn.example.com/banner.webp" />
        <a href="/despre">Aceasta nu este o imagine</a>
        </body></html>
        """
        finder = ImageFinder()
        finder.feed(test_html)
        print("Ex. 39 - Imagini test:", finder.images)
        assert finder.images == [
            "/logo.png", "poza.jpg", "https://cdn.example.com/banner.webp"
        ], "Parserul nu a găsit exact imaginile așteptate"
        print("Testul a trecut!")
        finder = ImageFinder()
        finder.feed(response.text)
        print("Imagini găsite pe site:", len(finder.images))
        for src in finder.images:
            print(src)
        print("Număr apariții <img:", response.text.lower().count("<img"))

       
        first = page_fingerprint(BASE_URL)
        time.sleep(1)
        second = page_fingerprint(BASE_URL)
        print("Ex. 40 - Amprenta 1:", first)
        print("Amprenta 2:", second)
        print("Amprente identice:", first == second)
        # Amprentele diferă dacă se schimbă conținutul primit, inclusiv elemente dinamice.

      
        with open("headers.json", "w", encoding="utf-8") as file:
            json.dump(dict(response.headers), file, indent=2, ensure_ascii=False)
        with open("headers.json", "r", encoding="utf-8") as file:
            loaded_headers = json.load(file)
        print("Ex. 41 - Content-Type din fișier:", loaded_headers.get("Content-Type", "lipsește"))

        
        print("Ex. 42 - IP cybercor.org:", resolve("cybercor.org"))

       
        print("Ex. 43 - Zile până la expirarea certificatului:", cert_days_left("cybercor.org"))
    except (requests.RequestException, OSError, socket.error, ssl.SSLError, KeyError, ValueError) as error:
        print("O operație web/DNS/TLS nu a reușit:", error)


if __name__ == "__main__":
    main()
