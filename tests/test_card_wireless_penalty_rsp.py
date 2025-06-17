import pytest
import jsonschema
import json

SCHEMA_FILE = "card.wireless.penalty.rsp.notecard.api.json"

def test_minimal_valid_rsp(schema):
    """Tests a minimal valid response (empty object)."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_seconds(schema):
    """Tests valid seconds field."""
    instance = {"seconds": 300}
    jsonschema.validate(instance=instance, schema=schema)

def test_seconds_invalid_type(schema):
    """Tests invalid type for seconds."""
    instance = {"seconds": "300"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'300' is not of type 'integer'" in str(excinfo.value)

def test_valid_max(schema):
    """Tests valid max field."""
    instance = {"max": 5}
    jsonschema.validate(instance=instance, schema=schema)

def test_max_invalid_type(schema):
    """Tests invalid type for max."""
    instance = {"max": "5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'5' is not of type 'integer'" in str(excinfo.value)

def test_valid_multiplier(schema):
    """Tests valid multiplier field."""
    instance = {"multiplier": 1.5}
    jsonschema.validate(instance=instance, schema=schema)

def test_multiplier_invalid_type(schema):
    """Tests invalid type for multiplier."""
    instance = {"multiplier": "1.5"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'1.5' is not of type 'number'" in str(excinfo.value)

def test_valid_current(schema):
    """Tests valid current field."""
    instance = {"current": 2}
    jsonschema.validate(instance=instance, schema=schema)

def test_current_invalid_type(schema):
    """Tests invalid type for current."""
    instance = {"current": "2"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'2' is not of type 'integer'" in str(excinfo.value)

def test_current_negative_value(schema):
    """Tests invalid negative value for current."""
    instance = {"current": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_valid_remaining(schema):
    """Tests valid remaining field."""
    instance = {"remaining": 180}
    jsonschema.validate(instance=instance, schema=schema)

def test_remaining_invalid_type(schema):
    """Tests invalid type for remaining."""
    instance = {"remaining": "180"}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "'180' is not of type 'integer'" in str(excinfo.value)

def test_remaining_negative_value(schema):
    """Tests invalid negative value for remaining."""
    instance = {"remaining": -1}
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "-1 is less than the minimum of 0" in str(excinfo.value)

def test_valid_all_fields(schema):
    """Tests valid response with all fields."""
    instance = {
        "seconds": 300,
        "max": 3,
        "multiplier": 1.5,
        "current": 2,
        "remaining": 450
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_additional_property(schema):
    """Tests valid response with an additional property."""
    instance = {"seconds": 300, "additional": "property"}
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
