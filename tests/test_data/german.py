ISO_CODE = "de"
TEST_DATA = [
    # Basic punctuation
    "Hallo Welt!| Wie geht es dir?| Mir geht es gut.",
    "Wie ist dein Name?| Mein Name ist Jonas.",
    "Da ist es!| Ich habe es endlich gefunden.",
    "Hast du die Nummer 2 entfernt?| Bitte mach es rückgängig.",

    # Abbreviations
    "Mein Name ist Jonas E. Schmidt.",
    "Bitte blättern Sie zu S. 55.",
    "Ich kann den Mt. Fuji von hier aus sehen.",
    "St. Michael liegt in der 5. Straße nahe der Ampel.",
    "Ich brauche 3 Dinge, z. B. einen Hut, einen Mantel und eine Tasche.",
    "Der Bericht wurde im Dez. veröffentlicht.| Er wurde von Prof. Schmidt und Dr. Jones genehmigt.",
    "Die Temperatur erreichte 37,5 °C um 6 Uhr am Di., 4. Feb.",
    "Siehe Abb. 2 in Bd. 3, Kap. 4, S. 18-22.",
    "Der Beweis ist in Gl. (7) und Bsp. IV dargestellt.",
    "Wir sehen uns am Fr., 14. Feb.",
    "Sie finden es unter Nr. 1026.253.553.| Dort ist der Schatz.",
    "Wir wählen zuerst Option A.| Danach besprechen wir die Details.",
    "Rufen Sie Tel. 555-0199 an.| Senden Sie ein Fax. 02-555 morgen.",

    # Structural headings
    "Kapitel 1. Der Anfang.| Es war dunkel und still im Raum. | Nichts bewegte sich.",
    "Abschnitt 3.1. Arbeitsumfang.| Das Projekt deckt mehrere Sprachen ab.",
    "Die Ergebnisse waren nicht eindeutig.| Kapitel 3. Diskussion folgt sofort.| Das Team überarbeitete das Modell.",

    # Parentheses and quotes
    "Er lehrt Naturwissenschaften (er arbeitete zuvor 5 Jahre als Ingenieur) an der örtlichen Universität.",
    "(Siehe Abb. 4. Dies skizziert das Speicherlayout.)| Die Engine führt das Nächste aus.",
    'Sie drehte sich zu ihm: „Das ist großartig.“| Sie hielt ihm das Buch hin.',
    '„Ist das okay?“, fragte sie.',
    "Laut seinem Verleger kaufte Schmidt das Unternehmen 1985 [oder 1984?], war aber erst ab 1990 aktiv.",
    'Dann hielt er an.| „Warte“, sagte er.',
    "Der Brief schloss mit einer einfachen Warnung: ‚Folge mir nicht.‘| Dann ging sie.",
    'Er sagte: „Erster Satz. Zweiter Satz.“| Dann war er fertig.',

    # Ellipsis
    "Das Projekt (Sinta) stand kurz vor dem Abschluss... oder so dachten wir.",
    '„Wie konnten wir das übersehen!...“| Mark schrie und schlug mit der Hand auf den Tisch.',
    "Wir haben ein Speicherleck im C#-Wrapper gefunden....| Es war subtil.",

    # Mixed language
    "Das Treffen ist um 14 Uhr.| 请别迟到。",
    "那个会议在下午两点。|Please don't be late!"
]
