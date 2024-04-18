def check_for_repetitions(data):
    keys = set()
    values = set()
    for key, value in data.items():
        if key in keys:
            raise ValueError(f"Key {key} is repeated")
        keys.add(key)
        if value in values:
            raise ValueError(f"Value {value} is repeated")
        values.add(value)

    return data
