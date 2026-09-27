# Research Global Health

![CI](https://github.com/kholodkova/research-global-health/actions/workflows/ci.yml/badge.svg)

Учебный Python-проект для исследования и анализа данных в области глобального здравоохранения.

В качестве источника данных используются открытые данные Всемирной организации здравоохранения (WHO) — Global Health Estimates о ведущих причинах потери лет здоровой жизни (DALYs).

## Требования

- Python 3.12 или выше
- [uv](https://docs.astral.sh/uv/)

## Установка

Клонируйте репозиторий и перейдите в папку проекта:

```bash
git clone https://github.com/kholodkova/research-global-health.git
cd research-global-health
```

Установите зависимости и создайте виртуальное окружение:

```bash
uv sync
```

## Использование CLI

Показать текущую версию приложения:

```bash
uv run rg version
```

Ожидаемый вывод:

```text
research-global-health 0.1.0
```

Проверить текущую конфигурацию приложения:

```bash
uv run rg check-config
```

Ожидаемый вывод с настройками по умолчанию:

```text
data_dir: data
log_level: INFO
request_timeout: 30.0
max_concurrency: 8
github_token_set: False
```

Команда `check-config` показывает основные параметры конфигурации, но не выводит значение GitHub-токена.

## Конфигурация

Настройки приложения можно задавать с помощью переменных окружения с префиксом `RG_` или через файл `.env`.

| Переменная | Описание | Значение по умолчанию |
|---|---|---|
| `RG_GITHUB_TOKEN` | GitHub-токен | Не задан |
| `RG_DATA_DIR` | Директория для данных | `data` |
| `RG_LOG_LEVEL` | Уровень логирования | `INFO` |
| `RG_REQUEST_TIMEOUT` | Тайм-аут запросов в секундах | `30.0` |
| `RG_MAX_CONCURRENCY` | Максимальное количество параллельных операций (минимум `1`) | `8` |

Пример переопределения настроек через переменные окружения:

```bash
RG_LOG_LEVEL=DEBUG RG_MAX_CONCURRENCY=16 uv run rg check-config
```

Для локальной конфигурации можно создать `.env` на основе `.env.example`.

Секретные значения, такие как GitHub-токен, не следует добавлять в Git. Файл `.env` исключён из репозитория через `.gitignore`.

## Разработка

Запустить все тесты:

```bash
uv run pytest
```

Минимальный порог покрытия кода тестами — 70%.

Проверить код с помощью Ruff:

```bash
uv run ruff check .
```

Проверить форматирование:

```bash
uv run ruff format --check .
```

Проверить статическую типизацию с помощью mypy:

```bash
uv run mypy
```

Запустить все pre-commit проверки:

```bash
uv run pre-commit run --all-files
```

Установить pre-commit hook локально:

```bash
uv run pre-commit install
```

## Структура проекта

```text
research-global-health/
├── .github/
│   └── workflows/
│       └── ci.yml              # GitHub Actions CI
├── src/
│   └── research_global_health/
│       ├── api/                # Заготовка для API
│       ├── models/             # Модели данных
│       ├── pipelines/          # Пайплайны обработки данных
│       ├── sources/            # Источники данных
│       ├── storage/            # Работа с хранением данных
│       ├── __init__.py
│       ├── cli.py              # CLI приложения
│       ├── config.py           # Конфигурация приложения
│       ├── logging_setup.py    # Настройка логирования
│       └── py.typed
├── tests/
│   ├── conftest.py             # Общие фикстуры pytest
│   ├── test_cli.py             # Тесты CLI
│   └── test_config.py          # Тесты конфигурации
├── .env.example                # Пример переменных окружения
├── .gitignore
├── .pre-commit-config.yaml     # Настройки pre-commit
├── .python-version             # Версия Python
├── pyproject.toml              # Метаданные, зависимости и настройки инструментов
├── README.md
└── uv.lock                     # Зафиксированные версии зависимостей
```

## Источник данных

В проекте используются открытые данные Всемирной организации здравоохранения (WHO) из набора **Global Health Estimates (GHE): Leading Causes of DALYs**.

**Источник:**
[WHO — Global Health Estimates: Leading causes of DALYs](https://www.who.int/data/gho/data/themes/mortality-and-global-health-estimates/global-health-estimates-leading-causes-of-dalys)

**Рекомендуемое цитирование источника:**

> Global Health Estimates 2021: Disease burden by Cause, Age, Sex, by Country and by Region, 2000–2021. Geneva: World Health Organization; 2024.
