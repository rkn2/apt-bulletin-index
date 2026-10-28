"""Collapse APT's Comprehensive Index (a subject/author back-of-book index) into one row per Bulletin item.

Input:  raw/comprehensive_index_2025-12-19.xlsx  (https://irp.cdn-website.com/4f321b91/files/uploaded/Comprehensive+Index+for+Website+12-19-25.xlsx)
        raw/practice_points.csv                    (the 31-item list on https://www.apti.org/practice-points)
Output: build/articles.csv, build/rejects.csv
"""
import csv, re, sys, difflib, collections, unicodedata
from pathlib import Path
import openpyxl

HERE = Path(__file__).parent
SRC = HERE / "raw/comprehensive_index_2025-12-19.xlsx"
OUT = HERE / "build"; OUT.mkdir(exist_ok=True)

TYPES = ["ART", "BR", "LTR", "PP", "ED", "GE", "CF", "OP", "IT", "NOTE", "COMP", "FT", "PE", "MAIN", "BIB", "BTHL", "SPEC", "TN"]
TYPE_NAMES = {"ART": "Article", "BR": "Book review", "LTR": "Letter", "PP": "Practice Point", "ED": "Editorial",
              "GE": "Guest editor note", "CF": "Computer Forum", "OP": "Opinion", "IT": "Investigative technique",
              "NOTE": "Note", "COMP": "Compilation/bibliography", "FT": "Feature", "PE": "PE (index code)",
              "MAIN": "Maintenance", "BIB": "Bibliography", "BTHL": "Building Technology Heritage Library",
              "SPEC": "Special", "TN": "Technical note"}
ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}

def roman(s):
    if s.isdigit(): return int(s)
    n = 0
    for a, b in zip(s, s[1:] + " "):
        v = ROMAN[a]; n += -v if b != " " and ROMAN.get(b, 0) > v else v
    return n

REF = re.compile(r"^(?:\{\w\})?\s*(" + "|".join(sorted(TYPES, key=len, reverse=True)) + r")?\s*(?:\([^)]*\))?\s*"
                 r"([IVXLC]+|\d+)[\s-]*(\d(?:[/-]\d)*?)-(\d\d)\s*,?\s*(?:pp?\.\s*([\d]+)(?:\s*-\s*(\d+))?)?")

def parse_ref(p):
    s = re.sub(r"[–—]", "-", p.strip())
    m = REF.match(s)
    if not m: return None
    typ, vol, iss, yy, p1, p2 = m.groups()
    y = int(yy); year = 1900 + y if y >= 69 else 2000 + y
    return dict(type=typ or "ART", volume=roman(vol), issue=iss.replace("-", "/"), year=year,
                page_start=int(p1) if p1 else None, page_end=int(p2) if p2 else (int(p1) if p1 else None))

def clean(t):
    t = unicodedata.normalize("NFC", t or "").replace("È", "é")
    t = re.sub(r"[“”]", '"', t).replace("’", "'")
    return t.strip().rstrip(",").strip()

def split_title(entry):
    """'"Title" by A and B, rev. by C' -> (title, by_text, rev_text, and_text)"""
    e = clean(entry)
    and_txt = None
    m = re.search(r"\(and ([^)]*)\)\s*,?$", e)
    if m: and_txt, e = m.group(1), e[:m.start()].strip()
    rev = None
    m = re.search(r",?\s*rev\. by (.*)$", e)
    if m: rev, e = m.group(1), e[:m.start()].strip()
    by = None
    m = re.search(r",?\s+(?:ed\.|comp\.)?\s*by (.*)$", e)
    if m: by, e = m.group(1), e[:m.start()].strip()
    return e.strip(' ",'), by, rev, and_txt

def names(txt):
    if not txt: return []
    txt = re.sub(r",?\s+and\s+", ", ", txt.strip().rstrip(","))
    out = []
    for n in re.split(r",\s*", txt):
        n = n.strip()
        if n in ("Jr.", "Sr.", "III", "II") and out: out[-1] += ", " + n; continue
        if n: out.append(n)
    return out

PERSON = re.compile(r"^[A-ZÀ-Ý'’\-\. ]+, [A-ZÀ-Ý][a-zà-ÿ]")

def person_name(cat):
    last, first = cat.split(", ", 1)
    sfx = ""
    m = re.match(r"(.*), (Jr\.|Sr\.|III|II)$", first)
    if m: first, sfx = m.group(1), ", " + m.group(2)
    last = "-".join(w.capitalize() for w in last.split("-"))
    last = " ".join(w if w.isupper() and len(w) <= 3 and "." in w else (w[0] + w[1:].lower() if w else w) for w in last.split(" "))
    last = re.sub(r"\b(Mc|Mac|O')([a-z])", lambda m: m.group(1) + m.group(2).upper(), last)
    last = re.sub(r"-([a-z])", lambda m: "-" + m.group(1).upper(), last)
    return f"{first} {last}{sfx}".replace("’", "'")

def nkey(n): return re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", n.lower()).encode("ascii", "ignore").decode())

def tkey(t): return re.sub(r"[^a-z0-9]", "", t.lower())[:70]

