"""Merge the three sources into one row per Bulletin item.

Precedence for title/authors/issue/page/type:
  TOC PDFs (vols 39-56, 2008-2026)  >  Crossref/JSTOR (vols 1-35, 1969-2004)  >  APT Comprehensive Index.
The index's subject headings are attached to every item it matches (topics column).
Index items with no TOC/Crossref match are kept (source = index); inside TOC-covered issues those are
almost always book reviews, since TOCs list reviews only as a "Book Reviews" section.

Run build_index.py first. Output: build/master.csv, build/unmatched_report.txt
"""
import csv, json, re, difflib, collections, unicodedata
from pathlib import Path

HERE = Path(__file__).parent
B = HERE / "build"

def tkey(t):
    t = unicodedata.normalize("NFKD", t or "").encode("ascii", "ignore").decode().lower()
    t = re.sub(r"^(practice points?\s*(no\.?|number)?\s*\d+\s*:?\s*)", "", t)
    return re.sub(r"[^a-z0-9]", "", t)

def sim(a, b):
    a, b = tkey(a), tkey(b)
    if not a or not b: return 0
    if len(a) > 15 and len(b) > 15 and (a.startswith(b) or b.startswith(a)): return 0.95
    return difflib.SequenceMatcher(None, a[:120], b[:120]).ratio()

SECTION_TYPE = {"article": "Article", "practice_point": "Practice Point", "book_reviews": "Book reviews (section)",
                "editorial": "Editorial", "letter": "Letter", "guest_editor": "Guest editor note", "other": "Other"}
INDEX_TYPE = {"ART": "Article", "PP": "Article", "BR": "Book review", "LTR": "Letter", "ED": "Editorial",
              "GE": "Guest editor note", "OP": "Opinion", "IT": "Article", "CF": "Computer Forum", "NOTE": "Note",
              "TN": "Note", "COMP": "Bibliography", "BIB": "Bibliography", "FT": "Final Touch", "PE": "Article",
              "MAIN": "Article", "SPEC": "Other", "BTHL": "Building Technology Heritage Library"}
# The index's "PP" code predates the Practice Points series (1989-92 items) and is unreliable after it,
# so an item is a Practice Point only when it carries a series number.

items = []

# 1. TOCs
toc_vols, toc_issues = set(), set()
for f in ["toc_parsed_a.json", "toc_parsed_b.json"]:
    for iss in json.load(open(B / f)):
        toc_vols.add(int(iss["volume"])); toc_issues.add((int(iss["volume"]), str(iss["issue"])))
        for it in iss["items"]:
            if it.get("section") == "other" and re.search(r"(?i)advertisers|membership|^index|guidelines for authors|author guidelines|endowment|contents", it["title"]):
                continue  # masthead/back-matter, not content
            items.append(dict(source="TOC", volume=int(iss["volume"]), issue=str(iss["issue"]), year=iss["year"],
                              page_start=it.get("page"), title=it["title"], authors="; ".join(it.get("authors") or []),
                              type=SECTION_TYPE.get(it.get("section"), "Other"), pp_number=it.get("pp_number") or "",
                              doi="", note=it.get("note") or ""))

# 2. Crossref (JSTOR backfile)
for x in json.load(open(HERE / "raw/crossref_apt.json")):
    t = (x.get("title") or [""])[0]
    if x.get("subtitle"): t += ": " + x["subtitle"][0]
    if not t.strip(): continue
    vol = int(re.sub(r"\D", "", x.get("volume") or "0") or 0)
    if vol in toc_vols: continue
    pg = (x.get("page") or "").split("-")[0]
    items.append(dict(source="Crossref/JSTOR", volume=vol, issue=x.get("issue") or "", year=x["published"]["date-parts"][0][0],
                      page_start=int(pg) if pg.isdigit() else None, title=re.sub(r"\s+", " ", t).strip(),
                      authors="; ".join(f"{a.get('given', '')} {a.get('family', '')}".strip() for a in x.get("author", [])),
                      type="", pp_number="", doi=x["DOI"], note=""))

# 3. Match index items to TOC/Crossref items in the same or adjacent volume
idx = list(csv.DictReader(open(B / "articles.csv")))
by_vol = collections.defaultdict(list)
for i, it in enumerate(items): by_vol[it["volume"]].append(i)
for it in items: it.update(topics="", index_type="", index_authors="", book_authors="", pp_pdf="", index_refs="")

