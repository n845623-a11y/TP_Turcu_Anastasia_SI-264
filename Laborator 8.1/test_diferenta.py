from diferenta import cai_noi


def test_doar_ce_e_nou():
    acum = {"a", "b", "c"}
    baza = {"a", "b", "d"}
    assert cai_noi(acum, baza) == {"c"}
