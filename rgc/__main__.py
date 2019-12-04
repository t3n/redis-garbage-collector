import argparse

from rgc.cache import clean


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clean up Flow cache in Redis.')
    parser.add_argument('Cache', metavar='cache', type=str, help='Name of cache to clean up.')
    parser.add_argument('--dry-run', action='store_true')

    args = parser.parse_args()

    clean(args.Cache, args.dry_run)
