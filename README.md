# Landing Content Factory · Eduson

Конструктор лендингов в стилистике [Eduson Academy](https://eduson.academy). Продакт открывает HTML-страницу-конструктор, чекбоксами выбирает варианты блоков, нажимает «Сгенерировать промт» — в буфер копируется (или скачивается .txt) структурированный промт со списком блоков и ТЗ, который вставляется в чат с Claude. На выходе — готовый HTML лендинга.

🌐 **Открытый деплой:** https://eduson-ops.github.io/landing-factory/

## Запуск локально

```powershell
# в корне проекта
python -m http.server 8000
```

Открыть в браузере:

- **http://localhost:8000/** — главная страница, конструктор (= `constructor.html`)
- http://localhost:8000/blocks/_kitchen-sink.html — палитра/типографика/компоненты (radio-переключатель темы)
- http://localhost:8000/blocks/_kitchen-sink.html?theme=dark — тёмная тема через URL

> Блоки **обязательно открывать через dev-server**. Если открыть `.html` двойным кликом, относительные пути к `../css/` сломаются.

## Как работает конструктор

1. **Выбор блоков.** Каталог сгруппирован по типам: hero, программа, FAQ, формат, ментор, проекты, отзывы, цена, CTA, sticky. Чекбокс на каждой карточке. Превью — живой `<iframe>` со scale 0.3125. Если блок не загрузился — красная плашка с причиной (404, dev-server упал и т.д.).
2. **Тема.** `Light · Violet` (по умолчанию) или `Dark · Orange`. Тема ставится на `<body>` собранного HTML. Блоки `hero-03-dark` и `stats-01-dark` имеют тему зашитую в файл — их переключатель не трогает.
3. **Режим промта:**
   - **Claude Code CLI** (рекомендуется, ~1.5 KB) — компактный промт со списком путей файлов и инструкцией. Claude в CLI сам читает файлы через `Read`. Не работает в claude.ai/chat.
   - **claude.ai (браузер)** (~30–100 KB) — полный inline HTML с CSS/JS внутри и Unsplash-картинками вместо `placeholder.svg`. Работает в любом чате Claude. Лучше «Скачать .txt» и приложить файлом.
4. **Кнопки.** «Скопировать в буфер» или «Скачать .txt». Под ними — счётчик символов/приближённых токенов.
5. **Защита от ошибок.** Если хотя бы один выбранный блок не загрузился — модал с предупреждением «N блоков не загрузились — всё равно сгенерировать?».

## Структура

```
.
├── README.md
├── constructor.html          ← главная
├── blocks/
│   ├── _kitchen-sink.html    ← контрольный файл
│   ├── css/
│   │   ├── tokens.css        ← дизайн-токены (#6B5EEC, #FFD53B, радиусы 8/12/20/30/100)
│   │   ├── themes.css        ← .theme-light-violet (def.), .theme-dark-orange
│   │   ├── base.css          ← reset, Inter, .container, mobile breakpoints (768/360)
│   │   └── components.css    ← .btn, .badge-yellow, .icon-circle, .card, .accordion-item, .field, .placeholder-photo
│   ├── js/
│   │   └── components.js     ← общий JS через event delegation (аккордеон + слайдер + форма)
│   ├── img/
│   │   └── placeholder.svg   ← локальная фото-заглушка
│   ├── 01-hero/        4 варианта (classic, with-form, dark, centered)
│   ├── 02-target-audience/   1
│   ├── 03-pain-split/        1
│   ├── 04-benefits/          1
│   ├── 05-program/           2 (accordion, accordion-pdf)
│   ├── 06-format/            1
│   ├── 07-mentor/            2 (chat, tags)
│   ├── 08-projects/          1
│   ├── 09-result-stats/      1 (stats-dark — зашитая тема)
│   ├── 10-experts/           1
│   ├── 11-graduates/         2 (quotes, reviews)
│   ├── 12-ratings/           1
│   ├── 13-diploma/           1
│   ├── 14-pricing/           1
│   ├── 15-faq/               1
│   ├── 16-cta-form/          2 (inline, callback)
│   └── 17-sticky-footer/     1 (фиксированная плашка с data-preview-only маркером)
└── refrences/               ← скриншоты Eduson (опечатка сохранена намеренно)
```

## Дизайн-токены

Все значения верифицированы grep-ом по реальному CSS-экспорту Tilda (`refrences/Операционный директор лендинг.txt`):

| Токен | Значение |
|---|---|
| `--color-bg` | `#F3F3F6` |
| `--color-text` | `#1E1E20` |
| `--color-text-muted` | `#A3A3AB` |
| `--color-primary` | `#6B5EEC` |
| `--color-accent-yellow` | `#FFD53B` |
| `--color-cta-dark` | `#0F0F12` |
| `--radius-pill` | `100px` |
| `--radius-lg` | `30px` |
| `--radius-md` | `20px` |
| Шрифт | `'Inter'` + `font-optical-sizing: auto` (через Google Fonts opsz axis) |

Тёмная тема (`.theme-dark-orange`) переопределяет primary на `#FF6B0F` и поверхности на чёрные оттенки.

## Правила для шаблонов блоков

1. **Подключение CSS/JS — относительные пути двухуровневые:**
   ```html
   <link rel="stylesheet" href="../css/tokens.css">
   <script src="../js/components.js" defer></script>
   ```
   В собранном `index.html` Claude автоматически меняет `../../css/` → `blocks/css/` (см. Mode A инструкцию).
2. **Тема — через класс на `<body>`:** `theme-light-violet` (по умолчанию) или `theme-dark-orange`.
3. **Картинки — через `.placeholder-photo`:** локальный `blocks/img/placeholder.svg`.
4. **Иконки — inline SVG** (Heroicons MIT) внутри `<span class="icon-circle">`.
5. **Аккордеон / слайдер** — атрибуты `data-accordion-head`, `data-slider-arrow` и т.д. JS уже подключён через `components.js`.
6. **Mobile breakpoints:** 768px (tablet), 360px (mobile minimum). Все блоки должны собираться корректно на 360px.

## Расширение каталога

Добавить новый вариант блока:
1. Создать `blocks/{NN}-type/type-{NN}-{slug}.html` со ссылками на CSS/JS как выше.
2. Добавить запись в массив `CATALOG` в [constructor.html](constructor.html) (название группы + path + name + slug).
3. Если нужна свежая иконография — `<svg viewBox="0 0 24 24" ...>` инлайн.

## Известные ограничения

- **Sticky-footer в превью** — переключается в `position: relative` через `?preview=1` (специальный inline-скрипт с `data-preview-only`, конструктор автоматически вырезает его при сборке промта).
- **`Inter Display` в исходнике Tilda не существует отдельно** — используется один Inter с `font-optical-sizing: auto`.
- **Папка называется `refrences/`** (опечатка от первой попытки), не меняем — все ссылки и комментарии используют именно это имя.
