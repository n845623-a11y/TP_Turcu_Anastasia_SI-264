

import requests
import urllib.request
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def main():

    print("Ex. 1 - versiunea requests:", requests.__version__)
    print("urllib.request este din biblioteca standard Python.")

    # Ex. 2: primul stil
    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        print("Ex. 2 - requests.get:", response.status_code)
        # Avantaj: requests.get este clar și arată de unde vine funcția.
        # Stilul from requests import get permite scrierea mai scurtă: get(...).
    except requests.RequestException as error:
        print("Ex. 2 - Cererea nu a reușit:", error)

    
    from requests import get
    try:
        response = get(BASE_URL, timeout=TIMEOUT)
        print("Ex. 2 - from requests import get:", response.status_code)
    except requests.RequestException as error:
        print("Cererea nu a reușit:", error)
    time.sleep(1)

    
    import requests as rq
    try:
        response = rq.get(BASE_URL, timeout=TIMEOUT)
        print("Ex. 3 - alias rq:", response.status_code)
        # Aliasul scurt ajută când este cunoscut (de ex. np pentru numpy);
        # un alias neobișnuit poate face codul mai greu de înțeles.
    except rq.RequestException as error:
        print("Cererea nu a reușit:", error)
    time.sleep(1)

   
    try:
        request = urllib.request.Request(BASE_URL, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
            body = response.read().decode("utf-8", errors="replace")
            print("Ex. 4 - status:", response.status)
            print("Primele 200 de caractere:", body[:200])
    except Exception as error:
        print("Ex. 4 - Cererea nu a reușit:", error)

    
    print("Ex. 5 - câteva nume din requests:", [name for name in dir(requests) if name in ("get", "Session", "exceptions")])
    # get este o funcție, Session este o clasă, exceptions este un modul/pachet de excepții.

    
    help(requests.get)
    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        print("Ex. 6 - cerere cu timeout:", response.status_code)
    except requests.RequestException as error:
        print("Cererea nu a reușit:", error)
    time.sleep(1)

    try:
        start = time.perf_counter()
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        total = time.perf_counter() - start
        print(f"Ex. 7 - timp total: {total:.3f} secunde")
        print(f"Ex. 7 - response.elapsed: {response.elapsed.total_seconds():.3f} secunde")
        # perf_counter măsoară timpul total observat de program; elapsed măsoară
        # timpul dintre trimiterea cererii și primirea răspunsului de către requests.
    except requests.RequestException as error:
        print("Cererea nu a reușit:", error)
    time.sleep(1)

    
    try:
        import bs4
        print("Ex. 8 - BeautifulSoup este instalat:", bs4.__version__)
    except ImportError:
        print("Instalați modulul cu: pip install beautifulsoup4")

    print("\nVerificare: un modul este un fișier de cod, un pachet grupează module,")
    print("iar biblioteca este o colecție de cod reutilizabil.")


if __name__ == "__main__":
    main()
