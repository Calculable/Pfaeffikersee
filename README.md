# pfäffikersee.org

Eine statische Astro-Website über den Pfäffikersee. Migration von Squarespace; siehe [MIGRATION.md](MIGRATION.md) für Anforderungen, Fortschritt und Freigaben.

## Lokal ansehen

Node.js 24 oder neuer installieren, dann im Projektordner:

```sh
npm ci
npm run dev -- --host 127.0.0.1 --port 4340
```

Die Vorschau läuft unter http://127.0.0.1:4340/.

```sh
npm run build
python3 scripts/check-site.py
```

`dist/` enthält die fertig gebaute Website. Der Ordner wird bei jedem Build neu erstellt und nicht in Git gespeichert.

## Inhalte bearbeiten

- `src/content/pages/<seite>/index.md`: Texte, Bilder und Metadaten einer Seite.
- `path` am Dateianfang bestimmt die URL unabhängig vom Ordnernamen. Bestehende Werte beibehalten.
- `heading`: sichtbarer Seitentitel; `title`: Titel für Browser und Suchmaschinen.
- `image`: Titelbild; `description`: vorhandene SEO-Beschreibung. Die Quelle enthielt meist keine Beschreibung; diese wurde nicht erfunden.
- `src/content/pages/home/links.md`: weiterführende Links auf der Startseite.
- `src/content/projects.json`: Themenkarten der Startseite, Reihenfolge und Texte.
- `public/media/`: lokal gespeicherte Bilder. Verwendete Pfade beginnen mit `/media/`.
- `src/site.ts`: Navigation, Domain, Basin- und GoatCounter-Endpunkt sowie Suchmaschinenfreigabe.
- `src/styles/site.css`: gemeinsames Layout und Gestaltung.

Ein Bild mit Bildunterschrift lässt sich so schreiben:

```md
![Beschreibung des Bildes](/media/beispiel.jpg)

_Bildunterschrift mit [Bildquelle](https://example.org)._
```

Ein kleiner Markdown-Baustein macht daraus automatisch eine Abbildung mit dezenter, zentrierter Bildunterschrift. Für die Galerie wird das Bild zusätzlich verlinkt:

```md
[![Beschreibung](/media/beispiel.jpg)](/media/beispiel.jpg)
```

Für Karten und Videos bleiben kleine HTML-Platzhalter im Markdown. Die eigentliche Einbettung entsteht erst nach einem Klick. Das braucht weder Squarespace noch eine zusätzliche JavaScript-Bibliothek.

## Migration und Veröffentlichung

`migration/assets.json` ordnet die ursprünglichen Bild-URLs den lokalen Dateien zu. `migration/source/` enthält das lokale Quellenarchiv und wird **nicht** auf GitHub hochgeladen. Die einmaligen Import-Skripte dürfen nicht über bearbeitete Markdown-Inhalte ausgeführt werden.

Die Website wird unter https://www.pfäffikersee.org veröffentlicht. Änderungen auf `main` werden durch GitHub Actions gebaut und automatisch auf GitHub Pages bereitgestellt. Für Änderungen einen Arbeitsbranch verwenden, lokal prüfen und danach in `main` zusammenführen.

`indexable: true` in `src/site.ts` aktiviert Suchmaschinenfreigabe, öffentliche Sitemap und GoatCounter. Die 404-Seite bleibt von Suchmaschinen ausgeschlossen. Domain und Mail-Einstellungen werden weiterhin bei Hosttech verwaltet.

Basin: https://usebasin.com/app/forms/75327/form_setup (gemeinsam mit Portfolio; Kennzeichnung durch `site_source` und `form_source`)

GoatCounter: https://pfaeffikersee.goatcounter.com

Bildrechte und Quellenangaben stehen weiterhin auf den jeweiligen Inhaltsseiten. Die Fotos sind nicht pauschal unter einer neuen Lizenz veröffentlicht.
