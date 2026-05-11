# Эмулятор Mode A инструкции из constructor.html.
# Читает выбранные блоки, извлекает <body>, чистит preview-скрипты,
# убирает повторное подключение components.js, заменяет пути,
# собирает в landing-ai-engineer.html.

import re
from pathlib import Path

ROOT = Path(__file__).parent

# v9-preset «ИИ-инженер» — hero-05 (bg-photo) + ai-tools-01 + projects-01 (горизонтальный слайдер)
BLOCKS = [
    'blocks/01-hero/hero-05-bg-photo.html',
    'blocks/18-text-section/text-01-narrative.html',
    'blocks/09-result-stats/stats-02-salary.html',
    'blocks/02-target-audience/target-02-cards-text.html',
    'blocks/23-ai-tools/ai-tools-01-grid.html',
    'blocks/19-skills/skills-01-table.html',
    'blocks/05-program/program-02-accordion-pdf.html',
    'blocks/08-projects/projects-01-slider.html',
    'blocks/13-diploma/diploma-02-two-docs.html',
    'blocks/10-experts/experts-01-slider.html',
    'blocks/12-ratings/ratings-01-aggregators.html',
    'blocks/21-partners/partners-01-logos.html',
    'blocks/20-trust/trust-01-stats-hero.html',
    'blocks/22-employer/employer-01-cta.html',
    'blocks/14-pricing/pricing-02-two-tracks.html',
    'blocks/15-faq/faq-01-accordion.html',
    'blocks/16-cta-form/cta-01-inline.html',
]

BODY_RE         = re.compile(r'<body[^>]*>([\s\S]*?)</body>', re.IGNORECASE)
HEAD_RE         = re.compile(r'<head[^>]*>([\s\S]*?)</head>', re.IGNORECASE)
STYLE_RE        = re.compile(r'<style[^>]*>([\s\S]*?)</style>', re.IGNORECASE)
PREVIEW_RE      = re.compile(r'<script\s[^>]*data-preview-only[^>]*>[\s\S]*?</script>', re.IGNORECASE)
COMPONENTS_RE   = re.compile(r'<script\s+src=["\'][^"\']*components\.js["\'][^>]*>\s*</script>', re.IGNORECASE)

def extract(path: Path):
    """Возвращает (body_html, css_text) — CSS из <style>-блоков в <head>
    нужно сохранить, иначе layout каждого блока сломается."""
    text = path.read_text(encoding='utf-8')
    head_m = HEAD_RE.search(text)
    body_m = BODY_RE.search(text)
    if not body_m:
        return f'<!-- ОШИБКА: не найден <body> в {path} -->', ''
    body = body_m.group(1)
    body = PREVIEW_RE.sub('', body)
    body = COMPONENTS_RE.sub('', body)
    body = body.replace('../../css/', 'blocks/css/').replace('../../js/', 'blocks/js/').replace('../../img/', 'blocks/img/')
    body = body.replace('../css/',    'blocks/css/').replace('../js/',    'blocks/js/').replace('../img/',    'blocks/img/')

    css_chunks = []
    if head_m:
        for m in STYLE_RE.finditer(head_m.group(1)):
            css_chunks.append(m.group(1).strip())
    return body.strip(), '\n'.join(css_chunks)

bodies = []
all_css = []
for rel in BLOCKS:
    body, css = extract(ROOT / rel)
    bodies.append(f'<!-- {rel} -->\n{body}\n')
    if css:
        all_css.append(f'/* ─── {rel} ─── */\n{css}')

HEAD = f'''<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Курс ИИ-инженер — Eduson Academy</title>
  <link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,100..900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="blocks/css/tokens.css">
  <link rel="stylesheet" href="blocks/css/themes.css">
  <link rel="stylesheet" href="blocks/css/base.css">
  <link rel="stylesheet" href="blocks/css/components.css">
  <script src="blocks/js/components.js" defer></script>
  <style>
{chr(10).join(all_css)}
  </style>
</head>
<body class="theme-light-violet">
'''
FOOT = '\n</body>\n</html>\n'

html = HEAD + ''.join(bodies) + FOOT

