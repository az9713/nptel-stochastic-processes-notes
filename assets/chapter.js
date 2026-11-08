'use strict';
const chapterButton = id => document.getElementById(id);
// Approval is presentation state; preserve the reviewed scientific source body.
if (document.body.dataset.pilotApproved === 'true') {
  const eyebrow = document.querySelector('article .eyebrow');
  if (eyebrow) eyebrow.textContent = eyebrow.textContent.replace(' · Pilot for author review', '');
}
document.querySelectorAll('figure img').forEach(img => {
  const link = document.createElement('a');
  link.href = img.getAttribute('src');
  link.target = '_blank';
  link.rel = 'noopener';
  link.className = 'figure-link';
  link.setAttribute('aria-label', 'Open figure at full size');
  link.title = 'Open the original figure to zoom';
  img.before(link);
  link.append(img);
});
if (window.matchMedia('(max-width: 900px)').matches) {
  const contents = chapterButton('toc-disclosure');
  if (contents) contents.open = false;
}
chapterButton('theme')?.addEventListener('click', event => {
  const active = document.body.classList.toggle('light');
  event.currentTarget.textContent = active ? 'Dark theme' : 'Light theme';
  event.currentTarget.setAttribute('aria-pressed', String(active));
});
chapterButton('size')?.addEventListener('click', event => {
  event.currentTarget.setAttribute('aria-pressed', String(document.body.classList.toggle('large')));
});
chapterButton('solutions')?.addEventListener('click', event => {
  const active = event.currentTarget.getAttribute('aria-pressed') !== 'true';
  document.querySelectorAll('details.solution').forEach(node => { node.open = active; });
  event.currentTarget.setAttribute('aria-pressed', String(active));
  event.currentTarget.textContent = active ? 'Hide solutions' : 'Show solutions';
});
chapterButton('print')?.addEventListener('click', () => window.print());
document.querySelectorAll('.copybtn').forEach(button => {
  button.addEventListener('click', async () => {
    const code = button.parentElement.querySelector('code').textContent;
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(code);
      } else {
        const field = document.createElement('textarea');
        field.value = code;
        document.body.append(field);
        field.select();
        const copied = document.execCommand('copy');
        field.remove();
        if (!copied) throw new Error('clipboard unavailable');
      }
      button.textContent = 'Copied!';
    } catch {
      button.textContent = 'Select and copy code';
    }
    setTimeout(() => { button.textContent = 'Copy'; }, 1500);
  });
});
let savedSolutions = null;
window.addEventListener('beforeprint', () => {
  if (savedSolutions !== null) return;
  savedSolutions = Array.from(document.querySelectorAll('details.solution'), n => [n, n.open]);
  savedSolutions.forEach(([node]) => { node.open = true; });
});
window.addEventListener('afterprint', () => {
  if (savedSolutions === null) return;
  savedSolutions.forEach(([node, open]) => { node.open = open; });
  savedSolutions = null;
});