unmatched = []
for r in idx:
    v = int(r["volume"])
    cands = [i for dv in (0, -1, 1) for i in by_vol.get(v + dv, [])]
    best, score = None, 0
    for i in cands:
        s = sim(r["title"], items[i]["title"])
        if s > score: best, score = i, s
    if best is None or score < 0.82:
        # second chance: same issue, start page within 1, looser title match (index and JSTOR word titles differently)
        pg = int(r["page_start"]) if (r["page_start"] or "").isdigit() else None
        near = [(sim(r["title"], items[i]["title"]), i) for i in by_vol.get(v, [])
                if pg is not None and items[i]["issue"] == r["issue"] and items[i]["page_start"]
                and abs(int(items[i]["page_start"]) - pg) <= 1]
        # several book reviews often share one page, so reviews need a near-exact title to merge
        near = [x for x in near if x[0] >= (0.85 if r["type"] == "BR" else 0.6)]
        if near: best, score = max(near)[1], 0.82
    if best is not None and score >= 0.82:
        it = items[best]
        it["topics"] = "; ".join(sorted(set(filter(None, it["topics"].split("; ") + r["topics"].split("; ")))))
        it["index_type"] = it["index_type"] or r["type"]
        it["index_authors"] = it["index_authors"] or r["authors"]
        it["book_authors"] = it["book_authors"] or r["book_authors"]
        it["pp_number"] = it["pp_number"] or r["pp_number"]
        it["pp_pdf"] = it["pp_pdf"] or r["pp_pdf"]
        it["index_refs"] = r["index_refs"]
        continue
    in_toc = (v, r["issue"]) in toc_issues
    typ = "Practice Point" if r["pp_number"] else INDEX_TYPE.get(r["type"], r["type_name"])
    if in_toc and not r["pp_number"]:
        typ = "Book review or minor item (index only)"
    if in_toc: unmatched.append((v, r["issue"], r["type"], r["title"], round(score, 2)))
    items.append(dict(source="Index", volume=v, issue=r["issue"], year=int(r["year"]), page_start=r["page_start"],
                      title=r["title"], authors=r["authors"], type=typ, pp_number=r["pp_number"], doi="", note="",
                      topics=r["topics"], index_type=r["type"], index_authors=r["authors"], book_authors=r["book_authors"],
                      pp_pdf=r["pp_pdf"], index_refs=r["index_refs"]))

# 4. Settle type for Crossref rows from the index type, then by title
for it in items:
    if it["type"]: continue
    t = it["title"].lower()
    if it["index_type"]: it["type"] = INDEX_TYPE.get(it["index_type"], it["index_type"])
    elif re.match(r"(letters?\b|correspondence|response to|reply)", t): it["type"] = "Letter"
    elif re.match(r"(errata|correction)", t): it["type"] = "Other"
    elif t in ("final touch", "computer forum", "articles in french", "front matter", "back matter"): it["type"] = "Other"
    else: it["type"] = "Article (type not indexed; may be a review)"
    if it["type"] == "Book review" and it["book_authors"]:
        # Crossref lists reviewer and book author together; keep only the reviewer(s) as authors
        ba = {tkey(n) for n in it["book_authors"].split("; ")}
        it["authors"] = "; ".join(a for a in it["authors"].split("; ") if tkey(a) not in ba) or it["index_authors"]

# Practice Point numbers + PDFs from the website list, matched on title
pps = [p for p in csv.DictReader(open(HERE / "raw/practice_points.csv")) if "Spanish" not in p["number"]]
pp_missing = []
for p in pps:
    best = max(items, key=lambda it: sim(it["title"], p["title"]))
    if sim(best["title"], p["title"]) >= 0.8:
        best["pp_number"], best["pp_pdf"], best["type"] = p["number"], p["url"], "Practice Point"
    else:
        pp_missing.append(p)
for p in pp_missing:  # published on the website but not found in any TOC/index (e.g. not yet indexed)
    items.append(dict(source="Practice Points page", volume="", issue="", year="", page_start="", title=p["title"], authors="",
                      type="Practice Point", pp_number=p["number"], doi="", note="Not found in TOCs or index; issue unknown",
                      topics="", index_type="", index_authors="", book_authors="", pp_pdf=p["url"], index_refs=""))

def sort_key(it):
    iss = str(it["issue"] or "0"); first = int(re.match(r"\d+", iss).group()) if re.match(r"\d+", iss) else 0
    return (int(it["volume"] or 999), first, int(it["page_start"] or 0) if str(it["page_start"] or "").isdigit() else 0)
items.sort(key=sort_key)
for n, it in enumerate(items, 1): it["id"] = f"APT{n:05d}"

fields = ["id", "year", "volume", "issue", "page_start", "type", "pp_number", "title", "authors", "book_authors", "topics",
          "source", "doi", "pp_pdf", "index_refs", "index_type", "index_authors", "note"]
with open(B / "master.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fields, extrasaction="ignore"); w.writeheader(); w.writerows(items)

with open(B / "unmatched_report.txt", "w") as f:
    f.write(f"Index items in TOC-covered volumes with no TOC match ({len(unmatched)}):\n")
    for u in sorted(unmatched): f.write(f"  {u}\n")
    f.write(f"\nPractice Points not found ({len(pp_missing)}): {[p['number'] for p in pp_missing]}\n")

c = collections.Counter(it["type"] for it in items)
print(len(items), "items"); print(c); print(collections.Counter(it["source"] for it in items))
print("PP numbers:", sorted(int(it["pp_number"]) for it in items if str(it["pp_number"]).isdigit()))
print("no topics (articles/PP):", sum(1 for it in items if not it["topics"] and it["type"] in ("Article", "Practice Point", "Article (type not indexed)")))
print("index items unmatched in TOC volumes:", len(unmatched), "| PP missing:", [p["number"] for p in pp_missing])
