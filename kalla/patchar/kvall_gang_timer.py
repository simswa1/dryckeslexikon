"""Lägger till Gänget (namn, vems tur), Kvällens lista och Timer i mall.html (2026-11-25).
Kör en gång: python3 patchar/kvall_gang_timer.py  (från app/). CSS och JS läses från patchar/kvall_gang_timer_*.txt."""
import pathlib, sys
här = pathlib.Path(__file__).resolve().parent
mf = här.parent / "mall.html"
m = mf.read_text(encoding="utf-8")
if "inforKvallen" in m: sys.exit("Redan inlagt.")
def byt(gammal, ny, antal=1):
    global m
    n = m.count(gammal)
    if n != antal: sys.exit(f"Hittade {n} st (väntade {antal}): {gammal[:80]!r}")
    m = m.replace(gammal, ny)
css = (här / "kvall_gang_timer_css.txt").read_text(encoding="utf-8")
js = (här / "kvall_gang_timer_js.txt").read_text(encoding="utf-8")
byt("</style>", css + "</style>")
byt("$('#slump').addEventListener('click', slumpa);", js + "$('#slump').addEventListener('click', slumpa);")
# Startsidan: två knappar under de stora
byt("<p>${T('Slå 1–10 tärningar.')}</p></a>\n  </nav>`;", "<p>${T('Slå 1–10 tärningar.')}</p></a>\n  </nav>\n  ${inforKvallen()}`;")
# Leksidan: + Kvällen, vems tur, timer, bläddra i kvällens lista
byt("""<h1>${esc(F(l,'namn'))}</h1><button type="button" class="favknapp ${FAV.has(l.id)?'pa':''}" data-fav="${esc(l.id)}" aria-pressed="${FAV.has(l.id)}">${FAV.has(l.id)?T('♥ Sparad'):T('♡ Spara')}</button></div></div>""",
    """<h1>${esc(F(l,'namn'))}</h1><div class="lekknappar"><button type="button" class="favknapp ${FAV.has(l.id)?'pa':''}" data-fav="${esc(l.id)}" aria-pressed="${FAV.has(l.id)}">${FAV.has(l.id)?T('♥ Sparad'):T('♡ Spara')}</button><button type="button" class="favknapp kvknapp ${KV.includes(l.id)?'pa':''}" data-kv="${esc(l.id)}" aria-pressed="${KV.includes(l.id)}">${KV.includes(l.id)?T('✓ Kvällen'):T('+ Kvällen')}</button></div></div></div>""")
byt("""      <div><small>${T('Behövs')}</small><b><a href="#grupp-${l._grupp}">${esc(T(gruppAv(l._grupp).namn))}</a></b></div>
    </div>""", """      <div><small>${T('Behövs')}</small><b><a href="#grupp-${l._grupp}">${esc(T(gruppAv(l._grupp).namn))}</a></b></div>
    </div>
    ${turHtml()}""")
byt("    ${lst(T('Regler'), F(l,'regler'), true)}\n", "    ${lst(T('Regler'), F(l,'regler'), true)}\n    ${timerFor_lek(l)}\n")
byt("""    ${F(l,'taggar') && F(l,'taggar').length ? `<div class="taggar">${F(l,'taggar').map(t=>`<span>#${esc(t)}</span>`).join('')}</div>` : ''}
    """, """    ${F(l,'taggar') && F(l,'taggar').length ? `<div class="taggar">${F(l,'taggar').map(t=>`<span>#${esc(t)}</span>`).join('')}</div>` : ''}
    ${kvBar(l)}""")
# Navigering: kvällens lista
byt("  if (SP.id) stangSpel();\n  const lek = h.match(/^lek-(.+)$/);",
    "  if (SP.id) stangSpel();\n  const lek = h.match(/^lek-(.+)$/);\n  if (!lek) document.body.classList.remove('medkv');\n  if (lek && forraHash === 'kvallen') KVAKTIV = true;\n  if (!h || LISTOR[h]) KVAKTIV = false;")
byt("else if (lek){ $('#tbk').href = senasteLista ? '#'+senasteLista : '#'; lekSida(lek[1]); window.scrollTo(0,0); }",
    "else if (lek){ $('#tbk').href = KVAKTIV && KV.includes(lek[1]) ? '#kvallen' : senasteLista ? '#'+senasteLista : '#'; lekSida(lek[1]); window.scrollTo(0,0); }")
