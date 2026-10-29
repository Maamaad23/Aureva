"""Pages « Rapatriement de corps vers <pays> » (référencement Google et réponses des IA).

Usage : python3 _atelier/pays/build.py
Sources, jamais recopiées à la main :
- documents : Operations/_sources/documents_pays/pays.json (vérifié par pays, champ « fiabilite »)
- vols directs : tables ROUTES et AIR d'index.html, villes et codes de la liste des pays
Écrit rapatriement-corps-<pays>.html à la racine, puis met à jour sitemap.xml et llms.txt.
On ne publie ni les sources concurrentes ni les notes « bon à savoir » des pays à confirmer.
"""
import html
import json
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "_atelier"))
from typo import html_typo  # noqa: E402

DATA = ROOT.parent / "Operations/_sources/documents_pays/pays.json"
SITE = "https://aurevafreight.com/"
DEPARTS = {"BSL": "Bâle-Mulhouse", "SXB": "Strasbourg", "LYS": "Lyon", "PAR": "Paris", "LIL": "Lille", "MRS": "Marseille",
           "NCE": "Nice", "MPL": "Montpellier", "TLS": "Toulouse", "BOD": "Bordeaux", "NTE": "Nantes"}
OFFICIEL = re.compile(r"consulat|ambassade|e-consulat|démarches consulaires", re.I)
NOTE = {
    "officielle": "Liste établie d’après les sources officielles du consulat, vérifiée le {d}.",
    "recoupee": "Liste recoupée sur plusieurs sources, vérifiée le {d}. Le consulat fait foi.",
    "a_confirmer": "Liste indicative, vérifiée le {d} : le consulat la confirme à chaque dossier.",
}

e = html.escape


def slug(nom):
    t = unicodedata.normalize("NFD", nom).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]+", "-", t).strip("-")


def dico(js, name):
    m = re.search(r"const %s = \{(.*?)\};" % name, js, re.S)
    return dict(re.findall(r"(\w+): '([^']*)'", m.group(1)))


def lire_site():
    s = (ROOT / "index.html").read_text(encoding="utf-8")
    air, routes = dico(s, "AIR"), dico(s, "ROUTES")
    villes = {}
    for cities, codes in re.findall(r'<li data-cities="([^"]*)" data-codes="([^"]*)"', s):
        for c, k in zip(html.unescape(cities).split("|"), codes.split("|")):
            villes[c] = k
    return air, routes, villes


def vols(code, air, routes):
    """[(départ, [compagnies])] dans l'ordre des départs ; * = en saison."""
    out = []
    for part in routes.get(code, "").split():
        dep, cies = part.split(":")
        out.append((dep, [air.get(c.rstrip("*"), c.rstrip("*")) + (" (en saison)" if c.endswith("*") else "") for c in cies.split(",")]))
    return sorted(out, key=lambda x: list(DEPARTS).index(x[0]))


