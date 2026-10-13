import requests

SITES = [
    # Pagini obișnuite (Părțile 2, 3 și 4)
    "https://example.com",
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://httpbin.org/status/200",
    "https://httpbin.org/redirect/1",
    "https://httpbin.org/delay/2",
    # Pagini care eșuează
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://httpbin.org/delay/10",
    "http://this-site-does-not-exist.invalid",
    # Anteturi de securitate (Partea 5)
    "https://httpbin.org/response-headers?X-Frame-Options=DENY&X-Content-Type-Options=nosniff",
    "https://httpbin.org/response-headers?x-frame-options=DENY",
    # Răspunde aleatoriu cu 200 sau 500 (Partea 6)
    "https://httpbin.org/status/200,500",
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options",
]


def build_url(host, path):
    """Returnează o adresă completă, de exemplu https://example.com/login."""
    pass


def is_https(url):
    """Returnează True dacă adresa începe cu https://, altfel False."""
    pass


def show_response(url):
    """Trimite un GET la url și afișează statusul și Content-Type."""
    pass


def check_site(url):
    """Returnează un dicționar cu: status, content_type, length, server."""
    pass


def scan_sites():
    """Verifică toate site-urile din SITES, afișează-le pe cele care merg și un rezumat."""
    pass


def check_headers(url):
    """Returnează un dicționar cu: present, missing, score."""
    pass


def retry_check(url, attempts=3):
    """Încearcă de cel mult `attempts` ori; returnează un dicționar cu: status, attempts."""
    pass
import requests


SITES = [
    "https://httpbin.org/html",
    "https://httpbin.org/json",
    "https://example.com",
    "https://httpbin.org/status/200",
    "https://httpbin.org/status/404",
    "https://httpbin.org/status/500",
    "https://this-site-does-not-exist.invalid"
]

SECURITY_HEADERS = [
    "Strict-Transport-Security",
    "Content-Security-Policy",
    "X-Frame-Options",
    "X-Content-Type-Options"
]

def build_url(host, path):
    """Construiește URL-ul indiferent dacă path începe sau nu cu /."""
    if not path.startswith("/"):
        path = "/" + path
    return f"https://{host}{path}"

def is_https(url):
    """Returnează True dacă URL-ul începe cu https://, altfel False."""
    return url.startswith("https://")


def show_response(url):
    """Trimite o cerere GET și afișează codul de stare și Content-Type."""
    response = requests.get(url)
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('Content-Type', 'unknown')}")



  def check_site(url):
    """Verifică un site și returnează un dicționar cu detalii, fără a genera erori."""
    try:
        response = requests.get(url, timeout=5)
        content_type = response.headers.get("Content-Type", "unknown").split(";")[0].strip()
        server = response.headers.get("Server", "unknown")
        return {
            "status": response.status_code,
            "content_type": content_type,
            "length": len(response.content),
            "server": server
        }
    except Exception as e:
        return {"status": None, "error": str(e)}


def scan_sites():
    """Verifică toate site-urile din SITES, afișează cele cu status 200 sortate după lungime și un rezumat."""
    results = []
    success_count = 0
    fail_count = 0

    for url in SITES:
        res = check_site(url)
        if res["status"] == 200:
            success_count += 1
            results.append((url, res["length"]))
        else:
            fail_count += 1

  
    results.sort(key=lambda x: x[1], reverse=True)

    for url, length in results:
        print(f"{url:<30} -> 200, {length} octeți")

    print(f"Reușite: {success_count} | Eșuate: {fail_count}")



def check_headers(url):
    """Verifică prezența antetelor de securitate și calculează un scor."""
    try:
        response = requests.get(url, timeout=5)
        # Convertim cheile antetelor primite la lowercase pentru căutare case-insensitive
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        
        present = []
        missing = []

        for header in SECURITY_HEADERS:
            if header.lower() in headers_lower:
                present.append(header)
            else:
                missing.append(header)

        score = int((len(present) / len(SECURITY_HEADERS)) * 100)

        return {
            "present": present,
            "missing": missing,
            "score": score,
        }
    except Exception as e:
        return {"status": None, "error": str(e)}



def retry_check(url, attempts=3):
    """Încearcă verificarea de cel mult 'attempts' ori în caz de eroare sau status >= 500."""
    last_status = None
    last_error = None

    for current_attempt in range(1, attempts + 1):
        try:
            response = requests.get(url, timeout=5)
            last_status = response.status_code

            # Dacă statusul este sub 500 (inclusiv 404), ne oprești imediat
            if last_status < 500:
                return {"status": last_status, "attempts": current_attempt}
            
            # Dacă statusul >= 500, continuăm bucla (dacă mai avem încercări)
        except Exception as e:
            last_error = str(e)
            last_status = None

  
    result = {"status": last_status, "attempts": attempts}
    if last_error:
        result["error"] = last_error
    return result
