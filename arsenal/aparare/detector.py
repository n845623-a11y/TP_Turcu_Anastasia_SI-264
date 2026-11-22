"""Detector defensiv de incercari repetate de autentificare SSH."""
import argparse
import json
from arsenal.aparare.parse_auth import citeste_esecuri, pe_ip


def suspecti(counts, prag=10):
    if prag < 1:
        raise ValueError(f"prag invalid: {prag} (cel putin 1)")
    return [(ip, n) for ip, n in counts.most_common() if n >= prag]


def main():
    p = argparse.ArgumentParser(description="Detecteaza posibile atacuri brute force")
    p.add_argument("log", help="Calea catre auth.log")
    p.add_argument("--prag", type=int, default=10)
    p.add_argument("--json", action="store_true")
    a = p.parse_args()
    if a.prag < 1:
        p.error(f"prag invalid: {a.prag} (cel putin 1)")
    esecuri = citeste_esecuri(a.log)
    counts = pe_ip(esecuri)
    sus = suspecti(counts, a.prag)
    if a.json:
        print(json.dumps({"esecuri": len(esecuri), "pe_ip": dict(counts), "suspecti": [{"ip": ip, "incercari": n} for ip, n in sus]}, indent=2, ensure_ascii=False))
    else:
        print(f"Esecuri de autentificare: {len(esecuri)}")
        for ip, n in counts.most_common():
            print(f" {ip}: {n}")
        print(f"Suspecti (prag {a.prag}):")
        for ip, n in sus:
            print(f" {ip} ({n} incercari) BRUTE FORCE")


if __name__ == "__main__":
    main()
