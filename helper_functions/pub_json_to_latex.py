import json

# Input JSON file
input_json = "./cv_files/publications.json"
# Output LaTeX file
output_tex = "./latex/publications.tex"

# Function to escape LaTeX special characters
def escape_latex(text):
    special_chars = {
        "%": "\\%",
        "&": "\\&",
        "#": "\\#",
        "_": "\\_",
        "{": "\\{",
        "}": "\\}",
        "$": "\\$",
        "^": "\\^{}",
        "~": "\\textasciitilde{}"
    }
    for char, replacement in special_chars.items():
        text = text.replace(char, replacement)
    return text

# Function to fix nested parentheses inside \underline{}
def fix_nested_parentheses(text):
    return text.replace("(", "[").replace(")", "]")

# Function to make "Or Litany" bold in author lists
def bold_or_litany(authors):
    return authors.replace("Or Litany", r"\underline{Or Litany}")

# Load JSON data
with open(input_json, "r", encoding="utf-8") as f:
    data = json.load(f)

# Extract publications
publications = data["publications"]

# Start LaTeX formatted output (requires \\usepackage{enumitem} in main doc)
latex_output = "\\begin{enumerate}[leftmargin=*]\n\n"

for pub in publications:
    title = escape_latex(pub.get("name", "Unknown Title"))
    authors = escape_latex(pub.get("authors", "Unknown Authors"))
    publication = escape_latex(pub.get("publication", "Unknown Conference"))
    paper_link = pub.get("paper", "")
    misc = pub.get("misc", "")

    # Make "Or Litany" bold
    authors = bold_or_litany(authors)

    # Process misc (e.g., "Highlight (top 10% of accepted papers)")
    if misc:
        misc = escape_latex(misc.replace("<mark>", "").replace("</mark>", "").replace("<em>", "").replace("</em>", ""))
        misc = fix_nested_parentheses(misc)  # Replace ( ) with [ ]
        misc = f"\\\\ \\underline{{{misc}}}"  # Add forced line break only if misc exists
    else:
        misc = ""  # Ensure no extra LaTeX commands if misc is empty

    # Formatting LaTeX entry
    entry = f"    \\item \\textbf{{{title}}}, {authors}, \\textit{{{publication}}}{misc}"

    # Add paper link if available
    if paper_link:
        entry += f". \\href{{{paper_link}}}{{[Paper]}}"

    entry += ".\n"  # Keep each entry in a single line
    latex_output += entry

# End LaTeX formatted output
latex_output += "\\end{enumerate}\n"

# Save to file
with open(output_tex, "w", encoding="utf-8") as f:
    f.write(latex_output)

print(f"LaTeX-formatted publications saved to {output_tex}")
