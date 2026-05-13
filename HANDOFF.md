# Landing Content Factory · Handoff

Дата: 2026-05-13
Репо: https://github.com/eduson-ops/landing-factory
Pages: https://eduson-ops.github.io/landing-factory/

---

## Что это

Конструктор лендингов в стилистике Eduson Academy. Пользовательский сценарий:

1. Продакт открывает [constructor.html](constructor.html) в браузере
2. Тычком выбирает нужные блоки из ~31 шаблона (карточки с превью)
3. Описывает курс в textarea «ТЗ для лендинга» (или нажимает «+ шаблон» — каркас собирается из выбранных блоков)
4. Жмёт «Скопировать промт» → в буфер уходит структурированный промт со списком файлов блоков и ТЗ
5. Вставляет в Claude Code CLI (или claude.ai в браузере для второго режима) → на выходе готовый `index.html` лендинга в стиле Eduson

Альтернативно: «Посмотреть собранный лендинг» открывает live-превью без Claude — конструктор сам склеивает блоки и показывает result в iframe (Desktop / Tablet / Mobile toggle).

---

## Quick start

```powershell
# из корня проекта
python -m http.server 8000
# открыть http://localhost:8000/constructor.html
```

Блоки **обязательно через dev-server** — двойной клик ломает относительные пути `../css/`.

Деплой автоматически на GitHub Pages при push в main (см. `.nojekyll` для отключения Jekyll, иначе `_kitchen-sink.html` 404 из-за подчёркивания).

---

## Архитектура

```
.
├── constructor.html             # SPA-конструктор (один файл, vanilla JS)
├── index.html                   # meta-redirect на constructor.html для Pages
├── README.md                    # пользовательский гайд
├── HANDOFF.md                   # этот файл
├── eduson-research.md           # результаты краулинга 11 курсов eduson.academy
├── build-ai-engineer.py         # тест-скрипт сборки лендинга «ИИ-инженер» (валидация Mode A)
├── landing-ai-engineer.html     # output build-скрипта, выкатывается на Pages как preview
├── .nojekyll                    # отключает Jekyll на Pages
└── blocks/
    ├── _kitchen-sink.html       # контрольный файл со всеми компонентами
    ├── css/
    │   ├── tokens.css           # дизайн-токены (#6B5EEC, #FFD53B, радиусы 8/12/20/30/100)
    │   ├── themes.css           # .theme-light-violet (def.) / .theme-dark-orange
    │   ├── base.css             # reset, Inter, .container, mobile breakpoints
    │   └── components.css       # .btn, .badge-yellow, .icon-circle, .accordion-item, etc.
    ├── js/
    │   └── components.js        # общий JS через event delegation (аккордеон + слайдер + форма)
    ├── img/
    │   └── placeholder.svg      # serый прямоугольник 4:3 «Photo»
    ├── 01-hero/                 # 4 hero (classic/with-form/dark/centered)
    ├── 02-target-audience/      # 2 (с фото / без фото)
    ├── 03-pain-split/           # 1 (проблемы и решения)
    ├── 04-benefits/             # 1 (что вы получите)
    ├── 05-program/              # 2 (accordion / accordion-pdf)
    ├── 06-format/               # 1 (vertical alternating «Как проходит обучение»)
    ├── 07-mentor/               # 2 (chat / личный ментор + tags)
    ├── 08-projects/             # 1 (горизонтальный слайдер)
    ├── 09-result-stats/         # 2 (dark / зарплаты)
    ├── 10-experts/              # 1 (слайдер преподавателей)
    ├── 11-graduates/            # 2 (цитаты / отзывы)
    ├── 12-ratings/              # 1 (агрегаторы — exact)
    ├── 13-diploma/              # 2 (split / два документа — exact)
    ├── 14-pricing/              # 2 (1 тариф / 2 трека)
    ├── 15-faq/                  # 1 (аккордеон)
    ├── 16-cta-form/             # 2 (inline / callback)
    ├── 17-sticky-footer/        # 1 (нижняя плашка)
    ├── 18-text-section/         # 1 (narrative о рынке)
    ├── 19-skills/               # 1 (таблица навыков)
    ├── 20-trust/                # 1 (про доверие — exact)
    ├── 21-partners/             # 1 (логотипы — exact)
    ├── 22-employer/             # 1 (оплата от работодателя)
    ├── 23-ai-tools/             # 1 (нейросети-помощники)
    └── 25-portfolio-gallery/    # 1 (masonry-галерея работ)
```

