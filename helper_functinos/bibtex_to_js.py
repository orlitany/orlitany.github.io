import bibtexparser
import json
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

# read bib file into a biubtex dbase
with open("citations.bib") as bibtex_file:
  bib_database = bibtexparser.load(bibtex_file)

# make a new dict to store by bibs by title
bib_dict = {}

writer = BibTexWriter()
for entry_dict in bib_database.entries:
  # entry_dict = bib_database.get_entry_list()[0]
  db = BibDatabase()
  db.entries = [entry_dict]
  bibtex_str = writer.write(db)
  bib_dict[entry_dict['ID']] = bibtex_str
  
# save file to js 
with open("bibs.js","w") as f:  
  f.write('bibs = ')
  json.dump(bib_dict,f, indent = 3)