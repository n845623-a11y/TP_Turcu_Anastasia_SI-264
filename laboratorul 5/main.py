
import argparse
import csv
from datetime import datetime
import json

import webtools


def main():
    """Citește URL-ul din linia de comandă și creează rapoartele."""
    parser = argparse.ArgumentParser(description="Generează un raport simplu despre un site web.")
    parser.add_argument("url", help="URL-ul de verificat, de exemplu https://cybercor.org")
    args = parser.parse_args()
    url = args.url

   
    response = webtools.fetch(url)
    print("Ex. 44 - Titlu:", webtools.get_title(response.text))

    
    from webtools import get_title, security_headers
    print("Ex. 45 - Titlu prin import direct:", get_title(response.text))
    print("Ex. 45 - Antete:", security_headers(url))

    
    from webtools import DEFAULT_HEADERS
    print("Ex. 47 - Antete implicite:", DEFAULT_HEADERS)

    
    paths = ["/", "/robots.txt", "/sitemap.xml"]
    statuses = webtools.check_paths(url, paths)

    checked_at = datetime.now().isoformat()
    with open("report.csv", "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["path", "status", "checked_at"])
        for path, status in statuses.items():
            writer.writerow([path, status, checked_at])
    print("Ex. 49 - Salvat în report.csv")

    
    webtools.site_report(url)


if __name__ == "__main__":
    main()
