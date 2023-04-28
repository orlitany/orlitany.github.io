import json
from pylatex import Document, Section, Subsection, Command, Enumerate, Itemize, Package, Tabular
from pylatex.utils import bold

# read academic CV data from JSON file
with open('./cv_files/cv.json', 'r') as f:
    data = json.load(f)

# create a new document with default settings
from pylatex import Document, Section, Subsection, Itemize, Enumerate
from pylatex.utils import NoEscape

doc = Document(documentclass='res', document_options=['margin', 'line'],fontenc=None, inputenc=None,lmodern=False,textcomp=False,page_numbers=False)
# doc = Document(documentclass='res', document_options=['margin', 'line'])
# 

# create the document class and set the parameters
cv_preample = NoEscape(r"""
\oddsidemargin -.5in
\evensidemargin -.5in
\textwidth=6.0in
\itemsep=0in
\parsep=0in

\newenvironment{list1}{
  \begin{list}{\ding{113}}{%
      \setlength{\itemsep}{0in}
      \setlength{\parsep}{0in} \setlength{\parskip}{0in}
      \setlength{\topsep}{0in} \setlength{\partopsep}{0in}
      \setlength{\leftmargin}{0.17in}}}{\end{list}}
\newenvironment{list2}{
  \begin{list}{$\bullet$}{%
      \setlength{\itemsep}{0in}
      \setlength{\parsep}{0in} \setlength{\parskip}{0in}
      \setlength{\topsep}{0in} \setlength{\partopsep}{0in}
      \setlength{\leftmargin}{0.2in}}}{\end{list}}
""")


doc.preamble.append(Command('usepackage', 'color'))
doc.preamble.append(Command('usepackage', 'hyperref'))
doc.preamble.append(cv_preample)

# start the document
# doc.append(NoEscape('\\name{{{0} \\vspace*{{{1}}}}}'.format(data["name"], "0.1in")))
# doc.append(NoEscape(fr'\name{{{data["name"]} \vspace*{{{"0.1in"}}}}}'))
# doc.append(NoEscape(fr'\begin{{resume}}'))

# Add contact information section
# doc.append(NoEscape(fr'Escape is here:\n but still {"hi"}'))
doc.append(
r"""\name{{ {} \vspace*{{ {} }} }}""".format(data["name"], ".1in"))



# doc.append(NoEscape(r"""
# \name{ {} \vspace*{} }""".format(data["name"],".1in")))

# \begin{resume}
# \section{\sc Contact Information}
# \vspace{.05in}
# \begin{tabular}{@{}p{2in}p{4in}}
# Senior Research Scientist,    & {\it Cell:}  (+1)669-264-3983 \\
# NVIDIA &  {\it E-mail:}  orlitany at gmail dot com\\ 
#  &  {\it Homepage:} \url{https://orlitany.github.io} \\
# \end{tabular}


# \section{\sc Research Interests}
# Computer Vision, 3D Deep Learning for Scene Understanding, Generative AI, Learning under limited supervision.



 



# doc.append(Command('maketitle'))
# doc.append(Command('tableofcontents'))

# add education section
# with doc.create(Section('Education')):
#     for edu in data['education']:
#         with doc.create(Subsection(edu['degree'])):
#             doc.append(bold(edu['institution']))
#             doc.append(f", {edu['location']}, {edu['date']}")
#             with doc.create(Itemize()) as itemize:
#                 for detail in edu['details']:
#                     itemize.add_item(detail)

# add employment section
# with doc.create(Section('Employment')):
#     for emp in data['employment']:
#         with doc.create(Subsection(emp['position'])):
#             doc.append(bold(emp['institution']))
#             doc.append(f", {emp['location']}, {emp['date']}")
#             doc.append('\nResponsibilities:')
#             with doc.create(Itemize()) as itemize:
#                 for res in emp['responsibilities']:
#                     itemize.add_item(res)

# add publications section
# with doc.create(Section('Publications')):
#     with doc.create(Subsection('Selected Publications')):
#         with doc.create(Enumerate()) as enum:
#             for pub in data['publications']:
#                 enum.add_item(f"{pub['authors']}. \"{pub['title']}\". {pub['journal']}, {pub['date']}.")

# save the LaTeX document to a file
# doc.generate_pdf('academic_cv', clean_tex=False)
doc.generate_tex('./latex/academic_cv')
