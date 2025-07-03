let myVue = new Vue({
    el: "#vue-app",
    data() {
        return {
            publications: [],
            bibs: [],
            events: [],
            talks: [],
            press: [],
            expandedSections: {
                workshops: false,
                talks: false,
                publications: false,
                press: false
            }
        };
    },
    computed: {
        displayedWorkshops() {
            return this.expandedSections.workshops ? this.events : this.events.slice(0, 3);
        },
        displayedTalks() {
            return this.expandedSections.talks ? this.talks : this.talks.slice(0, 3);
        },
        displayedPublications() {
            return this.expandedSections.publications ? this.publications : this.publications.slice(0, 3);
        },
        displayedPress() {
            return this.expandedSections.press ? this.press : this.press.slice(0, 3);
        }
    },
    methods: {
        toggleSection(section) {
            this.expandedSections[section] = !this.expandedSections[section];
        },
        hasMoreItems(section) {
            switch(section) {
                case 'workshops':
                    return this.events.length > 3;
                case 'talks':
                    return this.talks.length > 3;
                case 'publications':
                    return this.publications.length > 3;
                case 'press':
                    return this.press.length > 3;
                default:
                    return false;
            }
        },
        breakbib2(x) {
            if (x.bibtex in this.bibs) { return this.bibs[x.bibtex]; } else {
                return "Coming soon";
            }
        },
        breakbib(x) {
  let bib_split = x.split(",");
  if (bib_split.length === 1) return bib_split[0];
  const firstLine = bib_split[0] + ",\n";
  const rest = bib_split.slice(1).map(s => s.trim()).join(",\n");
  return firstLine + rest;
}
,
        boldMyName(x) {
            let phrase = "Or Litany";
            let pos = x.search(phrase);
            let length = phrase.length;
            x = x.slice(0, pos) + "<strong>" + x.slice(pos, pos + length) +
                "</strong>" + x.slice(pos + length);
            return x;
        },
        concat(x) {
            let txt;
            txt = x.name + ", " + x.venue + " " + x.year;
            if ("upcoming" in x) {
                txt = "<mark>[UPCOMING]</mark> " + txt;
            }
            return txt;
        },
        render(x) {
            let txt;
            txt = x.title + ". ";
            if ("slides" in x) {
                txt += "<a :href=\"" + x.slides + "\">Slides</a>";
            }
            //  + ", "+x.venue + " " + x.year            
            // if ("upcoming" in x){
            //   txt = "<mark>[UPCOMING]</mark> " + txt
            // }
            return txt;
        },
        copyBib(paperId) {
    const selector = `[data-paper-id="${paperId}"] .bibtex-block pre span`;
    const span = document.querySelector(selector);
    if (!span) {
        alert("Could not find bib entry");
        return;
    }

    const text = span.textContent;
    navigator.clipboard.writeText(text).then(() => {
        const btn = document.querySelector(`[data-paper-id="${paperId}"] .copy-btn`);
        if (btn) {
            const oldText = btn.innerText;
            btn.innerText = "Copied!";
            setTimeout(() => btn.innerText = oldText, 1000);
        }
    }).catch(err => {
        console.error('Copy failed', err);
        alert('Failed to copy BibTeX.');
    });
}

    }
});

$.getJSON('./cv_files/workshops.json', function (json) {
    myVue.events = json.events;
});

$.getJSON('./cv_files/publications.json', function (json) {
    myVue.publications = json.publications;
});

$.getJSON('./cv_files/bibs.json', function (json) {
    myVue.bibs = json;
});

$.getJSON('./cv_files/talks.json', function (json) {
    myVue.talks = json.talks;
});

$.getJSON('./cv_files/press.json', function (json) {
    myVue.press = json.press;
});

