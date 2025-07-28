import pytest
import jsonschema

SCHEMA_FILE = "note.template.rsp.notecard.api.json"

def test_minimal_valid_response(schema):
    """Tests a minimal valid response."""
    instance = {}
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_total_only(schema):
    """Tests a valid response with only total field."""
    instance = {
        "total": 32
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_template_only(schema):
    """Tests a valid response with only template field."""
    instance = {
        "template": 16
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_body_only(schema):
    """Tests a valid response with only body field."""
    instance = {
        "body": 20
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_all_fields(schema):
    """Tests a valid response with all fields."""
    instance = {
        "total": 32,
        "template": 16,
        "body": 16
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_zero_values(schema):
    """Tests valid response with zero values."""
    instance = {
        "total": 0,
        "template": 0,
        "body": 0
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_total_type(schema):
    """Tests invalid type for total field."""
    instance = {
        "total": "32"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_total_negative(schema):
    """Tests invalid negative value for total field."""
    instance = {
        "total": -1
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is less than the minimum of 0" in str(excinfo.value)

def test_invalid_template_type(schema):
    """Tests invalid type for template field."""
    instance = {
        "template": 16.5
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_template_negative(schema):
    """Tests invalid negative value for template field."""
    instance = {
        "template": -5
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is less than the minimum of 0" in str(excinfo.value)

def test_invalid_body_type(schema):
    """Tests invalid type for body field."""
    instance = {
        "body": "20"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'integer'" in str(excinfo.value)

def test_invalid_body_negative(schema):
    """Tests invalid negative value for body field."""
    instance = {
        "body": -10
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is less than the minimum of 0" in str(excinfo.value)

def test_valid_additional_property(schema):
    """Tests that additional properties are allowed in response."""
    # Note: The original response schema didn't have additionalProperties: false,
    # so additional properties should be allowed
    instance = {
        "total": 32,
        "custom_field": "allowed"
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_validate_samples_from_schema(schema):
    """Tests that all samples in the schema are valid."""
    if 'samples' in schema:
        import json
        for sample in schema['samples']:
            if 'json' in sample:
                instance = json.loads(sample['json'])
                jsonschema.validate(instance=instance, schema=schema)