# pip install bibtexparser
import os
import bibtexparser
import copy 
import markdown
import markdown_it
import codecs

def parse_bibtex_file(file_path):
    with open(file_path, 'r') as bibtex_file:
        parser = bibtexparser.bparser.BibTexParser()
        parser.customization = bibtexparser.customization.convert_to_unicode
        bib_database = bibtexparser.load(bibtex_file, parser=parser)
        return bib_database

def parse_MD(file_path):
    # Read the input Markdown file
    with codecs.open(file_path, mode='r', encoding='utf-8') as file:
        md_content = file.read()

    # Parse the Markdown content
    md_parser = markdown_it.MarkdownIt()
    parsed_content = md_parser.render(md_content)
    return parsed_content

# You can access other fields as well, e.g., citation['author'], citation['year'], etc.

journals = "/workspaces/lorenzo-stacchio.github.io/content/publication/journal-article/cite.bib"
template_journal_md = "/workspaces/lorenzo-stacchio.github.io/content/publication/journal-article/index.md"
pub_dir = "/workspaces/lorenzo-stacchio.github.io/content/publication/"

journal_citations = parse_bibtex_file(journals)

print(journal_citations)
# Now, 'citations' is a list of dictionaries, with each dictionary representing a BibTeX entry.
# You can access fields like 'author', 'title', 'year', etc. in each entry.
print(parse_MD(template_journal_md))

for idx, citation in enumerate(journal_citations.entries):
    bib_database = copy.deepcopy(journal_citations)
    bib_database.entries = bib_database.entries[idx:idx+1] 
    title = citation['title']
    # print(citation.keys())
    # print(citation['title'])
    out_dir = pub_dir + title + "/"
    print(out_dir)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    bib = out_dir + "cite.bib"

    with open(bib, 'w') as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)

    break