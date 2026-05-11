# Эмулятор Mode A инструкции из constructor.html.
# Читает выбранные блоки, извлекает <body>, чистит preview-скрипты,
# убирает повторное подключение components.js, заменяет пути,
# собирает в landing-ai-engineer.html.

import re
from pathlib import Path

ROOT = Path(__file__).parent

# Блоки в порядке для лендинга «ИИ-инженер» (по ТЗ)
BLOCKS = [
    'blocks/01-hero/hero-04-centered.html',
    'blocks/18-text-section/text-01-narrative.html',
    'blocks/09-result-stats/stats-02-salary.html',
    'blocks/02-target-audience/target-02-cards-text.html',
    'blocks/19-skills/skills-01-table.html',
    'blocks/08-projects/projects-02-list.html',
    'blocks/05-program/program-02-accordion-pdf.html',
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
    # Hero: заголовок, eyebrow, lead
    ('<h1>Руководитель<br>медицинской организации</h1>',
     '<h1>Курс<br>ИИ-инженер</h1>'),
    ('<span class="badge-yellow hero4-eyebrow">Создан · 2026</span>',
     '<span class="badge-yellow hero4-eyebrow">−60% до 11 мая</span>'),
    ('<p class="hero4-lead">Освойте профессию управленца в медицине<br>и увеличьте свой доход</p>',
     '<p class="hero4-lead">За 4–9 месяцев вы освоите профессию ИИ-инженера: быстрее, если уже знаете Python, или с вводным блоком, если начинаете с нуля.</p>'),
    # Hero буллеты
    ('<p>Освоите <b>стратегию, финансы, маркетинг</b>, управление командой и процессами</p>',
     '<p>Научитесь разрабатывать и внедрять <b>ИИ-решения</b> с разработкой и без</p>'),
    ('<p>Настроите клиентский сервис и <b>перестанете зависеть<br>от звёздных врачей</b></p>',
     '<p>Освоите актуальные инструменты: от <b>Python и нейросетей</b> до векторных баз</p>'),
    ('<p>Получите <b>диплом<br>о профессиональной переподготовке</b></p>',
     '<p>Получите <b>диплом о профпереподготовке</b> или удостоверение о повышении квалификации</p>'),
    # Hero CTA
    ('<button class="btn btn--primary btn--lg">Записаться на курс</button>\n      </div>\n\n      <div class="hero4-bottom">',
     '<button class="btn btn--primary btn--lg">Записаться со скидкой</button>\n        <button class="btn btn--ghost btn--lg" style="margin-left:12px">Получить консультацию</button>\n      </div>\n\n      <div class="hero4-bottom">'),
    # Hero нижние 4 карточки
    ('<h4>Практическая отработка навыков</h4>\n          <p>и реальные кейсы медбизнеса</p>',
     '<h4>Учитесь без расписания и дедлайнов</h4>\n          <p>Доступ к материалам и регулярным обновлениям курса — навсегда</p>'),
    ('<h4>Готовые шаблоны:</h4>\n          <p>регламенты, финмодели и чек-листы по СанПиН</p>',
     '<h4>2 документа</h4>\n          <p>Удостоверение о повышении квалификации или диплом о профпереподготовке</p>'),
    ('<h4>Автоматизация и ускорение работы</h4>\n          <p>с ИИ</p>',
     '<h4>9 проектов в портфолио</h4>\n          <p>Отработаете навыки на практике и впечатлите работодателей</p>'),
    ('<h4>Бессрочный доступ</h4>\n          <p>к материалам и бесплатным обновлениям</p>',
     '<h4>Личный куратор на 365 дней</h4>\n          <p>На связи 24/7 — ответит на любой вопрос по курсу</p>'),
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
