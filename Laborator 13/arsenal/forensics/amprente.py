import argparse
import hashlib
import os

MAGIC = {b"\x89PNG": "PNG", b"%PDF": "PDF", b"PK\x03\x04": "ZIP"}


def tip(head):
    for semnatura, nume in MAGIC.items():
        if head.startswith(semnatura):
            return nume
    return "necunoscut"


def amprenta_fisier(cale):
    with open(cale, "rb") as fisier:
        date = fisier.read()
    return {
        "nume": os.path.basename(cale),
        "tip": tip(date[:8]),
        "sha256": hashlib.sha256(date).hexdigest()[:16],
    }


def amprente_lenes(folder):
    for nume in sorted(os.listdir(folder)):
        cale = os.path.join(folder, nume)
        if os.path.isfile(cale):
            yield amprenta_fisier(cale)


def scaneaza(folder):
    return list(amprente_lenes(folder))


def main():
    parser = argparse.ArgumentParser(description="Calculeaza amprentele fisierelor dintr-un folder.")
    parser.add_argument("folder", help="Folderul cu fisiere de examinat.")
    argumente = parser.parse_args()

    for fisa in scaneaza(argumente.folder):
        print(f"{fisa['nume']:14} {fisa['tip']:11} {fisa['sha256']}")


if __name__ == "__main__":
    main()
