
import requests
import time

BASE_URL = "https://cybercor.org"
TIMEOUT = 10


def fetch(url: str, timeout: int = 10) -> requests.Response:
    """Trimite o cerere GET și returnează răspunsul serverului."""
    return requests.get(url, timeout=timeout)


def get_status(url: str) -> int:
    """Returnează codul de stare HTTP pentru o adresă."""
    return fetch(url).status_code


def get_title(html: str) -> str:
    """Extrage titlul dintre tag-urile title din codul HTML."""
    lower_html = html.lower()
    start = lower_html.find("<title>")
    if start == -1:
        return ""
    start += len("<title>")
    end = lower_html.find("</title>", start)
    if end == -1:
        return ""
    return html[start:end].strip()


def page_exists(url: str) -> bool:
    """Verifică dacă URL-ul răspunde fără eroare de rețea."""
    try:
        response = fetch(url)
        return response.status_code < 400
    except requests.RequestException:
        return False


def check_paths(base: str, paths: list[str]) -> dict[str, int]:
    """Returnează codul HTTP pentru fiecare cale indicată."""
    results = {}
    for index, path in enumerate(paths):
        if index:
            time.sleep(1)
        url = base.rstrip("/") + "/" + path.lstrip("/")
        try:
            results[path] = get_status(url)
        except requests.RequestException:
            results[path] = 0
    return results


def get_header(url: str, name: str, default: str = "lipsește") -> str:
    """Returnează valoarea unui antet HTTP sau valoarea implicită."""
    response = fetch(url)
    return response.headers.get(name, default)


def security_headers(url: str) -> dict[str, bool]:
    """Verifică prezența celor cinci antete de securitate cerute."""
    response = fetch(url)
    names = [
        "Strict-Transport-Security",
        "Content-Security-Policy",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
    ]
    return {name: name in response.headers for name in names}


def score_headers(results: dict[str, bool]) -> str:
    """Returnează scorul antetelor prezente, de exemplu 3/5."""
    return f"{sum(results.values())}/{len(results)}"


def fetch_robots(base: str) -> str | None:
    """Returnează textul robots.txt sau None dacă nu poate fi citit."""
    try:
        response = fetch(base.rstrip("/") + "/robots.txt")
        if response.status_code == 200:
            return response.text
        return None
    except requests.RequestException:
        return None


def disallowed_paths(robots_text: str | None) -> list[str]:
    """Extrage valorile Disallow din robots.txt; acceptă și None."""
    if not robots_text:
        return []
    paths = []
    for line in robots_text.splitlines():
        line = line.strip()
        if line.lower().startswith("disallow:"):
            value = line.split(":", 1)[1].strip()
            if value:
                paths.append(value)
    return paths


def response_times(*urls: str) -> dict[str, float | None]:
    """Returnează timpul de răspuns în secunde pentru fiecare URL."""
    results = {}
    for index, url in enumerate(urls):
        if index:
            time.sleep(1)
        try:
            start = time.perf_counter()
            fetch(url)
            results[url] = round(time.perf_counter() - start, 3)
        except requests.RequestException:
            results[url] = None
    return results


def log(message: str, **details) -> None:
    """Afișează un mesaj urmat de detaliile primite ca argumente numite."""
    extra = " | ".join(f"{key}={value}" for key, value in details.items())
    print(f"{message} | {extra}" if extra else message)


def main():
    try:
        
        response = fetch(BASE_URL)
        print("Ex. 21 - Cod de stare:", response.status_code)

        
        print("Ex. 22 - Coduri:", check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

        print("Ex. 23 - Timeout implicit:", fetch(BASE_URL).status_code)
        time.sleep(1)
        print("Ex. 23 - Timeout 3:", fetch(BASE_URL, timeout=3).status_code)

        
        print("Ex. 24 - Titlu:", get_title(response.text))
        print("Ex. 25 - Docstring:", get_title.__doc__)
        help(get_title)

        
        print("Ex. 26 - get_status(123) ar produce o eroare la cererea HTTP, nu din cauza adnotării.")
        # Nu apelăm get_status(123), pentru a nu opri programul.

       
        print("Ex. 27 - Domeniu invalid:", page_exists("https://this-domain-does-not-exist.invalid"))

       
        print("Ex. 28 - Căi:", check_paths(BASE_URL, ["/", "/robots.txt", "/sitemap.xml"]))

      
        print("Ex. 29 - Server:", get_header(BASE_URL, name="Server"))

        headers = security_headers(BASE_URL)
        print("Ex. 30 - Antete de securitate:", headers)
        print("Ex. 31 - Scor:", score_headers(headers))

        
        robots = fetch_robots(BASE_URL)
        print("Ex. 32 - Căi Disallow:", disallowed_paths(robots))
        print("Ex. 32 - Test cu None:", disallowed_paths(None))

       
        print("Ex. 33 - Timpi:", response_times(BASE_URL, BASE_URL + "/robots.txt"))

        log("verificat", url=BASE_URL, status=response.status_code)
        print("\nDiferență: print() afișează valoarea pe ecran; return o trimite înapoi")
        print("codului care a apelat funcția, pentru a putea fi folosită mai departe.")
    except requests.RequestException as error:
        print("Eroare de rețea:", error)


if __name__ == "__main__":
    main()
