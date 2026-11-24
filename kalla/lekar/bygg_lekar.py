import json, re, sys

L = []

def lek(id, namn, kategori, kort, smin, smax, tid, alkohol, behover, regler,
        varianter=None, taggar=None, osaker=False, kommentar=None):
    d = {"id": id, "namn": namn, "kategori": kategori, "kort": kort,
         "spelare": {"min": smin, "max": smax}, "tid": tid, "alkohol": alkohol,
         "behover": behover, "regler": regler}
    if varianter: d["varianter"] = varianter
    if taggar: d["taggar"] = taggar
    d["osaker"] = osaker
    if kommentar: d["osaker_kommentar"] = kommentar
    L.append(d)

# ---------------- KORTLEKAR ----------------
lek("kungen-i-ringen", "Kungen i ringen (Ring of Fire)", "Kortlek",
    "Kort dras ett i taget runt ett glas i mitten, och varje kortvalör har sin egen regel.",
    3, 12, "30–60 min", True, ["Kortlek", "Ett stort glas eller en mugg", "Dricka"],
    ["Ställ ett tomt glas i mitten och lägg korten med baksidan upp i en ring runt det.",
     "Spelarna turas om att dra ett kort och gör det som kortet säger.",
     "Ess – Vattenfall: alla börjar dricka samtidigt och får sluta först när personen till höger slutat.",
     "2 – Du: välj någon som dricker.",
     "3 – Jag: du dricker själv.",
     "4 – Golv: sista person som rör golvet dricker.",
     "5 – Killar: alla killar dricker.",
     "6 – Tjejer: alla tjejer dricker.",
     "7 – Himlen: sista person som pekar upp mot taket dricker.",
     "8 – Kompis: välj en kompis som dricker varje gång du dricker resten av leken.",
     "9 – Rim: säg ett ord, sedan ska alla i tur och ordning rimma på det. Den som tvekar eller upprepar dricker.",
     "10 – Kategorier: välj en kategori (t.ex. bilmärken). Alla säger ett ord i tur och ordning, den som inte kommer på något dricker.",
     "Knekt – Regel: hitta på en regel som gäller resten av leken. Den som bryter mot den dricker.",
     "Dam – Frågemästare: tills nästa dam dras dricker den som svarar på en fråga från dig.",
     "Kung – Häll lite av din dryck i glaset i mitten. Den som drar den fjärde kungen dricker glaset (eller tar en klunk, om ni kommit överens om det).",
     "Den som bryter ringen av kort när den drar dricker."],
    varianter=["Tummen: ett kort (ofta 7 eller dam) gör dig till tummästare. När du lägger tummen på bordet ska alla andra göra likadant, den sista dricker.",
               "Alkoholfritt: byt dricka mot små uppdrag eller poäng."],
    taggar=["klassiker", "stora grupper", "uppvärmning"], osaker=True,
    kommentar="Vad varje kort betyder skiljer sig mycket mellan sällskap. Här är en vanlig version, men 7, 8, dam och kung byts ofta ut.")

# Simons kompisgängs egen lek (regler från Simon 2026-11-24)
lek("olspelet", "Ölspelet", "Kortlek",
    "Vårt gängs eget kortspel: dra ett kort i taget medsols, och varje kort har sin egen uppgift.",
    3, 10, "30–60 min", True, ["Kortlek", "Dricka"],
    ["Spelare ett tar första kortet i leken. Därefter går turen medsols (klockans varv).",
     "Den som drar ett kort gör det som kortet säger.",
     "Ess – Vattenfall: alla börjar dricka, och man får sluta först när personen före har slutat (se leken Vattenfall).",
     "Röda kort 2–6: ge bort lika många klunkar som kortet visar.",
     "Svarta kort 2–6: ta lika många klunkar själv som kortet visar.",
     "7 – Burr: spela burr. Räkna i tur och ordning och säg 'burr' i stället för tal som innehåller en 7:a eller går jämnt upp i 7. Den som gör fel får straff.",
     "8 – Saga: varje spelare lägger till ett ord och upprepar vad alla andra har sagt. Den första som inte klarar uppgiften får straff.",
     "9 – Association: säg ett ord som associeras med det förra ordet, alltså inte med det första ordet. Den som svävar för långt iväg får straff.",
     "10 – Tema: bestäm ett tema, till exempel klädmärken. Den som inte kommer på något eller säger något som redan är sagt får straff.",
     "Knekt – Regel: bestäm en regel som alla ska följa under resten av spelet. Knekten får också ta bort en tidigare regel.",
     "Dam – Alla tjejer dricker.",
     "Kung – Alla killar dricker."],
    taggar=["egen lek", "kortlek", "stora grupper"], osaker=False)
L[-1]["svarighet"] = "Medel"
# Visas under kortet när man drar i den digitala kortleken (#kortlek-olspelet).
L[-1]["kortregler"] = [
    {"valor": ["A"], "titel": "Vattenfall", "text": "Alla börjar dricka, och man får sluta först när personen före har slutat."},
    {"valor": ["2","3","4","5","6"], "farg": "rod", "titel": "Ge bort klunkar", "text": "Ge bort lika många klunkar som kortet visar."},
    {"valor": ["2","3","4","5","6"], "farg": "svart", "titel": "Ta klunkar", "text": "Ta lika många klunkar själv som kortet visar."},
    {"valor": ["7"], "titel": "Burr", "text": "Spela burr: räkna i tur och ordning och säg 'burr' i stället för tal som innehåller en 7:a eller går jämnt upp i 7. Den som gör fel får straff."},
    {"valor": ["8"], "titel": "Saga", "text": "Varje spelare lägger till ett ord och upprepar vad alla andra har sagt. Den första som inte klarar uppgiften får straff."},
    {"valor": ["9"], "titel": "Association", "text": "Säg ett ord som associeras med det förra ordet, inte med det första. Den som svävar för långt iväg får straff."},
    {"valor": ["10"], "titel": "Tema", "text": "Bestäm ett tema, till exempel klädmärken. Den som inte kommer på något eller säger något som redan är sagt får straff."},
    {"valor": ["J"], "titel": "Regel", "text": "Bestäm en regel som alla ska följa under resten av spelet. Du får också ta bort en tidigare regel."},
    {"valor": ["Q"], "titel": "Tjejerna dricker", "text": "Alla tjejer dricker."},
    {"valor": ["K"], "titel": "Killarna dricker", "text": "Alla killar dricker."},
]

