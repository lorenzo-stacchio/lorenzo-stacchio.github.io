# Regenerate content/publication/<title>/{index.md,cite.bib} from the .bib files.
#
#   pip install bibtexparser
#   python content/publication/bib_parsers.py
#
# journals.bib and conferences.bib are the source of truth. Every page under
# content/publication/ is derived from them, so edit the .bib and rerun rather
# than hand-editing a generated index.md.
#
# Custom fields understood beyond standard BibTeX:
#   keywords  comma-separated -> Hugo tags
#   featured  true/false      -> Hugo `featured`
#   exclude   true            -> keep the entry on record but generate no page
#   month     1-12            -> orders publications within a year

import os
import re
import copy
import datetime

import bibtexparser

HERE = os.path.dirname(os.path.abspath(__file__))
JOURNALS = os.path.join(HERE, "journals.bib")
CONFERENCES = os.path.join(HERE, "conferences.bib")
PUB_DIR = HERE

# Fields that are ours, not BibTeX's: kept out of the per-paper cite.bib so the
# snippet a reader copies is valid BibTeX.
PRIVATE_FIELDS = ("keywords", "featured", "exclude")

# Long venue name -> the abbreviation shown in the citation view.
SHORT_NAMES = [
    ("IEEE Transactions on Visualization and Computer Graphics", "IEEE TVCG"),
    ("ACM Transactions on Multimedia Computing, Communications and Applications", "ACM TOMM"),
    ("International Symposium on Mixed and Augmented Reality Adjunct", "ISMAR-Adjunct"),
    ("International Symposium on Mixed and Augmented Reality Workshops", "ISMAR-W"),
    ("International Symposium on Mixed and Augmented Reality", "ISMAR"),
    ("Conference on Virtual Reality and 3D User Interfaces Abstracts and Workshops", "IEEE VRW"),
    ("Winter Conference on Applications of Computer Vision", "WACV"),
    ("International Conference on Image Analysis and Processing", "ICIAP"),
    ("Computer Vision -- ECCV 2024 Workshops", "ECCV Workshops"),
    ("International Conference on Entertainment Computing", "IFIP-ICEC"),
    ("Engineering Applications of Artificial Intelligence", "EAAI"),
    ("International Journal of Digital Earth", "IJDE"),
    ("Digital Applications in Archaeology and Cultural Heritage", "DAACH"),
    ("Metaverse Computing, Networking, and Applications", "IEEE MetaCom"),
    ("Artificial Intelligence and eXtended and Virtual Reality", "IEEE AIxVR"),
    ("Information Technology for Social Good", "ACM GoodIT"),
    ("IEEE Signal Processing Letters", "IEEE SPL"),
    ("Computers in Human Behavior", "CHB"),
    ("Frontiers in Computer Science", "Frontiers CS"),
    ("Frontiers in Virtual Reality", "Frontiers VR"),
    ("Neural Computing and Applications", "NCAA"),
    ("Virtual Reality \\& Intelligent Hardware", "VRIH"),
    ("The Visual Computer", "TVC"),
    ("CEUR Workshop Proceedings", "CEUR-WS"),
    ("Virtual Reality", "Virtual Reality"),
]


def safe_dir_name(title):
    # ':' '?' and friends are illegal in Windows paths and make the repo
    # impossible to check out there. Hugo strips them when building slugs,
    # so removing them keeps the published /publication/ URLs unchanged.
    name = re.sub(r'[:?*"<>|\\/]', "", title)
    name = re.sub(r"\s+", " ", name).strip()
    return name.rstrip(". ")


def yaml_single_quoted(value):
    # In single-quoted YAML the only escape is a doubled quote.
    return "'" + str(value).replace("'", "''") + "'"


def parse_bibtex_file(file_path):
    with open(file_path, "r", encoding="utf-8") as bibtex_file:
        parser = bibtexparser.bparser.BibTexParser(common_strings=True)
        parser.customization = bibtexparser.customization.convert_to_unicode
        parser.ignore_nonstandard_types = False
        return bibtexparser.load(bibtex_file, parser=parser)


def format_authors(citation):
    """'Last, First and Last, First' -> ['First Last', ...]"""
    authors = []
    for author in citation["author"].split(" and "):
        author = author.strip()
        if not author:
            continue
        if "," in author:
            surname, given = [x.strip() for x in author.split(",", 1)]
            authors.append(f"{given} {surname}".strip())
        else:
            authors.append(author)
    return authors


