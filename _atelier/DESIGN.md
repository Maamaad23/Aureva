---
title: AUREVA Freight · Design System
platform: web
stack: HTML/CSS/JS (single-file, no build)
updated: 2026-10-17
---

# Design System

Source de vérité de la charte AUREVA. Les documents (plaquette, PowerPoint, convention, papier à lettre, signature) dérivent de ce fichier.

## Color

**Strategy**: Committed. Le navy porte toute la surface, l'or est l'unique accent identitaire (10 à 15 %). Le bloc contact est le seul aplat or (moment « drenched »).

| Token | Value | Role |
|-------|-------|------|
| `--ink-0` | `oklch(15% .03 250)` ≈ `#050D16` | Fond le plus profond : nav pleine, sections alternées, footer |
| `--ink-1` | `oklch(21% .04 250)` ≈ `#0D1B2A` | Surface principale |
| `--ink-2` | `oklch(25.5% .042 250)` | Surface élevée (formulaire) |
| `--gold` | `oklch(74% .115 85)` ≈ `#C9A84C` | CTA, kickers, accents |
| `--gold-hi` | `oklch(82% .105 85)` | Survol, liens sur fond sombre |
| `--paper` | `oklch(96% .012 85)` | Texte principal |
| `--paper-2` | `oklch(83% .015 85)` | Texte secondaire |
| `--paper-3` | `oklch(70% .018 85)` | Métadonnées, légendes (AA sur ink-0/ink-1) |
| `--line` / `--line-strong` | paper à 14 % / 28 % | Filets |

Jamais de `#000` ni de `#fff`. Toutes les couleurs passent par les tokens.

## Typography

| Role | Family | Size |
|------|--------|------|
| Display, titres, valeurs | **Marcellus** (400 uniquement, capitales romaines gravées) | h1 `clamp(2.75rem → 5.5rem)`, h2 `clamp(2.125rem → 3.625rem)`, h3 `clamp(1.375rem → 1.625rem)` |
| Texte, UI, étiquettes | **Hanken Grotesk** 400 / 500 / 600 (police variable) | corps 17px, lead `clamp(19 → 22px)`, étiquettes 13px min |

- Étiquettes : Hanken 600, majuscules, interlettrage .12 à .14em, or.
- Pas d'italique décoratif, pas de police mono, `font-synthesis:none` (Marcellus n'a pas de gras).
- Aucun texte sous 12px.
- Polices hébergées dans `fonts/` (woff2 latin) et préchargées : aucune requête vers Google.

## Logo

Fichiers dans `Logo/exports/` (copie web dans `Images/`) :

| Fichier | Usage |
|---------|-------|
| `aureva-mark-dark` | Aile or + trait crème, pour fond sombre (nav, favicon) |
| `aureva-mark-light` | Aile, couleurs d'origine, pour fond clair |
| `aureva-logo-dark` | Logo complet, AUREVA crème + Freight or, fond sombre |
| `aureva-logo-light` | Logo complet d'origine, fond transparent, fond clair (impression) |

Sur le site, le nom « AUREVA / Freight » est écrit en texte (Marcellus + Hanken), à côté de l'aile.

## Signature visuelle

- **Bandeau « lettre de transport »** (`.awb`) : champs numérotés 01 à 04, filets fins, valeur en Marcellus. Repris du formulaire LTA.
- **Tableaux Solari** (`.board`, `.flap`) : Départs (BSL, LYS, SXB, ZRH) et Arrivées par région, choisies avec des onglets illustrés (`.rtab`). Les tuiles défilent à l'apparition et à chaque changement d'onglet.
- **Frise de la chronologie** (`.chrono`) : 9 étapes alternées Vous (gauche) / AUREVA (droite, fond `--ink-2`, numéro or). La ligne or se trace au défilement et chaque étape s'allume au passage.
- **Vidéos** : boucle muette « Le voyage » en fond de hero (sans texte), film sous-titré de 29 s dans la chronologie (FR / EN / DE, logo + carte finale).

## Spacing & layout

- Échelle 4pt : `--s-1` 4px … `--s-10` 144px. Sections `--s-10` (desktop) / `--s-9` (mobile).
- Conteneur `--max` 78rem, gouttière `clamp(1.25rem, 4vw, 3.5rem)`.
- Compositions asymétriques (7/5, 5/7), sections alternées ink-1 / ink-0.

## Motion

- Easing `cubic-bezier(.16,1,.3,1)`. Pas de rebond. Transform et opacity uniquement.
- Hero : titre révélé ligne par ligne, puis texte et CTA ; profondeur au défilement (contenu qui remonte et s'efface, vidéo qui avance légèrement).
- Titres h2 : révélation de bas en haut (`clip-path`). Images : ouverture du cadre + léger recul.
- Barre de progression or sous la navigation. Reflet sur les boutons or au survol. Défilé continu des compagnies (pause au survol).
- Tout est sous `.js`, posé seulement si `prefers-reduced-motion` n'est pas actif : sinon contenu visible d'emblée, vidéos non chargées.

## Interdits

Bordures latérales décoratives, texte en dégradé, effet verre, chiffres-vitrines, grilles de cartes identiques, tirets longs dans le texte, police mono comme déguisement « technique ».

## Interrupteur IATA

`<html data-iata="obtenu">` affiche les mentions IATA / HUM ; `data-iata="en-cours"` les masque et affiche « Agrément IATA en cours ». Classes : `.iata-only`, `.iata-wait`.

## Direction artistique (2026-10-22)

- **Or réservé** aux boutons, au slogan, aux étapes AUREVA, aux routes de la carte et aux états actifs. Surtitres, numéros secondaires et libellés passent en tons papier.
- **Peu de cadres** : les blocs tiennent par l'espace et les fonds. Pas de bordure autour du film, des tableaux, des garanties ni des compagnies.
- **Une seule section claire** : `#garanties` (fond papier, tokens inversés localement), lue comme un document officiel.
- **Chronologie** en tableau de route compact (numéro · qui · étape · détail), plus de zigzag.
- **Photos** : étalonnage commun (`saturate(.78)`) + grain léger, en attendant de vraies photos (bureau, plaque, tarmac BSL).