lek("bussen", "Bussen", "Kortlek",
    "Gissa rätt på kort för att dela ut klunkar, och den som förlorar får åka bussen i slutet.",
    3, 8, "30–45 min", True, ["Kortlek (gärna två)", "Dricka"],
    ["Omgång 1 – Röd eller svart: alla gissar i tur och ordning om nästa kort är rött eller svart. Fel gissning = drick 1.",
     "Omgång 2 – Över eller under: gissa om nästa kort är högre eller lägre än ditt första kort. Fel = drick 2.",
     "Omgång 3 – Innanför eller utanför: gissa om nästa kort hamnar mellan eller utanför dina två kort. Fel = drick 3.",
     "Omgång 4 – Färg: gissa kortets färg (hjärter, ruter, spader, klöver). Fel = drick 4.",
     "Pyramiden: lägg ut en pyramid av kort med baksidan upp och vänd ett i taget. Har du ett kort med samma valör får du dela ut klunkar (fler ju högre upp i pyramiden).",
     "Den som har flest kort kvar på handen åker bussen.",
     "Bussen: lägg ut en rad på 5–10 kort. Busschauffören gissar högre eller lägre för varje kort. Vid fel gissning dricker hen och börjar om från början. Klara hela raden för att gå av."],
    varianter=["Om två har lika många kort kvar avgörs det med ett högt kort eller båda åker."],
    taggar=["klassiker"], osaker=True,
    kommentar="Antal klunkar, hur pyramiden poängsätts och hur många kort bussen har varierar mellan sällskap.")

lek("pyramiden", "Pyramiden", "Kortlek",
    "Alla har fyra kort, en pyramid av kort vänds en i taget och den som har samma valör delar ut klunkar, eller bluffar att den har det.",
    3, 8, "20–40 min", True, ["Kortlek", "Dricka"],
    ["Dela ut 4 kort till varje spelare. Alla får titta på sina kort i 30 sekunder och sedan läggs de upp och ner.",
     "Lägg ut en pyramid med baksidan upp: 5 kort i nedersta raden, sedan 4, 3, 2 och 1 i toppen.",
     "Vänd korten ett i taget, nerifrån och upp.",
     "Den som har (eller påstår sig ha) samma valör som det vända kortet får ge bort klunkar: 1 klunk på nedersta raden, 2 på nästa och så vidare upp till 5.",
     "Den som får klunkar kan säga 'bluff'. Då måste utdelaren visa kortet. Har hen inte kortet dricker hen dubbelt. Hade hen kortet dricker den som anklagade dubbelt.",
     "Ett kort som visats byts mot ett nytt från högen."],
    taggar=["minne", "bluff"], osaker=True,
    kommentar="Vissa spelar att det översta kortet ger 10 klunkar eller att man dricker själv på varannan rad.")

lek("fuck-the-dealer", "Fuck the Dealer", "Kortlek",
    "Gissa vilket kort som kommer härnäst. Gissar du fel dricker du, gissar alla fel får given dricka.",
    3, 10, "20–30 min", True, ["Kortlek", "Dricka"],
    ["En spelare är giv och håller kortleken.",
     "Spelaren till vänster gissar valören på översta kortet. Givaren säger 'högre' eller 'lägre' om det är fel, och spelaren får en gissning till.",
     "Rätt på första försöket: givaren dricker 5. Rätt på andra: givaren dricker 3.",
     "Fel två gånger: spelaren dricker lika många klunkar som skillnaden mellan gissningen och kortet.",
     "Kortet läggs uppvänt så alla ser vilka kort som redan kommit.",
     "Om tre spelare i rad gissar fel lämnar givaren över leken till nästa person."],
    taggar=["gissning"], osaker=True,
    kommentar="Antal klunkar och hur många fel i rad innan given byts varierar (ofta tre).")

lek("presidenten", "Presidenten", "Kortlek",
    "Ett klätterkortspel där vinnaren blir president och den som kommer sist blir skurk, med fördelar och straff nästa runda.",
    4, 8, "30–60 min", False, ["Kortlek"],
    ["Dela ut hela leken. 2 är högst, sedan ess, kung och nedåt till 3.",
     "Den som har klöver 3 börjar och lägger ett kort eller flera av samma valör.",
     "Nästa spelare måste lägga lika många kort med högre valör, eller passa.",
     "När alla passat vinner den som lade sist högen och börjar en ny stack.",
     "Den som först blir av med sina kort blir president, sedan vicepresident, och så vidare. Sista person blir skurk.",
     "Nästa runda ger skurken sina två bästa kort till presidenten, som ger tillbaka två valfria kort."],
    varianter=["Som dryckeslek: presidenten bestämmer när skurken ska dricka, och den som passar dricker 1."],
    taggar=["strategi"], osaker=True,
    kommentar="Leken har många namn (Skitgubbe-varianter, Kungen och skurken, Asshole) och detaljer som vilket kort som är högst skiljer sig.")

lek("hastkapplopning", "Hästkapplöpning", "Kortlek",
    "Satsa klunkar på ett ess (en häst) och se vilken som först når mållinjen.",
    3, 20, "10–15 min", True, ["Kortlek", "Dricka"],
    ["Plocka ut de fyra essen och lägg dem på rad som startlinje. Det är hästarna.",
     "Lägg 6–8 kort med baksidan upp i en rad bredvid. Det är banan.",
     "Alla satsar ett antal klunkar på en häst (färg).",
     "Vänd ett kort i taget från leken. Esset i samma färg flyttar ett steg fram.",
     "När alla hästar passerat ett bankort vänds det. Hästen i det kortets färg flyttas ett steg bakåt.",
     "Första ess över mållinjen vinner. De som satsat på vinnaren delar ut sina insatsklunkar, alla andra dricker sina."],
    taggar=["stora grupper", "lätt"], osaker=True,
    kommentar="Vissa låter vinnarna ge bort dubbla insatsen.")

