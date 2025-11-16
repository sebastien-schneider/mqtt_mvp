import pytest
import publisher

def test_generate_fms_data():
    data = publisher.generate_fms_data()
    assert "vehicle_id" in data
    assert "timestamp" in data
    assert 0 <= data["speed"] <= 120
    assert 700 <= data["rpm"] <= 3500
    assert 0 <= data["fuel_level"] <= 100
