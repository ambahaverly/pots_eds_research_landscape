from src.prepare import evidence_level, extract_year


def test_extract_year():
    assert extract_year("2024 Jan 15") == 2024
    assert extract_year("No date") is None


def test_evidence_level():
    assert evidence_level(["Randomized Controlled Trial"]) == "Randomized controlled trial"
    assert evidence_level(["Case Reports"]) == "Case report"
    assert evidence_level(["Systematic Review"]) == "Systematic review/meta-analysis"
