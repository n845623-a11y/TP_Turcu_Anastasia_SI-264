"""Analizează capturile locale ale laboratorului și produce un raport JSON."""

import argparse
import json
from pathlib import Path

GTFO = {"find", "vim.basic", "vim", "nmap", "cp", "bash",
        "less", "awk", "python3", "perl"}


def citeste_linii(cale):
    with open(cale, encoding="utf-8") as fisier:
        linii = [linie.strip() for linie in fisier]
    return [linie for linie in linii if linie and not linie.startswith("#")]


def nume(cale):
    return cale.rsplit("/", 1)[-1]


def suid_constatari(cale):
    cai = citeste_linii(cale)
    return [
        {"cale": c, "nume": nume(c),
         "risc": "mare" if nume(c) in GTFO else "normal"}
        for c in sorted(set(cai))
    ]


def sudo_constatari(cale):
    constatari = []
    for linie in citeste_linii(cale):
        user, separator, drept = linie.partition(" : ")
        if not separator or not user.strip() or not drept.strip():
            raise ValueError(f"{cale}: regulă sudo invalidă: {linie!r}")
        constatari.append({
            "user": user.strip(),
            "drept": drept.strip(),
            "risc": "mare" if "NOPASSWD" in drept else "normal",
        })
    return constatari


def cron_constatari(cale):
    constatari = []
    for linie in citeste_linii(cale):
        # Cinci câmpuri de timp, un utilizator, apoi comanda întreagă.
        campuri = linie.split(maxsplit=6)
        if len(campuri) != 7:
            raise ValueError(f"{cale}: intrare cron invalidă: {linie!r}")
        constatari.append({"user": campuri[5], "comanda": campuri[6]})
    return constatari


def enumereaza(director):
    director = Path(director)
    return {
        "suid": suid_constatari(director / "suid.txt"),
        "sudo": sudo_constatari(director / "sudo.txt"),
        "cron": cron_constatari(director / "crontab.txt"),
    }


def grupeaza_dupa_risc(raport):
    grupuri = {}
    for categorie, constatari in raport.items():
        for constatare in constatari:
            eticheta = constatare["nume"] if categorie == "suid" else constatare["user"]
            risc = constatare.get("risc", "normal")
            grupuri.setdefault(risc, []).append(eticheta)
    return grupuri


def main():
    parser = argparse.ArgumentParser(description="Analizează fișierele de captură.")
    parser.add_argument("capturi", type=Path)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--risc", choices=["mare"])
    parser.add_argument("--grupare-risc", action="store_true")
    argumente = parser.parse_args()

    try:
        raport = enumereaza(argumente.capturi)
        if argumente.risc:
            raport = {
                categorie: [c for c in constatari if c.get("risc") == argumente.risc]
                for categorie, constatari in raport.items()
            }

        rezultat = grupeaza_dupa_risc(raport) if argumente.grupare_risc else raport
        continut_json = json.dumps(rezultat, indent=2, ensure_ascii=False)
        if argumente.json or argumente.grupare_risc:
            print(continut_json)
            return

        Path("enum.json").write_text(continut_json + "\n", encoding="utf-8")
    except (OSError, ValueError) as eroare:
        parser.exit(1, f"Eroare: {eroare}\n")

    for categorie, constatari in raport.items():
        mari = [c for c in constatari if c.get("risc") == "mare"]
        print(f"{categorie}: {len(constatari)} gasite, {len(mari)} cu risc mare")
    utilizatori = {c["user"] for c in raport["sudo"]} | {
        c["user"] for c in raport["cron"]
    }
    print("utilizatori implicati:", ", ".join(sorted(utilizatori)))
    print("Raport salvat in enum.json")


if __name__ == "__main__":
    main()
