# Dryckeslexikon (tidigare Lekbiblioteket)
- Lekarna ligger i `../lekar/lekar.json` (genereras av `../lekar/bygg_lekar.py`). Svårighetsgrad i `../lekar/svarighet.json`.
- Fält: id (unikt, kebab-case, a–z), namn, kategori, kort, spelare {min,max|null}, tid, alkohol (används inte i appen), behover[], regler[], varianter[], taggar[], osaker + osaker_kommentar, valfritt svarighet och grupp.
- Bygg: `python3 bygg.py` här. Skapar
  - `index.html`: fristående fil, publicerad som Claude-artifact: https://claude.ai/artifact/XZrq4dSZLanEocCMTtSHry
  - `webb/`: installerbar webbapp (manifest, offline via sw.js, ikoner). Ladda upp hela mappen till ett webbhotell med https. Samma innehåll finns zippat i `dryckeslexikon-webb.zip`.
- Ikon: `ikon/ikon.svg` (källa) och PNG i 1024/512/192/180/32. 1024 är App Store-storleken.
- Favoriter sparas i telefonens webbläsare (localStorage), inget skickas någonstans.
- Bild per lek: ritas i `bilder/rita_lekbilder.py` (en rad per lek-id) -> `bilder/lekbilder.json`. Kör skriptet och sedan bygg.py. Saknas bild visas gruppens ikon.