### Что НЕ в zip-ке (gitignored)

- `refrences/` — ~130 скриншотов + Tilda-экспорт (~31 MB)
- `research/raw/` — сырой HTML 7 курсов eduson.academy (~10 MB), для локального разбора
- `voice-promt.txt` — оригинальное голосовое ТЗ
- `*.pdf` — PDF-брифы курсов

Эти файлы — твой локальный source-of-truth, в репо не пушим.

---

## Каталог блоков — статус верификации

Каждый блок в `BLOCK_META` (constructor.html, ~строка 691) имеет:
- `type: 'universal' | 'exact'` — адаптируется под курс vs копируется как есть
- `canonicalOrder: 1..99` — позиция в каноничной последовательности Eduson
- `sourceUrl` — eduson.academy URL эталона (если есть — в карточке появляется иконка «оригинал ↗»)
- `notes` — пояснение что верифицировано / что нужно

В UI карточки блока:
- 🏷 бейдж типа (universal / exact)
- 4️⃣ номер canonical-позиции в углу
- ⚠ «замена ассетов» для блоков с brand-плейсхолдерами
- ❓ «нужен референс» (красный) для блоков без `sourceUrl`
- ↗ ссылка на eduson.academy если есть `sourceUrl`

### Pixel-target переписаны под эталон-скрин (12.05–13.05.2026)

| Блок | Эталон |
|---|---|
| `hero-04-centered` | Eduson «Руководитель медицинской организации» |
| `hero-02-with-form` | Eduson «Менеджер проектов» (3-кол + trust-bar) |
| `hero-03-dark` | Eduson «Разработчик на Python» |
| `target-01-cards-photo` | Eduson «Обучение для всех, кто хочет...» (мед.директор) |
| `pain-01-photo-bullets` | Eduson «Вместо общей теории — реальные задачи медбизнеса» |
| `text-01-narrative` | Eduson «Займите нишу ИИ» |
| `format-01-mosaic` | Eduson «Как проходит обучение» (3 verticalрежима) |
| `mentor-02-tags` | Eduson «Личный ментор на всём пути обучения» |
| `pricing-01-card` | Eduson «Стоимость курса» (1 тариф) |
| `ratings-01-aggregators` | SVG letter-marks вместо цветных точек |
| `partners-01-logos` | SVG letter-marks (8 компаний-партнёров) |
| `trust-01-stats-hero` | Eduson «Академия Эдюсон — это про доверие» |

### Удалены как «не из эталона»

- `hero-05-bg-photo` — был придуман по ошибочной гипотезе агента (пустой bg+overlay не используется на eduson.academy)
- `projects-02-list` — голосовая ОС: «портфолио вертикальным списком — херня полная»
- `skills-group-01` — был придуман как 3-кол grid, не подтвердился по эталонам

### Ещё не верифицированы (отмечены ❓ «нужен референс» в UI)

