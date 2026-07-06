#!/usr/bin/env python3
"""Generate CV LaTeX from JSON and compile latex/cv.pdf."""

import json
import os
import re
import subprocess
import sys

import bibtexparser
from bibtexparser.customization import splitname

ROOT = os.path.dirname(os.path.abspath(__file__))
CV_FILES = os.path.join(ROOT, "cv_files")
LATEX_DIR = os.path.join(ROOT, "latex")


def format_authors_from_bib(author_field):
    """Format a BibTeX 'author' field for LaTeX, underlining Or Litany.

    Uses bibtexparser's name splitting (handles both 'Last, First' and
    'First Last' BibTeX conventions) rather than naively splitting on
    whitespace, so multi-token first/last names abbreviate correctly.
    """
    names = [n.strip() for n in author_field.split(" and ") if n.strip()]
    formatted = []
    for name in names:
        parts = splitname(name, strict_mode=False)
        first = " ".join(parts.get("first", [])).strip()
        von = " ".join(parts.get("von", [])).strip()
        last = " ".join(parts.get("last", [])).strip()
        jr = " ".join(parts.get("jr", [])).strip()
        last_full = " ".join(p for p in (von, last, jr) if p)

        if first == "Or" and last_full == "Litany":
            formatted.append(r"\underline{O.Litany}")
        else:
            initial = first[0] if first else ""
            last_hyphen = last_full.replace(" ", "-")
            formatted.append(f"{initial}.{last_hyphen}" if last_hyphen else initial)
    return ", ".join(formatted)


def convert_award(award):
    """Render the bib entry's custom 'award' field (a short highlight/badge) for LaTeX."""
    if not award:
        return ""
    return r"\textcolor{red}{" + award.replace("%", r"\%") + "}"


def generate_publications_tex():
    with open(os.path.join(CV_FILES, "publications.bib")) as f:
        bib_db = bibtexparser.load(f)

    pubs = bib_db.entries  # preserved in the curated (newest-first) order
    published = [p for p in pubs if p.get("venue", "") != "Preprint"]
    preprints = [p for p in pubs if p.get("venue", "") == "Preprint"]

    def render_entry(pub):
        name = pub.get("title", "")
        authors = format_authors_from_bib(pub.get("author", ""))
        venue = pub.get("venue", "")
        award = convert_award(pub.get("award", ""))

        entry = f'\\item ``{name}\'\', {authors}, {venue}'
        if award:
            entry += f" {award}"
        entry += "."
        return entry

    lines = [r"\begin{enumerate}", ""]
    for pub in published:
        lines.append(render_entry(pub))
        lines.append("")
    lines.append(r"\end{enumerate}")

    lines += ["", r"\section{\sc Preprints}", "", r"\begin{enumerate}", ""]
    for pub in preprints:
        lines.append(render_entry(pub))
        lines.append("")
    lines.append(r"\end{enumerate}")

    return "\n".join(lines)


def generate_workshops_tex():
    with open(os.path.join(CV_FILES, "workshops.json")) as f:
        data = json.load(f)

    # Regex to detect "Nth Word on/for ..." prefixes, e.g. "6th Workshop on ..."
    ordinal_re = re.compile(r"^(\d+(?:st|nd|rd|th) \w+ (?:on|for) )(.+)$", re.IGNORECASE)

    lines = [r"\begin{itemize}"]
    for event in data["events"]:
        name = event["name"]
        venue = event.get("venue", "")
        year = event["year"]
        typ = event.get("type", "workshop")
        link = event.get("link", "")

        m = ordinal_re.match(name)
        if m:
            core_name = m.group(2)
            ordinal = re.match(r"(\d+(?:st|nd|rd|th))", m.group(1)).group(1)
            ordinal_label = f"{ordinal} {typ}"
        else:
            core_name = name
            ordinal_label = None

        if link:
            name_tex = f"\\href{{{link}}}{{{core_name}}}"
        else:
            name_tex = core_name

        if ordinal_label:
            descriptor = f"{ordinal_label} at {venue}, {year}"
        elif venue:
            descriptor = f"{typ} at {venue}, {year}"
        else:
            descriptor = f"{typ}, {year}"

        lines.append(f"\\item ``{name_tex}'' {descriptor}.")
    lines.append(r"\end{itemize}")

    return "\n".join(lines)


def generate_advising_tex():
    with open(os.path.join(CV_FILES, "students.json")) as f:
        data = json.load(f)

    current = data.get("current", [])
    alumni = data.get("alumni", [])

    types_order = ["PhD", "MSc", "Postdoc", "Intern"]
    type_labels = {
        "PhD": "PhD Students",
        "MSc": "MSc Students",
        "Postdoc": "Postdoc",
        "Intern": "Interns",
    }

    lines = [r"\section{\sc Advising}", ""]

    for typ in types_order:
        current_of_type = [s for s in current if s["type"] == typ]
        alumni_of_type = [s for s in alumni if s["type"] == typ]

        if not current_of_type and not alumni_of_type:
            continue

        lines.append(f"{{\\bf {type_labels[typ]}}}")
        lines.append(r"\begin{list2}")

        for s in current_of_type:
            name = s["name"]
            year = s.get("startYear", "")
            note = s.get("note", "")
            entry = f"  \\item {name}"
            if note:
                entry += f" ({note})"
            entry += f", {year} -- Present"
            lines.append(entry)

        for s in alumni_of_type:
            name = s["name"]
            year = s.get("graduationYear", "")
            position = s.get("currentPosition", "")
            note = s.get("note", "")
            entry = f"  \\item {name}"
            if note:
                entry += f" ({note})"
            entry += f", Graduated {year}"
            if position:
                entry += f" (Next: {position})"
            lines.append(entry)

        lines.append(r"\end{list2}")
        lines.append(r"\vspace*{.05in}")
        lines.append("")

    return "\n".join(lines)


def main():
    print("Generating publications.tex...", flush=True)
    publications_tex = generate_publications_tex()
    publications_path = os.path.join(LATEX_DIR, "publications.tex")
    with open(publications_path, "w") as f:
        f.write(publications_tex)
    print(f"  Written: {publications_path}", flush=True)

    print("Generating workshops.tex...", flush=True)
    workshops_tex = generate_workshops_tex()
    workshops_path = os.path.join(LATEX_DIR, "workshops.tex")
    with open(workshops_path, "w") as f:
        f.write(workshops_tex)
    print(f"  Written: {workshops_path}", flush=True)

    print("Generating advising.tex...", flush=True)
    advising_tex = generate_advising_tex()
    advising_path = os.path.join(LATEX_DIR, "advising.tex")
    with open(advising_path, "w") as f:
        f.write(advising_tex)
    print(f"  Written: {advising_path}", flush=True)

    print("Compiling cv.tex with tectonic...", flush=True)
    result = subprocess.run(
        ["tectonic", "cv.tex"],
        cwd=LATEX_DIR,
    )
    if result.returncode != 0:
        print("ERROR: tectonic failed.", file=sys.stderr)
        sys.exit(result.returncode)

    built_pdf = os.path.join(LATEX_DIR, "cv.pdf")
    print(f"Done. PDF at {built_pdf}")


if __name__ == "__main__":
    main()