def page(p, d, autres, air, routes, villes):
    nom, vers, sl = p["nom"], p["vers"], slug(p["nom"])
    url = f"{SITE}rapatriement-corps-{sl}.html"
    lignes, departs = [], []
    for ville in [v.strip() for v in p["arrivees"].split(",")]:
        code = villes.get(ville)
        vv = vols(code, air, routes) if code else []
        if not vv:
            continue
        for dep, _ in vv:
            if DEPARTS[dep] not in departs:
                departs.append(DEPARTS[dep])
        cies = sorted({c for _, cs in vv for c in cs})
        lignes.append(f"<tr><th scope=\"row\">{e(ville)} <span class=\"code\">{code}</span></th>"
                      f"<td>{e(', '.join(DEPARTS[x] for x, _ in vv))}</td><td>{e(', '.join(cies))}</td></tr>")
    villes_txt = ", ".join(v.strip() for v in p["arrivees"].split(","))
    deps_txt = ", ".join(departs)
    pieces = "".join(f"<li>{e(x['t'])}</li>" for x in p["pieces"])
    socle = "".join(f"<li>{e(x['t'])} <span class=\"who\">{e(x['q'])}</span></li>" for x in d["socle"]["pieces"])
    # Notes internes écartées : pays à confirmer, et ce qui pousse vers un autre prestataire
    savoir = [x for x in p["savoir"] if "prestataire" not in x] if p["fiabilite"] != "a_confirmer" else []
    savoir_html = ("<section aria-labelledby=\"s3\"><h2 id=\"s3\"><span>03</span>Bon à savoir</h2><ul class=\"list\">"
                   + "".join(f"<li>{e(x)}</li>" for x in savoir) + "</ul></section>") if savoir else ""
    sources = [s for s in p["sources"] if OFFICIEL.search(s["t"]) and not re.search(r"lost|nour|kohen", s["t"] + s["u"], re.I)]
    sources_html = ("<p class=\"note\">Sources : " + " · ".join(
        f"<a href=\"{e(s['u'])}\" rel=\"noopener nofollow\" target=\"_blank\">{e(s['t'])}</a>" for s in sources) + ".</p>") if sources else ""
    verifie = "26 octobre 2026" if d["verifie"] == "2026-10-26" else d["verifie"]
    faq = [
        (f"Combien de temps faut-il pour rapatrier un corps {vers} ?",
         "Cela dépend des documents, de l’autorisation du consulat et des places en soute. Nous cherchons le premier vol direct "
         "compatible avec la date d’inhumation prévue, 7 jours sur 7, jours fériés compris."),
        (f"Depuis quels aéroports de France partir {vers} ?",
         f"En vol direct, depuis {deps_txt}, selon la ville d’arrivée. Nous réservons sur la compagnie qui part la première, "
         "sans escale ni correspondance."),
        (f"Quel cercueil pour un rapatriement {vers} ?", d["socle"]["cercueil"]),
        ("Une famille peut-elle vous contacter directement ?",
         "Oui. En France, un rapatriement passe obligatoirement par une pompe funèbre habilitée : nous contactons la vôtre, "
         "ou nous vous proposons l’une de nos partenaires, puis nous organisons le vol avec elle. Nous ne facturons jamais les familles."),
    ]
    faq_html = "".join(f"<details><summary>{e(q)}</summary><p>{e(r)}</p></details>" for q, r in faq)
    autres_html = " · ".join(f"<a href=\"rapatriement-corps-{slug(a)}.html\">{e(a)}</a>" for a in autres if a != nom)
    desc = (f"Rapatriement de corps par avion {vers} pour les pompes funèbres : vols directs depuis la France "
            f"vers {villes_txt}, documents du consulat, cercueil. 7 jours sur 7.")
    if len(desc) > 165:
        desc = (f"Rapatriement de corps par avion {vers} pour les pompes funèbres : vols directs depuis la France, "
                "documents du consulat, cercueil. 7 jours sur 7.")
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Accueil", "item": SITE},
            {"@type": "ListItem", "position": 2, "name": "Destinations", "item": SITE + "#destinations"},
            {"@type": "ListItem", "position": 3, "name": f"Rapatriement de corps {vers}", "item": url}]},
        {"@type": "Service", "@id": url + "#service", "name": f"Rapatriement de corps par avion {vers}",
         "serviceType": "Transport funéraire aérien international", "url": url,
         "provider": {"@type": "Organization", "@id": SITE + "#org", "name": "AUREVA Freight", "url": SITE},
         "audience": {"@type": "BusinessAudience", "audienceType": "Pompes funèbres"},
         "areaServed": {"@type": "Country", "name": nom}, "description": desc},
        {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in faq]},
    ]}
    tpl = (ROOT / "_atelier/pays/page.html").read_text(encoding="utf-8")
    out = (tpl.replace("{{TITLE}}", e(f"Rapatriement de corps {vers} · AUREVA Freight"))
              .replace("{{DESC}}", e(desc)).replace("{{URL}}", url)
              .replace("{{LD}}", json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"))
              .replace("{{H1}}", e(f"Rapatriement de corps {vers}")).replace("{{NOM}}", e(nom)).replace("{{VERS}}", e(vers))
              .replace("{{VILLES}}", e(villes_txt)).replace("{{LIGNES}}", "".join(lignes))
              .replace("{{AUTORITE}}", e(p["autorite"])).replace("{{PIECES}}", pieces).replace("{{SOCLE}}", socle)
              .replace("{{CERCUEIL}}", e(d["socle"]["cercueil"])).replace("{{NOTE}}", e(NOTE[p["fiabilite"]].format(d=verifie)))
              .replace("{{SAVOIR}}", savoir_html).replace("{{SOURCES}}", sources_html).replace("{{FAQ}}", faq_html)
              .replace("{{AUTRES}}", autres_html).replace("{{N_QUI}}", "04" if savoir else "03")
              .replace("{{N_FAQ}}", "05" if savoir else "04"))
    # La typographie ne touche ni au JSON-LD ni aux adresses
    (ROOT / f"rapatriement-corps-{sl}.html").write_text(html_typo(out), encoding="utf-8")
    return sl, nom, vers


def main():
    d = json.loads(DATA.read_text(encoding="utf-8"))
    air, routes, villes = lire_site()
    noms = [p["nom"] for p in d["pays"]]
    faites = [page(p, d, noms, air, routes, villes) for p in d["pays"]]
    for old in ROOT.glob("rapatriement-corps-*.html"):
        if old.stem.removeprefix("rapatriement-corps-") not in {s for s, _, _ in faites}:
            old.unlink()
    # sitemap.xml : une entrée par page pays, remplacée à chaque build
    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sm = re.sub(r"\s*<url>\s*<loc>[^<]*rapatriement-corps-.*?</url>", "", sm, flags=re.S)
    add = "".join(f"\n  <url>\n    <loc>{SITE}rapatriement-corps-{s}.html</loc>\n    <lastmod>{d['verifie']}</lastmod>\n  </url>" for s, _, _ in faites)
    (ROOT / "sitemap.xml").write_text(sm.replace("\n</urlset>", add + "\n</urlset>"), encoding="utf-8")
    # llms.txt : liste des pages pays, entre deux repères
    ll = (ROOT / "llms.txt").read_text(encoding="utf-8")
    bloc = "## Rapatriement par pays (vols directs, documents, cercueil)\n\n" + "".join(
        f"- [Rapatriement de corps {v}]({SITE}rapatriement-corps-{s}.html)\n" for s, _, v in faites)
    ll = re.sub(r"## Rapatriement par pays.*?(?=\n## |\Z)", "", ll, flags=re.S).rstrip() + "\n\n" + bloc
    (ROOT / "llms.txt").write_text(ll, encoding="utf-8")
    print(len(faites), "pages pays :", ", ".join(n for _, n, _ in faites))


if __name__ == "__main__":
    main()
