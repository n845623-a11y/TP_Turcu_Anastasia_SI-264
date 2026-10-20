
import requests
import time

BASE_URL = "https://cybercor.org"
ECHO_URL = "https://httpbin.org"
TIMEOUT = 10


def main():
    try:
        response = requests.get(BASE_URL, timeout=TIMEOUT)
        # Ex. 9: status_code, ok, url și encoding sunt atribute.
        print("Ex. 9 - status_code (atribut):", response.status_code)
        print("Ex. 9 - ok (atribut):", response.ok)
        print("Ex. 9 - url (atribut):", response.url)
        print("Ex. 9 - encoding (atribut):", response.encoding)

      
        response.raise_for_status()
        print("Ex. 10 - pagina principală a răspuns fără eroare HTTP.")
        time.sleep(1)
        try:
            missing = requests.get(ECHO_URL + "/status/404", timeout=TIMEOUT)
            missing.raise_for_status()
        except requests.HTTPError:
            print("Ex. 10 - Pagina cerută nu există sau a returnat o eroare HTTP.")

       
        print("Ex. 11 - Antete:")
        for name, value in response.headers.items():
            print(f"{name}: {value}")

        
        print("Ex. 12 - Server:", response.headers.get("Server", "lipsește"))
        print("Ex. 12 - Content-Type:", response.headers.get("Content-Type", "lipsește"))
        print("Ex. 12 - content-type:", response.headers.get("content-type", "lipsește"))
        print("Observație: numele antetelor HTTP nu țin cont de litere mari/mici.")

       
        print('Ex. 13 - Numărul aparițiilor cuvântului "cyber":',
              response.text.lower().count("cyber"))

        
        html = response.text
        start = html.lower().find("<title>")
        end = html.lower().find("</title>", start + len("<title>")) if start != -1 else -1
        if start != -1 and end != -1:
            title = html[start + len("<title>"):end].strip()
        else:
            title = "Titlul nu a fost găsit"
        print("Ex. 14 - Titlu:", title)

       
        lines = html.splitlines()
        longest = max(lines, key=len) if lines else ""
        print("Ex. 15 - Număr linii:", len(lines))
        print("Ex. 15 - Lungimea celei mai lungi linii:", len(longest))

        
        if response.url.startswith("https://"):
            print("Ex. 16 - Conexiune securizată (URL HTTPS).")
        else:
            print("Ex. 16 - Conexiune nesecurizată (URL fără HTTPS).")

        time.sleep(1)
        # Ex. 17: redirecționări HTTP -> HTTPS
        redirected = requests.get("http://cybercor.org", timeout=TIMEOUT, allow_redirects=True)
        print("Ex. 17 - Redirecționări:")
        for item in redirected.history:
            print(item.status_code, item.url)
        print("URL final:", redirected.url)

        time.sleep(1)
        head_response = requests.head(BASE_URL, timeout=TIMEOUT, allow_redirects=True)
        get_response = requests.get(BASE_URL, timeout=TIMEOUT)
        print("Ex. 18 - bytes HEAD:", len(head_response.content))
        print("Ex. 18 - bytes GET:", len(get_response.content))
        # La HEAD, serverul nu trimite în mod normal corpul paginii; de aceea este mai mic sau 0.

        
        if response.cookies:
            for cookie in response.cookies:
                print("Ex. 19 - Cookie:", cookie.name, "| secure:", cookie.secure)
        else:
            print("Ex. 19 - Niciun cookie setat")

        time.sleep(1)
        
        with requests.Session() as session:
            session.headers.update({"User-Agent": "WebLab-Student"})
            echo = session.get(ECHO_URL + "/headers", timeout=TIMEOUT)
            echo.raise_for_status()
            data = echo.json()
            print("Ex. 20 - User-Agent trimis:",
                  data.get("headers", {}).get("User-Agent", "nu a fost găsit"))
        print("\nVerificare: response.text este un atribut; response.json() este o metodă")
        print("care transformă corpul JSON într-un dicționar/listă Python.")
    except requests.RequestException as error:
        print("Eroare de rețea:", error)


if __name__ == "__main__":
    main()
