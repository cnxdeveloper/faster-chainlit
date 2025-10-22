from typing import Any

import orjson


class JSONEncoder:
    def __init__(self, *, default=None, option=0):
        """
        Wrapper giống json.JSONEncoder nhưng dùng orjson.

        :param default: hàm xử lý object không serialize được
        :param option: orjson option flags (ví dụ orjson.OPT_INDENT_2)
        """
        self.default = default
        self.option = option

    def encode(self, obj):
        return orjson.dumps(obj, default=self.default, option=self.option).decode()

    def iterencode(self, obj):
        # giữ API giống json.JSONEncoder
        yield self.encode(obj)

    # để gọi trực tiếp như json.JSONEncoder().encode(obj)
    def __call__(self, obj):
        return self.encode(obj)


def dumps(
    obj: Any,
    *,
    skipkeys=False,
    ensure_ascii=False,
    check_circular=True,
    allow_nan=True,
    cls=None,
    indent=None,
    separators=None,
    default=None,
    sort_keys=False,
    **kwargs,
) -> str:
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
        return (
            result.decode("utf-8").encode("ascii", "backslashreplace").decode("ascii")
        )

    return result.decode("utf-8")


def loads(
    s: str | bytes,
    *,
    cls=None,
    object_hook=None,
    parse_float=None,
    parse_int=None,
    parse_constant=None,
    object_pairs_hook=None,
    **kwargs,
) -> Any:
    """
    Wrapper API-compatible với json.loads nhưng dùng orjson bên trong.
    """
    return orjson.loads(s)
