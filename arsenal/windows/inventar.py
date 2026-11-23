"""Modele și raport de alarme pentru capturi Windows."""

import argparse
import json
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from pathlib import Path

CAI_SUSPECTE = ("\\temp\\", "\\roaming\\")
EXPLICATII_ID = {
    4625: "Autentificare eșuată. Eșecurile repetate pot indica un atac prin forță brută.",
    1102: "Jurnalul de audit a fost șters.",
    7045: "Un serviciu nou a fost instalat.",
}
SUSPECTE_ID = {4625, 1102, 7045}


@dataclass
class Proces:
    pid: int
    nume: str
    user: str
    cale: str

    def e_suspect(self) -> bool:
        cale = self.cale.replace("/", "\\").casefold()
        return any(fragment in cale for fragment in CAI_SUSPECTE)


@dataclass
class Eveniment:
    id: int
    nivel: str
    sursa: str
    cont: str
    mesaj: str

    def e_suspect(self) -> bool:
        return self.id in SUSPECTE_ID or self.nivel == "critical"

    def explica(self) -> str:
        return EXPLICATII_ID.get(self.id, self.mesaj)


def procese_din_json(cale: str | Path) -> list[Proces]:
    with open(cale, encoding="utf-8-sig") as fisier:
        return [Proces(**date) for date in json.load(fisier)]


def evenimente_din_json(cale: str | Path) -> list[Eveniment]:
    with open(cale, encoding="utf-8-sig") as fisier:
        return [Eveniment(**date) for date in json.load(fisier)]


@dataclass
class Inventar:
    procese: list[Proces]

    @classmethod
    def din_json(cls, cale: str | Path) -> "Inventar":
        return cls(procese_din_json(cale))

    def __len__(self) -> int:
        return len(self.procese)

    def suspecte(self) -> list[Proces]:
        return [proces for proces in self.procese if proces.e_suspect()]

    def pe_user(self) -> dict[str, list[str]]:
        grupuri: dict[str, list[str]] = {}
        for proces in self.procese:
            grupuri.setdefault(proces.user, []).append(proces.nume)
        return grupuri

    def scor(self, evenimente: Iterable[Eveniment] = ()) -> int:
        return len(self.suspecte()) + sum(event.e_suspect() for event in evenimente)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("capturi", type=Path, help="Directorul cu cele două capturi JSON")
    parser.add_argument("--json", action="store_true", help="Afișează alarmele în format JSON")
    argumente = parser.parse_args()

    try:
        inventar = Inventar.din_json(argumente.capturi / "procese.json")
        evenimente = evenimente_din_json(argumente.capturi / "evenimente.json")
    except (OSError, ValueError, TypeError) as eroare:
        parser.error(str(eroare))

    suspecte = inventar.suspecte()
    alarme = [eveniment for eveniment in evenimente if eveniment.e_suspect()]
    if argumente.json:
        raport = {
            "procese_suspecte": [asdict(proces) for proces in suspecte],
            "evenimente_alarma": [asdict(eveniment) for eveniment in alarme],
        }
        print(json.dumps(raport, indent=2))
        return

    print(f"Procese: {len(inventar)} | suspecte: {len(suspecte)}")
    for proces in suspecte:
        print(f"  [{proces.pid}] {proces.nume}  ({proces.user})  {proces.cale}")

    print(f"Evenimente: {len(evenimente)} | alarma: {len(alarme)}")
    for event in alarme:
        print(f"  {event.id} [{event.nivel}] {event.cont}: {event.mesaj}")


if __name__ == "__main__":
    main()
