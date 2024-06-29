"""
Resolves the incoming request from the user
"""

key_value_store = {}  # store the KV


def resolve_set(data: str) -> str:
    """
    resolves SET method
    """

    list_data: list[str] = data.split(" ")

    try:
        key, value = list_data[1], list_data[2]
    except IndexError as idxErr:
        return f"{idxErr}"

    key_value_store[key] = value.split("\n")[0]
    return "OK"


def resolve_get(data: str) -> str:
    """
    resolves GET method
    """
    list_data: list[str] = data.split(" ")
    key = list_data[1].split("\n")[0]

    try:
        value = str(key_value_store[key])
        return value
    except Exception as Error:
        return f"not found : {Error}"


def resolve_ping() -> str:
    """
    resolves PING
    """
    return "PONG"