byt("else if (VERKTYG[h]){ $('#tbk').href = forraHash && forraHash !== h && !VERKTYG[forraHash] ? '#'+forraHash : '#'; VERKTYG[h](); window.scrollTo(0,0); }",
    "else if (VERKTYG[h]){ $('#tbk').href = h !== 'kvallen' && forraHash && forraHash !== h && !VERKTYG[forraHash] ? '#'+forraHash : '#'; VERKTYG[h](); window.scrollTo(0,0); }")
# Spelläget: visa vem som läser upp frågan, i gängets turordning
byt("  SP.ko = ko.ordning; SP.pos = Math.min(ko.pos, SP.ko.length - 1); SP.niva = niva; SP.lage = 'spel';",
    "  SP.ko = ko.ordning; SP.pos = Math.min(ko.pos, SP.ko.length - 1); SP.niva = niva; SP.lage = 'spel'; SP.tur0 = GANG.tur - SP.pos;")
byt("""`<div class="frkort n-${n} ${anim||''}" id="frkort" data-spel="nasta">""",
    """`<div class="frkort n-${n} ${anim||''}" id="frkort" data-spel="nasta">${gangN() ? `<div class="vem">${T('{n} läser upp', {n: esc(GANG.namn[(((SP.tur0 + SP.pos) % gangN()) + gangN()) % gangN()])})}</div>` : ''}""")
byt("function sparaPos(){ const k = LEKKO[lk(SP.id)]; if (k){ k.pos = SP.pos; skrivLS('dryckeslexikon-lekko', LEKKO); } }",
    "function sparaPos(){ const k = LEKKO[lk(SP.id)]; if (k){ k.pos = SP.pos; skrivLS('dryckeslexikon-lekko', LEKKO); } if (gangN() && SP.tur0 != null){ GANG.tur = (((SP.tur0 + SP.pos) % gangN()) + gangN()) % gangN(); sparaGang(); } }")
# Impostor: gängets namn i stället för Spelare 1, 2, 3 ...
byt("const maxImp = n => Math.max(1, Math.min(3, Math.floor((n - 1) / 2)));",
    "const maxImp = n => Math.max(1, Math.min(3, Math.floor((n - 1) / 2)));\nconst imMedNamn = () => IMI.medNamn !== false && GANG.namn.length >= 3;\nconst imAntal = () => imMedNamn() ? Math.min(20, GANG.namn.length) : IMI.spelare;\nconst imSp = (i, liten) => IM.namn ? esc(IM.namn[i]) : T(liten ? 'spelare {i}' : 'Spelare {i}', {i: i + 1});")
byt("function imStart(){\n  IMI.imp = Math.min(IMI.imp, maxImp(IMI.spelare));",
    "function imStart(){\n  const N = imAntal();\n  IMI.imp = Math.min(IMI.imp, maxImp(N));")
byt("  const imps = new Set(); while (imps.size < IMI.imp) imps.add(Math.floor(Math.random() * IMI.spelare));\n  IM = {fas:'titta', i:0, visar:false, kat, ord, imps, borjar: Math.floor(Math.random() * IMI.spelare)};",
    "  const imps = new Set(); while (imps.size < IMI.imp) imps.add(Math.floor(Math.random() * N));\n  IM = {fas:'titta', i:0, visar:false, kat, ord, imps, n: N, namn: imMedNamn() ? GANG.namn.slice(0, N) : null, borjar: Math.floor(Math.random() * N)};")
byt("  const v = $('#vy'), n = IMI.spelare;\n  if (IM.fas === 'val'){",
    "  const v = $('#vy'), n = IM.fas === 'val' ? imAntal() : IM.n;\n  if (IM.fas === 'val'){")
