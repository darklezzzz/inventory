"""Transactional stock accounting with an immutable operation journal."""

import sqlite3
from datetime import datetime, timezone
from pathlib import Path


class Inventory:
    def __init__(self, database):
        Path(database).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(database)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript("""
        CREATE TABLE IF NOT EXISTS products (
          sku TEXT PRIMARY KEY, name TEXT NOT NULL, category TEXT NOT NULL,
          stock INTEGER NOT NULL DEFAULT 0 CHECK(stock>=0), active INTEGER NOT NULL DEFAULT 1);
        CREATE TABLE IF NOT EXISTS operations (
          id INTEGER PRIMARY KEY, sku TEXT REFERENCES products(sku),
          delta INTEGER NOT NULL, created_at TEXT NOT NULL, note TEXT NOT NULL);
        """)

    def add(self, sku, name, category):
        if any(not isinstance(v, str) or not v.strip() for v in (sku, name, category)):
            raise ValueError("Артикул, название и категория обязательны")
        try:
            with self.db:
                self.db.execute(
                    "INSERT INTO products(sku,name,category) VALUES(?,?,?)", (sku, name, category)
                )
        except sqlite3.IntegrityError as exc:
            raise ValueError("Артикул уже зарегистрирован") from exc
        return self.get(sku)

    def get(self, sku):
        row = self.db.execute("SELECT * FROM products WHERE sku=? AND active=1", (sku,)).fetchone()
        if row is None:
            raise ValueError("Товар не найден")
        return dict(row)

    def update(self, sku, name, category):
        self.get(sku)
        if not name.strip() or not category.strip():
            raise ValueError("Название и категория обязательны")
        with self.db:
            self.db.execute(
                "UPDATE products SET name=?,category=? WHERE sku=?", (name, category, sku)
            )
        return self.get(sku)

    def delete(self, sku):
        if self.get(sku)["stock"]:
            raise ValueError("Сначала спишите остаток")
        with self.db:
            self.db.execute("UPDATE products SET active=0 WHERE sku=?", (sku,))

    def move(self, sku, quantity, kind, note=""):
        if type(quantity) is not int or quantity <= 0:
            raise ValueError("Количество должно быть положительным целым")
        if kind not in ("receipt", "writeoff"):
            raise ValueError("Неизвестный тип операции")
        delta = quantity if kind == "receipt" else -quantity
        with self.db:
            cur = self.db.execute(
                "UPDATE products SET stock=stock+? WHERE sku=? AND active=1 AND stock+?>=0",
                (delta, sku, delta),
            )
            if cur.rowcount != 1:
                self.get(sku)
                raise ValueError("Недостаточный остаток")
            self.db.execute(
                "INSERT INTO operations(sku,delta,created_at,note) VALUES(?,?,?,?)",
                (sku, delta, datetime.now(timezone.utc).isoformat(), note),
            )
        return self.get(sku)

    def search(self, text="", category=None):
        query = "SELECT * FROM products WHERE active=1 AND (instr(name,?)>0 OR instr(sku,?)>0)"
        values = [text, text]
        if category is not None:
            query += " AND category=?"
            values.append(category)
        return [dict(r) for r in self.db.execute(query + " ORDER BY sku", values)]

    def journal(self):
        return [dict(r) for r in self.db.execute("SELECT * FROM operations ORDER BY id")]

    def report(self):
        items = self.search()
        return {
            "items": items,
            "total_stock": sum(i["stock"] for i in items),
            "operations": self.journal(),
        }
