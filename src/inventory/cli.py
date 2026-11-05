"""Command line interface; run --help for available operations."""

import argparse
import json
import sqlite3

from .core import Inventory


def main():
    parser = argparse.ArgumentParser(description="inventory")
    parser.add_argument("--database", default=".data/application.db")
    commands = parser.add_subparsers(dest="command", required=True)
    sub = commands.add_parser("add")
    sub.add_argument("sku")
    sub.add_argument("name")
    sub.add_argument("category")
    sub = commands.add_parser("get")
    sub.add_argument("sku")
    sub = commands.add_parser("update")
    sub.add_argument("sku")
    sub.add_argument("name")
    sub.add_argument("category")
    sub = commands.add_parser("delete")
    sub.add_argument("sku")
    sub = commands.add_parser("receipt")
    sub.add_argument("sku")
    sub.add_argument("quantity", type=int)
    sub.add_argument("--note", default="")
    sub = commands.add_parser("writeoff")
    sub.add_argument("sku")
    sub.add_argument("quantity", type=int)
    sub.add_argument("--note", default="")
    sub = commands.add_parser("search")
    sub.add_argument("--text", default="")
    sub.add_argument("--category")
    sub = commands.add_parser("report")
    sub = commands.add_parser("journal")
    args = parser.parse_args()
    try:
        app = Inventory(args.database)
        if args.command == "add":
            result = app.add(args.sku, args.name, args.category)
        if args.command == "get":
            result = app.get(args.sku)
        if args.command == "update":
            result = app.update(args.sku, args.name, args.category)
        if args.command == "delete":
            result = app.delete(args.sku)
        if args.command == "receipt":
            result = app.move(args.sku, args.quantity, "receipt", args.note)
        if args.command == "writeoff":
            result = app.move(args.sku, args.quantity, "writeoff", args.note)
        if args.command == "search":
            result = app.search(args.text, args.category)
        if args.command == "report":
            result = app.report()
        if args.command == "journal":
            result = app.journal()
        print(
            json.dumps(result, ensure_ascii=False, indent=2)
            if not isinstance(result, str)
            else result
        )
        if isinstance(result, dict) and result.get("passed") is False:
            return 1
        return 0
    except (ValueError, OSError, sqlite3.Error) as exc:
        parser.exit(2, f"Ошибка: {exc}\n")


if __name__ == "__main__":
    raise SystemExit(main())
