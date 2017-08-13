import pandas as pd
import os

articles = pd.read_csv("publications.tsv", sep="\t", header=0)

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

for row, item in articles.iterrows():
    md_filename = str(item.pub_date) + "-" + item.slug + ".md"
    html_filename = str(item.pub_date) + "-" + item.slug 
    year = item.pub_date[:4]
    md = "---\ntitle: \""   + item.title + '"\n'
    
    md += """collection: publication\npermalink: /publication/""" + html_filename
    md += "\ndate: " + str(item.pub_date) 
    md += "\nvenue: '" + html_escape(item.venue) + "'"
    if type(item.journalurl) is str:
        md += "\njournalurl: '" + item.journalurl + "'"
    if type(item.pdfurl) is str:
        md += "\npdfurl: '" + item.pdfurl + "'"
    if type(item.arxivurl) is str:
        md += "\narxivurl: '" + item.arxivurl + "'"
    if type(item.imageurl) is str:
        md += "\nimageurl: '" + item.imageurl + "'"
    if type(item.citation) is str:
        md += "\ncitation: '" + html_escape(item.citation) + "'"
    md += "\n---"
    if type(item.imageurl) is str:
        md += "\n![image](/images/" + item.imageurl + ")  "
    md += "\nAbstract: " + html_escape(item.description) + "\n"
    md_filename =  "../_publications/"+os.path.basename(md_filename)
    with open(md_filename, 'w') as f:
        f.write(md)