wb = openpyxl.load_workbook(SRC, read_only=True)
rows = list(wb.active.iter_rows(min_row=2, values_only=True))
rejects, groups = [], collections.defaultdict(list)
for cat, entry, ref, *_ in rows:
    if not ref:
        continue  # "See ..." cross-references
    r = parse_ref(ref)
    if not r:
        rejects.append(dict(category=cat, entry=entry, ref=ref, reason="unparsed ref")); continue
    title, by, rev, and_txt = split_title(entry)
    # Page refs in the index are unreliable (e.g. 52.4 lists one article at five start pages), so group by
    # volume here and split by title below; issue and page are then the majority over the item's rows.
    groups[r["volume"]].append(dict(cat=cat, entry=entry, ref=ref, title=title, by=by, rev=rev, and_txt=and_txt, **r))

articles = []
for key, items in groups.items():
    # split one page-group into distinct items by title similarity
    clusters = []
    for it in items:
        k = tkey(it["title"])
        for c in clusters:
            if difflib.SequenceMatcher(None, k, c["k"]).ratio() > 0.8 or (k and c["k"] and (k.startswith(c["k"]) or c["k"].startswith(k))):
                c["items"].append(it); break
        else:
            clusters.append(dict(k=k, items=[it]))
    for c in clusters:
        its = c["items"]
        title = collections.Counter(i["title"] for i in its if i["title"]).most_common(1)
        title = max((i["title"] for i in its), key=len) if not title else title[0][0]
        types = collections.Counter(i["type"] for i in its)
        typ = "PP" if types.get("PP") or any((i["cat"] or "").upper() == "PRACTICE POINTS" for i in its) else (
              "ART" if types.get("ART") else types.most_common(1)[0][0])
        by_lists = [names(i["by"]) for i in its if i["by"]]
        by_best = max(by_lists, key=len) if by_lists else []
        rev = next((i["rev"] for i in its if i["rev"]), None)
        persons, subjects = [], []
        for i in its:
            cat = (i["cat"] or "").strip()
            if not cat: continue
            if PERSON.match(cat) and (not i["by"] or i["and_txt"] or nkey(person_name(cat)) in {nkey(n) for n in by_best + names(rev)}):
                persons.append(person_name(cat))
                if i["and_txt"]: persons += names(i["and_txt"])
            else:
                subjects.append(cat)
        # authors: by-text order first, then any author headings not already present
        if typ == "BR":
            reviewers = names(rev) or [p for p in persons if nkey(p) not in {nkey(n) for n in by_best}]
            authors = list(dict.fromkeys(reviewers)); book_authors = by_best
        else:
            authors = list(by_best); book_authors = []
            have = {nkey(a) for a in authors}
            for p in persons:
                if nkey(p) not in have: authors.append(p); have.add(nkey(p))
        y = its[0]
        mode = lambda f: collections.Counter(i[f] for i in its if i[f] is not None).most_common(1)[0][0] if any(i[f] is not None for i in its) else None
        refs = {(i["issue"], i["page_start"]) for i in its}
        articles.append(dict(
            volume=y["volume"], issue=mode("issue"), year=mode("year"), page_start=mode("page_start"), page_end=mode("page_end"),
            ref_conflict="yes" if len(refs) > 1 else "",
            type=typ, type_name=TYPE_NAMES.get(typ, typ), title=title, authors="; ".join(authors),
            book_authors="; ".join(book_authors), topics="; ".join(sorted(set(subjects) - {"PRACTICE POINTS"})),
            index_refs=" | ".join(sorted({i["ref"] for i in its})), n_index_rows=len(its)))

articles.sort(key=lambda a: (a["volume"], a["issue"], a["page_start"] or 0, a["title"]))

# Practice Point numbers from the website list
pps = list(csv.DictReader(open(HERE / "raw/practice_points.csv")))
for a in articles: a["pp_number"] = ""; a["pp_pdf"] = ""
unmatched = []
for pp in pps:
    if "Spanish" in pp["number"]: continue
    best = max(articles, key=lambda a: difflib.SequenceMatcher(None, tkey(a["title"]), tkey(pp["title"])).ratio())
    score = difflib.SequenceMatcher(None, tkey(best["title"]), tkey(pp["title"])).ratio()
    if score >= 0.75:
        best["pp_number"], best["pp_pdf"] = pp["number"], pp["url"]
        if best["type"] != "PP": best["type"], best["type_name"] = "PP", TYPE_NAMES["PP"]
    else:
        unmatched.append((pp["number"], pp["title"], best["title"], round(score, 2)))

fields = list(articles[0].keys())
with open(OUT / "articles.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fields); w.writeheader(); w.writerows(articles)
with open(OUT / "rejects.csv", "w", newline="") as f:
    w = csv.DictWriter(f, ["category", "entry", "ref", "reason"]); w.writeheader(); w.writerows(rejects)

print(f"{len(rows)} index rows -> {len(articles)} items; {len(rejects)} rejects")
print(collections.Counter(a["type"] for a in articles))
print("no author (ART/PP):", sum(1 for a in articles if a["type"] in ("ART", "PP") and not a["authors"]))
print("issues:", len({(a['volume'], a['issue']) for a in articles}), "max vol", max(a["volume"] for a in articles))
print("PP unmatched:", unmatched)
