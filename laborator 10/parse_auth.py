"""Citirea si numararea esecurilor SSH din auth.log."""
import argparse
import re
from collections import Counter

TIPAR = re.compile(r"Failed password for (?:invalid user )?(\S+) from (\S+) port")


def esec(linie):
    m = TIPAR.search(linie)
    if m is None:
        return None
    return (m.group(1), m.group(2))


def citeste_esecuri(cale):
    esecuri = []
    try:
        with open(cale, encoding="utf-8", errors="replace") as f:
            for linie in f:
                r = esec(linie)
                if r is not None:
                    esecuri.append({"user": r[0], "ip": r[1]})
    except (FileNotFoundError, PermissionError, IsADirectoryError, OSError) as exc:
        print(f"Nu pot citi {cale}: {exc}")
    return esecuri


def pe_ip(esecuri):
    return Counter(e["ip"] for e in esecuri)


def main():
    p = argparse.ArgumentParser(description="Numara esecurile SSH din auth.log")
    p.add_argument("log", help="Calea catre auth.log")
    a = p.parse_args()
    esecuri = citeste_esecuri(a.log)
    print(f"Esecuri de autentificare: {len(esecuri)}")
    for ip, n in pe_ip(esecuri).most_common():
        print(f" {ip}: {n}")


if __name__ == "__main__":
    main()
