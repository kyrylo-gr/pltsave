def stringify_elm(elm) -> str:
    if isinstance(elm, dict):
        return stringify_dict(elm)
    if isinstance(elm, list):
        return f'[{",".join([stringify_elm(l) for l in elm])}]'
    return str(elm)


def stringify_dict(data: dict):
    res = ""
    for key, value in data.items():
        res += f"{key}:{stringify_elm(value)},"
    return "{" + res[:-1] + "}"
