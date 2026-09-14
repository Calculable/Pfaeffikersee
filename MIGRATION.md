# Migration pfäffikersee.org – Squarespace → Astro / GitHub Pages

## Anforderungen und Freigaben
- Zielordner: /Users/jan/Documents/Projekte/Github/Pfäffikersee/Webseite (vorhandener leerer Unterordner).
- Gleicher Ansatz wie Portfolio: einfache Astro-Website, sauberer konsistenter Stil, Fokus auf Originalinhalte, leicht editierbare Markdown-Dateien pro Seite.
- URLs erhalten; öffentlich verfügbare Medien lokal speichern; SEO-Daten übernehmen. Keine Abhängigkeit von Squarespace zur Laufzeit, kein animierter Squarespace-Hintergrund.
- Quelle ist derzeit nicht öffentlich online; angemeldete Squarespace-Vorschau ist zugänglich. Keine Änderungen am Original.
- GitHub-Repository erstellen, mit Arbeitsbranch arbeiten, lokal testen.
- Basin für Formulare; GoatCounter für Statistik. Konten/Endpunkte prüfen, keine Portfolio-Endpunkte ungeprüft wiederverwenden.
- Zuerst lokale Vorschau und ausdrückliche Nutzerfreigabe. Domain/DNS bei Hosttech erst danach ändern.
- Bis zum Domainumzug noindex auf sämtlichen Seiten; Suchmaschinen erst beim freigegebenen Domainumzug zulassen.
- Technische Entscheidungen und Prüfungen hier dokumentieren; Fortschritt je Seite melden.

## Vorläufige Seitenliste (Navigation und Startseite)
- [x] / – Startseite
- [x] /biodiversitaet
- [x] /geschichte
- [x] /galerie
- [x] /seegfroerni
- [x] /sehenswuerdigkeiten
- [x] /wasserqualitaet
- [x] /voegel
- [x] /kontakt
- [x] /datenschutzerklaerung
- [x] Weitere Seiten/Unterseiten in Squarespace inventarisieren

## Weitere Schritte
- [x] Originalinhalte und SEO archivieren
- [x] GitHub-Repository erstellen
- [x] Astro-Grundgerüst und Medienimport
- [x] Basin und GoatCounter konfigurieren
- [x] Lokale Build-, Link-, Medien- und Mobilprüfung
- [x] Lokale Vorschau zur Nutzerfreigabe
- [ ] Domainumzug NUR nach Freigabe; DNS/Mail sichern, HTTPS und URLs prüfen

## Stand am 14. September 2026
- Repository: https://github.com/Calculable/Pfaeffikersee
- Arbeitsbranch: `migration/squarespace`; `main` enthält zunächst den Migrationsplan.
- Lokale Vorschau: http://127.0.0.1:4340/ (Astro dev server).
- 10 Inhaltsseiten plus eigene 404-Seite. Alle bisherigen Seitenpfade bleiben gleich.
- 105 lokale Bilddateien, insgesamt ca. 54 MB. Keine Squarespace-Dateien werden zur Laufzeit geladen.
- Weitere Squarespace-Seiten «Über uns» und «Initiativen» waren nicht verlinkt. Dazu wurde nachgefragt; bis zu einer anderslautenden Antwort sind sie gemäss Vorgabe «gleicher Ansatz» vorerst ausgeschlossen. System-404 wurde durch eine eigene einfache Fehlerseite ersetzt.
- Noch kein Deployment und keine Änderung an Domain, DNS, Nameservern oder Squarespace.

## Technische Entscheidungen
- Statische Astro-Seiten; jede Seite in `src/content/pages/<seite>/index.md`. `path` erhält die URL unabhängig von der Dateistruktur.
- Startseitenkarten in `src/content/projects.json`, weiterführende Links in `home/links.md`. Texte bleiben editierbar, ohne das Layout anzufassen.
- Systemschriftarten, ruhige Grüntöne, volle Bildbreite im Titelbereich, mobile Menüschaltfläche, begrenzte Bildhöhen, leichte Kartenanimation mit Reduced-Motion-Unterstützung.
- Als Startbild dient die bereits vorhandene Seeaufnahme `IMG_8473.jpg`. Das ursprüngliche Bild mit einem Pfäffikersee-Glas bleibt in der Galerie erhalten.
- Bilder in Markdown-Syntax. Eine kursiv gesetzte Zeile direkt nach einem Bild wird als zentrierte Bildunterschrift gerendert (kleiner `rehype-figures`-Baustein). Credits und Lizenzlinks bleiben erhalten.
- OpenStreetMap ersetzt die Squarespace/Google-Karteneinbettung. Die Karte lädt erst nach Klick; keine API-Schlüssel notwendig. YouTube ebenfalls erst nach Klick und über youtube-nocookie.com.
- Galerie: 13 Bilder (12 ursprüngliche Galerieaufnahmen plus bisheriges Startbild), Vergrösserung über natives Dialogelement, schliessbar mit Schaltfläche und Escape. Kein jQuery.
- Der alte Webcam-Stream `hdK0TyGY-EU` war nicht verfügbar. Die aktuelle Quelle auf https://www.retti.ch/webcam verwendet `3f97bPoCzow`; dieser Stream wird jetzt eingebettet und der Anbieter direkt verlinkt.
- Wasserqualitäts-Diagramm als zugängliche Markdown-Tabelle mit unveränderten Werten: Naturnahe 24,1 %, Landwirtschaft 50,7 %, Feuchtgebiet 7,9 %, Siedlung 17,4 %.
- Keine ungenutzten Squarespace-section-IDs. Seiten-URL-Pfade bleiben erhalten; originale Beschreibung-Metadaten waren überwiegend leer. Titel übernommen; Canonical/Open Graph auf die künftige Domain korrigiert. Doppelte und Squarespace-spezifische SEO-Tags entfallen.
- Datenschutz ersetzt alte Squarespace-/Google-Analytics-/Font-Angaben durch GitHub Pages, Basin, GoatCounter, OpenStreetMap und YouTube. Verwendete Anbieterquellen stehen direkt im Text.
- `indexable: false` in `src/site.ts` sperrt Indexierung via noindex/nofollow, lässt die Sitemap leer und deaktiviert GoatCounter. robots.txt erlaubt Abrufe, damit Crawler das noindex lesen können. Erst bei freigegebenem Domainumzug auf true setzen; 404 bleibt noindex.
- GitHub Actions prüft nur den Build und die statischen Seiten; keine automatische Veröffentlichung vor der Freigabe.