# ── Контент-подмены под ТЗ «ИИ-инженер» ──────────────────────────────────────
# Эмуляция шага 9 Mode A: «подставь данные из ТЗ в заголовки/тексты/...,
# не меняя CSS-классы и структуру разметки». В реальном use case это делает
# Claude по тексту ТЗ — здесь мы воспроизводим вручную для валидации.
PATCHES = [
    # Hero-05: заголовок, lead, eyebrow, meta
    ('<h1>Заголовок профессии или роли</h1>',
     '<h1>ИИ-инженер</h1>'),
    ('<p class="hero5-lead">Краткое ценностное обещание: что человек научится делать и какой результат получит за конкретный срок.</p>',
     '<p class="hero5-lead">За 4–9 месяцев освоите профессию ИИ-инженера: ускоренный трек если знаете Python, или с вводным блоком с нуля.</p>'),
    ('<span class="hero5-eyebrow">Онлайн-курс</span>',
     '<span class="hero5-eyebrow">Онлайн-курс · старт в любой день</span>'),
    ('с нуля за N месяцев',
     'с нуля за 4–9 месяцев'),
    ('N студентов',
     '3 700 студентов'),
    # ai-tools-01: 8 generic слотов → инструменты курса
    ('<h3>Чат-ассистент</h3>',
     '<h3>GPT-4o · GigaChat · DeepSeek</h3>'),
    ('<p>Универсальный помощник для текста, идей, кода</p>',
     '<p>Чат-модели для разработки и интеграций</p>'),
    ('<h3>Помощник по коду</h3>',
     '<h3>LangChain · LangGraph · CrewAI</h3>'),
    ('<p>Автодополнение и рефакторинг в редакторе</p>',
     '<p>Фреймворки агентов и оркестрации цепочек</p>'),
    ('<h3>Генератор изображений</h3>',
     '<h3>Hugging Face · Llama · Mistral</h3>'),
    ('<p>Концепт-арт, иллюстрации, мокапы по описанию</p>',
     '<p>Open-source модели и fine-tuning под задачу</p>'),
    ('<h3>Документы и тексты</h3>',
     '<h3>FastAPI · Docker · n8n</h3>'),
    ('<p>Черновики, резюме, отчёты по шаблонам</p>',
     '<p>Развёртывание ИИ-сервисов в продакшен</p>'),
    ('<h3>Анализ данных</h3>',
     '<h3>Chroma · Qdrant</h3>'),
    ('<p>Расчёты, графики и сводки по таблицам</p>',
     '<p>Векторные базы под retrieval-augmented generation</p>'),
    ('<h3>Перевод и саммари</h3>',
     '<h3>Python · SQL · JSON · Git</h3>'),
    ('<p>Длинные статьи, видео, встречи — в выжимке</p>',
     '<p>Базовый стек, идущий вводным блоком при необходимости</p>'),
    ('<h3>Аудио и подкасты</h3>',
     '<h3>RAG и агентные системы</h3>'),
    ('<p>Расшифровка, озвучка, голос-клонирование</p>',
     '<p>Архитектура решений на стыке моделей и данных</p>'),
    ('<h3>Видео и презентации</h3>',
     '<h3>Dify · Vector DB · API-интеграции</h3>'),
    ('<p>Слайды и видео-нарезки по сценарию</p>',
     '<p>Связка моделей с внешними сервисами и фронтом</p>'),
    # Эксперты — 4 из ТЗ вместо 6 заглушек
    ('<h3>Анна Иванова</h3><p>Lead Analyst, Яндекс</p>',
     '<h3>Андрон Алексанян</h3><p>6+ лет в аналитике и бизнесе. CEO платформы IT&nbsp;Resume</p>'),
    ('<h3>Сергей Петров</h3><p>Head of Data, Сбер</p>',
     '<h3>Любовь Бурцева</h3><p>4+ года опыта. Бэкенд-разработчик в «Рамблере». Ментор по Python</p>'),
    ('<h3>Ольга Смирнова</h3><p>Product Lead, Ozon</p>',
     '<h3>Илья Чумаченков</h3><p>8+ лет в управлении проектами. Эксперт по нейросетям, основатель IIMATES</p>'),
    ('<h3>Денис Орлов</h3><p>Senior PM, VK</p>',
     '<h3>Александр Шамша</h3><p>Менеджер продуктов в Академии Эдюсон. Внедряет ИИ-инструменты</p>'),
    # FAQ — 6 вопросов из ТЗ
    ('<h3>Сколько времени занимает обучение?</h3>',
     '<h3>Мне нужно знать язык Python, чтобы пройти курс «ИИ-инженер»?</h3>'),
    ('Курс рассчитан на 6 месяцев. Доступ к материалам и обновлениям — навсегда. Вы сами выбираете комфортный темп.',
     'Нет, начинать можно без опыта. Для этого есть трек с вводным блоком по Python, API и базовой работе с данными. Сложной математики не будет — мы объясняем модели на понятных примерах и через практику. А если вы уже знаете Python, можно сразу идти по ускоренному треку.'),
    ('<h3>Что делать, если я не успеваю учиться?</h3>',
     '<h3>С чего начинается обучение для новичков?</h3>'),
    ('Доступ к курсу остаётся навсегда — можете возвращаться к материалам, когда удобно. Куратор поможет составить план под ваш ритм.',
     'С базовых вещей: Python, работы с API, структуры ИТ-систем и понимания того, как устроены нейросети. Дальше быстро переходите к практике — пишете простые скрипты и собираете полноценные приложения.'),
    ('<h3>Поможете, если я не разберусь в материале?</h3>',
     '<h3>Есть ли на этом курсе гарантия трудоустройства?</h3>'),
    ('Личный куратор отвечает на вопросы 7 дней в неделю в Telegram. Также подключаются методисты и преподаватели курса.',
     'Нет. Но вы получите всё для успешной карьеры: на выходе у вас будет портфолио с 9 проектами и удостоверение о повышении квалификации или диплом о профпереподготовке.'),
    ('<h3>Чем этот курс лучше бесплатных материалов в интернете?</h3>',
     '<h3>Чем работа специалиста по ИИ отличается от задач аналитика или разработчика?</h3>'),
    ('Программа построена практиками отрасли, материалы собраны в логичную траекторию, есть проверка домашних заданий и реальные кейсы.',
     'ИИ-инженер действует на стыке разработки и работы с данными: проектирует системы с моделями — RAG, агентов, дообучения. В отличие от аналитика — реализует логику. В отличие от разработчика — управляет неопределённостью моделей.'),
    ('<h3>Можно ли вернуть деньги, если курс не подойдёт?</h3>',
     '<h3>Есть ли у вас рассрочка без переплат?</h3>'),
    ('Да, в течение 14 дней с момента оплаты вернём 100% стоимости — без объяснения причин.',
     'Да. Беспроцентная рассрочка на 24 месяца — оформить можно при подаче заявки. Стоимость делится на равные ежемесячные платежи без переплат и скрытых процентов.'),
    ('<h3>Что я получу после завершения курса?</h3>',
     '<h3>Какие инструменты я изучу на курсе?</h3>'),
    ('Диплом о профессиональной переподготовке государственного образца, удостоверение от Eduson Academy и портфолио из 6 кейсов.',
     'GPT-4o (OpenAI API), GigaChat, DeepSeek, Llama, Mistral, Hugging Face. Фреймворки LangChain, LangGraph, CrewAI. Векторные базы Chroma, Qdrant. Запуск и интеграции: FastAPI, Docker, n8n, Dify. База: Python, SQL, JSON, Git, GitHub.'),
]

applied = 0
missed = []
for old, new in PATCHES:
    if old in html:
        html = html.replace(old, new, 1)
        applied += 1
    else:
        missed.append(old[:60])

out = ROOT / 'landing-ai-engineer.html'
out.write_text(html, encoding='utf-8')
print(f'Built: {out}  ({out.stat().st_size:,} bytes, {len(BLOCKS)} blocks, {sum(len(c) for c in all_css):,} bytes inline CSS)')
print(f'Patches: {applied}/{len(PATCHES)} applied' + (f', missed: {missed}' if missed else ''))
