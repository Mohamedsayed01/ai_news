// ══════════════════════════════════════════════════════
//  Dark Mode
// ══════════════════════════════════════════════════════
function toggleDark() {
    const isDark = document.getElementById('htmlRoot').classList.toggle('dark');
    localStorage.setItem('snapnews_dark', isDark);
    syncDarkIcon(isDark);
}
function syncDarkIcon(isDark) {
    document.getElementById('moonIcon')?.classList.toggle('hidden', isDark);
    document.getElementById('sunIcon')?.classList.toggle('hidden', !isDark);
}
// Prevent flash — runs immediately
(function () {
    if (localStorage.getItem('snapnews_dark') === 'true') {
        document.getElementById('htmlRoot').classList.add('dark');
        document.addEventListener('DOMContentLoaded', () => syncDarkIcon(true));
    }
})();

// ══════════════════════════════════════════════════════
//  Summary Modal
// ══════════════════════════════════════════════════════
async function openSummary(btn) {
    const title = btn.dataset.title;
    const url   = btn.dataset.url;
    const desc  = btn.dataset.desc;

    const modal    = document.getElementById('summaryModal');
    const titleEl  = document.getElementById('modalTitle');
    const bodyEl   = document.getElementById('modalSummary');
    const footerEl = document.getElementById('modalFooter');

    titleEl.textContent = title;
    footerEl.classList.add('hidden');
    bodyEl.innerHTML = `
        <div class="flex flex-col items-center justify-center py-16 gap-5">
            <div class="relative w-14 h-14">
                <div class="absolute inset-0 rounded-full border-4 border-blue-100 dark:border-slate-700"></div>
                <div class="absolute inset-0 rounded-full border-4 border-transparent border-t-blue-600 animate-spin"></div>
            </div>
            <div class="text-center">
                <p class="text-sm font-semibold text-gray-700 dark:text-gray-300">Generating AI Briefing</p>
                <p class="text-xs text-gray-400 mt-1">Fetching full article from source…</p>
            </div>
        </div>`;
    modal.classList.remove('hidden');

    try {
        const res  = await fetch('/api/summarize', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ url, description: desc })
        });
        const data = await res.json();

        if (!data.summary) throw new Error('Empty summary');

        const usedFull = data.used_full;

        // badge
        const badge = document.createElement('div');
        badge.className = 'mb-4 flex items-center gap-2';
        const badgeSpan = document.createElement('span');
        badgeSpan.className = 'sn-source-badge' + (usedFull ? ' full' : '');
        badgeSpan.textContent = usedFull ? '✓ Based on full article' : '◷ Based on article preview';
        badge.appendChild(badgeSpan);
        bodyEl.innerHTML = '';
        bodyEl.appendChild(badge);

        // briefing
        const briefingWrap = document.createElement('div');
        briefingWrap.className = 'sn-briefing';
        briefingWrap.innerHTML = data.summary;
        bodyEl.appendChild(briefingWrap);

        // Wire up footer buttons
        document.getElementById('modalReadLink').href = data.original_url;
        document.getElementById('modalShareBtn').onclick = () => shareArticle(data.original_url);
        footerEl.classList.remove('hidden');

    } catch (_) {
        bodyEl.innerHTML = `
            <div class="flex flex-col items-center justify-center py-16 gap-3 text-red-500">
                <svg class="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                          d="M12 9v4m0 4h.01M10.29 3.86L1.82 18a2 2 0 001.71 3h16.94a2 2 0 001.71-3L13.71 3.86a2 2 0 00-3.42 0z"/>
                </svg>
                <p class="text-sm font-semibold">Failed to generate summary</p>
                <p class="text-xs text-gray-400">Please check your API key and try again.</p>
            </div>`;
    }
}

function closeModal() {
    document.getElementById('summaryModal').classList.add('hidden');
}
document.addEventListener('click', e => {
    if (e.target === document.getElementById('summaryModal')) closeModal();
});
document.addEventListener('keydown', e => {
    if (e.key === 'Escape') closeModal();
});

// ══════════════════════════════════════════════════════
//  Share
// ══════════════════════════════════════════════════════
function shareArticle(url) {
    if (navigator.share) {
        navigator.share({ title: 'SnapNews', url }).catch(() => {});
    } else {
        navigator.clipboard.writeText(url).then(() => showToast('🔗 Link copied!'));
    }
}