## Dienste und noch offene Nutzerschritte
- Basin-Formular «Pfäffikersee – Kontakt», ID 75385, Endpunkt `https://usebasin.com/f/9c7305fcc763` zunächst angelegt, nach Nutzerentscheidung nicht mehr verwendet. Ein Name-Feld, E-Mail, Nachricht, Honeypot. Kein Versand einer Testnachricht durch den Agenten.
- Nutzer hat ausdrücklich die kostenlose gemeinsame Nutzung des vorhandenen Portfolio-Endpunkts gewählt. Aktiv ist daher `https://usebasin.com/f/ff509d632e80` (Formular 75327). `form_source=Pfäffikersee – Kontakt` und `site_source=pfaeffikersee.org` kennzeichnen Anfragen. Das neu angelegte Formular 75385 wird nicht verwendet; vor Ende der Testphase aufräumen. Die neue Empfänger-Verifizierung dafür ist für den gemeinsamen Endpunkt nicht erforderlich. Zustellung vor dem Domainumzug mit dem Nutzer testen.
- GoatCounter: https://pfaeffikersee.goatcounter.com separat angelegt. Domain gesetzt; Dashboard privat; individuelle Seitenaufrufe deaktiviert. Bestehende Datenschutzeinstellungen vom Portfolio übernommen. Konto zeigt noch E-Mail-Verifizierung an; Nutzer darauf hingewiesen.
- Basin zeigt noch 12 Tage Premium-Testphase. Der [kostenlose Tarif](https://usebasin.com/pricing) erlaubt einen Endpunkt und 50 Einsendungen/Monat. Gewählte Lösung: gemeinsamer bestehender Endpunkt, daher kein neues Abo. Nicht mehr benötigtes Formular 75385 vor Ende der Testphase entfernen (dauerhafte Löschung nur nach Bestätigung).

## Prüfergebnisse
- `npm run build`: 11 HTML-Seiten erfolgreich gebaut; `npm install`: keine gemeldeten Sicherheitslücken.
- `python3 scripts/check-site.py`: URLs, lokale Links/Bilder, genau ein H1, Canonical-Domain, keine aktiven iframes vor Klick, keine Squarespace-Abhängigkeiten und noindex geprüft.
- Original-Textblöcke mit gebautem Inhalt abgeglichen. Nur offensichtliche Tippfehler korrigiert und Datenschutzerklärung bewusst aktualisiert.
- Vier ungültige Quellen-URLs schon im Original erkannt und korrigiert (Markdown fälschlich im Linkziel bzw. Bildcredit anstelle einer Lizenz-URL).
- Mobile Navigation öffnen/schliessen, Bilddialog öffnen/schliessen, Karte nach Klick und aktualisierten YouTube-Player geprüft. Keine horizontale Überbreite auf den geprüften Mobilseiten.

## Vor Domainumzug zwingend
- [ ] Nutzer bestätigt lokale Vorschau und gibt Domainumzug ausdrücklich frei.
- [ ] Basin- und GoatCounter-E-Mail-Verifizierung abgeschlossen; Kontaktformular-Zustellung mit Nutzer getestet; Basin-Tarif nach Testphase geklärt.
- [ ] Bestehende DNS-Einträge bei Hosttech sichern; Mail/MX/TXT unverändert lassen.
- [ ] GitHub Pages Deployment einrichten, Custom Domain setzen, korrekte IDNA/Punycode-Schreibweise verwenden.
- [ ] Beim Domainumzug Indexierung und GoatCounter aktivieren, Build erneut prüfen.
- [ ] Apex und www, HTTPS, Canonical-URLs, alle zehn Routen, robots.txt und Sitemap auf der öffentlichen Domain prüfen.
