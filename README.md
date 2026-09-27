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

### Локальный расчёт DALY

Чтение XLSX требует отдельной группы `analysis` (также включена в `dev` для тестов).
Исходные файлы WHO не включены в репозиторий: скачайте их самостоятельно с
[официальной страницы WHO](https://www.who.int/data/gho/data/themes/mortality-and-global-health-estimates/global-health-estimates-leading-causes-of-dalys),
в разделе **Download the data → BY COUNTRY → DALY estimates, 2000–2021**.
Сохраните исходные имена файлов. Укажите каталог с шестью файлами
`ghe2021_daly_bycountry_<год>.xlsx` за 2000, 2010, 2015, 2019, 2020 и 2021 годы:

```bash
uv run --group analysis python -m research_global_health.pipelines.daly --source-dir /path/to/downloads
```

Результат — `data/local/daly_rus.csv`, исключённый из Git. Срез: Россия (`RUS`),
оба пола (`Persons`), все возрасты (`All ages`), все причины (`All Causes`, код 0).
DALY сохраняются в тысячах; изменение относительно 2000 года рассчитывается как
`(значение / значение_2000 - 1) * 100`. Это изменение абсолютного объёма DALY,
а не показателя на душу населения или возраст-стандартизованного показателя.

На сайте размещается подготовленная таблица и график с атрибуцией WHO.
Условия данных WHO указаны отдельно от лицензии кода в
[описании P5](docs/lab2/p5/index.md).

### Локальная таблица и график

После извлечения CSV сформируйте черновики результатов для двух версий P5:

```bash
uv run --group analysis python -m research_global_health.pipelines.daly_report
uv run --group analysis python -m research_global_health.pipelines.daly_report --through-year 2021
```

Первая команда использует годы до 2020 включительно, вторая добавляет 2021.
Результаты (`results.md` и `daly.png`) сохраняются отдельно в
`data/local/report-2020/` и `data/local/report-2021/`, вне Git и сайта.
Проценты пересчитываются из исходных значений CSV. График показывает только
доступные годы, без интерполяции промежуточных годовых значений.

Для обновления результатов первой версии на сайте после проверки расчёта:

```bash
uv run --group analysis python -m research_global_health.pipelines.daly_report --output-dir docs/lab2/p5
```

Эта команда перезаписывает `docs/lab2/p5/results.md` и `daly.png`.
Снимок результатов включается в сайт; исходные XLSX и промежуточный CSV — нет.
Скачать XLSX необходимо только для пересчёта, для сборки сайта они не нужны.

### Локальный сайт

Установить зависимости сайта вместе с окружением проекта:

```bash
uv sync --group docs --locked
```

Запустить предпросмотр (точный адрес будет в выводе команды):

```bash
uv run --group docs mkdocs serve
```

Проверить сборку сайта, считая предупреждения ошибками:

```bash
uv run --group docs mkdocs build --strict
```

Собранные страницы находятся в `site/`; этот каталог не включается в Git.
Зависимости сайта выделены в группу `docs` и не входят в runtime-зависимости CLI.

### Версии сайта (mike)

Обычный `mkdocs serve` показывает текущие исходники. Для нескольких версий
используется `mike serve`. Команды ниже создают локальные коммиты в служебной
ветке `gh-pages`; выполняйте их только после согласования или в отдельной
временной копии репозитория. Без `--push` файлы не отправляются на хостинг.

```bash
# Сначала подготовьте снимок результатов до 2020 года.
uv run --group docs mike deploy v1.0 latest
# Затем подготовьте снимок с 2021 годом и соответствующие тексты страниц.
uv run --group docs mike deploy --update-aliases v1.1 latest
uv run --group docs mike set-default latest
uv run --group docs mike list
uv run --group docs mike serve -a 127.0.0.1:8002
```

В локальном предпросмотре доступны `/v1.0/`, `/v1.1/` и `/latest/`.
Настройка публикации по Git-тегам выполняется отдельным этапом.

### Проверки Python-проекта

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
