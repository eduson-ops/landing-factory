/* Eduson blocks — общая интерактивность через делегирование событий.
   Подключается раз в каждый блок: <script src="../../js/components.js" defer></script>
   В собранном index.html — раз в <head>. Дубликаты тегов идемпотентны. */

(() => {
  if (window.__edusonComponentsLoaded) return;
  window.__edusonComponentsLoaded = true;

  // Аккордеон
  document.addEventListener('click', (e) => {
    const head = e.target.closest('[data-accordion-head]');
    if (!head) return;
    const item = head.closest('[data-accordion-item]');
    if (!item) return;
    const accordion = item.closest('[data-accordion]');
    if (accordion && accordion.dataset.accordion === 'single') {
      accordion.querySelectorAll('[data-accordion-item].is-open').forEach((sib) => {
        if (sib !== item) sib.classList.remove('is-open');
      });
    }
    item.classList.toggle('is-open');
  });

  // Слайдер: prev/next через горизонтальный scroll-snap
  document.addEventListener('click', (e) => {
    const arrow = e.target.closest('[data-slider-arrow]');
    if (!arrow) return;
    const slider = arrow.closest('[data-slider]');
    if (!slider) return;
    const track = slider.querySelector('[data-slider-track]');
    if (!track) return;
    const dir = arrow.dataset.sliderArrow === 'next' ? 1 : -1;
    const step = track.querySelector('[data-slider-item]')?.getBoundingClientRect().width || 280;
    track.scrollBy({ left: dir * (step + 16), behavior: 'smooth' });
  });

  // Форма заявки — заглушка submit
  document.addEventListener('submit', (e) => {
    const form = e.target.closest('[data-cta-form]');
    if (!form) return;
    e.preventDefault();
    const ok = form.querySelector('[data-cta-success]');
    if (ok) ok.hidden = false;
    form.querySelectorAll('input, button').forEach((el) => (el.disabled = true));
  });
})();