| Блок | Статус |
|---|---|
| `hero-01-classic` | Источник не верифицирован |
| `target-02-cards-text` | Возможно ops-director / hr — нужен скрин |
| `benefits-01-grid` | Часто встроено в hero-04 — может быть лишним отдельно |
| `program-01-accordion` | По ОС выглядит хорошо, точный источник неясен |
| `stats-01-dark` | Тёмные результаты — нужен скрин |
| `stats-02-salary` | Зарплаты — есть PM эталон с фото-плашками над зарплатами, нужно перерисовать |
| `skills-01-table` | Нужен скрин — Python-style с dark tag-pills |
| `mentor-01-chat` | Не верифицирован |
| `experts-01-slider` | Композиция выверена, нужен скрин для финала |
| `graduates-01-quotes`, `graduates-02-reviews` | Оба — нужны скрины |
| `expert-quote-01` | Создан по гипотезе про MBA-цитаты (Адизес) — не подтверждено |
| `diploma-02-two-docs` | Не верифицирован |
| `pricing-02-two-tracks` | Не верифицирован |
| `employer-01-cta` | Не верифицирован |
| `cta-01-inline`, `cta-02-callback` | Оба — нужны скрины |
| `faq-01-accordion` | По ОС выглядит хорошо (минимальные правки если нужны) |
| `sticky-01-bottom-bar` | Не верифицирован |
| `portfolio-gallery-01` | Гипотеза по web-designer — нужен скрин для верификации |
| `program-cards-01` | Гипотеза по mba-all (агрегатор) — нужен скрин |
| `ai-tools-01-grid` | Подтверждён grep-ом по python.html, но композиция не верифицирована |

---

## Дизайн-система (`blocks/css/`)

### Цвета (выверены grep-ом по Tilda-экспорту `Операционный директор`)

| Токен | Значение |
|---|---|
| `--color-primary` | `#6B5EEC` (фиолет) |
| `--color-accent-yellow` | `#FFD53B` (жёлтый акцент) |
| `--color-text` | `#1E1E20` |
| `--color-text-muted` | `#A3A3AB` |
| `--color-bg` | `#F3F3F6` |
| `--color-surface` | `#FFFFFF` |
| `--color-cta-dark` | `#0F0F12` (для тёмных CTA — менеджер-проектов hero) |

### Радиусы

| `--radius-pill` | `100px` |
| `--radius-lg` | `30px` |
| `--radius-md` | `20px` |
| `--radius-sm` | `12px` |

### Шрифт

`Inter` через Google Fonts с `font-optical-sizing: auto` (опт. размер `opsz` axis 14..32). Один шрифт на весь проект — у Eduson по факту так же.

### Темы

`<body class="theme-light-violet">` — по умолчанию.
`<body class="theme-dark-orange">` — для IT-курсов (jeggli `hero-03-dark`, `stats-01-dark` имеют тему зашитую жёстко).

---

## UI конструктора

### Левая панель — каталог
- 7 групп блоков с раскрытием
- Поиск по названию/тегам
- Каждая карточка: live-превью iframe с scale 0.3125 + бейджи + canonical-номер + ext-link

### Правая панель
- Тема (Light / Dark)
- Чекбокс «Соблюдать порядок Eduson» (по умолчанию вкл.) — авто-сортировка выбранных блоков по `canonicalOrder`
- Список выбранных блоков с reorder-кнопками (если чекбокс выкл.)
- Textarea «ТЗ для лендинга» + кнопка «+ шаблон» (генерирует каркас под выбранные блоки из `BRIEF_BY_SLUG`)
- Радио «Куда вставлять?» — `CLI` (Mode A) / `Браузер` (Mode B)
- Кнопки: «Скопировать промт» / «Скачать .txt» / «Посмотреть собранный лендинг» / «Поделиться выбором ссылкой»

### Header
- Поиск
- Счётчик выбранных
- 4 пресета: «IT/ИИ-курс» / «Софт-навыки» / «Минимальный» / «Полный»

---

## Промт-режимы

### Mode A — Claude Code CLI (рекомендуемый, ~1.5 KB)
Промт ссылается на пути файлов блоков. Claude в CLI сам читает их через `Read`, извлекает `<body>` + `<style>`, склеивает в `index.html`. Добавлена явная секция «ТОЧНЫЕ блоки» — Claude знает, что в exact-блоках контент не подменять.

### Mode B — claude.ai (браузер, ~30–100 KB)
Полный inline HTML с CSS внутри + Unsplash-картинки вместо `placeholder.svg`. Brand-placeholders в exact-блоках помечены HTML-комментарием `[EXACT]` чтобы браузерный Claude не редактировал.

`buildAssembledHtml()` для live-превью:
- `BASE_PATH = location.origin + dirname(pathname)` — корректно работает и локально, и на Pages
- `rewriteImgPathsPreview/ModeB` — переписывают `../../img/` под текущий хост

