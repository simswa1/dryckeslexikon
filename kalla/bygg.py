"""Bygger appen från mall.html + ../lekar/lekar.json (+ svarighet.json).
Kör: python3 bygg.py   (från mappen app/)
Resultat:
  index.html  – en fristående fil (det som publiceras som Claude-artifact)
  webb/       – installerbar webbapp (PWA) med ikon, manifest och offline-stöd.
                Ladda upp hela mappen till valfri webbhotell (GitHub Pages, Netlify ...).
"""
import json, pathlib, shutil, hashlib
här = pathlib.Path(__file__).resolve().parent
lekar = json.loads((här.parent / "lekar" / "lekar.json").read_text(encoding="utf-8"))
svf = här.parent / "lekar" / "svarighet.json"
svar = json.loads(svf.read_text(encoding="utf-8")) if svf.exists() else {}
for l in lekar:
    if not l.get("svarighet") and svar.get(l["id"]): l["svarighet"] = svar[l["id"]]
pf = här.parent / "lekar" / "popularitet.json"
pop = json.loads(pf.read_text(encoding="utf-8")) if pf.exists() else {}
for l in lekar:
    if l.get("popularitet") is None: l["popularitet"] = pop.get(l["id"], 50)
saknar = [l["id"] for l in lekar if not l.get("svarighet")]
if saknar: print("Saknar svårighetsgrad:", ", ".join(saknar))
ids = [l["id"] for l in lekar]
dubbletter = {i for i in ids if ids.count(i) > 1}
if dubbletter: raise SystemExit(f"Dubbla id: {dubbletter}")
data = json.dumps(lekar, ensure_ascii=False).replace("</", "<\\/")
ff = här.parent / "lekar" / "fragor.json"
fragor = json.loads(ff.read_text(encoding="utf-8")) if ff.exists() else {}
okanda = [k for k in fragor if k not in ids]
if okanda: raise SystemExit(f"Frågor till okänd lek: {okanda}")
for k, v in fragor.items():
    v["nivaer"] = {n: [str(q).strip() for q in v.get("nivaer", {}).get(n, []) if str(q).strip()] for n in ("Lugn", "Lagom", "Het")}
    print(f"Frågor {k}: " + ", ".join(f"{n} {len(q)}" for n, q in v["nivaer"].items()))
# En lek kan låna en annan leks frågor: "fragor_fran" (lek-id) och ev. "spel_instruktion" i lekar.json.
for l in lekar:
    kalla = l.get("fragor_fran")
    if not kalla: continue
    if kalla not in fragor: raise SystemExit(f"{l['id']}: fragor_fran pekar på {kalla} som saknar frågor")
    fragor[l["id"]] = dict(fragor[kalla], **({"instruktion": l["spel_instruktion"]} if l.get("spel_instruktion") else {}))
    print(f"Frågor {l['id']}: lånar från {kalla}")
fragdata = json.dumps(fragor, ensure_ascii=False).replace("</", "<\\/")
# Impostor: ordbank per kategori (källa: fliken "Impostor" i Google-arket "Dryckeslexikon – frågebank")
imf = här.parent / "lekar" / "impostor.json"
imp = json.loads(imf.read_text(encoding="utf-8")) if imf.exists() else {"kategorier": {}}
imp["kategorier"] = {k: list(dict.fromkeys(str(o).strip() for o in v if str(o).strip())) for k, v in imp.get("kategorier", {}).items()}
imp["kategorier"] = {k: v for k, v in imp["kategorier"].items() if v}
print("Impostor: " + ", ".join(f"{k} {len(v)}" for k, v in imp["kategorier"].items()))
impdata = json.dumps(imp, ensure_ascii=False).replace("</", "<\\/")
# Körkortet: påståenden per nivå (källa: fliken "Körkortet" i Google-arket "Dryckeslexikon – frågebank")
kkf = här.parent / "lekar" / "korkortet.json"
kk = json.loads(kkf.read_text(encoding="utf-8")) if kkf.exists() else {"nivaer": {}}
kk["nivaer"] = {n: list(dict.fromkeys(str(q).strip() for q in kk.get("nivaer", {}).get(n, []) if str(q).strip())) for n in ("Lugn", "Lagom", "Het")}
print("Körkortet: " + ", ".join(f"{n} {len(q)}" for n, q in kk["nivaer"].items()))
ktf = här.parent / "lekar" / "korkortet_teman.json"
if ktf.exists():
    kt = json.loads(ktf.read_text(encoding="utf-8"))
    allakk = {q for v in kk["nivaer"].values() for q in v}
    kk["teman"] = {q: t for q, t in kt.get("teman", {}).items() if q in allakk}
    kk["grupper"] = kt.get("grupper", {})
    utan = len(allakk) - len(kk["teman"])
    if utan: print(f"Körkortet: {utan} påståenden saknar tema (jämförs på ord)")
