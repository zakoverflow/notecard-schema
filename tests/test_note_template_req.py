import pytest
import jsonschema

SCHEMA_FILE = "note.template.req.notecard.api.json"

def test_valid_req(schema):
    """Tests a minimal valid request."""
    instance = {
        "req": "note.template",
        "file": "data.qo",
        "template": {"id": "string"}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_cmd(schema):
    """Tests a minimal valid command."""
    instance = {
        "cmd": "note.template",
        "file": "data.qo",
        "body": {"temperature": 14.1}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_with_both_template_and_body(schema):
    """Tests a valid request with both template and body."""
    instance = {
        "req": "note.template",
        "file": "sensor.qo",
        "template": {"location": True, "timestamp": 14.1},
        "body": {"temperature": 14.1, "humidity": 14.1}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_template_only(schema):
    """Tests a valid request with only template."""
    instance = {
        "req": "note.template",
        "file": "events.qo",
        "template": {"urgent": True, "category": "string"}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_body_only(schema):
    """Tests a valid request with only body."""
    instance = {
        "req": "note.template",
        "file": "tracking.qo",
        "body": {"lat": 14.1, "lon": 14.1, "speed": 14.1}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_valid_qos_file(schema):
    """Tests a valid request with .qos file."""
    instance = {
        "req": "note.template",
        "file": "secure.qos",
        "body": {"data": "string"}
    }
    jsonschema.validate(instance=instance, schema=schema)

def test_invalid_missing_template_and_body(schema):
    """Tests invalid request missing both template and body."""
    instance = {
        "req": "note.template",
        "file": "data.qo"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    # Should fail the anyOf validation that requires at least one of template or body
    assert "is not valid under any of the given schemas" in str(excinfo.value)

def test_invalid_file_pattern(schema):
    """Tests invalid file patterns (not .qo or .qos)."""
    invalid_files = [
        "data.qi",
        "data.db", 
        "data.dbs",
        "data.txt",
        "data",
        ".qo",
        "data.qoo"
    ]
    
    for filename in invalid_files:
        instance = {
            "req": "note.template",
            "file": filename,
            "template": {"test": True}
        }
        with pytest.raises(jsonschema.ValidationError) as excinfo:
            jsonschema.validate(instance=instance, schema=schema)
        assert "does not match" in str(excinfo.value)

def test_file_field_required_with_template_or_body(schema):
    """Tests that file field is required when template or body is present."""
    # Test missing file with template
    instance = {
        "req": "note.template",
        "template": {"test": True}
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    # The exact error message may vary, but it should indicate file is required

    # Test missing file with body
    instance = {
        "req": "note.template", 
        "body": {"test": True}
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)

def test_template_field_type(schema):
    """Tests the template field type validation."""
    # Valid object
    instance = {
        "req": "note.template",
        "file": "data.qo",
        "template": {"key": "value"}
    }
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {
        "req": "note.template",
        "file": "data.qo", 
        "template": "not an object"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_body_field_type(schema):
    """Tests the body field type validation."""
    # Valid object
    instance = {
        "req": "note.template",
        "file": "data.qo",
        "body": {"sensor": 14.1}
    }
    jsonschema.validate(instance=instance, schema=schema)

    # Invalid type
    instance = {
        "req": "note.template",
        "file": "data.qo",
        "body": [1, 2, 3]
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "is not of type 'object'" in str(excinfo.value)

def test_additional_properties_not_allowed(schema):
    """Tests that additional properties are not allowed."""
    instance = {
        "req": "note.template",
        "file": "data.qo",
        "template": {"test": True},
        "invalid_property": "not allowed"
    }
    with pytest.raises(jsonschema.ValidationError) as excinfo:
        jsonschema.validate(instance=instance, schema=schema)
    assert "Additional properties are not allowed" in str(excinfo.value)

def test_validate_samples_from_schema(schema):
    """Tests that all samples in the schema are valid."""
    if 'samples' in schema:
        import json
        for sample in schema['samples']:
            if 'json' in sample:
                instance = json.loads(sample['json'])
                jsonschema.validate(instance=instance, schema=schema)