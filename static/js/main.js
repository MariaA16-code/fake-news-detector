// ── PREDICT ──
function predict() {
  const text = document.getElementById('newsText').value.trim();

  if (!text) {
    alert('Please paste a news article first.');
    return;
  }

  if (text.split(' ').length < 10) {
    alert('Please enter a longer text for accurate results.');
    return;
  }

  fetch('/predict', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ text })
  })
  .then(res => res.json())
  .then(data => {
    showResult(data);
  });
}

// ── SHOW RESULT ──
function showResult(data) {
  const card = document.getElementById('resultCard');
  card.style.display = 'block';

  // Badge
  const badge = document.getElementById('resultBadge');
  badge.textContent = data.label === 'Real' ? '✅ Real News' : '❌ Fake News';
  badge.className = 'result-badge';
  badge.classList.add(data.label === 'Real' ? 'badge-real' : 'badge-fake');

  // Confidence
  document.getElementById('confidence').textContent = data.confidence + '%';

  // Bars
  document.getElementById('realBar').style.width = data.real_prob + '%';
  document.getElementById('fakeBar').style.width = data.fake_prob + '%';
  document.getElementById('realVal').textContent  = data.real_prob + '%';
  document.getElementById('fakeVal').textContent  = data.fake_prob + '%';

  // Scroll to result
  card.scrollIntoView({ behavior: 'smooth' });
}

// ── CLEAR ──
function clearAll() {
  document.getElementById('newsText').value = '';
  document.getElementById('resultCard').style.display = 'none';
  document.getElementById('resultBadge').textContent  = '';
  document.getElementById('realBar').style.width = '0%';
  document.getElementById('fakeBar').style.width = '0%';
}