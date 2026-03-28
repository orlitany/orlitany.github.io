#!/usr/bin/env python3
"""Generate publications.tex and advising.tex from JSON, then compile cv.tex with tectonic."""

import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
CV_FILES = os.path.join(ROOT, "cv_files")
LATEX_DIR = os.path.join(ROOT, "latex")


def abbreviate_author(name):
    """Convert full name to abbreviated: 'FirstName Last Name' -> 'F.Last-Name'."""
    name = name.strip()
    parts = name.split()
    if not parts:
        return name
    initial = parts[0][0]
    last_parts = parts[1:]
    last_name = "-".join(last_parts) if last_parts else ""
    return f"{initial}.{last_name}" if last_name else initial


def format_authors(authors_str):
    """Format comma-separated author names for LaTeX, underlining Or Litany."""
    authors = [a.strip() for a in authors_str.split(",")]
    formatted = []
    for author in authors:
        if author in ("Or Litany", "O. Litany"):
            formatted.append(r"\underline{O.Litany}")
        else:
            formatted.append(abbreviate_author(author))
    return ", ".join(formatted)


def convert_misc(misc):
    """Convert HTML misc field to LaTeX."""
    if not misc:
        return ""
    # <mark>...</mark>  ->  \textcolor{red}{...}
    result = re.sub(
        r"<mark>(.*?)</mark>",
        lambda m: r"\textcolor{red}{" + m.group(1).replace("%", r"\%") + "}",
        misc,
    )
    # <em>...</em>  ->  \emph{...}
    result = re.sub(r"<em>(.*?)</em>", lambda m: r"\emph{" + m.group(1) + "}", result)
    return result


def generate_publications_tex():
    with open(os.path.join(CV_FILES, "publications.json")) as f:
        data = json.load(f)

    pubs = data["publications"]
    published = [p for p in pubs if p.get("publication", "") != "Preprint"]
    preprints = [p for p in pubs if p.get("publication", "") == "Preprint"]

    lines = [r"\begin{enumerate}", ""]
    for pub in published:
        name = pub["name"]
        authors = format_authors(pub["authors"])
        venue = pub.get("publication", "")
        misc = convert_misc(pub.get("misc", ""))

        entry = f'\\item ``{name}\'\', {authors}, {venue}'
        if misc:
            entry += f" {misc}"
        entry += "."
        lines.append(entry)
        lines.append("")
    lines.append(r"\end{enumerate}")

    lines += ["", r"\section{\sc Preprints}", "", r"\begin{enumerate}", ""]
    for pub in preprints:
        name = pub["name"]
        authors = format_authors(pub["authors"])
        misc = convert_misc(pub.get("misc", ""))

        entry = f'\\item ``{name}\'\', {authors}, Preprint'
        if misc:
            entry += f" {misc}"
        entry += "."
        lines.append(entry)
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

    print("Done. PDF generated at latex/cv.pdf")


if __name__ == "__main__":
    main()