lek("hogt-eller-lagt", "Högt eller lågt", "Kortlek",
    "En enkel lek där man i tur och ordning gissar om nästa kort blir högre eller lägre.",
    2, 10, "10–20 min", True, ["Kortlek", "Dricka"],
    ["Vänd upp ett kort.",
     "Nästa spelare gissar om nästa kort är högre eller lägre.",
     "Fel gissning: drick lika många klunkar som antalet kort i högen, och högen börjar om.",
     "Rätt tre gånger i rad: du får skicka vidare turen."],
    taggar=["lätt"], osaker=False)

lek("kortet-i-pannan", "Kortet i pannan", "Kortlek",
    "Alla håller ett kort mot pannan utan att se det själva och satsar på om de har högst.",
    3, 10, "10–20 min", True, ["Kortlek", "Dricka"],
    ["Dela ut ett kort till varje spelare. Ingen får titta på sitt eget.",
     "Alla håller samtidigt upp kortet mot pannan så att alla andra ser det.",
     "Gå runt och låt var och en välja att stanna eller lägga sig.",
     "Den som lägger sig dricker 1. Bland de som stannat dricker den med lägst kort lika många klunkar som antalet som stannade."],
    taggar=["bluff", "snabb"], osaker=True,
    kommentar="Straffsystemet är en vanlig husregel, inte en fast standard.")

lek("tjugoett", "21", "Frågelek",
    "Räkna till 21 i tur och ordning och lägg till nya regler varje gång någon når 21.",
    3, 15, "15–30 min", True, ["Dricka"],
    ["Spelarna räknar uppåt från 1 i tur och ordning. Varje person får säga 1, 2 eller 3 tal.",
     "Säger du ett tal säger nästa person nästa tal. Säger du två byter riktningen. Säger du tre hoppar ni över nästa person.",
     "Den som säger 21 dricker och får sedan hitta på en ny regel, t.ex. att 7 ska ersättas med 'hej' eller att 12 och 15 byter plats.",
     "Den som tvekar, säger fel eller bryter mot en regel dricker och räkningen börjar om från 1."],
    taggar=["uppvärmning", "inget material"], osaker=True,
    kommentar="Reglerna för vad 2 och 3 tal betyder skiljer sig. Ibland betyder två tal 'byt riktning' och tre 'hoppa över'.")

# ---------------- TÄRNING ----------------
lek("maxla", "Mäxla", "Tärning",
    "Bluffspel med två tärningar där du måste slå högre än personen före, eller ljuga om det.",
    3, 10, "20–40 min", True, ["2 tärningar", "En kopp att skaka i", "Dricka"],
    ["Slå tärningarna under koppen utan att andra ser och läs av resultatet. Den högsta tärningen läses först: 6 och 3 blir 63.",
     "Rangordning från högst: Mäxla (2–1), sedan par (6–6 högst ner till 1–1), sedan vanliga tal från 65 ner till 31. 3–2 är 'lilla mäxlan' i vissa sällskap.",
     "Säg högt vad du slog, eller ljug. Ditt bud måste vara högre än föregående spelares.",
     "Skicka koppen vidare dold. Nästa spelare kan tro dig och slå själv, eller lyfta på koppen.",
     "Lyfter man och den förra ljög dricker lögnaren. Talade den förra sanning dricker den som lyfte.",
     "Slår någon mäxla avslöjas den direkt och alla andra dricker."],
    taggar=["bluff", "klassiker"], osaker=True,
    kommentar="Om 3–1 eller 3–2 är speciella och hur många klunkar mäxla ger varierar.")

lek("tre-man", "Tre-mannen", "Tärning",
    "Slå två tärningar runt bordet, där olika summor ger olika regler och en spelare utses till tre-man.",
    3, 12, "20–40 min", True, ["2 tärningar", "Dricka"],
    ["Alla slår en tärning. Den som först får en trea blir tre-man.",
     "I tur och ordning slår spelarna två tärningar.",
     "Summa 7: den till vänster om slagaren dricker. Summa 11: den till höger dricker. Summa 9: ingen regel i vissa sällskap, i andra dricker personen mittemot.",
     "Par: slagaren ger bort tärningarna till två personer som dricker eller ger bort klunkar.",
     "Varje trea som syns, och summan 3, gör att tre-mannen dricker.",
     "En 2 och 1 (summa 3): slagaren blir ny tre-man.",
     "Får du inget som ger regler går turen vidare."],
    taggar=["tärning"], osaker=True,
    kommentar="Leken har många lokala versioner, särskilt vad 9, 10 och par betyder.")

lek("lognartarning", "Lögnartärning", "Tärning",
    "Alla har dolda tärningar och budar om hur många av ett visst tal som finns totalt runt bordet.",
    2, 6, "20–40 min", False, ["5 tärningar och en kopp per spelare"],
    ["Alla skakar sina 5 tärningar under koppen och tittar i hemlighet.",
     "Första spelaren budar, t.ex. 'fyra femmor', vilket betyder att det minst finns fyra femmor bland alla tärningar.",
     "Nästa spelare måste höja budet (fler tärningar eller samma antal av högre tal) eller säga 'lögn'.",
     "Vid 'lögn' visar alla sina tärningar. Ettor räknas ofta som joker.",
     "Den som hade fel förlorar en tärning. Den sista med tärningar kvar vinner."],
    varianter=["Dryckesvariant: den som förlorar en tärning dricker."],
    taggar=["bluff", "strategi"], osaker=False)

