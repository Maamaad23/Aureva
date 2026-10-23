"""Typographie française (règles de l'Imprimerie nationale) pour les textes du site.

Usage : python3 _atelier/typo.py   (réécrit index.html et mentions-legales.html, idempotent)
Le script ne touche qu'aux textes visibles et aux attributs lisibles (alt, aria-label,
placeholder, title, content, label), jamais aux scripts, styles, adresses ou emails.
build.py applique la même fonction aux clés de strings.py : les traductions restent trouvées.

Règles :
- espace fine insécable avant ; ! ? et à l'intérieur des guillemets « »
- espace insécable avant :
- espace insécable entre un nombre et ce qui suit (7 jours, 20 rue, 68390 Sausheim)
  et dans « 7 jours sur 7 », « 24 h », « 15 000 »
- apostrophe typographique ’ et points de suspension …
- pas de mot d'une lettre (à, y) ni « AUREVA » seul en fin de ligne
- trait d'union insécable dans les noms composés courts (Bâle‑Mulhouse)
"""
import re
from pathlib import Path

NB, FINE = "\u00a0", "\u202f"
ATTRS = ("alt", "aria-label", "placeholder", "title", "content", "label")
SKIP_ATTR = re.compile(r"^(https?:|mailto:|tel:|#|\.{0,2}/|[\w.-]+\.(html|webp|jpg|png|pdf)\b)|@|^[\d\s,.;]+$|width=")


ENT = re.compile(r"&(#?\w+);")


def fr(t):
    t = ENT.sub(lambda m: "\x00" + m.group(1) + "\x01", t)
    t = _fr(t)
    return re.sub("\x00(#?\\w+)\x01", r"&\1;", t)


def _fr(t):
    t = re.sub(r"(?<=\w)'(?=\w)", "’", t)
    t = t.replace("...", "…")
    t = re.sub(r"[ \u00a0\u202f]*([;!?])", lambda m: FINE + m.group(1), t)
    t = re.sub(r"(?<=\S)[ \u00a0\u202f]+:(?=\s|$)", NB + ":", t)
    t = re.sub(r"«[ \u00a0\u202f]*", "«" + FINE, t)
    t = re.sub(r"[ \u00a0\u202f]*»", FINE + "»", t)
    t = re.sub(r"(?<=\d) (?=\d{3}\b)", FINE, t)
    t = re.sub(r"(?<=\d) (?=[^\W\d_]|%|€|h\b)", NB, t)
    t = re.sub(r"\b(sur|et|de|à) (?=\d)", lambda m: m.group(1) + NB, t)
    t = re.sub(r"(?<![\w’])([àÀyaA]) (?=\w)", lambda m: m.group(1) + NB, t)
    t = re.sub(r"\bAUREVA (?=Freight\b)", "AUREVA" + NB, t)
    t = re.sub(r"\b(Bâle|Basel)-(Mulhouse)\b", "\\1\u2011\\2", t)
    # pas d'espace fine devant ! ? dans une adresse ou un code
    t = re.sub(r"(https?://\S*?)\u202f([?!])", r"\1\2", t)
    return t


def key(t):
    """Forme neutre d'un texte, pour retrouver une phrase quelle que soit sa typographie."""
    t = t.replace("’", "'").replace("…", "...").replace("\u2011", "-")
    t = re.sub(r"[\u00a0\u202f]", " ", t)
    t = re.sub(r" ([;!?:»])", r"\1", t)
    t = t.replace("« ", "«")
    return t


def html_typo(src):
    parts = re.split(r"(<script\b.*?</script>|<style\b.*?</style>|<!--.*?-->|<[^>]+>)", src, flags=re.S)
    out, pre = [], False
    for p in parts:
        if p.startswith("<script") or p.startswith("<style") or p.startswith("<!--"):
            out.append(p)
        elif p.startswith("<"):
            low = p[:5].lower()
            if low.startswith(("<pre", "<code")):
                pre = True
            elif low.startswith(("</pre", "</cod")):
                pre = False
            out.append(re.sub(r'\b(%s)="([^"]*)"' % "|".join(ATTRS),
                              lambda m: m.group(0) if SKIP_ATTR.search(m.group(2)) else f'{m.group(1)}="{fr(m.group(2))}"', p))
        else:
            out.append(p if pre or "@" in p else fr(p))
    return "".join(out)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[1]
    for name in ("index.html", "mentions-legales.html"):
        f = root / name
        s = f.read_text(encoding="utf-8")
        n = html_typo(s)
        f.write_text(n, encoding="utf-8")
        print(name, "ok" if n == s else "mis à jour")
