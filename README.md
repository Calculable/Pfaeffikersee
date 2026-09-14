# pfäffikersee.org

## Lokal starten

Voraussetzung: Node.js 24 und npm.

```sh
npm ci
npm run dev -- --host 127.0.0.1 --port 4340
```

Die Vorschau läuft unter http://127.0.0.1:4340/.

## Build und Vorschau

```sh
npm run build
npm run preview
```

Der Build liegt in `dist/`.

## Veröffentlichen

Änderungen lokal prüfen, committen und in `main` zusammenführen. Ein Push auf `main` veröffentlicht die Website automatisch über GitHub Pages:

```sh
git push origin main
```

Website: https://www.pfäffikersee.org/