// ══════════════════════════════════════════════════════
//  Toast
// ══════════════════════════════════════════════════════
function showToast(msg) {
    const t = document.createElement('div');
    t.innerHTML = msg;
    t.className = [
        'fixed bottom-6 left-1/2 -translate-x-1/2 z-[9999]',
        'bg-gray-900 text-white text-sm px-5 py-3 rounded-2xl shadow-xl',
        'transition-opacity duration-300 pointer-events-none'
    ].join(' ');
    document.body.appendChild(t);
    setTimeout(() => { t.style.opacity = '0'; }, 2000);
    setTimeout(() => t.remove(), 2400);
}

// ══════════════════════════════════════════════════════
//  Save Articles
// ══════════════════════════════════════════════════════
function getSaved() {
    try { return JSON.parse(localStorage.getItem('snapnews_saved') || '[]'); }
    catch { return []; }
}
function setSaved(list) {
    localStorage.setItem('snapnews_saved', JSON.stringify(list));
    updateSavedBadge();
    renderSavedPanel();
}
function saveArticle(btn) {
    const { title, url, desc, cat } = btn.dataset;
    const saved = getSaved();
    if (saved.find(a => a.url === url)) { showToast('Already saved!'); return; }
    saved.unshift({ title, url, desc, category: cat, savedAt: new Date().toLocaleDateString() });
    setSaved(saved);
    const orig = btn.innerHTML;
    btn.innerHTML = '✅';
    setTimeout(() => btn.innerHTML = orig, 1800);
    showToast('📌 Article saved!');
}
function removeSaved(encodedUrl) {
    const url = decodeURIComponent(encodedUrl);
    setSaved(getSaved().filter(a => a.url !== url));
}
function clearSaved() {
    if (confirm('Clear all saved articles?')) setSaved([]);
}
function updateSavedBadge() {
    const count = getSaved().length;
    const badge = document.getElementById('savedBadge');
    if (!badge) return;
    badge.textContent = count > 9 ? '9+' : count;
    badge.style.display = count > 0 ? 'flex' : 'none';
}
function renderSavedPanel() {
    const list = document.getElementById('savedList');
    if (!list) return;
    const saved = getSaved();
    if (!saved.length) {
        list.innerHTML = `
            <div class="flex flex-col items-center justify-center h-full py-20 text-center gap-3 text-gray-400">
                <svg class="w-10 h-10 opacity-30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5"
                          d="M5 5a2 2 0 012-2h10a2 2 0 012 2v16l-7-3.5L5 21V5z"/>
                </svg>
                <p class="text-sm">No saved articles yet</p>
                <p class="text-xs text-gray-300">Click 🔖 on any article to save it</p>
            </div>`;
        return;
    }
    list.innerHTML = saved.map(a => `
        <div class="bg-gray-50 dark:bg-slate-800 border border-gray-100 dark:border-slate-700 rounded-2xl p-4">
            <span class="text-[10px] font-bold uppercase tracking-wider text-blue-500">${a.category}</span>
            <p class="font-semibold text-sm mt-1.5 line-clamp-2 text-gray-900 dark:text-white leading-snug">${a.title}</p>
            <p class="text-[11px] text-gray-400 mt-1">${a.savedAt}</p>
            <div class="flex gap-2 mt-3">
                <a href="${a.url}" target="_blank" rel="noopener"
                   class="flex-1 text-center text-xs py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-xl transition font-semibold">
                    Read
                </a>
                <button onclick="removeSaved('${encodeURIComponent(a.url)}')"
                        class="px-3 text-xs py-2 border border-gray-200 dark:border-slate-600 rounded-xl hover:bg-red-50 dark:hover:bg-red-900/20 text-red-500 transition font-semibold">
                    Remove
                </button>
            </div>
        </div>`).join('');
}

// ══════════════════════════════════════════════════════
//  Saved Panel
// ══════════════════════════════════════════════════════
function toggleSavedPanel() {
    const panel   = document.getElementById('savedPanel');
    const overlay = document.getElementById('savedOverlay');
    const isOpen  = !panel.classList.contains('translate-x-full');
    panel.classList.toggle('translate-x-full', isOpen);
    overlay.classList.toggle('hidden', isOpen);
    if (!isOpen) renderSavedPanel();
}

// ══════════════════════════════════════════════════════
//  Init
// ══════════════════════════════════════════════════════
document.addEventListener('DOMContentLoaded', () => {
    updateSavedBadge();
    renderSavedPanel();
});
