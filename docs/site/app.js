'use strict';
const english = document.documentElement.lang === 'en';
const form = document.querySelector('#quota-form');
function computeQuota() {
  const fields = ['installed', 'available', 'reserve', 'percent'].map(id => document.getElementById(id));
  const [total, available, reserve, percent] = fields.map(el => el.valueAsNumber);
  const valid = fields.every(el => el.checkValidity() && el.value.trim() !== '') && available <= total;
  document.getElementById('quota-error').textContent = valid ? '' : (english ? 'Enter valid values. Available memory cannot exceed installed memory.' : 'Saisis des valeurs valides. La mémoire disponible ne peut pas dépasser la mémoire installée.');
  document.getElementById('quota-value').textContent = valid ? new Intl.NumberFormat(english ? 'en-GB' : 'fr-BE', {maximumFractionDigits:2}).format(Math.max(0, Math.min(total * percent / 100, available - reserve))) + (english ? ' GB' : ' Go') : '—';
}
form.addEventListener('input', computeQuota);
form.addEventListener('submit', event => event.preventDefault());
computeQuota();
const search = document.getElementById('source-search');
const records = [...document.querySelectorAll('.source')];
const normalize = value => value.normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
function filterSources(){
  const query = normalize(search.value.trim());
  let count = 0;
  for(const record of records){record.hidden = !normalize(record.textContent).includes(query); if(!record.hidden) count++;}
  document.querySelectorAll('.source-group').forEach(group => {group.hidden = ![...group.querySelectorAll('.source')].some(r => !r.hidden);if(query && !group.hidden) group.open = true;});
  document.getElementById('source-count').textContent = english ? `${count} / ${records.length} entries` : `${count} / ${records.length} entrées`;
}
search.addEventListener('input', filterSources);
function revealReference(){
  const target = document.getElementById(location.hash.slice(1));
  if(!target || !target.classList.contains('source')) return;
  search.value='';filterSources();
  const parent=target.closest('details');if(parent) parent.open=true;
  target.scrollIntoView({block:'start'});
}
window.addEventListener('hashchange', revealReference);
filterSources();revealReference();
