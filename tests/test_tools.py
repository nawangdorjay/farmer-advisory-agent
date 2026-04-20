"""Tests for Farmer Advisory Agent tools."""
import json
import sys
import os

# Add parent dir to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agent.tools import (
    get_crop_info,
    get_pest_info,
    get_government_schemes,
    get_market_prices,
    get_crop_calendar,
)


def test_crop_info_rice():
    result = get_crop_info("rice")
    assert result["found"] is True
    assert result["crop"] == "rice"
    assert "seasons" in result
    assert "varieties" in result
    print("✅ test_crop_info_rice passed")


def test_crop_info_unknown():
    result = get_crop_info("dragonfruit")
    assert result["found"] is False
    print("✅ test_crop_info_unknown passed")


def test_crop_info_fuzzy():
    result = get_crop_info("sugar")
    assert result["found"] is True
    assert "sugarcane" in result["crop"]
    print("✅ test_crop_info_fuzzy passed")


def test_pest_info_rice():
    result = get_pest_info("rice")
    assert result["found"] is True
    assert result["crop"] == "rice"
    assert len(result["common_pests"]) > 0
    print("✅ test_pest_info_rice passed")


def test_pest_info_symptom():
    result = get_pest_info("rice", "diamond spots on leaves")
    assert result["found"] is True
    assert len(result.get("matches", [])) > 0
    print("✅ test_pest_info_symptom passed")


def test_govt_schemes():
    result = get_government_schemes("loan")
    assert len(result["schemes"]) > 0
    names = [s["name"] for s in result["schemes"]]
    assert any("Kisan Credit Card" in n for n in names)
    print("✅ test_govt_schemes passed")


def test_govt_schemes_with_state():
    result = get_government_schemes("insurance", state="Maharashtra")
    assert len(result["schemes"]) > 0
    print("✅ test_govt_schemes_with_state passed")


def test_market_prices():
    result = get_market_prices("wheat")
    assert result.get("national_avg") is not None
    print("✅ test_market_prices passed")


def test_market_prices_state():
    result = get_market_prices("rice", state="Punjab")
    assert result.get("price") is not None
    assert result.get("state") == "Punjab"
    print("✅ test_market_prices_state passed")


def test_crop_calendar():
    result = get_crop_calendar("north india")
    assert "calendar" in result
    assert "rice" in result["calendar"]
    print("✅ test_crop_calendar passed")


def test_crop_calendar_specific():
    result = get_crop_calendar("north india", "wheat")
    assert "calendar" in result
    assert "rabi" in result["calendar"]
    print("✅ test_crop_calendar_specific passed")


if __name__ == "__main__":
    tests = [
        test_crop_info_rice,
        test_crop_info_unknown,
        test_crop_info_fuzzy,
        test_pest_info_rice,
        test_pest_info_symptom,
        test_govt_schemes,
        test_govt_schemes_with_state,
        test_market_prices,
        test_market_prices_state,
        test_crop_calendar,
        test_crop_calendar_specific,
    ]
    passed = 0
    failed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"❌ {test.__name__} failed: {e}")
            failed += 1

    print(f"\n{'='*40}")
    print(f"Results: {passed} passed, {failed} failed")
    if failed == 0:
        print("All tests passed! 🎉")
