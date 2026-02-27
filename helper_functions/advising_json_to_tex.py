import json
import re

def format_author(name):
    """
    Formats a full name into 'F.Lastname' format and underlines 'O.Litany'.
    """
    # Clean up whitespace and HTML tags like <br> if present
    name = name.replace('<br>', '').replace('</br>', '').strip()
    
    parts = name.split()
    if not parts:
        return ""
    
    # Handle cases where there might be a middle name or initial
    # Strategy: Take the first character of all parts except the last one
    formatted_name = name
    if len(parts) > 1:
        initials = "".join([p[0] for p in parts[:-1]])
        last_name = parts[-1]
        formatted_name = f"{initials}.{last_name}"
    
    # Check if this is the target author to underline
    # Checks for "Litany" to be robust against "Or Litany", "O.Litany", etc.
    if "Litany" in formatted_name:
        return f"\\underline{{{formatted_name}}}"
    
    return formatted_name

def escape_latex_percent(text):
    """Escape % for LaTeX (e.g. in '10%' -> '10\\%')."""
    return (text or "").replace("%", "\\%")


def process_misc(misc_str):
    """
    Converts HTML tags in 'misc' (like <mark>) to LaTeX.
    All marked content (Spotlight, Oral, Highlight, Best Paper, etc.) is colored red.
    """
    if not misc_str:
        return ""

    def format_mark_content(content):
        content = escape_latex_percent(content)
        return f' \\textcolor{{red}}{{{content}}}'

    # Replace <mark>Content</mark> with red text
    processed = re.sub(
        r'<mark>(.*?)</mark>',
        lambda m: format_mark_content(m.group(1)),
        misc_str
    )

    return processed


def is_preprint(pub):
    """True if the publication is a preprint (Preprint, arXiv, etc.)."""
    venue = (pub.get('publication') or '').strip().lower()
    if not venue:
        return False
    return venue == 'preprint' or venue == 'arxiv' or 'preprint' in venue or 'arxiv' in venue


def format_entry(pub):
    """Format a single publication as one line (title, authors, venue, misc)."""
    title = f"``{escape_latex_percent(pub['name'])}''"
    raw_authors = pub.get('authors', '')
    author_list = [a.strip() for a in raw_authors.split(',')]
    formatted_authors = [format_author(a) for a in author_list if a.strip()]
    authors_str = ", ".join(formatted_authors)
    venue = escape_latex_percent(pub.get('publication', ''))
    misc = process_misc(pub.get('misc', ''))
    return f"{title}, {authors_str}, {venue}{misc}."


def json_to_tex(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        publications = data.get('publications', [])
        published = [p for p in publications if not is_preprint(p)]
        preprints = [p for p in publications if is_preprint(p)]
        
        published_lines = [format_entry(pub) for pub in published]
        preprint_lines = [format_entry(pub) for pub in preprints]
            
        # Write to .tex file: main list, then Preprints section with its list
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\\begin{enumerate}\n\n")
            f.write("\n\n".join(f"\\item {line}" for line in published_lines))
            f.write("\n\n\\end{enumerate}\n\n")
            f.write("\\section{\\sc Preprints}\n\n")
            f.write("\\begin{enumerate}\n\n")
            f.write("\n\n".join(f"\\item {line}" for line in preprint_lines))
            f.write("\n\n\\end{enumerate}\n")
            
        print(f"Successfully converted {len(published_lines)} publications + {len(preprint_lines)} preprints to {output_file}")

    except FileNotFoundError:
        print(f"Error: Could not find file '{input_file}'")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{input_file}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# ---------------------------------------------------------------------------
# Advising: students.json -> advising.tex (list2 format for res.cls)
# ---------------------------------------------------------------------------

def escape_latex_special(text):
    """Escape &, %, _ for LaTeX in names/notes."""
    return (text or "").replace("&", "\\&").replace("%", "\\%").replace("_", "\\_")


def format_advising_current(student):
    name = escape_latex_special(student.get("name", ""))
    start = student.get("startYear", "")
    note = escape_latex_special((student.get("note") or "").strip())
    if note:
        return f"  \\item {name} ({note}), {start} -- Present"
    return f"  \\item {name}, {start} -- Present"


def format_advising_alumni(student):
    name = escape_latex_special(student.get("name", ""))
    year = student.get("graduationYear", "")
    pos = escape_latex_special((student.get("currentPosition") or "").strip())
    note = escape_latex_special((student.get("note") or "").strip())
    if note and not pos:
        return f"  \\item {name} ({note}), Graduated {year}"
    if pos and note:
        return f"  \\item {name} ({note}), Graduated {year} (Next: {pos})"
    if pos:
        return f"  \\item {name}, Graduated {year} (Next: {pos})"
    return f"  \\item {name}, Graduated {year}"


def students_to_advising_tex(input_file, output_file):
    """Generate advising.tex from students.json (list2 format for res.cls)."""
    try:
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        current = data.get("current", [])
        alumni = data.get("alumni", [])

        def by_type(students, t):
            return [s for s in students if (s.get("type") or "").strip() == t]

        sections = ["\\section{\\sc Advising}", ""]
        for kind, title in [
            ("PhD", "PhD Students"),
            ("MSc", "MSc Students"),
            ("Postdoc", "Postdoc"),
            ("Intern", "Interns"),
        ]:
            cur = by_type(current, kind)
            alu = by_type(alumni, kind)
            if cur or alu:
                sections.append(f"{{\\bf {title}}}")
                sections.append("\\begin{list2}")
                sections.extend(format_advising_current(s) for s in cur)
                sections.extend(format_advising_alumni(s) for s in alu)
                sections.append("\\end{list2}")
                sections.append("\\vspace*{.05in}")
                sections.append("")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(sections).rstrip() + "\n")
        print(f"Successfully wrote advising to {output_file}")
    except FileNotFoundError:
        print(f"Error: Could not find file '{input_file}'")
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{input_file}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    students_to_advising_tex("cv_files/students.json", "latex/advising.tex")