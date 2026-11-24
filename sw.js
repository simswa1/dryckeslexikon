// Offline-stöd: sparar appen i telefonen. Byggversion ändras automatiskt vid varje bygge.
const CACHE = 'dryckeslexikon-4cee3a53ed';
const FILER = ['./', './index.html', './manifest.webmanifest', './ikon/ikon-180.png', './ikon/ikon-192.png', './ikon/ikon-512.png', './ikon/ikon-32.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILER))); self.skipWaiting(); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(k => Promise.all(k.filter(n => n !== CACHE).map(n => caches.delete(n))))); self.clients.claim(); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin === location.origin) {
    // Appens egna filer: nätet först (så uppdateringar syns), cache om man är offline.
    e.respondWith(fetch(e.request).then(r => { const k = r.clone(); caches.open(CACHE).then(c => c.put(e.request, k)); return r; })
      .catch(() => caches.match(e.request).then(r => r || caches.match('./index.html'))));
  } else if (/fonts\.(googleapis|gstatic)\.com$/.test(url.hostname)) {
    // Typsnitt: cache först.
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(n => { const k = n.clone(); caches.open(CACHE).then(c => c.put(e.request, k)); return n; })));
  }
});
