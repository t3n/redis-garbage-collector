#!/usr/bin/env python3

import argparse
import redis


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


def clean(name: str, dry_run: bool) -> None:
    r = redis.Redis(db=2, decode_responses=True)

    entry = scan_keys(r, name + ":entry:*")
    entries = list_entries(r, name + ":entries")
    tag = scan_keys(r, name + ":tag:*")
    tags = scan_keys(r, name + ":tags:*")
    print("entry: {0}, entries: {1}, tag: {2}, tags: {3}".format(len(entry), len(entries), len(tag), len(tags)))

    entries_to_remove = removeable_entries(entry, entries)
    tags_to_remove = removeable_entries(entry, tags)
    print("removeable entries: {0}, removeable tags: {1}".format(len(entries_to_remove), len(tags_to_remove)))

    for e in entries_to_remove:
        if dry_run:
            if len(entries_to_remove) < 100:
                print(name + ":entries", e)
        else:
            r.lrem(name + ":entries", 0, e)

    for t in tags_to_remove:
        remove_from_tag = scan_set(r, t)
        for i in remove_from_tag:
            if dry_run:
                if len(tags_to_remove) < 100:
                    print(t.split(":")[-1], name + ":tag:" + i)
                    print(t, i)
            else:
                r.srem(name + ":tag:" + i, t.split(":")[-1])
                r.srem(t, i)

    r.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean up Flow cache in Redis.')
    parser.add_argument('Cache', metavar='cache', type=str, help='Name of cache to clean up.')
    parser.add_argument('--dry-run', action='store_true')

    args = parser.parse_args()

    clean(args.Cache, args.dry_run)
