'use strict';
const byId = id => document.getElementById(id);
byId('theme')?.addEventListener('click', event => {
  const active = document.body.classList.toggle('light');
  event.currentTarget.textContent = active ? 'Dark theme' : 'Light theme';
  event.currentTarget.setAttribute('aria-pressed', String(active));
});
byId('size')?.addEventListener('click', event => {
  const active = document.body.classList.toggle('large');
  event.currentTarget.setAttribute('aria-pressed', String(active));
});
byId('expand')?.addEventListener('click', event => {
  const active = event.currentTarget.getAttribute('aria-pressed') !== 'true';
  document.querySelectorAll('details.chapter').forEach(node => { node.open = active; });
  event.currentTarget.setAttribute('aria-pressed', String(active));
  event.currentTarget.textContent = active ? 'Collapse chapters' : 'Expand chapters';
});
byId('search')?.addEventListener('input', event => {
  const query = event.currentTarget.value.toLowerCase().trim();
  let count = 0;
  document.querySelectorAll('details.chapter').forEach(node => {
    node.hidden = !node.textContent.toLowerCase().includes(query);
    if (!node.hidden) count += 1;
  });
  byId('search-count').textContent = `${count} chapters shown`;
});
let printState = [];
window.addEventListener('beforeprint', () => {
  printState = Array.from(document.querySelectorAll('details.chapter'), node => [node, node.open, node.hidden]);
  printState.forEach(([node]) => { node.open = true; node.hidden = false; });
});
window.addEventListener('afterprint', () => {
  printState.forEach(([node, open, hidden]) => { node.open = open; node.hidden = hidden; });
});