lek("tarning-sexan", "Sexan", "Tärning",
    "Skicka tärningen runt bordet och den som slår en sexa måste börja dricka eller göra ett uppdrag.",
    3, 15, "10–20 min", True, ["1 tärning", "Dricka"],
    ["Tärningen skickas runt bordet och alla slår i tur och ordning.",
     "Den som slår 6 tar en klunk eller ett uppdrag.",
     "Den som slår 1 skickar en klunk till valfri person.",
     "Övriga tal: inget händer."],
    taggar=["lätt", "snabb"], osaker=True,
    kommentar="Det här är en enkel grundversion. Säg till om du har en specifik version i tankarna.")

# ---------------- ÖLSPEL / BORDSLEK ----------------
lek("beer-pong", "Beer pong", "Ölspel/bordslek",
    "Två lag kastar pingisbollar i varandras muggar. Träffar ni måste motståndarna dricka.",
    2, 4, "15–30 min per match", True, ["Långt bord", "20 muggar", "2 pingisbollar", "Dricka"],
    ["Ställ 10 muggar i en triangel (4-3-2-1) i varje bordsände och fyll dem lite.",
     "Lagen turas om att kasta. Båda i laget kastar en gång per tur.",
     "Bollen i en mugg: motståndarna dricker innehållet och tar bort muggen.",
     "Träffar båda i laget under samma tur får de kasta igen.",
     "Studsar bollen i bordet först och går i räknas det oftast som två muggar, men då får motståndarna försöka slå bort bollen.",
     "Laget får två gånger per match be om att muggarna ställs om (re-rack).",
     "Laget som först tar bort alla motståndarens muggar vinner. Förloraren får en sista chans att träffa alla återstående (redemption)."],
    varianter=["Fyll muggarna med vatten och drick ur ett eget glas, mer hygieniskt."],
    taggar=["klassiker", "tävling", "lag"], osaker=True,
    kommentar="Studs, armbågsregeln och re-rack är husregler som skiljer sig mellan sällskap.")

lek("flip-cup", "Flip cup", "Ölspel/bordslek",
    "Lagstafett där man dricker sin mugg och sedan ska vända den upp och ner genom att knäppa på kanten.",
    6, 20, "10–20 min", True, ["Långt bord", "En plastmugg per spelare", "Dricka"],
    ["Dela upp er i två lika stora lag som står på var sin sida av bordet, mittemot varandra.",
     "Alla har en mugg med lite dricka framför sig.",
     "Första personen i varje lag dricker upp och ställer muggen upp och ner på bordskanten med kanten utanför bordet.",
     "Knäpp på muggen så att den vänder och landar upp och ner. Först då får nästa person i laget börja.",
     "Laget vars sista person först lyckas vända muggen vinner."],
    taggar=["lag", "tävling", "stora grupper"], osaker=False)

lek("myntet", "Quarters (Myntet)", "Ölspel/bordslek",
    "Studsa ett mynt mot bordet och ner i ett glas. Träffar du får du välja vem som dricker.",
    2, 10, "15–30 min", True, ["Ett mynt", "Ett glas", "Dricka"],
    ["Ställ ett glas i mitten av bordet.",
     "Spelarna försöker i tur och ordning studsa ett mynt mot bordet så att det landar i glaset.",
     "Träff: välj någon som dricker, och du får kasta igen.",
     "Tre träffar i rad: du får hitta på en regel.",
     "Miss: myntet går vidare till nästa person."],
    taggar=["skicklighet"], osaker=False)

lek("olstafett", "Ölstafett", "Ölspel/bordslek",
    "Lagstafett där varje person springer, dricker och springer tillbaka.",
    6, 30, "10 min", True, ["En burk eller mugg per person", "Plats att springa"],
    ["Dela upp er i lag och ställ upp på led.",
     "Placera en dryck per person på andra sidan rummet eller gården.",
     "Första personen springer, dricker upp och springer tillbaka och klappar nästa i handen.",
     "Laget som blir klart först vinner."],
    varianter=["Snurra runt en pinne tio gånger innan du springer tillbaka (yrsel)."],
    taggar=["utomhus", "lag"], osaker=False)

lek("kubb", "Kubb", "Utomhus",
    "Svenskt kastspel där lagen försöker välta motståndarnas kubbar och till sist kungen.",
    2, 12, "20–60 min", False, ["Kubbspel (10 kubbar, 1 kung, 6 kastpinnar, 4 hörnpinnar)", "Gräsmatta"],
    ["Markera en plan, ungefär 5 x 8 meter. Ställ 5 kubbar på varje baslinje och kungen i mitten.",
     "Lag A kastar sina 6 pinnar underifrån med vertikal rotation för att välta lag B:s kubbar.",
     "Lag B kastar sedan de vältade kubbarna till lag A:s planhalva, där de ställs upp som fältkubbar.",
     "Fältkubbar måste fällas innan baslinjekubbar. Om laget inte fäller alla fältkubbar får motståndarna kasta från den främsta kvarvarande fältkubben.",
     "När alla motståndarens kubbar är fällda får laget försöka fälla kungen från baslinjen. Lyckas det vinner laget.",
     "Fäller man kungen för tidigt förlorar man direkt."],
    varianter=["Som dryckeslek: varje gång ditt lag tappar en kubb dricker du."],
    taggar=["utomhus", "lag", "sommar"], osaker=False)

lek("snurra-flaskan", "Snurra flaskan", "Mingel",
    "Snurra en flaska i mitten av ringen. Den den pekar på får en fråga, ett uppdrag eller en puss.",
    4, 15, "15–30 min", False, ["En tom flaska"],
    ["Sitt i en ring på golvet med flaskan i mitten.",
     "Den som börjar snurrar flaskan.",
     "Personen flaskan pekar på får det ni har bestämt: en fråga, en utmaning, eller i den klassiska versionen en puss.",
     "Den som pekats ut snurrar nästa gång."],
    taggar=["klassiker"], osaker=False)

