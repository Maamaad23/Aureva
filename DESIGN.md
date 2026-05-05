---
title: AUREVA Freight — Design System
platform: web
stack: HTML/CSS/JS (single-file, no build)
scan_date: 2026-05-05
---

# Design System

## Color

**Strategy**: Committed — navy carries the surface, gold is the single identity accent (~10–15% usage).

| Token | Value | Role |
|-------|-------|------|
| `--void` | `#050D16` | Deepest backgrounds (hero overlay, nav bg, void) |
| `--navy` | `#0D1B2A` | Primary surface — body, cards, sections |
| `--navy2` | `#122030` | Elevated surfaces, subtle section separation |
| `--gold` | `#C9A84C` | Brand accent — CTAs, labels, active states, em |
| `--gold2` | `#A8892A` | Pressed/active gold state |
| `--gold-hi` | `#E2C06E` | Hover state on gold elements |
| `--cream` | `#F5F1E8` | Primary text color on dark surfaces |
| `--mist` | `rgba(245,241,232,.72)` | Secondary text, subdued labels |
| `--ghost` | `rgba(245,241,232,.12)` | Hairline borders, dividers |

**Dark theme**: permanent. Navy deep background, cream text, gold accent. No light mode.

**Contrast compliance**: All body text `--cream` on `--navy` passes WCAG AA (≥4.5:1).

## Typography

| Role | Family | Weight | Size | Notes |
|------|--------|--------|------|-------|
| Display / Hero | Fraunces (serif) | 200–300 | clamp(52px,7vw,88px) | Optical sizing auto, line-height 1.02 |
| H2 section | Fraunces (serif) | 300 | clamp(36px,5vw,58px) | line-height 1.05 |
| H3 | Fraunces (serif) | 300 | clamp(20px,2.5vw,28px) | |
| Body | Karla (sans) | 300 | 16px | line-height 1.85, max 65ch |
| Labels / UI | JetBrains Mono | 500 | 9–10px | letter-spacing .16–.18em, uppercase |
| Monospace data | JetBrains Mono | 400 | 9px | airport codes, metadata |

**Scale rules**: Fraunces for anything expressive/emotive. Karla for body prose. JetBrains Mono exclusively for labels, badges, navigation links, and data fields.

**`em` tags**: italic + gold (`color:var(--gold)`) — emphasis is tonal, never bold.

## Spacing

| Step | Value | Use |
|------|-------|-----|
| Section padding | 108px top/bottom | `.sec` (desktop) |
| Section padding | 80px | 860px breakpoint |
| Section padding | 64px | 560px breakpoint |
| Wrap | `max-width:1160px`, `padding:0 5%` | `.wrap` / `.sec-inner` |
| Card gap | 24–32px | grid gaps |
| Label bottom | 20px | `.label` margin-bottom |

## Components

### Navigation (`#nav`)
- Sticky, 68px height (60px mobile)
- Background: `rgba(5,13,22,.9)` + `backdrop-filter:blur(24px)`
- Border bottom: `1px solid rgba(201,168,76,.07)` → `.scrolled` → `.14`
- Brand: logo (52px) + separator + brand name + IATA badge
- Links: JetBrains Mono, 9px, `.16em` tracking, `rgba(cream,.55)` → gold on hover
- Mobile: burger animates to X; full-screen overlay with Fraunces italic links (clamp 32–56px)

### Buttons (`.btn`)
- Base: `font-family:var(--mono); font-size:10px; letter-spacing:.18em; padding:15px 36px`
- `.btn-gold`: `background:var(--gold); color:var(--void)`; hover lifts `translateY(-2px)` + `--gold-hi`
- `.btn-outline`: transparent, `border:1px solid var(--ghost)`; hover → gold border + gold text
- Active: `scale(.97)` on all

### Labels (`.label`)
- JetBrains Mono, 10px, 500 weight, `.18em` tracking, uppercase, gold
- `::before` — 20px gold hairline rule
- Acts as section kicker above every heading

### Reveal animations
- `.rev`: fade-up (translateY 18px → 0, opacity 0 → 1), 900ms ease-out-quart
- `.rev-l` / `.rev-r`: fade-left / fade-right (translateX ±22px)
- Stagger delays: `.d1`–`.d5` (.1s–.5s increments)
- Triggered by IntersectionObserver adding `.on`

### Cards (`.d-card` / `.faq-item`)
- No box-shadows as primary decoration
- Dark cards: `background:var(--navy2)` or `var(--void)`; border `1px solid var(--ghost)`
- Hover: `translateY(-4px)` + border brightens to `rgba(gold,.2)`
- IATA featured card: `border:1px solid rgba(gold,.25)`, horizontal layout, premium variant

### FAQ Accordion
- `grid-template-rows: 0fr → 1fr` (layout-safe, no max-height hack)
- Transition: `.45s cubic-bezier(.23,1,.32,1)`
- Inner content: `min-height:0; overflow:hidden`

### Airport Badges (`.aero-badge`)
- JetBrains Mono, dark background, border
- `.home` variant: gold-tinted border, slightly higher opacity

## Motion

- **Easing**: `cubic-bezier(.16,1,.3,1)` (ease-out-quart) throughout
- **Scroll reveals**: 900ms, stagger up to 500ms
- **Hover lifts**: 160ms ease-out, `translateY(-2px)` or `-4px`
- **Mobile menu**: opacity + visibility 400ms ease-out-quart; link items stagger 80–260ms
- **Flight path SVG**: stroke-dashoffset draw, 2.8s, 300ms delay
- No bounce, no elastic, no spring physics
- `prefers-reduced-motion` respected via IntersectionObserver (no JS animation, only CSS transitions)

## Layout

- Single-column narrative scroll
- Max width `1160px` (var `--W`), centered, 5% side padding
- Split layouts (histoire, contact): `grid-template-columns: 1fr 1fr` → single column ≤860px
- Section backgrounds alternate: navy / void / navy to create rhythm without heavy borders
- Full-bleed image sections (hero, tarmac): `position:relative` + absolute overlay gradient

## Imagery

| Asset | Usage |
|-------|-------|
| `Embarquement.png` | Hero background — airport tarmac, aircraft |
| `Africa.png` | Aéroports section — continent map split |
| `Tarmac.png` | Mid-page quote section — full-bleed dark |
| `histoire-*.jpg` | Notre histoire — split image stack |
| `LogoAureva_transparent.png` | Nav + contact logos |
| `IATA_logo.png` | Nav IATA badge |

**Overlay convention**: `linear-gradient(110deg, rgba(void,.97) 0%, .88 48%, .28 100%)` for left-heavy text overlays + bottom fade `linear-gradient(to top, rgba(void,.98) 0%, transparent 38%)`.

## Breakpoints

| Breakpoint | Behavior |
|------------|----------|
| `≤900px` | Nav links hidden → burger + mobile overlay |
| `≤860px` | Section padding 108→80px; split layouts → single column |
| `≤768px` | Hero flight SVG opacity .22 |
| `≤560px` | Section padding 64px; font sizes floor to clamp minimum |

## Accessibility

- WCAG 2.1 AA target
- Focus: `outline:1px solid var(--gold); outline-offset:4px` on `:focus-visible`
- Mobile menu: `aria-expanded`, `aria-controls`, `aria-hidden` wired
- Escape key closes mobile overlay
- `lang="fr"` on `<html>`
- Semantic headings: h1 in hero, h2 per section, h3 for cards
