"""Génère en/index.html et de/index.html à partir de index.html (source française).

Usage : python3 _atelier/i18n/build.py
À relancer après chaque modification de index.html. Toute nouvelle phrase française
doit être ajoutée dans _atelier/i18n/strings.py, sinon le script la signale et la laisse en français.
"""
import html
import json
import re
from pathlib import Path

from strings import JS, KEEP, LD, T

import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from typo import key as tkey  # noqa: E402

# Les textes du site passent par la typographie française (_atelier/typo.py) : on compare sous forme neutre
TN = {tkey(k): v for k, v in T.items()}
KEEPN = {tkey(k) for k in KEEP}

ROOT = Path(__file__).resolve().parents[2]
SRC = (ROOT / "index.html").read_text(encoding="utf-8")
LANGS = {"en": 0, "de": 1}
LOCALE = {"en": "en_GB", "de": "de_DE"}
ATTR = re.compile(r'\b(alt|aria-label|placeholder|title|label|content)="([^"]*)"')
SKIP = re.compile(r"^[\W\d_]*$|^[A-Z]{3}$|^(AUREVA|Freight|LinkedIn|AUREVA Freight|support@aurevafreight\.com)$")


def tr(text, i, missing):
    key = tkey(html.unescape(text))
    if key in TN:
        return html.escape(TN[key][i], quote=False)
    if key not in KEEPN and not SKIP.match(key) and re.search(r"[a-zà-ÿ]{3}", key):
        missing.add(key)
    return text


def tr_attr(m, i, missing):
    name, val = m.group(1), m.group(2)
    key = tkey(html.unescape(val))
    if key in TN:
        return f'{name}="{html.escape(TN[key][i])}"'
    if name != "content" and re.search(r"[a-zà-ÿ]{3}", key) and not key.startswith("http"):
        missing.add(key)
    return m.group(0)


def tr_ld(obj, i):
    if isinstance(obj, dict):
        return {k: tr_ld(v, i) for k, v in obj.items()}
    if isinstance(obj, list):
        return [tr_ld(v, i) for v in obj]
    if isinstance(obj, str):
        if obj in LD:
            return LD[obj][i]
        if obj in T:
            return T[obj][i]
    return obj


def switcher(lang):
    links = {"fr": ("../", "FR"), "en": ("../en/", "EN"), "de": ("../de/", "DE")}
    out = []
    for code, (href, label) in links.items():
        if code == lang:
            out.append(f'<a href="./" lang="{code}" hreflang="{code}" aria-current="true">{label}</a>')
        else:
            out.append(f'<a href="{href}" lang="{code}" hreflang="{code}">{label}</a>')
    return "<!--LANG-->" + "".join(out) + "<!--/LANG-->"