# ---------------- FRÅGELEKAR ----------------
lek("jag-har-aldrig", "Jag har aldrig", "Frågelek",
    "Säg något du aldrig har gjort. Alla som har gjort det dricker.",
    3, 20, "15–60 min", True, ["Dricka"],
    ["Turas om att säga en mening som börjar med 'Jag har aldrig ...', t.ex. 'Jag har aldrig varit i Norge'.",
     "Alla som har gjort det tar en klunk.",
     "Den som säger meningen dricker inte (har man faktiskt gjort det får man dock välja att dricka).",
     "Fortsätt runt bordet."],
    varianter=["Fingerversion: alla håller upp 10 fingrar och fäller ett i stället för att dricka. Den som får ner alla först förlorar.",
               "Alkoholfritt: använd godis eller poäng."],
    taggar=["klassiker", "lära känna", "inget material"], osaker=False)

lek("mest-sannolikt", "Pekleken", "Frågelek",
    "Läs upp en fråga som 'Vem är mest sannolikt att...' och peka på samtidigt.",
    4, 20, "15–45 min", True, ["Dricka"],
    ["En person läser upp en fråga, t.ex. 'Vem är mest sannolikt att bli kändis?'",
     "Alla räknar till tre och pekar samtidigt på den de tror.",
     "Varje person dricker en klunk för varje finger som pekar på dem."],
    taggar=["lära känna", "inget material", "stora grupper"], osaker=False)

lek("snusdosan", "Snusdosan", "Frågelek",
    "Som Pekleken, fast ni kastar en snusdosa till den som påståendet stämmer mest in på.",
    3, 15, "15–45 min", True, ["Ett kastbart föremål (t.ex. en snusdosa)", "Dricka"],
    ["Ni spelar med ett kastbart föremål, förslagsvis en snusdosa, eftersom det är vanligt att någon i gruppen har en.",
     "Du får ett påstående, likt Pekleken.",
     "Sedan kastar du dosan till personen som påståendet stämmer mest in på.",
     "Den som får dosan läser upp nästa påstående."],
    taggar=["egen lek", "lära känna", "stora grupper"], osaker=False)
L[-1]["svarighet"] = "Lätt"
# Starta spel använder Peklekens frågor (samma påståenden passar).
L[-1]["fragor_fran"] = "mest-sannolikt"
L[-1]["spel_instruktion"] = "Läs upp påståendet. Kasta dosan till den det stämmer mest in på."

lek("impostor", "Impostor", "Ord & gissning",
    "Alla utom en får samma hemliga ord. Impostorn vet bara kategorin och måste bluffa sig igenom.",
    3, 20, "5–15 min per runda", True, ["En telefon (appen delar ut orden), eller lappar och penna"],
    ["Starta Impostor i appen och välj hur många ni är, hur många impostorer ni vill ha och vilka kategorier som ska vara med.",
     "Skicka runt telefonen. Var och en trycker fram sitt ord, tittar i hemlighet, gömmer det och lämnar vidare.",
     "Alla får samma hemliga ord, utom impostorn som bara får veta kategorin (eller ingenting, om ni väljer det svårare läget).",
     "Appen lottar vem som börjar. I tur och ordning säger var och en ett ord som hör ihop med det hemliga ordet. Inte för tydligt, då listar impostorn ut det. Inte för luddigt, då blir du misstänkt.",
     "Efter ett eller två varv diskuterar ni och röstar på den ni tror är impostor.",
     "Röstar ni ut fel person vinner impostorn. Röstar ni ut impostorn får den en chans att gissa ordet. Gissar den rätt vinner impostorn ändå, annars vinner resten.",
     "Förslag: de som förlorar rundan tar en klunk."],
    varianter=["Utan telefon: en spelledare skriver samma ord på alla lappar utom en, där det står 'Impostor'.",
               "Svårare: impostorn får inte ens veta kategorin.",
               "Flera impostorer: med många spelare kan ni ha två eller tre impostorer, som inte vet om varandra."],
    taggar=["bluff", "stora grupper", "spel i telefonen"], osaker=False)
L[-1]["svarighet"] = "Lätt"
L[-1]["grupp"] = "prat"
# Länkar till spelläget #impostor (ordbanken ligger i impostor.json).
L[-1]["verktyg"] = "impostor"

lek("korkortet", "Körkortet", "Frågelek",
    "En spelare rangordnar allas körkort efter ett hemligt påstående. De andra gissar vilket påstående det var.",
    3, 10, "15–45 min", True, ["Ett körkort eller id-kort per person (eller någon annan personlig sak)", "En telefon (appen visar påståendena)"],
    ["Alla som är med i leken lägger fram en personlig sak, förslagsvis körkort eller id.",
     "Spelare ett har telefonen och får ett påstående, till exempel 'Vem är mest trolig att somna först på festen?'. Ingen annan får se det.",
     "Spelaren rangordnar därefter körkorten i den ordning de troligast stämmer in på påståendet, till minst troligt.",
     "Därefter presenterar appen 4, 6, 8 eller 10 påståenden, där ett av dem är det som spelare ett har rangordnat körkorten efter.",
     "Därefter ska de övriga spelarna komma fram till vilket påstående spelare ett har utgått från.",
     "Visa svaret och skicka telefonen vidare. Nästa spelare gör en ny runda.",
     "Förslag: gissar ni fel tar ni en klunk, gissar ni rätt tar den som rangordnade en klunk."],
    varianter=["Svårare: välj fler påståenden att gissa bland (8 eller 10).",
               "Utan telefon: rangordnaren skriver sitt påstående på en lapp och läser sedan upp några falska påståenden tillsammans med det riktiga."],
    taggar=["egen lek", "lära känna", "spel i telefonen"], osaker=False)
L[-1]["svarighet"] = "Lätt"
L[-1]["grupp"] = "prat"
# Länkar till spelläget #korkortet (påståendena ligger i korkortet.json).
L[-1]["verktyg"] = "korkortet"

