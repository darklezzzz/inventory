# Подтверждения GitHub Actions

Все ссылки ведут на реальные завершённые запуски.

- [Push main: успешный CI](https://github.com/darklezzzz/inventory/actions/runs/42021339982): `success`, commit `a64898ccf09fae16be5189fd3953b81563d9aad7`.
- [Pull request: успешный CI](https://github.com/darklezzzz/inventory/actions/runs/42021432248): `success`, commit `89583f3752019564a36cf92b55b4f3e171aa417a`.
- [Намеренная ошибка склада: отказ](https://github.com/darklezzzz/inventory/actions/runs/42021488734): `failure`, commit `e8a9224bbe2121e245f694d623d5ac0dcba3e92e`.
- [Исправляющий коммит склада: успешный CI](https://github.com/darklezzzz/inventory/actions/runs/42021611624): `success`, commit `1374225c90531320397199f0b9b821537826311b`.

[Pull request с проверкой](https://github.com/darklezzzz/inventory/pull/1).

Ошибка: поступление quantity - 1 в ветке ci-failure-example.
Исправление: полный quantity в ci-failure-demo; исправляющий коммит
1374225c90531320397199f0b9b821537826311b.
Успешный запуск исправления создан после завершения неуспешного запуска.
Локальные протоколы сохранены в examples/intentional-failure.txt и after-fix.txt.

Полная метаинформация: github-evidence.json в общем комплекте сдачи.
