from pathlib import Path

from arsenal.forensics.amprente import amprenta_fisier, amprente_lenes, scaneaza, tip

PROBE = Path(__file__).parent / "probe"


def test_tip_din_magic():
    assert tip(b"\x89PNG\r\n") == "PNG"
    assert tip(b"%PDF-1.4") == "PDF"
    assert tip(b"PK\x03\x04") == "ZIP"
    assert tip(b"text") == "necunoscut"


def test_amprenta_png():
    assert amprenta_fisier(PROBE / "imagine.png") == {
        "nume": "imagine.png",
        "tip": "PNG",
        "sha256": "ea3a9848da7e6c1d",
    }


def test_scaneaza_toate():
    rezultate = scaneaza(PROBE)
    assert [(fisa["nume"], fisa["tip"], fisa["sha256"]) for fisa in rezultate] == [
        ("arhiva.zip", "ZIP", "e026715077436f53"),
        ("imagine.png", "PNG", "ea3a9848da7e6c1d"),
        ("note.txt", "necunoscut", "27f8884260c60ec9"),
        ("raport.pdf", "PDF", "9023842e09242e5d"),
    ]
    assert list(amprente_lenes(PROBE)) == rezultate
