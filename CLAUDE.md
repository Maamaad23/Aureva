# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

Nav (5 rubriques + langues + bouton) → Hero (photo réelle, une phrase, un seul bouton « Ouvrir un dossier », lien discret « Vous êtes une famille ? », bandeau `.awb`) → 01 Fonctionnement (3 étapes en photo, carrousel à glisser sur téléphone, détail en 9 étapes replié) → 02 Destinations (question « Où doit reposer le défunt ? » + carte d’embarquement, tout pays du monde via Intl.DisplayNames et `WORLD` ; carte de l’Afrique sur ordinateur seulement ; pays par région repliés « Voir tous les pays » ; tableau des compagnies `.board`) → 03 Confiance (`#nous` : bande du hublot `.cine` sans blocage, la caméra s’approche et la phrase s’éclaire au passage ; puis `#garanties` clair : accréditations, récit court, 3 réponses Qui êtes-vous / Et la famille / Les rites) → 04 Partenaires (`#partenaires`, fiche réflexe, « Recevoir la convention ») → 05 Questions (9, JSON-LD FAQPage identique hors question IATA) → 06 Contact → Familles (`#familles`, encadré après le contact : deux boutons, formulaire court, jamais de tarif) → Footer → barre mobile `.mbar`. Motion sur ordinateur et téléphone (Lenis et boutons aimantés à la souris seulement) ; mouvement réduit (`.calm`) : fondus, tuiles et tableau gardés, sans déplacement ni zoom.

Recherche de destination : départ au choix (BSL, SXB, LYS, ZRH, PAR), sinon le plus proche avec vol direct. Table `ROUTES` + `AIR` dans index.html = vols directs relevés en octobre 2026 (programmes des aéroports, Wikipédia), seulement les compagnies qui transportent les défunts (pas easyJet, Ryanair, Transavia, Volotea, Air Arabia). À revérifier à chaque saison (fin mars, fin octobre). AUREVA ne fait ni escale ni correspondance : sans vol direct relevé, le site le dit et invite à écrire (jamais « correspondance »). Le tableau `.board` liste les compagnies de `AIR` ; une compagnie touchée montre ses vols directs par départ.

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
