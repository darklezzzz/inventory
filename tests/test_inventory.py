import pytest
from inventory.core import Inventory


@pytest.fixture
def app(tmp_path):
    stock = Inventory(tmp_path / "inventory.db")
    stock.add("A1", "Болт", "Крепёж")
    return stock


def test_add(app):
    assert app.get("A1")["stock"] == 0


def test_duplicate(app):
    with pytest.raises(ValueError):
        app.add("A1", "Дубль", "Другое")


def test_receipt(app):
    assert app.move("A1", 10, "receipt")["stock"] == 10


def test_writeoff(app):
    app.move("A1", 10, "receipt")
    assert app.move("A1", 3, "writeoff")["stock"] == 7
    assert len(app.journal()) == 2


def test_insufficient_atomic(app):
    app.move("A1", 2, "receipt")
    with pytest.raises(ValueError):
        app.move("A1", 3, "writeoff")
    assert app.get("A1")["stock"] == 2
    assert len(app.journal()) == 1


@pytest.mark.parametrize("quantity", [0, -1, 1.5, True, "2"])
def test_invalid_quantity(app, quantity):
    with pytest.raises(ValueError):
        app.move("A1", quantity, "receipt")
    assert app.journal() == []


def test_update_search(app):
    app.update("A1", "Винт", "Металл")
    assert len(app.search("Вин", "Металл")) == 1


def test_delete(app):
    app.delete("A1")
    assert app.search() == []
    with pytest.raises(ValueError):
        app.get("A1")


def test_cannot_delete_stock(app):
    app.move("A1", 1, "receipt")
    with pytest.raises(ValueError):
        app.delete("A1")


def test_restart(app, tmp_path):
    app.move("A1", 3, "receipt")
    app.db.close()
    assert Inventory(tmp_path / "inventory.db").report()["total_stock"] == 3


def test_unknown_operation(app):
    with pytest.raises(ValueError):
        app.move("A1", 1, "unknown")
    with pytest.raises(ValueError):
        app.move("missing", 1, "receipt")
