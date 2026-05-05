# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Static multi-page site for **AUREVA Freight** — B2B international funeral air freight specialist (France → Sub-Saharan Africa & Maghreb). French language throughout. Deployed via GitHub Pages at `aurevafreight.com`.

## Stack

- Pure HTML/CSS/JS — no build system, no npm, no framework
- All CSS + JS inline inside each HTML file
- Assets: `Images/` directory (WebP primary, PNG originals kept locally)
- Deploy: push to `main` → GitHub Pages → `aurevafreight.com`
- Analytics: Plausible (`data-domain="aurevafreight.com"`, deferred)
- Form: Formspree AJAX (`https://formspree.io/f/mvzlovrr`) — not mailto

## Files

| File | Role |
|------|------|
| `index.html` | Main landing page — all sections |
| `mentions-legales.html` | Legal page (LCEN + RGPD + cookies) |
| `plaquette-aureva.html` | Downloadable presentation (HTML) |
| `plaquette-aureva.pdf` | Downloadable presentation (PDF, 411KB) |
| `DESIGN.md` | Full design system reference |
| `PRODUCT.md` | Brand strategy, audience, anti-references |
| `robots.txt` | `Allow: /`, `Disallow: /Images/` |
| `sitemap.xml` | index + mentions-legales, lastmod 2026-05-05 |

## Design system

| Token | Value | Use |
|-------|-------|-----|
| `--void` | `#050D16` | Deepest bg (hero overlay, nav) |
| `--navy` | `#0D1B2A` | Primary surface — body, cards |
| `--navy2` | `#122030` | Elevated surfaces |
| `--gold` | `#C9A84C` | Accent — CTAs, labels, em |
| `--gold2` | `#A8892A` | Gold pressed state |
| `--gold-hi` | `#E2C06E` | Gold hover |
| `--cream` | `#F5F1E8` | Primary text |
| `--mist` | `rgba(245,241,232,.72)` | Secondary text |
| `--ghost` | `rgba(245,241,232,.12)` | Hairline borders |
| `--W` | `1160px` | Max content width |
| `--mono` | `'JetBrains Mono',monospace` | Labels, UI |

**Fonts**: `Fraunces` (display/headings, weight 200–400, italic variants) + `Karla` (body, weight 300) + `JetBrains Mono` (labels, badges, nav links, 9–10px).

**Body background**: `#0D1B2A` (explicit hex, not CSS var — scanner compatibility).

## Page structure (index.html, sections in order)

1. `#nav` — sticky 68px, `rgba(5,13,22,.9)` bg + blur, logo + IATA badge + desktop nav links + LinkedIn icon + mobile burger
2. Mobile overlay — full-screen, Fraunces italic links, Escape/click-link closes
3. `#hero` — 100svh, `Embarquement.webp` parallax bg, animated flight-path SVG (BSL→Afrique), H1 word-by-word stagger on load
4. Ticker — infinite marquee, navy bg, gold text
5. `#histoire` — split layout (text left, images right), blockquote, islamic-sep ornament, hist-creds with counter animation (10+)
6. `#distingue` — IATA featured card + 6 `.dcard` advantage cards (urgency underline on "24 à 48h" in card 03)
7. `#aeroports` — departure board with stagger reveal + split image (`Departflight.webp`)
8. Afrique section — `Africa.webp` full-bleed + 10 destination country flags
9. Déroulement cargo — 3 image columns (`FlightDepart.webp`, `Cargo.webp`, `fenetre.webp`)
10. Tarmac quote — `Plume.webp` full-bleed, character-by-character blockquote reveal
11. Islamic ornament separator (before contact)
12. `#contact` — 2-col grid: info left (AUREVA logo + IATA badge side-by-side, `.ci-brand-row`), Formspree form right
13. Copyright strip

## Animation system