def build(lang):
    i = LANGS[lang]
    missing = set()
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<[^>]+>)", SRC, flags=re.S)
    out = []
    for p in parts:
        if not p:
            continue
        if p.startswith('<script type="application/ld+json">'):
            body = p[len('<script type="application/ld+json">'):-len("</script>")]
            data = tr_ld(json.loads(body), i)
            for node in data.get("@graph", []):
                if node.get("@type") in ("VideoObject",):
                    node["inLanguage"] = lang
                    node["contentUrl"] = node["contentUrl"].replace("film-voyage.mp4", f"film-voyage-{lang}.mp4")
                    node["thumbnailUrl"] = node["thumbnailUrl"].replace("film-poster.webp", f"film-poster-{lang}.webp")
            out.append('<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=1) + "\n</script>")
        elif p.startswith("<script"):
            for fr, vals in JS.items():
                p = p.replace(fr, vals[i])
            out.append(p)
        elif p.startswith("<style") or p.startswith("<!--"):
            out.append(p)
        elif p.startswith("<"):
            out.append(ATTR.sub(lambda m: tr_attr(m, i, missing), p))
        else:
            m = re.match(r"^(\s*)(.*?)(\s*)$", p, re.S)
            out.append(m.group(1) + (tr(m.group(2), i, missing) if m.group(2) else "") + m.group(3))
    s = "".join(out)

    # Langue, adresses, sélecteur
    s = s.replace('<html lang="fr"', f'<html lang="{lang}"', 1)
    s = s.replace('<link rel="canonical" href="https://aurevafreight.com/">', f'<link rel="canonical" href="https://aurevafreight.com/{lang}/">', 1)
    s = s.replace('<meta property="og:url" content="https://aurevafreight.com/">', f'<meta property="og:url" content="https://aurevafreight.com/{lang}/">', 1)
    s = s.replace('content="fr_FR"', f'content="{LOCALE[lang]}"', 1)
    s = re.sub(r"<!--LANG-->.*?<!--/LANG-->", switcher(lang), s, flags=re.S)
    s = s.replace('value="Nouvelle demande · AUREVA Freight"', f'value="Nouvelle demande ({lang.upper()}) · AUREVA Freight"')
    # Film et affiche dans la langue
    s = s.replace("Videos/film-voyage.mp4", f"Videos/film-voyage-{lang}.mp4")
    s = s.replace("Images/film-poster.webp", f"Images/film-poster-{lang}.webp")
    s = s.replace("Images/og-image.jpg", f"Images/og-image-{lang}.jpg")
    # Chemins relatifs : la page vit dans un sous-dossier
    s = re.sub(r"""(?<=["'(\s,])(Images|Videos|fonts|js)/""", r"../\1/", s)
    s = s.replace('href="plaquette-aureva.pdf"', 'href="../plaquette-aureva.pdf"')
    s = s.replace('href="fiche-reflexe-aureva.pdf"', 'href="../fiche-reflexe-aureva.pdf"')
    s = s.replace('data-prefill="Bonjour, je souhaite recevoir la convention partenaire AUREVA."',
                  'data-prefill="' + ("Hello, I would like to receive the AUREVA partner agreement." if lang == "en" else "Guten Tag, ich möchte die AUREVA-Partnervereinbarung erhalten.") + '"')
    s = s.replace('href="mentions-legales.html', 'href="../mentions-legales.html')
    # Email que la famille envoie à sa pompe funèbre
    s = s.replace('mailto:?subject=Rapatriement%20de%20notre%20proche%20%3A%20AUREVA%20Freight&amp;body=Bonjour%2C%0A%0APour%20le%20vol%20de%20rapatriement%20de%20notre%20proche%2C%20vous%20pouvez%20travailler%20avec%20AUREVA%20Freight%2C%20transitaire%20a%C3%A9rien%20fun%C3%A9raire%2C%20joignable%207%20jours%20sur%207%20%3A%0A%0Asupport%40aurevafreight.com%0Aaurevafreight.com%0A%0ACordialement%2C', 'mailto:?subject=Repatriation%20of%20our%20loved%20one%3A%20AUREVA%20Freight&amp;body=Hello%2C%0A%0AFor%20the%20repatriation%20flight%20of%20our%20loved%20one%2C%20you%20can%20work%20with%20AUREVA%20Freight%2C%20a%20funeral%20air%20freight%20forwarder%20reachable%207%20days%20a%20week%3A%0A%0Asupport%40aurevafreight.com%0Aaurevafreight.com%0A%0AKind%20regards%2C' if lang == "en" else 'mailto:?subject=%C3%9Cberf%C3%BChrung%20unseres%20Angeh%C3%B6rigen%3A%20AUREVA%20Freight&amp;body=Guten%20Tag%2C%0A%0AF%C3%BCr%20den%20%C3%9Cberf%C3%BChrungsflug%20unseres%20Angeh%C3%B6rigen%20k%C3%B6nnen%20Sie%20mit%20AUREVA%20Freight%20zusammenarbeiten%2C%20einem%20Luftfrachtspediteur%20f%C3%BCr%20%C3%9Cberf%C3%BChrungen%2C%20erreichbar%207%20Tage%20die%20Woche%3A%0A%0Asupport%40aurevafreight.com%0Aaurevafreight.com%0A%0AMit%20freundlichen%20Gr%C3%BC%C3%9Fen')

    out_dir = ROOT / lang
    out_dir.mkdir(exist_ok=True)
    (out_dir / "index.html").write_text(s, encoding="utf-8")
    return missing


if __name__ == "__main__":
    for lang in LANGS:
        missing = build(lang)
        print(f"{lang}/index.html écrit")
        for m in sorted(missing):
            print(f"  non traduit : {m}")
