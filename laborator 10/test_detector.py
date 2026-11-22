from collections import Counter
import pytest
from parse_auth import esec, pe_ip, citeste_esecuri
from detector import suspecti


def test_pragul_taie():
    c = Counter({"a": 13, "b": 2})
    assert suspecti(c, 10) == [("a", 13)]
    assert suspecti(c, 2) == [("a", 13), ("b", 2)]


def test_prag_invalid():
    with pytest.raises(ValueError, match="prag invalid"):
        suspecti({}, 0)


def test_numarare_si_linii_stricate(tmp_path):
    f = tmp_path / "auth.log"
    f.write_text("Failed password for root from 203.0.113.9 port 51230 ssh2\n"
                 "Failed password for invalid user test from 203.0.113.9 port 51231 ssh2\n"
                 "linie stricata\n", encoding="utf-8")
    assert esec("linie stricata") is None
    assert esec("Failed password for root from 203.0.113.9 port 51230 ssh2") == ("root", "203.0.113.9")
    assert pe_ip(citeste_esecuri(f)) == Counter({"203.0.113.9": 2})


def test_fisier_lipsa(tmp_path):
    assert citeste_esecuri(tmp_path / "lipsa.log") == []
