import bibtexparser
import json
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bibdatabase import BibDatabase

def bib_to_json(bibfile):
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
  with open("./cv_files/bibs.json","w") as f:  
    # f.write('bibs = ')
    json.dump(bib_dict,f, indent = 3)
    print("Created/updated file bibs.json")


def main():
  bib_to_json("./cv_files/citations.bib")

if __name__ == "__main__":
  main()