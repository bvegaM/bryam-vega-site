# bryamvega.com

Personal site — essays, talks, series, and about (with downloadable profile PDF). Bilingual (EN/ES). Built with [Astro 5](https://astro.build).

## Run locally

```bash
npm install
npm run dev          # http://localhost:4321
npm run build        # static output to ./dist
npm run preview      # serve ./dist
```

Requires Node 18.17+ or 20+.

## Site map

| Path                         | What it is                                                |
|------------------------------|------------------------------------------------------------|
| `/`                          | EN home — hero, identity stack, "Now", series map, talks  |
| `/blog/`                     | EN essays index (post cards with hero images)             |
| `/blog/[slug]/`              | EN essay                                                   |
| `/series/`                   | EN — all series, each with its posts                      |
| `/talks/`                    | Talks (bilingual)                                         |
| `/about/`                    | EN about + full profile PDF                               |
| `/es/...`                    | Spanish mirror of all of the above                        |

## Adding content

### A new essay
Drop a `.md` into `src/content/blog/` (single folder for both languages — separated by the `lang` field):

```yaml
---
title: "Your title"
description: "Short description (used for OG, listing, and meta description)"
pubDate: 2026-01-15
tags: ["tag1", "tag2"]
series: "Skill-Driven Development"   # must match a name in src/i18n/series.ts
lang: "en"                            # "en" or "es"
heroImage: "/images/blog/your-image.jpg"   # optional, place under public/images/blog/
heroImageCaption: "Optional caption"
draft: false
canonical: "https://other-site.com/post"   # optional, only if originally published elsewhere
---
```

If `heroImage` is omitted, the post card renders an emerald initial-letter fallback.

### A new talk
Drop a `.md` into `src/content/talks/`:

```yaml
---
title: "Talk title"
event: "Conference name"
location: "City, Country"
date: 2026-04-29
status: upcoming      # upcoming | delivered | proposed
language: en          # en | es
abstract: "Short abstract"
slides: "https://..."     # optional
video:  "https://..."     # optional
eventUrl: "https://..."   # optional
---
```

### A new series
Edit `src/i18n/series.ts` and add an entry. Posts are joined to a series by matching the
`series` frontmatter to the series `name`.

## Internationalization

- All UI strings live in `src/i18n/ui.ts`
- Helpers (lang detection, translation, locale-aware URLs, date formatting) in `src/i18n/utils.ts`
- Default locale is English with no prefix; Spanish is at `/es/`
- Each EN page has a Spanish mirror under `src/pages/es/`
- The language switcher in the header preserves the current path when switching

## Design notes

- Type pairing: **Instrument Serif** (display, italic accents) + **Source Serif 4** (body) + **JetBrains Mono** (mono / labels / metadata)
- Palette: warm paper (`#F5F1E8`) with deep emerald accent (`#0A6E4E` light / `#34D399` dark) — botanical / old-book / jeweled
- All colors are CSS variables in `src/styles/global.css` — change `--accent`, `--accent-2`, `--accent-soft` to retheme without touching components
- Code blocks use Shiki with the `vesper` theme — change in `astro.config.mjs`
- Light/dark via `prefers-color-scheme` + persistent toggle in the header (`localStorage`)

## Deploy to Cloudflare Pages

1. Push this repo to GitHub.
2. Cloudflare dashboard → **Workers & Pages** → **Create** → **Connect to Git**.
3. Build settings:
   - **Framework preset**: Astro
   - **Build command**: `npm run build`
   - **Build output directory**: `dist`
   - **Environment variable**: `NODE_VERSION=20`
4. Deploy. Subsequent pushes to `main` redeploy automatically.
5. Add your custom domain under **Custom domains**.

Update `site:` in `astro.config.mjs` to your final domain so canonical URLs and the sitemap are correct.

## Deploy to Vercel (alternative)

Run `vercel --prod` from the project root, or import the repo via the Vercel dashboard. Astro is auto-detected.
