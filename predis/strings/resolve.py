key_dict = {}


def resolve_set(data: str) -> str:
    data = data.split(" ")
    key = data[1]
    value = data[2]

    key_dict[key] = value.split("\n")[0]
    return "OK"


def resolve_get(data: str) -> str:
    data = data.split(" ")
    key = data[1].split("\n")[0]
    return str(key_dict[key])
