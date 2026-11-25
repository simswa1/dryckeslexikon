"""Lägger in 18+-spärr och 'Drick ansvarsfullt' i en mall/byggd index.html. Kör: python3 ansvar_patch.py FIL..."""
import sys
CSS = """.slump[hidden]{display:none}
/* 18+ och ansvar */
.ansvar{max-width:860px;margin:-60px auto 0;padding:0 16px calc(28px + env(safe-area-inset-bottom));text-align:center;color:var(--dim);font-size:.82rem}
.ansvar b{display:inline-block;margin-right:6px;padding:1px 7px;border-radius:999px;border:1.5px solid var(--ol);color:var(--ol);font-size:.75rem}
.aldersparr{position:fixed;inset:0;z-index:50;display:grid;place-items:center;padding:24px;background:rgba(14,8,20,.94);backdrop-filter:blur(8px)}
.aldersparr[hidden]{display:none}
.aldersparr .ruta18{max-width:380px;width:100%;text-align:center;background:var(--yta);border:1px solid var(--kant);border-radius:24px;padding:26px 22px;box-shadow:0 20px 50px rgba(0,0,0,.5)}
.aldersparr .tag18{display:inline-grid;place-items:center;width:76px;height:76px;border-radius:50%;border:4px solid var(--ol);color:var(--ol);font:800 1.9rem/1 "Baloo 2",sans-serif;margin-bottom:12px}
.aldersparr h2{font-size:1.6rem;margin:0 0 8px}
.aldersparr p{color:var(--dim);margin:0 0 18px}
.aldersparr button{display:block;width:100%;min-height:52px;border-radius:14px;border:0;font-weight:800;font-size:1.02rem;cursor:pointer;margin-top:10px}
.aldersparr .ja18{background:linear-gradient(150deg,#ffb838,#d9721e);color:#2a1300}
.aldersparr .nej18{background:var(--yta2);color:var(--text)}
.aldersparr .under18{color:var(--text);font-weight:700;margin-top:14px}"""
HTML = """<div class="wrap"><main id="vy"></main></div>
<footer class="ansvar"><b>18+</b>Drick ansvarsfullt. Ni bestämmer själva om, när och hur mycket det ska drickas.</footer>
<div class="aldersparr" id="aldersparr" role="dialog" aria-modal="true" aria-labelledby="a18h" hidden>
  <div class="ruta18">
    <div class="tag18" aria-hidden="true">18+</div>
    <h2 id="a18h">Är du 18 år eller äldre?</h2>
    <p>Dryckeslexikon innehåller lekar där dricka kan ingå och är till för dig som har fyllt 18. Drick ansvarsfullt. Alla lekar går lika bra att köra utan alkohol.</p>
    <button type="button" class="ja18" id="ja18">Ja, jag är 18 år eller äldre</button>
    <button type="button" class="nej18" id="nej18">Nej, jag är under 18</button>
    <p class="under18" id="under18" hidden>Appen är bara för dig som har fyllt 18. Välkommen tillbaka då!</p>
  </div>
</div>"""
JS = """route();
// 18+: frågan visas första gången appen öppnas. Svaret sparas i telefonen.
(() => {
  const NYCKEL = 'dryckeslexikon-18';
  let ok = false; try { ok = localStorage.getItem(NYCKEL) === 'ja'; } catch(e) {}
  const sparr = document.getElementById('aldersparr'); if (!sparr || ok) return;
  sparr.hidden = false; document.getElementById('ja18').focus();
  document.getElementById('ja18').addEventListener('click', () => { try { localStorage.setItem(NYCKEL, 'ja'); } catch(e) {} sparr.hidden = true; });
  document.getElementById('nej18').addEventListener('click', () => { document.getElementById('under18').hidden = false; });
})();"""
for f in sys.argv[1:]:
    s = open(f, encoding='utf-8').read()
    if 'id="aldersparr"' in s: print(f, 'redan klar'); continue
    for a, b in [('.slump[hidden]{display:none}', CSS), ('<div class="wrap"><main id="vy"></main></div>', HTML), ('\nroute();\n', '\n' + JS + '\n')]:
        assert s.count(a) == 1, (f, a); s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s); print(f, 'ok')