lek("sanning-eller-konsekvens", "Sanning eller konsekvens", "Frågelek",
    "Välj mellan att svara ärligt på en fråga eller göra en utmaning.",
    3, 15, "20–60 min", False, [],
    ["Turas om att fråga någon: 'Sanning eller konsekvens?'",
     "Väljer personen sanning måste hen svara ärligt på en fråga.",
     "Väljer personen konsekvens måste hen göra en utmaning som gruppen hittar på.",
     "Den som vägrar svara eller göra utmaningen får ett straff, t.ex. att dricka.",
     "Personen som just svarat frågar nästa."],
    taggar=["klassiker", "lära känna"], osaker=False)

lek("tva-sanningar-en-logn", "Två sanningar och en lögn", "Frågelek",
    "Berätta tre saker om dig själv, en är falsk, och de andra ska gissa vilken.",
    3, 15, "15–30 min", False, [],
    ["En person säger tre påståenden om sig själv. Två är sanna och ett är en lögn.",
     "Resten av gruppen diskuterar och gissar vilken som är lögnen.",
     "Som dryckeslek: alla som gissar fel dricker. Gissar alla rätt dricker berättaren."],
    taggar=["lära känna", "inget material"], osaker=False)

lek("heta-stolen", "Heta stolen", "Frågelek",
    "En person sitter i heta stolen och alla andra får ställa frågor som måste besvaras ärligt.",
    4, 15, "15–30 min", False, [],
    ["En person sätter sig i heta stolen.",
     "Under 2 minuter får alla andra ställa frågor, och personen måste svara ärligt.",
     "Den som vägrar svara på en fråga dricker eller får ett straff.",
     "Sedan går stolen vidare till nästa person."],
    taggar=["lära känna"], osaker=False)

lek("paranoia", "Paranoia", "Frågelek",
    "Viska en fråga om någon i sällskapet. Svaret sägs högt, men frågan avslöjas bara om man vågar.",
    4, 12, "15–30 min", True, ["Dricka", "Ett mynt (valfritt)"],
    ["Viska en fråga till personen bredvid, t.ex. 'Vem här är snyggast?'",
     "Hen svarar högt genom att säga ett namn ur gruppen.",
     "Den som blev nämnd kan dricka för att få höra frågan. Då avslöjas den högt.",
     "Annars förblir frågan hemlig och det är nästa persons tur att viska."],
    varianter=["Singla slant i stället för att dricka: krona betyder att frågan avslöjas."],
    taggar=["spänning"], osaker=False)

# ---------------- ORD & GISSNING ----------------
lek("bizz-buzz", "Bizz (Buzz)", "Ord & gissning",
    "Räkna i tur och ordning, men byt ut alla tal som har med 7 att göra mot ett ord.",
    3, 15, "10–20 min", True, ["Dricka"],
    ["Spelarna räknar i tur och ordning från 1.",
     "Alla tal som innehåller en 7:a eller är delbara med 7 ersätts med 'bizz'.",
     "Den som säger fel, tvekar för länge eller glömmer dricker och räkningen börjar om.",
     "Svårare: lägg till 'buzz' för tal med 5 eller delbara med 5. Tal som är både och blir 'bizz-buzz'."],
    taggar=["uppvärmning", "inget material"], osaker=False)

lek("kategorier", "Kategorier", "Ord & gissning",
    "Säg ett ord ur en kategori i tur och ordning. Den som inte kommer på något eller upprepar förlorar.",
    3, 15, "5–20 min", True, ["Dricka"],
    ["En person väljer en kategori, t.ex. 'ölsorter' eller 'svenska artister'.",
     "Gå runt och säg ett ord var som passar kategorin.",
     "Den som tvekar för länge, upprepar ett ord eller säger fel dricker och väljer nästa kategori."],
    taggar=["inget material", "snabb"], osaker=False)

lek("rimleken", "Rimleken", "Ord & gissning",
    "Säg ett ord och låt alla rimma på det i tur och ordning.",
    3, 15, "5–15 min", True, ["Dricka"],
    ["En person säger ett ord.",
     "Gå runt och säg ett ord som rimmar.",
     "Den som tvekar, upprepar eller hittar på ett ord som inte finns dricker och säger nästa ord."],
    taggar=["inget material", "snabb"], osaker=False)

lek("jag-packar-min-vaska", "Jag packar min väska", "Ord & gissning",
    "Minneslek där varje person lägger till en sak i väskan och måste komma ihåg allt som redan packats.",
    3, 15, "10–20 min", False, [],
    ["Första personen säger: 'Jag packar min väska och tar med mig ett ...', t.ex. en tandborste.",
     "Nästa upprepar allt som sagts och lägger till en ny sak.",
     "Den som glömmer något eller tar fel ordning åker ut (eller dricker).",
     "Sista personen kvar vinner."],
    taggar=["minne", "inget material"], osaker=False)

lek("sista-bokstaven", "Ordkedjan", "Ord & gissning",
    "Säg ett ord som börjar på sista bokstaven i föregående ord.",
    2, 15, "5–15 min", False, [],
    ["Välj gärna en kategori, t.ex. städer eller djur.",
     "Första personen säger ett ord, t.ex. 'Stockholm'.",
     "Nästa måste säga ett ord som börjar på sista bokstaven: 'Malmö'.",
     "Den som tvekar eller upprepar åker ut eller dricker."],
    taggar=["inget material"], osaker=False)

lek("kandisleken", "Kändisleken (Hatten)", "Ord & gissning",
    "Alla skriver namn på lappar. I tre omgångar ska lagen gissa samma namn med allt hårdare regler.",
    6, 20, "45–90 min", False, ["Lappar", "Pennor", "En hatt eller skål", "Timer"],
    ["Alla skriver 3–5 namn på kända personer (eller figurer) på var sin lapp och lägger dem i hatten.",
     "Dela upp er i två lag. Lagen turas om och en person i taget har 1 minut på sig.",
     "Omgång 1: förklara med ord så många namn som möjligt utan att säga namnet.",
     "Omgång 2: samma lappar, men bara ett enda ord per namn.",
     "Omgång 3: samma lappar, men bara med kroppsspråk (charad).",
     "Varje rätt gissat namn är ett poäng. Laget med flest poäng efter tre omgångar vinner."],
    taggar=["lag", "stora grupper", "favorit"], osaker=False)

