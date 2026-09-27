# Отчёт по лабораторной работе №2

## 1. Ход работы и созданные ресурсы

В работе выбран проект `research-global-health` с генератором MkDocs Material.
Исходный код, документация и автоматизация находятся в [репозитории GitHub](https://github.com/kholodkova/research-global-health).
Для отечественной публикации используется публичный репозиторий SourceCraft
`kholodkova-research-global-health/research-global-health`.

Сайт опубликован на двух площадках:

| Площадка | Ссылка | Проверка |
| --- | --- | --- |
| GitHub Pages | [v1.1](https://kholodkova.github.io/research-global-health/v1.1/) | открывается; переключатель версий работает |
| SourceCraft Sites | [v1.1](https://kholodkova-research-global-health.sourcecraft.site/research-global-health/v1.1/) | открывается; опубликованы `v1.0` и `v1.1` |
| GitHub Actions | [список запусков](https://github.com/kholodkova/research-global-health/actions) | CI и Site для `v1.1` завершились успешно |

Основной порядок работы: подготовка сайта и локальная строгая сборка; выбор
T4 и P5; добавление CI и Site; проверка ветки и PR; слияние PR №3; создание
тега `v1.1`; проверка двух деплоев и поиска.

## 2. Исследовательское задание T4

T4 — сравнение способов доставки статического сайта и границ доступа
автоматизации. Полный анализ прав, угроз и мер снижения риска приведён в
[разделе T4](t4.md). Рассмотрены GitHub Pages, SourceCraft Sites, SSH/SFTP,
FTP/FTPS и S3. Практический эксперимент проверил локальную страницу при CSP,
запрещающем загрузку внешних ресурсов.

## 3. Практическое задание P5

P5 реализован через `mike` и теги `v1.0`/`v1.1`. Версия `v1.0` содержит годы
2000, 2010, 2015, 2019 и 2020; `v1.1` добавляет 2021 год (78 278,86 тыс. DALY).
Алиас `latest` указывает на `v1.1`, а переключатель показывает обе версии.
Подробные данные и воспроизводимость находятся в [описании P5](p5/index.md).

## 4. Пайплайны

### CI

Файл: `.github/workflows/ci.yml`. Пайплайн запускается на `push` и
`pull_request`, устанавливает Python и зависимости через `uv`, затем выполняет
Ruff, форматирование, mypy и pytest:

```yaml
on:
  push:
  pull_request:

jobs:
  quality:
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
      - run: uv sync --locked
      - run: uv run ruff check .
      - run: uv run ruff format --check .
      - run: uv run mypy
      - run: uv run pytest
```

### Site

Файл: `.github/workflows/site.yml`. На каждой ветке выполняются проверки и
строгая сборка MkDocs. Для тегов `v1.0` и `v1.1` дополнительно формируются
деревья версий, загружается Pages-артефакт и запускаются два независимых job:
`deploy-pages` и `deploy-sourcecraft`.

```yaml
on:
  push:
    branches: ['**']
    tags: [v1.0, v1.1]
  pull_request:

jobs:
  build:
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - run: uv sync --locked --group docs
      - run: uv run --group docs mkdocs build --strict

  deploy-pages:
    if: startsWith(github.ref, 'refs/tags/')
    needs: build
    permissions:
      pages: write
      id-token: write
    steps:
      - uses: actions/deploy-pages@v4

  deploy-sourcecraft:
    if: startsWith(github.ref, 'refs/tags/')
    needs: build
    steps:
      - uses: actions/download-artifact@v4
      - name: Deliver static files to SourceCraft
        run: git clone; rsync; git commit; git push
```

Комментарии в исходных YAML объясняют разделение сборки и доставки, проверку
анцестра тега относительно `master`, отсутствие токена в URL и использование
минимальных разрешений. Полный текст доступен в [CI](https://github.com/kholodkova/research-global-health/blob/master/.github/workflows/ci.yml)
и [Site](https://github.com/kholodkova/research-global-health/blob/master/.github/workflows/site.yml).

### Успешные и проваленные запуски

| Сценарий | Результат | Ссылка |
| --- | --- | --- |
| Site на ветке `lab2` | Success, публикация пропущена по условию ветки | [run](https://github.com/kholodkova/research-global-health/actions/runs/36340827828) |
| Site для `v1.1` | Success: build, deploy-pages, deploy-sourcecraft | [Actions](https://github.com/kholodkova/research-global-health/actions) |
| Ошибка публикации после слияния PR | Failure: `would clobber existing tag` | [run](https://github.com/kholodkova/research-global-health/actions/runs/36345647029) |

Для успешных запусков сохранены скриншоты в `docs/assets/screens/`;
проваленный запуск дополнительно доступен по ссылке выше. Ошибка с тегом была
устранена заменой `git fetch origin master --tags` на
`git fetch origin master --no-tags`.

## 5. Измерения

Все значения ниже взяты из реальных запусков и локального эксперимента.

| Запуск/объект | Сборка | Развёртывание Pages | Развёртывание SourceCraft | Всего |
| --- | ---: | ---: | ---: | ---: |
| Site, ветка `lab2` | 22 с | — | — | 25 с |
| Site, тег `v1.1` | 28 с | 11 с | 15 с | 1 мин 20 с |

| Локальный эксперимент T4 | Обычная загрузка | CSP без внешних ресурсов |
| --- | ---: | ---: |
| Уникальные локальные HTTP-файлы со статусом 200 | 11 | 11 |
| Суммарный размер файлов | 479 486 байт (468,25 КиБ) | 479 486 байт (468,25 КиБ) |
| Изменение размера | — | 0 байт |
| Поиск `DALY` | 4 совпадения | 4 совпадения |

| Проверка поиска на GitHub Pages v1.1 | Совпадения |
| --- | ---: |
| `здравоохранение` | 1 |
| `лицензии` | 4 |
| `публикация` | 4 |
| `WHO` | 6 |
| `DALY` | 5 |

Время MkDocs в отдельном запуске составило 0,23 с. Это время самой сборки
документации и не включает установку окружения и проверки качества.

## 6. Отладка

| Реальная ошибка | Гипотеза | Проверка | Решение |
| --- | --- | --- | --- |
| `! [rejected] v1.0 -> v1.0 (would clobber existing tag)` | `fetch --tags` повторно получает уже существующий тег | Открытие шага `Build both release trees` и повтор локальной команды | Использован `git fetch origin master --no-tags`; тег перемещён на актуальный merge-коммит только после согласования |
| SourceCraft отвечал `404 Page Not Found` при наличии `index.html` и `sites.yaml` | Сайт ещё не активирован или не запущен SourceCraft CI | Проверены публичность организации/репозитория, ветка `main`, содержимое репозитория и карточка «Выкладки» | Добавлена корректная конфигурация `sites.yaml`, создан workflow `build-site`, после чего URL начал открываться |
| Поиск SourceCraft зависал на `Инициализация поиска` | Поисковый индекс не загрузился в клиентском маршруте | Тот же URL и те же запросы проверены на GitHub Pages | GitHub Pages подтвердил корректность индекса; результаты поиска зафиксированы таблицей выше |
| Локальная строгая сборка завершилась ошибкой доступа к `/Users/.../.cache/uv` | Ограничение sandbox на кэш, а не ошибка проекта | Повтор запуска с разрешённым доступом к кэшу | Сборка `mkdocs build --strict` завершилась успешно |

## 7. Вывод и рекомендуемый стек

Для публикации результатов исследований в этом проекте рекомендуется стек:
Python + `uv` для воспроизводимого окружения, MkDocs Material для статической
документации, `mike` для версий, GitHub Actions для проверок и сборки,
`upload-pages-artifact`/`deploy-pages` для GitHub Pages и SourceCraft Sites для
отечественного зеркала. Такой стек разделяет исходники, артефакт и права
публикации; результаты WHO остаются статическими проверяемыми файлами.

Рекомендация изменяется при следующих ограничениях:

- нужны серверные вычисления, авторизация или персональные данные — нужен
  серверный или облачный application hosting;
- требуется частое обновление больших файлов — нужен объектный storage и CDN;
- нельзя использовать GitHub или SourceCraft — выбирается собственный SFTP,
  S3-совместимый storage или внутренний сервер;
- требуется строгая защита цепочки поставки — actions закрепляются по SHA,
  вводятся review и отдельные доверенные runners;
- сайт должен работать без внешней сети — все шрифты, скрипты и модули нужно
  хранить локально и повторить измерение CSP.
