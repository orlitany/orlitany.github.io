import bibtexparser
import json
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

def bib_to_js(bibfile):
  # read bib file into a bibtex dbase
  with open(bibfile) as bibtex_file:
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
  with open("./bibs.js","w") as f:  
    f.write('bibs = ')
    json.dump(bib_dict,f, indent = 3)
    print("Created/updated file bibs.js")

def workshops_to_js(json_file):
  with open("./cv/workshops.json","r") as f:  
    content = f.read()
  with open("./workshops.js","w") as f:  
    f.write("events = " + content)
  

    
    # f.write('workshops = '+content)    
    # print("Created/updated file workshops.js") 

def main():
  bib_to_js("./cv/citations.bib")
  workshops_to_js("./cv/workshops.json")

if __name__ == "__main__":
  main()