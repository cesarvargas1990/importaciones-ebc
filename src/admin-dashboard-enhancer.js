function findAdminButton(label) {
  return [...document.querySelectorAll('.admin-sidebar button')].find(button => button.textContent.trim().startsWith(label));
}

function openDashboardDestination(index) {
  if (index === 0) {
    findAdminButton('Categorías')?.click();
    return;
  }

  const products = findAdminButton('Productos');
  products?.click();

  if (index === 2) {
    window.setTimeout(() => {
      [...document.querySelectorAll('.admin-featured-filter button')]
        .find(button => button.textContent.trim() === 'Destacados')
        ?.click();
    }, 0);
  }
}

function enhanceDashboardCards() {
  const cards = [...document.querySelectorAll('.admin-stats > div')];
  if (cards.length !== 3) return;

  cards.forEach((card, index) => {
    if (card.dataset.directAccess === 'true') return;
    card.dataset.directAccess = 'true';
    card.setAttribute('role', 'link');
    card.setAttribute('tabindex', '0');
    card.setAttribute('aria-label', ['Ver categorías activas', 'Ver productos', 'Ver productos destacados'][index]);
    card.addEventListener('click', () => openDashboardDestination(index));
    card.addEventListener('keydown', event => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        openDashboardDestination(index);
      }
    });
  });
}

if (typeof document !== 'undefined') {
  const observer = new MutationObserver(enhanceDashboardCards);
  observer.observe(document.body, { childList: true, subtree: true });
  enhanceDashboardCards();
}