byt("""      <div class="antalrad"><span>${T('Spelare')}</span><div class="stepper">
        <button type="button" data-im="sp-" aria-label="${T('Färre spelare')}" ${n<=3?'disabled':''}>−</button><output aria-live="polite">${n}</output>
        <button type="button" data-im="sp+" aria-label="${T('Fler spelare')}" ${n>=20?'disabled':''}>+</button></div></div>""",
    """      ${GANG.namn.length >= 3 ? `<button type="button" class="imvaxla" data-im="mednamn" aria-pressed="${imMedNamn()}" style="margin:0 0 14px"><i></i><span>${T('Använd gängets namn')}<small>${esc(GANG.namn.slice(0, 20).join(', '))}</small></span></button>` : `<p style="margin:-6px 0 10px"><a class="turtom" href="#ganget">${T('👥 Skriv in gänget så visas namnen i stället för Spelare 1, 2, 3')}</a></p>`}
      ${imMedNamn() ? '' : `<div class="antalrad"><span>${T('Spelare')}</span><div class="stepper">
        <button type="button" data-im="sp-" aria-label="${T('Färre spelare')}" ${n<=3?'disabled':''}>−</button><output aria-live="polite">${n}</output>
        <button type="button" data-im="sp+" aria-label="${T('Fler spelare')}" ${n>=20?'disabled':''}>+</button></div></div>`}""")
byt("<span class=\"num\">${T('Spelare {i}', {i: IM.i + 1})}</span>", "<span class=\"num\">${imSp(IM.i)}</span>")
byt("${sista ? T('Göm. Alla har sett sitt ord') : T('Göm och lämna till spelare {i}', {i: IM.i + 2})}",
    "${sista ? T('Göm. Alla har sett sitt ord') : IM.namn ? T('Göm och lämna till {n}', {n: imSp(IM.i + 1)}) : T('Göm och lämna till spelare {i}', {i: IM.i + 2})}")
byt("<span class=\"etikett\">${T('Spelare {i} börjar', {i: IM.borjar + 1})}</span>",
    "<span class=\"etikett\">${IM.namn ? T('{n} börjar', {n: imSp(IM.borjar)}) : T('Spelare {i} börjar', {i: IM.borjar + 1})}</span>")
byt("const lista = [...IM.imps].sort((a,b) => a-b).map(x => T('spelare {i}', {i: x + 1}));",
    "const lista = [...IM.imps].sort((a,b) => a-b).map(x => imSp(x, true));")
byt("${esc(lista.join(T(' och ')).replace(/^\\S/, c => c.toUpperCase()))}", "${lista.join(T(' och ')).replace(/^\\S/, c => c.toUpperCase())}")
byt("else if (a === 'gom'){ IM.visar = false; IM.gomd = Date.now(); if (IM.i < IMI.spelare - 1) IM.i++; else IM.fas = 'prata'; window.scrollTo(0,0); }",
    "else if (a === 'gom'){ IM.visar = false; IM.gomd = Date.now(); if (IM.i < IM.n - 1) IM.i++; else IM.fas = 'prata'; window.scrollTo(0,0); }\n  else if (a === 'mednamn'){ IMI.medNamn = !imMedNamn(); sparaIMI(); }")
byt("IMI = {spelare: Math.min(20, Math.max(3, IMI.spelare|0 || 5)), imp: Math.max(1, IMI.imp|0 || 1), visaKat: IMI.visaKat !== false,",
    "IMI = {spelare: Math.min(20, Math.max(3, IMI.spelare|0 || 5)), imp: Math.max(1, IMI.imp|0 || 1), visaKat: IMI.visaKat !== false, medNamn: IMI.medNamn !== false,")
# Körkortet: den som rangordnar går laget runt i gänget
byt("  KK = {fas:'hemlig', visar: !!byt, ratt, alt: blanda(falska.concat(ratt)), gissat: null};",
    "  const vem = byt ? KK.vem : turNamn(); if (!byt) flyttaTur(1);\n  KK = {fas:'hemlig', visar: !!byt, ratt, alt: blanda(falska.concat(ratt)), gissat: null, vem};")
byt("""<span class="num" style="font-size:clamp(2rem,10vw,3rem)">${T('Den som rangordnar')}</span>""",
    """<span class="num" style="font-size:clamp(2rem,10vw,3rem)">${KK.vem ? esc(KK.vem) : T('Den som rangordnar')}</span>""")
byt("${T('Lämna telefonen till nästa spelare')}", "${gangN() ? T('Lämna telefonen till {n}', {n: esc(turNamn())}) : T('Lämna telefonen till nästa spelare')}")
mf.write_text(m, encoding="utf-8")
print("Klart: gänget, kvällens lista och timer inlagda.")