def publication_venue(citation, mode):
    if mode == "journal":
        venue = citation.get("journal", "")
        publisher = citation.get("publisher", "")
        return f"{venue}, {publisher}" if publisher else venue
    return citation.get("booktitle", "")


def short_name(venue):
    for needle, short in SHORT_NAMES:
        if needle.lower() in venue.lower():
            return short
    return ""


def entry_date(citation):
    year = int(citation.get("year", datetime.datetime.now().year))
    try:
        month = max(1, min(12, int(citation.get("month", 1))))
    except ValueError:
        month = 1
    return datetime.date(year, month, 1)


def generateMD(citation, mode="journal"):
    title = citation["title"]
    venue = publication_venue(citation, mode)
    date = entry_date(citation)

    lines = ["---"]
    lines.append(f"title: {yaml_single_quoted(title)}")

    lines.append("authors:")
    for author in format_authors(citation):
        lines.append(f"- {author}")

    lines.append(f'date: "{date.isoformat()}"')
    lines.append(f'publishDate: "{date.isoformat()}"')
    lines.append(f'doi: "{citation.get("doi", "")}"')

    if mode == "journal":
        lines.append('publication_types: ["article-journal"]')
    else:
        lines.append('publication_types: ["paper-conference"]')

    lines.append(f"publication: {yaml_single_quoted(venue)}")
    lines.append(f"publication_short: {yaml_single_quoted(short_name(venue))}")

    # Abstracts are deliberately left empty: the .bib files carry no abstract
    # text, and inventing one would misstate the record.
    lines.append('abstract: ""')
    lines.append('summary: ""')

    keywords = [k.strip() for k in citation.get("keywords", "").split(",") if k.strip()]
    if keywords:
        lines.append("tags:")
        for keyword in keywords:
            lines.append(f"- {keyword}")
    else:
        lines.append("tags: []")

    featured = str(citation.get("featured", "false")).strip().lower() == "true"
    lines.append(f"featured: {str(featured).lower()}")

    if citation.get("url"):
        lines.append(f'url_source: "{citation["url"]}"')

    lines.append("---")
    lines.append("")

    note = citation.get("note", "").strip()
    if note:
        lines.append(note)
        lines.append("")

    return "\n".join(lines)


def write_cite_bib(citations, citation, path):
    """Write a one-entry .bib holding just this paper, without our private fields."""
    single = copy.deepcopy(citations)
    entry = {k: v for k, v in citation.items() if k not in PRIVATE_FIELDS}
    single.entries = [entry]
    single.comments = []
    with open(path, "w", encoding="utf-8", newline="\n") as bibtex_file:
        bibtexparser.dump(single, bibtex_file)


def main():
    generated = set()
    skipped = []

    for citations_path, mode in ((CONFERENCES, "conference"), (JOURNALS, "journal")):
        citations = parse_bibtex_file(citations_path)
        for citation in citations.entries:
            if str(citation.get("exclude", "")).strip().lower() == "true":
                skipped.append(citation["title"])
                continue

            out_dir = os.path.join(PUB_DIR, safe_dir_name(citation["title"]))
            os.makedirs(out_dir, exist_ok=True)
            generated.add(os.path.basename(out_dir))

            write_cite_bib(citations, citation, os.path.join(out_dir, "cite.bib"))

            with open(os.path.join(out_dir, "index.md"), "w",
                      encoding="utf-8", newline="\n") as md_file:
                md_file.write(generateMD(citation, mode=mode))

    print(f"generated {len(generated)} publication pages")
    for title in skipped:
        print(f"  skipped (exclude=true): {title}")

    # A folder with no matching .bib entry keeps a stale cite.bib forever, which
    # is how mismatched citations appeared here before. Surface them loudly.
    existing = {
        name for name in os.listdir(PUB_DIR)
        if os.path.isdir(os.path.join(PUB_DIR, name)) and not name.startswith("_")
        and name != "__pycache__"
    }
    for orphan in sorted(existing - generated):
        print(f"  ORPHAN (no .bib entry): {orphan}")


if __name__ == "__main__":
    main()
