# Research Global Health

Учебный Python-проект для исследования и анализа данных в области глобального здравоохранения.

В качестве источника данных используются открытые данные Всемирной организации здравоохранения (WHO) — Global Health Estimates о ведущих причинах потери лет здоровой жизни (DALYs).

## Установка

Для управления Python и зависимостями в проекте используется `uv`.

После клонирования репозитория перейдите в папку проекта:

```bash
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

Проверить текущую конфигурацию приложения:

```bash
uv run rg check-config
```

Команда `check-config` показывает основные параметры конфигурации, но не выводит значение GitHub-токена.

## Конфигурация

Настройки приложения можно задавать с помощью переменных окружения с префиксом `RG_` или через файл `.env`.

Доступные параметры:

- `RG_GITHUB_TOKEN` — GitHub-токен. По умолчанию не задан.
- `RG_DATA_DIR` — директория для данных. По умолчанию `data`.
- `RG_LOG_LEVEL` — уровень логирования. По умолчанию `INFO`.
- `RG_REQUEST_TIMEOUT` — тайм-аут запросов в секундах. По умолчанию `30.0`.
- `RG_MAX_CONCURRENCY` — максимальное количество параллельных операций. По умолчанию `8`, минимальное допустимое значение — `1`.

Например:

```bash
RG_LOG_LEVEL=DEBUG RG_MAX_CONCURRENCY=16 uv run rg check-config
```

Секретные значения, такие как GitHub-токен, не следует добавлять в Git.

## Тесты и проверка качества

Запустить все тесты:

```bash
uv run pytest
```

Проверить код с помощью Ruff:

```bash
uv run ruff check .
```

Проверить форматирование:

```bash
uv run ruff format --check .
```

Проверить типы с помощью mypy:

```bash
uv run mypy
```

Запустить все pre-commit проверки:

```bash
uv run pre-commit run --all-files
```


## Источник данных

В проекте используются открытые данные Всемирной организации здравоохранения (WHO) из набора **Global Health Estimates (GHE): Leading Causes of DALYs**.

**Источник:**
[WHO — Global Health Estimates: Leading causes of DALYs](https://www.who.int/data/gho/data/themes/mortality-and-global-health-estimates/global-health-estimates-leading-causes-of-dalys)

**Рекомендуемое цитирование источника:**

> Global Health Estimates 2021: Disease burden by Cause, Age, Sex, by Country and by Region, 2000–2021. Geneva: World Health Organization; 2024.
