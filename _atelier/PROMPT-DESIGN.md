# Prompt : refonte design du site AUREVA Freight

À copier tel quel dans une nouvelle session (Claude Code ouvert dans `Aureva - Site/`). Toutes les infos ci-dessous sont vérifiées et alignées avec la plaquette, la convention, la fiche réflexe et les mentions légales au 2026-10-22.

---

## Mission

Tu es directeur artistique et rédacteur senior. Tu portes le site d'AUREVA Freight au niveau d'un site primé (Awwwards), sans perdre une once de dignité. Le résultat doit donner envie à un directeur de pompe funèbre de signer la convention dans la journée, et rassurer une famille en deuil dès la première phrase.

Travaille dans `index.html` (seule source, tout inline). Régénère `en/` et `de/` avec `python3 _atelier/i18n/build.py` en complétant `_atelier/i18n/strings.py` jusqu'à zéro « non traduit ». Lis d'abord `CLAUDE.md`, `_atelier/DESIGN.md` et `_atelier/PRODUCT.md`.

## Qui est AUREVA

- AUREVA SAS, nom commercial AUREVA Freight. 20 rue du Jura, 68390 Sausheim (Haut-Rhin), à côté de l'EuroAirport Bâle-Mulhouse.
- Transitaire aérien funéraire. Commissionnaire de transport (registre DREAL Grand Est) et agent cargo IATA, obtenus le 2026-10-17.
- Rapatriement de corps par avion, de la France vers toute l'Afrique : Afrique de l'Ouest en priorité, Afrique du Nord au même poids, Afrique centrale et de l'Est.
- Départ de Bâle-Mulhouse ou de l'aéroport qui offre le premier vol disponible (Strasbourg, Lyon, Paris, Zurich).
- Équipe issue du fret aérien et de la douane, qui a elle-même vécu le rapatriement d'un proche. Connaît les délais d'une inhumation musulmane, accompagne chaque défunt quelle que soit sa religion.
- Slogan immuable : « Le dernier voyage, avec dignité ».
- Contact unique : support@aurevafreight.com. Joignables 7 jours sur 7, jours fériés compris.

## Les deux publics, dans cet ordre

1. **Les pompes funèbres : nos clientes.** Elles gardent la famille, les démarches, le consulat, la mise en bière, l'acheminement à l'aéroport et le contact à l'arrivée. AUREVA prend la partie vol : options et devis, réservation au premier vol disponible, lettre de transport aérien, remise à la compagnie, suivi jusqu'à l'atterrissage. La pompe funèbre reste en première ligne, la famille ne connaît qu'elle. Une commission lui est versée sur chaque dossier qu'elle nous confie (montant fixé à la signature, aucun engagement de volume). Tout le haut de page et les sections 01 à 03 leur parlent.
2. **Les familles : un apport, jamais une clientèle.** En France, un rapatriement passe obligatoirement par une pompe funèbre habilitée. La famille écrit depuis la rubrique Familles :
   - elle a déjà une pompe funèbre : nous la contactons pour le vol ;
   - elle n'en a pas : nous lui proposons 2 ou 3 pompes funèbres partenaires proches, elle choisit librement, nous transmettons sa demande avec son accord coché.
   AUREVA ne donne jamais de tarif et ne facture jamais une famille. Les dossiers venus d'une famille orientée ne donnent pas de commission. Argument de vente pour les pompes funèbres : « Les familles nous écrivent, nous vous les envoyons. »

## Structure à garder (contenu vérifié, à sublimer)

Nav → Hero → 01 Fonctionnement → bandeau des villes → 02 Destinations → 03 Garanties → 04 À propos (#nous) → 05 Familles (#familles) → 06 Questions → 07 Contact → Footer → barre mobile.
- Hero : H1 « Rapatriement de corps vers l'Afrique, aux côtés des pompes funèbres » (mot-clé SEO, ne pas changer le sens), photo réelle `photo-piste`, lien secondaire « Vous êtes une famille ? ».
- Destinations : question « Où doit reposer le défunt ? » qui répond par une phrase, pays par région sans onglets, carte. Ne jamais la rallonger.
- Familles : deux boutons « J'ai déjà une pompe funèbre » / « Je n'ai pas de pompe funèbre », puis formulaire court adapté (cas a : lien email prêt à envoyer à la pompe funèbre, ou son nom ; cas b : ville du défunt et pays d'inhumation ; toujours nom, email ou téléphone, accord obligatoire). Formspree `https://formspree.io/f/mvzlovrr`, objectifs Plausible `Contact` et `Famille`.
- FAQ : JSON-LD FAQPage identique à la FAQ visible (sauf la question IATA).

## Direction artistique

- Palette : navy `#0D1B2A`, or `#C9A84C`, crème `#F7F4EE`. Le site est sombre et nocturne : une piste au crépuscule, la lumière dorée d'un avion qui part. L'or est rare et précieux, jamais décoratif partout.
- Typo : Marcellus (titres) + Hanken Grotesk (texte), déjà hébergées dans `fonts/`. Grand contraste d'échelle, titres serrés, corps 17-18 px, interligne généreux, lignes de moins de 75 caractères.
- Un seul moment signature : la phrase « Nous ne transportons pas des marchandises. Nous accompagnons un dernier voyage. » sur les traînées de lumière (À propos). Tout le reste calme et discipliné.
- Motion : courbes personnalisées, une seule chorégraphie d'entrée, rien sous `prefers-reduced-motion`, 60 fps. Pas d'apparition en fondu sur chaque bloc.
- Écriture : humaine, chaleureuse, au présent (« nous assurons », jamais « nous allons »). Phrases courtes. On parle à une personne fatiguée, pressée, en deuil, ou à un professionnel qui veut une réponse claire. Aucun jargon marketing.
- Mobile d'abord : 390 px parfait, cibles tactiles de 44 px minimum, focus clavier visible, contraste WCAG AA.

## Interdits absolus

- Le nom du président ou de tout associé.
- Un numéro de téléphone AUREVA.
- Un tarif, un délai en jours, un délai de réponse chiffré (« sous 2 h », « 24 h »). On écrit « Joignables 7 jours sur 7 » et « premier vol disponible ».
- Un chiffre non vérifiable (nombre de dossiers, de partenaires, avis clients).
- Les urnes. Les tirets longs. « Maghreb » mis en avant (on dit « toute l'Afrique », « Afrique du Nord » dans les listes).
- Les mentions IATA / HUM hors des éléments `.iata-only`.
- Les images IA pour tout ce qui montre la réalité (cercueil, équipe, bureau, aéroport, familles). Photos réelles uniquement (Unsplash, crédit dans `mentions-legales.html`). L'IA ou le code seulement pour des visuels abstraits (lumière, lignes, carte).
- Les gimmicks génériques : étiquettes en capitales au-dessus de chaque titre, cartes arrondies identiques, dégradés décoratifs, « → » partout.

## Livraison et vérification

1. Plan de design court (palette, typo, mise en page, principes) avant de coder, revu contre ce brief.
2. Captures headless (puppeteer-core + Chrome système) à 1440, 834 et 390 px, en FR, EN et DE : aucun défilement horizontal, aucune image cassée, aucune erreur console, nav sur une ligne.
3. Test du formulaire Familles (champs obligatoires, Oui / Non, accord) avec Formspree simulé.
4. Scan des interdits sur `index.html`, `en/`, `de/`, `llms.txt`, `mentions-legales.html`.
5. Aucun commit, push ou déploiement sans accord explicite.
