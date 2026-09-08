# Slidev presentation

This directory contains the Slidev presentation for the corporate-insolvency
demonstration.

## Requirements

- Node.js 18 or later
- npm

## Run locally

```bash
npm install
npm run dev
```

Slidev starts a local development server and opens the presentation in a
browser. Changes to `slides.md` are reflected automatically.

## Build

```bash
npm run build
```

The static presentation is written to `dist/`.

## Export

```bash
npm run export
```

Slidev may prompt to install its browser dependency the first time a PDF is
exported.

## Files

| File | Purpose |
|---|---|
| `slides.md` | Slidev presentation entry point |
| `presentation.md` | Original narrative draft |
| `package.json` | Slidev dependencies and npm scripts |
