// Offline-stöd: sparar appen i telefonen. Byggversion ändras automatiskt vid varje bygge.
const CACHE = 'dryckeslexikon-a64f0069eb';
const FILER = ['./', './index.html', './manifest.webmanifest', './ikon/ikon-180.png', './ikon/ikon-192.png', './ikon/ikon-512.png', './ikon/ikon-32.png', './typsnitt/typsnitt.css', './typsnitt/rubik-latin-ext.woff2', './typsnitt/rubik-latin.woff2', './typsnitt/space-grotesk-latin-ext.woff2', './typsnitt/space-grotesk-latin.woff2'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILER))); self.skipWaiting(); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(k => Promise.all(k.filter(n => n !== CACHE).map(n => caches.delete(n))))); self.clients.claim(); });
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  const url = new URL(e.request.url);
  if (url.origin === location.origin) {
    // Appens egna filer: hämta från nätet och spara i telefonen (så uppdateringar syns).
    // Finns en sparad version väntar appen högst 2 sekunder på nätet och visar annars den sparade,
    // så att den startar snabbt även med dålig täckning. Nätsvaret sparas ändå till nästa gång.
    const natet = fetch(e.request).then(r => { if (r.ok) { const k = r.clone(); return caches.open(CACHE).then(c => c.put(e.request, k)).then(() => r); } return r; });
    e.waitUntil(natet.catch(() => {}));
    e.respondWith(caches.match(e.request).then(sparad => {
      if (!sparad) return natet.catch(() => caches.match('./index.html'));
      return Promise.race([natet.catch(() => sparad), new Promise(ok => setTimeout(() => ok(sparad), 2000))]);
    }));
  }
});
