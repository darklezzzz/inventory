import json
import tempfile
from pathlib import Path

from inventory.core import Inventory

with tempfile.TemporaryDirectory() as directory:
    app = Inventory(Path(directory) / "inventory.db")
    app.add("A1", "Болт", "Крепёж")
    app.move("A1", 10, "receipt", "Поставка")
    app.move("A1", 3, "writeoff", "Выдача")
    try:
        app.move("A1", 8, "writeoff")
    except ValueError as exc:
        rejected = str(exc)
    result = app.report() | {"rejected_writeoff": rejected}
    (Path(__file__).parent / "stock.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("Остаток:", result["total_stock"], "; запрет:", rejected)
