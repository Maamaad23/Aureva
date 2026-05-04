# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Static single-page site for **AUREVA Freight** — B2B international funeral air freight specialist (France → Sub-Saharan Africa & Maghreb). French language throughout. Deployed via GitHub Pages.

## Stack

- Pure HTML/CSS/JS — no build system, no npm, no framework
- Single file: `index.html` (all CSS inline in `<style>`, all JS inline in `<script>`)
- Assets: `Images/` directory (PNG, WebP)
- Deploy: push to `main` → GitHub Pages serves `index.html`

## Design system

| Token | Value |
|-------|-------|
| `--navy` | `#0D1B2A` |
| `--gold` | `#C9A84C` |
| `--cream` | `#F7F4EE` |
| `--text` | `#1a1a18` |
| `--muted` | `#4d4c44` |
| Max width | `1160px` (var `--W`) |

Fonts: `Cormorant Garamond` (headings, serif, weight 300–500) + `Outfit` (UI, sans-serif, weight 300–700).

## Page structure (sections in order)

1. `#nav` — sticky nav, mobile burger menu
2. `#hero` — full-viewport with parallax bg (`Embarquement.png`)
3. Ticker — infinite scroll marquee (navy bg, gold text)
4. `#histoire` — split layout (text left, images right)
5. `#aeroports` — airport badges grid + split image (`Africa.png`)
6. `#distingue` — IATA featured card + 6 advantage cards
7. Tarmac quote section — full-bleed dark bg (`Tarmac.png`)
8. `#contact` — two-column: info left, `mailto:` form right
9. Copyright strip

## Patterns

**Scroll reveal**: add `.rev` (fade up), `.rev-l` (fade left), `.rev-r` (fade right) + `.d1`–`.d5` stagger delays. IntersectionObserver in `<script>` handles `.on` class toggle.

**Buttons**: `.btn` base + modifier (`.btn-gold`, `.btn-navy`, `.btn-outline-navy`, `.btn-outline-gold`).

**Kicker labels**: `.kicker` (gold) / `.kicker.dark` (navy) / `.kicker.center` (adds line on both sides).

**Airport badges**: `.aero-badge` (dark) + `.aero-badge.home` (highlighted, for CDG/BSL home airports).

## Audience & tone

B2B only — funeral homes (*pompes funèbres*), not families. Copy is direct, dignified, professional. IATA certification and HUM operator status are primary trust signals. Islamic rites compliance is a key differentiator.

## Placeholder to fill

- Phone number: `href="tel:+33XXXXXXXXX"` in nav (line ~804)
- Form uses `mailto:support@aurevafreight.com` — no backend