lek("vem-ar-jag", "Vem är jag?", "Ord & gissning",
    "Alla har ett namn på en lapp i pannan och ställer ja- eller nej-frågor för att lista ut vem de är.",
    3, 15, "20–40 min", False, ["Post-it-lappar", "Penna"],
    ["Varje person skriver en känd person på en lapp och sätter den i pannan på personen bredvid, utan att hen ser.",
     "Turas om att ställa en ja- eller nejfråga, t.ex. 'Är jag en man?'",
     "Får du ja fortsätter du fråga. Får du nej går turen vidare.",
     "Den som först gissar rätt vinner. Leken fortsätter tills alla gissat."],
    varianter=["Som dryckeslek: drick varje gång du får ett nej."],
    taggar=["klassiker"], osaker=False)

lek("charader", "Charader", "Ord & gissning",
    "Visa en film, låt eller ett ord med kroppsspråk utan att prata, och låt laget gissa.",
    4, 20, "20–60 min", False, ["Lappar med ord", "Timer"],
    ["Dela upp er i två lag.",
     "En person drar en lapp och har 1–2 minuter på sig att visa ordet med gester. Inget prat, inga ljud.",
     "Det egna laget gissar. Rätt svar ger ett poäng.",
     "Lagen turas om. Laget med flest poäng vinner."],
    taggar=["lag", "klassiker"], osaker=False)

lek("rita-och-gissa", "Rita och gissa", "Ord & gissning",
    "Rita ett ord på papper medan laget gissar, utan bokstäver eller siffror.",
    4, 20, "20–60 min", False, ["Papper eller whiteboard", "Pennor", "Lappar med ord", "Timer"],
    ["Dela upp er i lag.",
     "En person drar ett ord och ritar det. Inga bokstäver, siffror eller ord får användas.",
     "Laget har 1 minut på sig att gissa.",
     "Rätt svar ger ett poäng. Lagen turas om."],
    taggar=["lag"], osaker=False)

lek("forbjudna-ord", "Förbjudna ord", "Ord & gissning",
    "Förklara ett ord för ditt lag utan att säga vissa förbjudna ord.",
    4, 20, "20–45 min", False, ["Lappar med ord och 3–5 förbjudna ord", "Timer"],
    ["Dela upp er i lag.",
     "En person drar ett kort med ett ord och några förbjudna ord, t.ex. 'Strand' utan 'sand', 'hav', 'sol'.",
     "Förklara så många ord som möjligt på 1 minut.",
     "Säger man ett förbjudet ord får motståndarna ett poäng (eller förklararen dricker)."],
    taggar=["lag"], osaker=False)

lek("viskleken", "Viskleken", "Ord & gissning",
    "En mening viskas runt i ringen och förvandlas på vägen.",
    5, 30, "5–10 min", False, [],
    ["Sitt eller stå i en ring.",
     "Första personen viskar en mening till nästa, en gång.",
     "Meningen viskas vidare hela vägen runt.",
     "Sista personen säger högt vad hen hörde och första personen avslöjar originalet."],
    taggar=["inget material", "stora grupper"], osaker=False)

# ---------------- MINGEL / SOCIALA ----------------
lek("maffia", "Maffia", "Mingel",
    "Rollspel där en hemlig maffia dödar invånare på natten och byn försöker hitta dem på dagen.",
    7, 20, "30–60 min", False, ["Spelkort eller lappar för roller"],
    ["En person är spelledare. Övriga får en hemlig roll: några maffia (ungefär en per fyra spelare), en detektiv, en läkare, resten invånare.",
     "Natt: alla blundar. Maffian öppnar ögonen och pekar ut ett offer. Läkaren pekar ut någon att rädda. Detektiven pekar på en person och spelledaren visar tummen upp eller ner om personen är maffia.",
     "Dag: alla öppnar ögonen. Spelledaren berättar vem som dog (om inte läkaren räddade personen).",
     "Byn diskuterar och röstar ut en misstänkt. Den utröstade visar sin roll och åker ut.",
     "Invånarna vinner när all maffia är ute. Maffian vinner när de är lika många som invånarna."],
    varianter=["Varulv: samma lek med varulvar och fler specialroller som häxa och siare."],
    taggar=["stora grupper", "bluff", "favorit"], osaker=False)

lek("blinkmordaren", "Blinkmördaren", "Mingel",
    "En hemlig mördare dödar genom att blinka åt folk. Alla andra försöker avslöja hen.",
    6, 30, "15–30 min", False, ["Kort eller lappar"],
    ["Dela ut ett kort till varje person. Den som får t.ex. spader ess är mördare, en annan är detektiv om ni vill.",
     "Mingla eller sitt i ring och titta på varandra.",
     "Mördaren dödar genom att blinka diskret åt någon. Den som blinkats åt väntar några sekunder och 'dör' sedan dramatiskt.",
     "Den som tror sig veta vem mördaren är säger 'Jag anklagar!'. Fel gissning gör att man åker ut.",
     "Mördaren vinner om alla dör innan hen blir avslöjad."],
    taggar=["stora grupper", "mingel"], osaker=False)

lek("stolleken", "Stoldansen", "Mingel",
    "Gå runt stolarna när musiken spelar. När den slutar måste alla hitta en stol, men det finns en för lite.",
    5, 20, "10–20 min", False, ["Stolar (en färre än antalet spelare)", "Musik"],
    ["Ställ stolarna i en ring med sitsen utåt. Det ska finnas en stol mindre än antalet spelare.",
     "Spela musik och låt alla gå runt.",
     "När musiken stoppas sätter sig alla så fort de kan. Den som blir utan åker ut.",
     "Ta bort en stol per omgång tills en vinnare finns kvar."],
    taggar=["fysisk", "klassiker"], osaker=False)