---

## State / Persistence

`localStorage[eduson-constructor-v1]` хранит: `selected[], theme, mode, brief, canonicalOrder`.
URL-параметры: `?b=hero-04,target-01,program-02&t=dark` — share-link.

---

## Open product TODO

### Высокий приоритет
- [ ] Прислать скрины-эталоны для всех ❓-блоков (см. таблицу выше) и переписать каждый pixel-target
- [ ] Решить вопрос с реальными SVG-логотипами (ratings-01, partners-01) — сейчас letter-marks как brand-placeholders, продакт заменяет перед публикацией
- [ ] stats-02-salary — нужен новый эталон (видел PM-вариант с зарплатой+фото-плашками, надо перерисовать)
- [ ] Проверить визуальное соответствие на Pages для всех переписанных блоков (hero-02/03/04, target-01, pain-01, format-01, mentor-02, pricing-01, ratings-01, partners-01, trust-01, text-01)

### Средний приоритет
- [ ] Преcеты курсов (PRESETS в constructor.html) — обновить под актуальный набор блоков. Сейчас `ai-engineer` ОК; `soft-skills`, `minimal`, `full` — не пересмотрены после правок
- [ ] `BRIEF_BY_SLUG` (брифы под каждый блок для шаблонной заполнялки) — некоторые ссылаются на удалённые блоки или не отражают новый контент
- [ ] Добавить недостающие блоки: возможно `hero-bg-photo` (если найдётся реальный пример — сейчас удалили как hero-05), «второй курс в подарок» для MBA, чек-листы / шаблоны для скачивания

### Низкий приоритет
- [ ] Очистить `eduson-research.md` от устаревших гипотез (агентский отчёт от первой фазы) — оставить только верифицированные паттерны
- [ ] `build-ai-engineer.py` — расширить под несколько тестовых курсов (мед.директор, менеджер проектов) для visual regression
- [ ] Удалить файл `blocks/01-hero/hero-05-bg-photo.html` (уже не в CATALOG, но файл лежит)

---

## Известные ограничения

- **Sticky-footer в превью** — переключается в `position: relative` через `?preview=1` (специальный inline-скрипт `data-preview-only`, конструктор автоматически вырезает его при сборке через `STRIP_PREVIEW_RE`)
- **Папка `refrences/`** — намеренная опечатка (от первой попытки), все ссылки используют именно её
- **Pages CDN-кэш** — после `git push` обновление видно через ~30-90 секунд, в превью карточек может потребоваться `Ctrl+Shift+R`

---

## Расширение каталога (как добавить блок)

1. Создать `blocks/{NN}-type/type-{NN}-{slug}.html` со ссылками на CSS/JS:
   ```html
   <link rel="stylesheet" href="../css/tokens.css">
   <script src="../js/components.js" defer></script>
   ```
2. В constructor.html добавить запись в массив `CATALOG` (соответствующая группа `items`)
3. В `BLOCK_META` добавить поля: `type`, `canonicalOrder`, `sourceUrl`, `notes`, `hasBrandPlaceholders`
4. Если новая иконография — `<svg viewBox="0 0 24 24">` инлайн (filled рекомендуется для брендового вида)

---

## Деплой собранного лендинга

После того как Claude собрал `index.html`:

| Способ | Время | Что получаете |
|---|---|---|
| **Netlify Drop** | 1 мин | Перетащить папку с `index.html` + `blocks/` — `https://random.netlify.app/` |
| **Vercel** | 2 мин | `vercel --prod` или drag-and-drop архива |
| **GitHub Pages** | 5 мин | Создать репо, push, Settings → Pages |

Скопировать в любой из них: `index.html` (собранный) + папки `blocks/css/`, `blocks/js/`, `blocks/img/`.

⚠ **Tilda не подходит** — работает только со своими zero-блоками.

---

## Контакты по продукту

GitHub: eduson-ops org
Pages для ревью: https://eduson-ops.github.io/landing-factory/
