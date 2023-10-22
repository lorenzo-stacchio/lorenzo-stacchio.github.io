# pip install bibtexparser
import os
import bibtexparser
import copy
import markdown
import markdown_it
import codecs
import datetime


def parse_bibtex_file(file_path):
    with open(file_path, 'r') as bibtex_file:
        parser = bibtexparser.bparser.BibTexParser()
        parser.customization = bibtexparser.customization.convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
        return bib_database


def generateMD(citation, featured=False, mode="journal"):
    # print(citation)
    final_md = "---\n"
    title = citation['title']
    title = title.replace(":", " ")

    final_md += f"title: '{title}'\n"
    final_md += "authors:\n"
    # print(citation["author"])
    for author in citation["author"].split(" and "):
        print(author)
        surname, name = [x.strip() for x in author.split(",")]
        final_md += f"- {name} {surname}\n"

    final_md += "author_notes:\n"
    # print(citation["author"])
    for author in citation["author"].split("and"):
        final_md += f"- \"\"\n"

    if "year" in citation:
        parsed_date = datetime.datetime.strptime(citation['year'], "%Y")
    else: # if none specificed, use actual year
        parsed_date =  datetime.datetime.strptime(str(datetime.datetime.now().year), "%Y")

    final_md += f"date: \"{parsed_date}\"\n"

    final_md += f"doi: \"\"\n"

    final_md += f"publishDate: \"2017-01-01T00:00:00Z\"\n"

    if mode == "journal":
        final_md += f"publication_types:  [\"article-journal\"]\n"
    else:
        final_md += f"publication_types:  [\"paper-conference\"]\n"

    # # Publication name and optional abbreviated publication name.
    if mode == "journal":
        final_md += f"publication: {citation['journal']}, {citation['publisher']}\n"
    else:
        print(citation)
        if "booktitle" in citation:
            final_md += f"publication: {citation['booktitle']}\n"
        else:
            final_md += f"publication: \"\"\n"

    final_md += f"publication_short: \"\"\n"
    final_md += f"abstract:  \"\"\n"

    # abstract: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere tellus ac convallis placerat. Proin tincidunt magna sed ex sollicitudin condimentum. Sed ac faucibus dolor, scelerisque sollicitudin nisi. Cras purus urna, suscipit quis sapien eu, pulvinar tempor diam. Quisque risus orci, mollis id ante sit amet, gravida egestas nisl. Sed ac tempus magna. Proin in dui enim. Donec condimentum, sem id dapibus fringilla, tellus enim condimentum arcu, nec volutpat est felis vel metus. Vestibulum sit amet erat at nulla eleifend gravida.

    # # Summary. An optional shortened abstract.
    final_md += f"summary:  \"\"\n"

    # TAGS
    final_md += f"tags:\n"
    final_md += f"- Source Themes\n"
    final_md += f"featured: {str(featured).lower()}\n"

    # tags:
    # - Source Themes
    # featured: false

    # # links:
    # # - name: ""
    # #   url: ""
    # url_pdf: http://arxiv.org/pdf/1512.04133v1
    # url_code: 'https://github.com/wowchemy/wowchemy-hugo-themes'
    # url_dataset: ''
    # url_poster: ''
    # url_project: ''
    # url_slides: ''
    # url_source: ''
    # url_video: ''
    final_md += "---\n"

    # final_md += "{{% callout note %}}\n Click the *Cite* button above to demo the feature to enable visitors to import publication metadata into their reference management software. \n{{% /callout %}}\n"

    return final_md

# You can access other fields as well, e.g., citation['author'], citation['year'], etc.


journals = "/workspaces/lorenzo-stacchio.github.io/content/publication/journals.bib"
conferences = "/workspaces/lorenzo-stacchio.github.io/content/publication/conferences.bib"

pub_dir = "/workspaces/lorenzo-stacchio.github.io/content/publication/"

journal_citations = parse_bibtex_file(journals)
conference_citations = parse_bibtex_file(conferences)

print(journal_citations)

# block_mode = [(journal_citations, "journal"),(conference_citations, "conference")]

block_mode = [(conference_citations, "conference"),
              (journal_citations, "journal")]

for (citations_n, mode) in block_mode:
    for idx, citation in enumerate(citations_n.entries):
        bib_database_n = copy.deepcopy(citations_n)
        bib_database_n.entries = bib_database_n.entries[idx:idx+1]

        title = citation['title']
        out_dir = pub_dir + title + "/"
        print(citation)
        if not os.path.exists(out_dir):
            os.mkdir(out_dir)
        bib = out_dir + "cite.bib"

        with open(bib, 'w') as bibtex_file:
            bibtexparser.dump(bib_database_n, bibtex_file)

        # NEW MD FILE
        last_n = 2
        md = generateMD(citation, featured=idx >= len(
            citations_n.entries)-last_n, mode=block_mode)
        print(md)
        md_out = out_dir + "index.md"

        with open(md_out, 'w') as md_file:
            md_file.write(md)
        # break
