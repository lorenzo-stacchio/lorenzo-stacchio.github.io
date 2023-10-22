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

def generateMD(citation, featured = False):
    print(citation)
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

    parsed_date = datetime.datetime.strptime(citation['year'], "%Y")

    final_md += f"date: \"{parsed_date}\"\n"

    final_md += f"doi: \"\"\n"    
    
    final_md += f"publishDate: \"2017-01-01T00:00:00Z\"\n"    

    final_md += f"publication_types:  [\"article-journal\"]\n"    


    # # Publication name and optional abbreviated publication name.
    final_md += f"publication: {citation['journal']}, {citation['publisher']}\n"
    final_md += f"publication_short: \"\"\n"
    final_md += f"abstract:  \"\"\n"    

    # abstract: Lorem ipsum dolor sit amet, consectetur adipiscing elit. Duis posuere tellus ac convallis placerat. Proin tincidunt magna sed ex sollicitudin condimentum. Sed ac faucibus dolor, scelerisque sollicitudin nisi. Cras purus urna, suscipit quis sapien eu, pulvinar tempor diam. Quisque risus orci, mollis id ante sit amet, gravida egestas nisl. Sed ac tempus magna. Proin in dui enim. Donec condimentum, sem id dapibus fringilla, tellus enim condimentum arcu, nec volutpat est felis vel metus. Vestibulum sit amet erat at nulla eleifend gravida.

    # # Summary. An optional shortened abstract.
    final_md += f"summary:  \"\"\n"

    ### TAGS
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
    final_md +="---\n"

    final_md +="{{% callout note %}}\n Click the *Cite* button above to demo the feature to enable visitors to import publication metadata into their reference management software. \n{{% /callout %}}\n"


    return final_md

# You can access other fields as well, e.g., citation['author'], citation['year'], etc.

journals = "/workspaces/lorenzo-stacchio.github.io/content/publication/journals.bib"
template_journal_md = "/workspaces/lorenzo-stacchio.github.io/static/templates/template_journal_index.md"
pub_dir = "/workspaces/lorenzo-stacchio.github.io/content/publication/"

journal_citations = parse_bibtex_file(journals)

print(journal_citations)
# Now, 'citations' is a list of dictionaries, with each dictionary representing a BibTeX entry.
# You can access fields like 'author', 'title', 'year', etc. in each entry.

for idx, citation in enumerate(journal_citations.entries):
    bib_database = copy.deepcopy(journal_citations)
    bib_database.entries = bib_database.entries[idx:idx+1] 
    title = citation['title']
    print(citation.keys())
    out_dir = pub_dir + title + "/"
    print(out_dir)
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)
    bib = out_dir + "cite.bib"

    with open(bib, 'w') as bibtex_file:
        bibtexparser.dump(bib_database, bibtex_file)

    ## NEW MD FILE
    last_n = 2
    md = generateMD(citation, featured = idx >= len(journal_citations.entries)-last_n)
    print(md)
    md_out = out_dir + "index.md"

    with open(md_out, 'w') as md_file:
        md_file.write(md)
    # break