"""Command-line interface for qrz-featured."""
import argparse
import json
import os
import sys

from .client import get_featured_member


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="qrz-featured",
        description="Look up the current QRZ.com Featured Member (unofficial).",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON to stdout")
    parser.add_argument("--username", default=os.environ.get("QRZ_USERNAME"))
    parser.add_argument("--password", default=os.environ.get("QRZ_PASSWORD"))
    args = parser.parse_args(argv)

    try:
        member = get_featured_member(username=args.username, password=args.password)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(member, ensure_ascii=False))
    else:
        line = member["callsign"]
        if member["name"]:
            line += f" ({member['name']})"
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
