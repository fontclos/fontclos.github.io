import pandas as pd
import getorg
from geopy import Nominatim
import os


html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    if type(text) is str:
        return "".join(html_escape_table.get(c,c) for c in text)
    else:
        return "False"


articles = pd.read_csv("talks.tsv", sep="\t", header=0)
geocoder = Nominatim()
loc_dict = {}
count = 0

for row, item in articles.iterrows():
    md_filename = str(item.date) + "-" + item.slug + ".md"
    html_filename = str(item.date) + "-" + item.slug 
    year = item.date[:4]

    map_text = item.date + ", " + item.talk_type + " at " + item.venue + "<br/>\n"
    map_text += "<a href='https://staeiou.github.io/talks/" + html_filename + "' target='_blank'>"
    map_text += html_escape(item.title) + "</a>"
    loc = geocoder.geocode(item.geoloc)
    loc_dict[map_text] = loc
    count += 1
    
    
    md = "---\ntitle: \""   + item.title + '"\n'
    md += "collection: talks" + "\n"
    if item.talk_type is not None:
        md += 'talk_type: "' + item.talk_type + '"\n'
    
    md += "permalink: /talks/" + html_filename + "\n"
    
    if item.venue is not None:
        md += 'venue: "' + item.venue + '"\n'
        
    if item.date is not None:
        md += "date: " + str(item.date) + "\n"
    
    if item.geoloc is not None:
        md += 'location: "' + str(item.geoloc) + '"\n'
       
    
    if len(str(item.summary))>10:
        md += 'excerpt: "'
        md += html_escape(item.summary) + '"\n'
    elif len(str(item.description))>10:
        if len(str(item.description))>200:
            md += 'excerpt: "'
            md += html_escape(item.description[:200])
            md += '..."\n'
        else:
            md += 'excerpt: "'
            md += html_escape(item.description) + '"\n'
    
    md += "---\n"
    
    if isinstance(item.url, str):
        md += "\n<a href='" + str(item.url) + "'>Link to more information</a>\n" 
    
    if len(str(item.description))>10:
        md += "\n" + html_escape(item.description) + "\n"
    md_filename = "../_talks/" + os.path.basename(md_filename)
    print(md)
    
    with open(md_filename, 'w') as f:
        f.write(md)

# talks map
m = getorg.orgmap.create_map_obj()
getorg.orgmap.map_location_dict(m, loc_dict)
getorg.orgmap.output_html_cluster_map(loc_dict, hashed_usernames=False)