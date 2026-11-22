"""Compară două liste de fișiere SUID obținute din capturi locale."""

import argparse
from pathlib import Path

from arsenal.privesc.enum import GTFO, citeste_linii, nume


def cai(fisier):
    return set(citeste_linii(fisier))


def cai_noi(acum, baza):
    return acum - baza


def main():
    parser = argparse.ArgumentParser(description="Compară captura SUID cu baza.")
    parser.add_argument("capturi", nargs="?", type=Path,
                        default=Path(__file__).with_name("start"))
    argumente = parser.parse_args()
    try:
        baza = cai(argumente.capturi / "baza_suid.txt")
        acum = cai(argumente.capturi / "suid.txt")
    except (OSError, ValueError) as eroare:
        parser.exit(1, f"Eroare: {eroare}\n")

    print(f"baza: {len(baza)}  acum: {len(acum)}")
    noi = sorted(cai_noi(acum, baza))
    print(len(noi), "SUID noi fata de sistemul curat")
    for cale in noi:
        print(f"  {cale}")

    risc = {nume(c): ("mare" if nume(c) in GTFO else "normal") for c in noi}
    periculoase = [c for c in noi if risc[nume(c)] == "mare"]
    print("periculoase NOI:", periculoase)


if __name__ == "__main__":
    main()
