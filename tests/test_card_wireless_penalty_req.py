import pytest
import jsonschema
import json

SCHEMA_FILE = "card.wireless.penalty.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request using 'req'."""
    instance = {"req": "card.wireless.penalty"}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid request using 'cmd'."""
    instance = {"cmd": "card.wireless.penalty"}
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_empty_object(schema):
    """Tests invalid empty object (needs req or cmd)."""
    instance = {}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_both_req_and_cmd(schema):
    """Tests invalid request having both req and cmd."""
    instance = {"req": "card.wireless.penalty", "cmd": "card.wireless.penalty"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is valid under each of" in str(excinfo.value)

def test_invalid_additional_property_with_req(schema):
    """Tests invalid request with req and an additional property."""
    instance = {"req": "card.wireless.penalty", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_invalid_additional_property_with_cmd(schema):
    """Tests invalid request with cmd and an additional property."""
    instance = {"cmd": "card.wireless.penalty", "extra": "field"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed ('extra' was unexpected)" in str(excinfo.value)

def test_valid_seconds(schema):
    """Tests valid seconds field."""
    instance = {"req": "card.wireless.penalty", "seconds": 300}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.wireless.penalty", "seconds": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"req": "card.wireless.penalty", "seconds": "300"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'300' is not of type 'integer'" in str(excinfo.value)

def test_seconds_out_of_range(schema):
    """Tests seconds value out of range."""
    instance = {"req": "card.wireless.penalty", "seconds": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_valid_max(schema):
    """Tests valid max field."""
    instance = {"req": "card.wireless.penalty", "max": 5}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.wireless.penalty", "max": 0}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max."""
    instance = {"req": "card.wireless.penalty", "max": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_valid_multiplier(schema):
    """Tests valid multiplier field."""
    instance = {"req": "card.wireless.penalty", "multiplier": 2.0}
    jsonschema.validate(instance=instance, schema=schema)
    instance = {"req": "card.wireless.penalty", "multiplier": 1.0}
    jsonschema.validate(instance=instance, schema=schema)

def test_multiplier_invalid_type(schema):
    """Tests invalid type for multiplier."""
    instance = {"req": "card.wireless.penalty", "multiplier": "2.0"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'2.0' is not of type 'number'" in str(excinfo.value)

def test_multiplier_out_of_range(schema):
    """Tests multiplier value out of range."""
    instance = {"req": "card.wireless.penalty", "multiplier": 0.5}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "0.5 is less than the minimum of 1" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests valid request with all fields."""
    instance = {"req": "card.wireless.penalty", "seconds": 300, "max": 5, "multiplier": 2.0}
    jsonschema.validate(instance=instance, schema=schema)

def test_validate_samples_from_schema(schema, schema_samples):
    """Tests that samples in the schema definition are valid."""
    for sample in schema_samples:
        sample_json_str = sample.get("json")
        if not sample_json_str:
            pytest.fail(f"Sample missing 'json' field: {sample.get('description', 'Unnamed sample')}")
        try:
            instance = json.loads(sample_json_str)
        except json.JSONDecodeError as e:
            pytest.fail(f"Failed to parse sample JSON: {sample_json_str}\nError: {e}")

        jsonschema.validate(instance=instance, schema=schema)
