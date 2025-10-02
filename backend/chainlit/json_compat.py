import orjson
from typing import Any

def dumps(obj: Any, *, skipkeys=False, ensure_ascii=False,
          check_circular=True, allow_nan=True, cls=None,
          indent=None, separators=None, default=None,
          sort_keys=False, **kwargs) -> str:
    """
    Wrapper API-compatible với json.dumps nhưng dùng orjson bên trong.
    Trả về str thay vì bytes.
    """

    option = 0

    # orjson mặc định đã compact như separators=(',', ':')
    # Nếu indent > 0 thì bật pretty print
    if indent is not None:
        option |= orjson.OPT_INDENT_2

    if sort_keys:
        option |= orjson.OPT_SORT_KEYS

    # orjson không hỗ trợ ensure_ascii=False trực tiếp,
    # nhưng mặc định đã UTF-8, còn ensure_ascii=True thì cần encode lại
    result = orjson.dumps(obj, default=default, option=option)

    if ensure_ascii:
        return result.decode("utf-8").encode("ascii", "backslashreplace").decode("ascii")

    return result.decode("utf-8")


def loads(s: str | bytes, *, cls=None, object_hook=None, parse_float=None,
          parse_int=None, parse_constant=None, object_pairs_hook=None, **kwargs) -> Any:
    """
    Wrapper API-compatible với json.loads nhưng dùng orjson bên trong.
    """
    return orjson.loads(s)
