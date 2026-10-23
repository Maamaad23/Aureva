# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Project

Site vitrine B2B d'**AUREVA Freight** (transport aérien funéraire France → toute l'Afrique). Site en FR / EN / DE (le français est la source). Cible : pompes funèbres. Déploiement via GitHub Pages (`maamaad23/Aureva`), domaine `aurevafreight.com`.

Agrément IATA et commissionnaire de transport **obtenus** (confirmé le 2026-10-17) : `data-iata="obtenu"`. L'interrupteur reste en place.

## Stack

- HTML/CSS/JS pur, tout inline, aucun build
- Fonts : Marcellus (display) + Hanken Grotesk (texte), hébergées dans `fonts/` et préchargées (plus de Google Fonts : CLS 0, RGPD)
- Images : `Images/*.webp` (variantes réduites en srcset, WebP qualité ~62). Images de partage `Images/og-image(-en|-de).jpg` 1200×630, faites à partir de `photo-piste.webp`.
- Photos : uniquement des photos réelles (Unsplash, crédits dans `mentions-legales.html`), jamais d'image IA. Hero = `Images/photo-piste.webp` (préchargée). Vidéo hero et film retirés le 2026-10-22 (archivés dans `_atelier/prive/videos-retirees/`, le film sert pour LinkedIn / WhatsApp).
- SEO : H1 = mot-clé (« Rapatriement de défunts vers l'Afrique… »), slogan en `.hero-title`. JSON-LD Organization + Service + FAQPage (garder synchro avec la FAQ visible). `llms.txt` à la racine.
- Formulaire : Formspree AJAX `https://formspree.io/f/mvzlovrr`, objectif Plausible `Contact` au succès
- Analytics : Plausible (sans cookie)

## Files

| File | Role |
|------|------|
| `index.html` | Page unique |
| `mentions-legales.html` | LCEN + RGPD + cookies (aucun nom de personne, volontaire) |
| `_atelier/DESIGN.md` | Charte complète : tokens, typo, logo, motifs, interdits |
| `_atelier/PRODUCT.md` | Cible, ton, anti-références |
| `fiche-reflexe-aureva.pdf` | Copie de `Marketing/Kit commercial/AUREVA_Fiche_Reflexe.pdf` (téléchargeable sur le site) |
| `plaquette-aureva.pdf` | Copie de `Marketing/Kit commercial/AUREVA_Plaquette.pdf` (téléchargeable sur le site) |
| `js/lenis-1.3.26.min.js` | Défilement fluide (MIT, hébergé ici), chargé seulement à la souris, jamais si mouvement réduit |
| `_atelier/` | Outils internes, hors site : `i18n/` (traductions), `carte/build-map.mjs` (régénère la carte SVG, à recoller dans index.html), `DESIGN.md`, `PRODUCT.md`, `prive/` (hors git : `engagement-futur.html` à remettre avec preuves, `videos-retirees/` films courts FR / EN / DE pour LinkedIn et WhatsApp). Jamais publié : `_config.yml` laisse Jekyll écarter les dossiers en `_` (ne pas remettre `.nojekyll`) |

## Structure de index.html

Nav (+ barre de progression) → Hero (photo réelle, une phrase, bandeau `.awb` en 3 cases) → 01 Fonctionnement (3 étapes en photo `.steps`, détail en 9 étapes dans `<details class="chrono-more">`) → 02 Destinations (question « Où doit reposer le défunt ? » qui remplit une carte d’embarquement BSL → code d’arrivée en tuiles animées, phrase de réponse, choix de l’aéroport si le pays en a plusieurs, lien qui préremplit le contact ; pays cliquables par région ; carte de toutes les routes avec avion sur la route choisie ; la recherche accepte tout pays du monde (noms via Intl.DisplayNames, aéroports principaux des pays les plus demandés dans `WORLD`) ; tableau des compagnies `.board` façon panneau des départs, codes en tuiles et noms qui se posent lettre à lettre) → 03 Garanties (interrupteur IATA) → 04 Partenaires (`#partenaires` : 3 avantages, fiche réflexe `fiche-reflexe-aureva.pdf` à télécharger (objectif Plausible `Fiche`, aussi dans le haut de page, la FAQ et le contact), bouton « Recevoir la convention » qui préremplit le contact ; la convention n'est pas publiée, elle porte un nom de dirigeant et la commission) → 05 À propos (`#nous` : scène `.cine` collante, on traverse le hublot `photo-hublot` en défilant pendant que la phrase `.statement` s'éclaire, puis « Avant de nous confier un défunt » : récit court + 8 questions de pompe funèbre (qui, vérifier avec SIREN et lien Annuaire des entreprises, où, qui suit, compagnies fréquentes, pas seulement l’Afrique, la famille, les rites) ; place prévue pour une vraie photo du bureau) → 06 Familles (`#familles` : deux boutons « J’ai déjà une pompe funèbre » / « Je n’ai pas de pompe funèbre » qui ouvrent un formulaire court adapté (a : lien email prêt + nom de la PF ; b : ville + pays), email ou téléphone, accord obligatoire, photo `photo-mains` en fond, objectif Plausible `Famille`, jamais de tarif aux familles) → 07 FAQ (10 questions triées par urgence, JSON-LD FAQPage identique hors question IATA) → 08 Contact → Footer → barre contact mobile `.mbar`. Motion : uniquement sous `.js` (haut de page façon cinéma : bandes noires qui s'ouvrent, rapprochement de la photo, grain, la caméra avance sur la piste au défilement ; hublot traversé dans À propos), rien si mouvement réduit (titres en masque, phrase qui s'éclaire, parallaxe, bandeau des villes, Lenis + boutons aimantés à la souris, transitions entre langues).

## Langues (FR / EN / DE)

Après chaque modification de texte : `python3 _atelier/typo.py` (typographie française : espaces insécables avant : ; ! ? et dans « », entre nombre et mot, apostrophe ’, pas de « à » seul en fin de ligne, Bâle‑Mulhouse insécable), puis `build.py`. Le build compare les phrases sous forme neutre, les clés de `strings.py` restent en typographie simple. `index.html` (français) est la seule source. `python3 _atelier/i18n/build.py` génère `en/index.html` et `de/index.html` à partir des traductions de `_atelier/i18n/strings.py` (toute phrase française absente est signalée). Ne jamais modifier `en/` ou `de/` à la main. Mentions légales et plaquette : français uniquement.

## Règles de contenu

- Ton opérationnel : « nous assurons », jamais « nous allons ».
- Cible : **toute l'Afrique**, Afrique de l'Ouest en priorité (clientèle des PF majoritairement africaine). Ne plus mettre « Maghreb » en avant (décision du 2026-10-17) ; on dit « Afrique du Nord » dans la liste des régions.
- Aucun téléphone, aucun tarif, aucun délai en jours ni délai de réponse chiffré (plus de « sous 2 heures » depuis le 2026-10-22 : on écrit « Joignables 7 jours sur 7 »), aucun chiffre non vérifié.
- Mentions IATA / HUM uniquement dans `.iata-only`.
- Pas de tirets longs dans le texte.

## Vérification

Captures headless (puppeteer-core + Chrome système) à 1440, 834 et 390 px ; vérifier absence de scroll horizontal et d'erreurs console.
