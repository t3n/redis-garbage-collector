def scan_keys(r, pattern: str) -> list:
    "Returns a list of all the keys matching a given pattern"

    result = []
    cur, keys = r.scan(cursor=0, match=pattern)
    result.extend(keys)
    while cur != 0:
        cur, keys = r.scan(cursor=cur, match=pattern)
        result.extend(keys)

    return result


def scan_set(r, name: str) -> list:
    "Returns a list of all the keys matching a given pattern"

    result = []
    cur, keys = r.sscan(name, cursor=0)
    result.extend(keys)
    while cur != 0:
        cur, keys = r.sscan(name, cursor=cur)
        result.extend(keys)

    return result


def list_entries(r, name: str) -> list:
    "Returns a list of all the keys found in a redis list"
    return r.lrange(name, 0, -1)


def removeable_entries(valid: list, total: list) -> list:
    "Returns a list of keys not of total not found in valid"

    result = total.copy()
    for t in total:
        for v in valid:
            if t.split(":")[-1] == v.split(":")[-1]:
                result.remove(t)

    return result
