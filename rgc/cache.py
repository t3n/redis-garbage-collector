import redis

from rgc.utils import scan_keys, scan_set, list_entries, removeable_entries


def clean(name: str, dry_run: bool) -> None:
    r = redis.Redis(db=2, decode_responses=True)

    entry = scan_keys(r, name + ":entry:*")
    entries = list_entries(r, name + ":entries")
    tag = scan_keys(r, name + ":tag:*")
    tags = scan_keys(r, name + ":tags:*")

    print("entry: {0}, entries: {1}, tag: {2}, tags: {3}".format(len(entry), len(entries), len(tag), len(tags)))
    entries_to_remove = removeable_entries(entry, entries)
    tags_to_remove = removeable_entries(entry, tags)

    for e in entries_to_remove:
        if dry_run:
            print(name + ":entries", e)
        else:
            r.lrem(name + ":entries", 0, e)

    for t in tags_to_remove:
        remove_from_tag = scan_set(r, t)
        for i in remove_from_tag:
            if dry_run:
                print(t.split(":")[-1], name + ":tag:" + i)
                print(t, i)
            else:
                r.srem(name + ":tag:" + i, t.split(":")[-1])
                r.srem(t, i)

    r.close()
