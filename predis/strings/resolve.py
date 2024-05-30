key_dict = {}


def resolve_set(data: str) -> str:
    list_data: list[str] = data.split(" ")
    key = list_data[1]
    value = list_data[2]

    key_dict[key] = value.split("\n")[0]
    return "OK"


def resolve_get(data: str) -> str:
    list_data: list[str] = data.split(" ")
    key = list_data[1].split("\n")[0]
    try:
        value = str(key_dict[key])
        return value
    except Exception as Error:
        return "not found"


def resolve_ping() -> str:
    return "PONG"
