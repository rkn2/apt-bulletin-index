# APT Bulletin content index

Every APT Bulletin item we could find, 1969 to 2026 (vol. 1 to 56.2): title, authors, year, volume and issue, type (article, Practice Point, book review, ...), the APT index's subject headings, and suggested tags for the APT technical committees, disaster work (DRI), and discipline (engineering, architecture, conservation). Built for the APT Publications Committee to see how content is spread across committees and disciplines.

## Where the data comes from

| Source | Covers | Used for |
|---|---|---|
| APT Comprehensive Index spreadsheet (apti.org, dated 2025-12-19) | 1969 to 2025 (vol. 1 to 55) | Subject headings (Topics column) for every item it lists; the only source for 2005 to 2007, issues 43.1 to 44.2/3 and 48.1, and for individual book reviews after 2008 |
| Crossref (JSTOR DOIs) | 1969 to 2004 (vol. 1 to 35) | Titles, authors, issue, page and DOI link |
| Table-of-contents PDFs posted on apti.org | 2008 to 2026 (vol. 39 to 56.2, missing 43.x, 44.x, 48.1) | Titles, authors, issue, page, Practice Point numbers |
| Practice Points page on apti.org | Practice Points 1 to 31 | PP numbers and PDF links |

When sources disagree, the TOC wins, then Crossref, then the index. The index has errors in recent volumes (vol. 52 lists the same article at several page numbers and mixes book reviewers into author lists), so for 2008 onward it supplies only topics.

## Known gaps

- Vol. 25 no. 1/2 (1993) and vol. 44 no. 4 (2013): not in any source we could reach. JSTOR (members only) has them.
- Vols. 1 to 4 (1969 to 1972) are thin: the early Newsletter/Bulletin years are only partly indexed.
- Book reviews after 2008 come from the index only (the TOCs list "Book Reviews" as one section). Index-only items in issues we have a TOC for are labelled "Book review or minor item (index only)".
- 63 index rows had references we could not parse; they are on the "Index rows not parsed" sheet.
- 49 items from 1969 to 2004 are "Article (type not indexed; may be a review)": JSTOR has them but the APT index doesn't, so their type is unknown. Some are book reviews (JSTOR then lists the book's author as an author too). The Summary sheet counts them as articles.
- Years for 2008 onward are the © year printed on each TOC, so a volume can span two years (vol. 54 is 2024 and 2025).
- Authors are as printed; the same person can appear in slightly different forms (e.g. "Lauren R. Hall" / "Lauren Reynolds Hall").

## Tags are suggestions

The committee and discipline columns were filled by a model from each item's title, topics and type, following RUBRIC.md. Nobody read the articles. Discipline describes the piece's main lens, not the authors' training. "Tag confidence" is low where the title is vague. Use the Reviewed column as the committee checks rows.

Committees: TC-Doc (Documentation), TCM (Materials), PETC (Preservation Engineering), Codes & Standards, TC-MH (Modern Heritage), TC-SP (Sustainable Preservation), plus Disaster (APTI Disaster Response Initiative, not a technical committee).

## Explore it

- Interactive page: https://rkn2.github.io/apt-bulletin-index/
- `docs/data/apt_bulletin_articles.csv`: articles and Practice Points, one row each. The tag columns are 1/0: `doc`, `mat`, `petc`, `codes`, `mh`, `sp`, `dis` (committees and disaster) and `eng`, `arch`, `cons` (discipline). `confidence` is the tagger's high/low.
- `docs/data/APT_Bulletin_Content_Index.xlsx`: the full workbook, including book reviews, letters and editorials on separate sheets, with a column for marking reviewed tags.
- `build/master.csv`: every item from every source before tagging, with source, DOI and APT index references.

Found a wrong tag, title or author? Open an issue.

## Rebuilding

APT's index spreadsheet and table-of-contents PDFs are APT's files and are not in this repo; `fetch_sources.sh` downloads them from apti.org.

```
./fetch_sources.sh                             # APT index + TOC PDFs -> raw/
uv run --with openpyxl python build_index.py   # index -> build/articles.csv
uv run python build_master.py                  # + Crossref + TOCs -> build/master.csv
uv run --with openpyxl python export_xlsx.py   # + tags -> build/APT_Bulletin_Content_Index.xlsx
cp build/APT_Bulletin_Content_Index.xlsx docs/data/   # and regenerate docs/data/apt_bulletin_articles.csv from its first sheet
```

TOC parsing (toc_parsers/) and tagging (build/classify/) were done by model agents; their outputs are saved, so rebuilding does not rerun them.

Built 2026-10-28.
