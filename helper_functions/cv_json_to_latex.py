import json

# Read the CV data from JSON file
with open('cv_files/cv.json', 'r') as f:
    cv = json.load(f)
    print(cv)

# Define the LaTeX template
template = r"""
\begin{document}
\end{tabular}
"""
latex_doc = template.format(first_last="Or Litany")

# Write the LaTeX document to file
with open('cv.tex', 'w') as f:
    f.write(template)