kkdata = json.dumps(kk, ensure_ascii=False).replace("</", "<\\/")
bf = här / "bilder" / "lekbilder.json"
bilder = json.loads(bf.read_text(encoding="utf-8")) if bf.exists() else {}
utan_bild = [i for i in ids if i not in bilder]
if utan_bild: print("Saknar bild (gruppens ikon visas):", ", ".join(utan_bild))
symboler = "\n".join(f'  <symbol id="lb-{i}" viewBox="0 0 100 100">{bilder[i]}</symbol>' for i in ids if i in bilder)
mall = (här / "mall.html").read_text(encoding="utf-8").replace("__LEKAR__", data).replace("__FRAGOR__", fragdata).replace("__IMPOSTOR__", impdata).replace("__KORKORTET__", kkdata).replace("<!--LEKBILDER-->", symboler)

# 1) Fristående fil (artifact)
(här / "index.html").write_text(mall.replace("<!--PWA-->", "").replace("/*PWA-SW*/", ""), encoding="utf-8")

# 2) Installerbar webbapp
webb = här / "webb"
if webb.exists(): shutil.rmtree(webb)
(webb / "ikon").mkdir(parents=True)
for n in (1024, 512, 192, 180, 32):
    shutil.copy(här / "ikon" / f"ikon-{n}.png", webb / "ikon" / f"ikon-{n}.png")
pwa_head = """<link rel="manifest" href="manifest.webmanifest">
<link rel="icon" type="image/png" sizes="32x32" href="ikon/ikon-32.png">
<link rel="apple-touch-icon" href="ikon/ikon-180.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
<meta name="apple-mobile-web-app-title" content="Dryckeslexikon">"""
pwa_sw = "if ('serviceWorker' in navigator) { try { navigator.serviceWorker.register('sw.js').catch(()=>{}); } catch(e) {} }"
html = mall.replace("<!--PWA-->", pwa_head).replace("/*PWA-SW*/", pwa_sw)
(webb / "index.html").write_text(html, encoding="utf-8")
manifest = {
  "name": "Dryckeslexikon", "short_name": "Dryckeslexikon", "lang": "sv",
  "description": "Idéer och regler för festlekar. Sällskapet bestämmer själv om, när och hur mycket det ska drickas.",
  "start_url": "./", "scope": "./", "display": "standalone",
  "background_color": "#1a1024", "theme_color": "#1a1024",
  "icons": [{"src": f"ikon/ikon-{n}.png", "sizes": f"{n}x{n}", "type": "image/png", "purpose": "any"} for n in (192, 512, 1024)]
         + [{"src": "ikon/ikon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable"}]
}
(webb / "manifest.webmanifest").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
version = hashlib.sha1(html.encode()).hexdigest()[:10]
(webb / "sw.js").write_text("""// Offline-stöd: sparar appen i telefonen. Byggversion ändras automatiskt vid varje bygge.
const CACHE = 'dryckeslexikon-%s';
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
  } else if (/fonts\\.(googleapis|gstatic)\\.com$/.test(url.hostname)) {
    // Typsnitt: cache först.
    e.respondWith(caches.match(e.request).then(r => r || fetch(e.request).then(n => { const k = n.clone(); caches.open(CACHE).then(c => c.put(e.request, k)); return n; })));
  }
});
""" % version, encoding="utf-8")
print(f"Byggde index.html och webb/ med {len(lekar)} lekar")
