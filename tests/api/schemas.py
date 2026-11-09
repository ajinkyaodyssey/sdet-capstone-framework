USER_SCHEMA = {
    "type": "object",
    "required": ["id", "email", "first_name", "last_name"],
    "properties": {
        "id": {"type": "integer", "minimum": 1},
        "email": {"type": "string", "minLength": 5},
        "first_name": {"type": "string", "minLength": 1},
        "last_name": {"type": "string", "minLength": 1},
    },
}