| Class/mechanism | Behaviour |
|-----------------|-----------|
| `.rev` | Fade-up on scroll (translateY 18px → 0, 900ms ease-out-quart) |
| `.rev-l` / `.rev-r` | Fade left/right (translateX ±22px) |
| `.d1`–`.d5` | Stagger delays .1s–.5s |
| `.board-reveal` | Left-slide stagger on departure board rows (nth-child delays 0–.49s) |
| `.hero-w` | H1 word stagger on page load (CSS `--d` var per word, .08s–.67s) |
| `.islamic-sep` | Gold geometric ornament (2 crossed squares), fade in on scroll, 50s rotation |
| `.urgency-txt::after` | Gold underline draws under "24 à 48h" when card enters viewport |
| `.hist-cred-n.flashed` | `cred-flash` keyframe — gold glow on IATA/7j/7; counter 0→10 on "10+" |
| `.tarmac-char` | Character-by-character blockquote reveal |
| Flight path SVG | `stroke-dashoffset` draw animation (2.8s, 300ms delay) |
| Hero spotlight | Radial gradient follows cursor (lazy lerp) |

All animations respect `prefers-reduced-motion: reduce`.

IO observer: `document.querySelectorAll('.rev,.rev-l,.rev-r,.board-reveal,.islamic-sep')` — threshold `.08`, rootMargin `0px 0px -32px 0px`.

## Images (Images/ directory)

| File | Usage | Size |
|------|-------|------|
| `Embarquement.webp` | Hero CSS background | 163KB |
| `Africa.webp` | Afrique section full-bleed | 121KB |
| `Cargo.webp` | Déroulement cargo card | 151KB |
| `Plume.webp` | Tarmac quote bg | 45KB |
| `Coran.webp` | Histoire overlay | 72KB |
| `volafrique.webp` | Histoire main image | 81KB |
| `Departflight.webp` | Aéroports split | 114KB |
| `FlightDepart.webp` | Déroulement card | 68KB |
| `fenetre.webp` | Déroulement card | 83KB |
| `IATA-ANUBIS.webp` | IATA badge (nav + hero + contact) | 21KB |
| `LogoAureva_transparent.png` | Logo (PNG — favicon + img) | 148KB |
| `og-image.jpg` | OG/Twitter share 1200×630 | 169KB |

PNG originals kept locally (not served). Do NOT delete WebP files.

## Patterns

**Labels**: `.label` — JetBrains Mono, 10px, .18em tracking, gold, `::before` gold hairline. `.label.center` adds `::after` line too.

**Buttons**: `.btn` + `.btn-gold` / `.btn-outline`. Active: `scale(.97)`. Hover lifts `translateY(-2px)`.

**Form fields**: `.f-in` — gold-tinted border, focus glow. `maxlength` set on all fields.

**Form state**: `.f-form-wrap.hide` + `.f-success.show` — inline success. Plausible goal `plausible('Contact')` fires on success.

**Contact brand row**: `.ci-brand-row` — AUREVA logo (38px) + gold hairline separator + IATA logo (38px), side-by-side.

**Islamic ornament**: `.islamic-sep` with two SVG `<rect>` rotated 0°/45° = 8-pointed star geometry. Used twice: after histoire blockquote, before contact section.

**Board rows**: `.board-row.board-reveal` inside `.board-rows` — nth-child CSS delays trigger sequential stagger when all `.on` simultaneously.

## Legal (mentions-legales.html)

Contains: Éditeur (AUREVA SAS), SIREN (102 873 577), TVA (FR14102873577), Dir. publication (AUREVA SAS), email, Hébergeur (GitHub San Francisco). No personal names, no street address — intentional.

## Placeholders remaining

- Phone number: not yet added (operational — when ready, add `href="tel:+33..."` in nav + contact section)

## What is frozen (do not restructure)

Content, section order, design tokens, Formspree endpoint, Plausible domain. Animations may be extended. Images may be replaced with better versions (keep WebP format, same filenames).