lek("musikquiz", "Gissa låten", "Ord & gissning",
    "Spela korta intron av låtar och se vem som gissar artist och titel först.",
    2, 30, "20–60 min", False, ["Högtalare", "En spellista"],
    ["En person är DJ och spelar 5–10 sekunder av en låt.",
     "Spelarna eller lagen ropar eller skriver ner artist och låttitel.",
     "Ett poäng för artist och ett för titel.",
     "Den med flest poäng efter alla låtar vinner."],
    varianter=["Som dryckeslek: den som gissar fel eller sist dricker."],
    taggar=["musik", "lag"], osaker=False)

lek("power-hour", "Power hour (Centurion)", "Övrigt",
    "En spellista byter låt varje minut och alla tar en liten klunk vid varje byte.",
    2, 50, "60 min", True, ["Spellista med 60 låtar på 1 minut vardera", "Dricka"],
    ["Gör en spellista där varje låt spelas exakt en minut.",
     "Vid varje låtbyte tar alla en liten klunk (traditionellt en shot öl).",
     "Fortsätt i en timme. Centurion är varianten med 100 minuter."],
    varianter=["Rekommenderat: använd svagdricka eller vatten varannan minut."],
    taggar=["musik", "stora grupper"], osaker=False,
    kommentar=None)

lek("film-drickspel", "Drickspel till film eller serie", "Övrigt",
    "Bestäm saker som brukar hända i en film eller serie och drick varje gång de händer.",
    2, 20, "Hela filmen", True, ["En film eller serie", "Dricka"],
    ["Välj en film eller serie.",
     "Gör en lista med 4–8 saker som brukar hända, t.ex. 'någon säger huvudpersonens namn' eller 'en bil exploderar'.",
     "Varje gång något på listan händer tar alla en klunk.",
     "Ge gärna varje person en egen sak att hålla koll på."],
    taggar=["lugnt", "film"], osaker=False)

lek("tummen", "Tummästaren", "Mingel",
    "En person är tummästare och kan när som helst lägga tummen på bordet. Den sista att märka det och göra likadant dricker.",
    3, 20, "Pågår under kvällen", True, ["Dricka"],
    ["Utse en tummästare, t.ex. genom ett kort i en annan lek.",
     "När tummästaren diskret lägger tummen mot bordskanten ska alla andra göra likadant.",
     "Den sista som märker det dricker.",
     "Rollen kan gå vidare till förloraren eller stanna hos tummästaren."],
    varianter=["Fråga-mästaren: den som svarar på en fråga från frågemästaren dricker."],
    taggar=["pågår hela kvällen", "inget material"], osaker=False)

lek("skal-for-guvernoren", "Skål för guvernören", "Ord & gissning",
    "Räkna till 21 i tur och ordning, med regler som byggs på efter varje lyckad runda.",
    3, 15, "15–30 min", True, ["Dricka"],
    ["Räkna i tur och ordning från 1 till 21, en siffra per person.",
     "Den som tvekar eller säger fel dricker och man börjar om.",
     "Den som säger 21 säger 'skål för guvernören', alla dricker och personen hittar på en ny regel för ett tal, t.ex. att 9 ska sägas på tyska.",
     "Reglerna gäller resten av leken och blir svårare och svårare."],
    taggar=["inget material"], osaker=True,
    kommentar="Mycket lik leken 21. Kanske ska de slås ihop till en lek med varianter?")

lek("ja-nej-leken", "Ja- och nejleken", "Ord & gissning",
    "Svara på frågor utan att säga ja eller nej.",
    2, 15, "5–15 min", False, [],
    ["En person ställer snabba frågor till en annan.",
     "Den som svarar får inte säga 'ja', 'nej' eller nicka eller skaka på huvudet.",
     "Den som klarar en minut vinner. Den som säger fel åker ut (eller dricker)."],
    taggar=["inget material", "snabb"], osaker=False)

lek("vattenfall", "Vattenfall", "Ölspel/bordslek",
    "Alla börjar dricka samtidigt och ingen får sluta förrän personen före slutat.",
    3, 15, "1–2 min", True, ["Dricka"],
    ["Alla sitter i en ring.",
     "Den som startar börjar dricka. Sedan börjar nästa, och så vidare runt ringen.",
     "Startaren får sluta när hen vill. Varje annan person får sluta först när personen före har slutat."],
    taggar=["snabb", "del av andra lekar"], osaker=False)

lek("olschack", "Ölschack", "Ölspel/bordslek",
    "Vanligt schack, men pjäserna är små glas och den som slår en pjäs dricker den.",
    2, 2, "30–60 min", True, ["Schackbräde", "32 små glas med två olika drycker"],
    ["Ställ upp glas som schackpjäser, med en färg dryck per sida. Märk glasen så att ni ser vilken pjäs som är vilken.",
     "Spela schack som vanligt.",
     "När du slår en pjäs dricker du upp den.",
     "Den som tar kungen vinner."],
    taggar=["två personer", "strategi"], osaker=False)

# ---------------- gemensam regel ----------------
# Simon: appen är en idésamling. Sällskapet bestämmer själv om, när och hur mycket man dricker.
KLUNKREGEL = "Sällskapet bestämmer alltid själv om, när och hur mycket man dricker. Klunkar och straff i reglerna är bara förslag."
for d in L:
    d["regler"].append(KLUNKREGEL)

# ---------------- skriv ----------------
ids = [d["id"] for d in L]
assert len(ids) == len(set(ids)), "dubbla id"
for d in L:
    assert re.fullmatch(r"[a-z0-9-]+", d["id"]), d["id"]
    assert d["regler"]
out = sys.argv[1]
with open(out, "w", encoding="utf-8") as f:
    json.dump(L, f, ensure_ascii=False, indent=2)
print(len(L), "lekar,", sum(d["osaker"] for d in L), "osäkra")
