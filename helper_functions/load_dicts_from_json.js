// Configuration: Number of items to show before "Show more" button
const INITIAL_ITEMS_TO_SHOW = {
    workshops: 3,
    talks: 3,
    publications: 10,
    press: 3,
    news: 5
};
const NEWS_ITEMS_PER_PAGE = 5;

let myVue = new Vue({
    el: "#vue-app",
    data() {
        return {
            publications: [],
            bibs: [],
            events: [],
            talks: [],
            press: [],
            news: [],
            newsToShow: INITIAL_ITEMS_TO_SHOW.news,
            courses: [],
            students: { current: [], alumni: [] },
            studentsTab: 'current', // 'current' or 'alumni'
            showStudents: false,
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
            const limit = INITIAL_ITEMS_TO_SHOW.workshops;
            return this.expandedSections.workshops ? this.events : this.events.slice(0, limit);
        },
        displayedTalks() {
            const limit = INITIAL_ITEMS_TO_SHOW.talks;
            return this.expandedSections.talks ? this.talks : this.talks.slice(0, limit);
        },
        displayedPublications() {
            const limit = INITIAL_ITEMS_TO_SHOW.publications;
            return this.expandedSections.publications ? this.publications : this.publications.slice(0, limit);
        },
        displayedPress() {
            const limit = INITIAL_ITEMS_TO_SHOW.press;
            return this.expandedSections.press ? this.press : this.press.slice(0, limit);
        },
        displayedNews() {
            return this.news.slice(0, this.newsToShow);
        },
        hasMoreNews() {
            return this.newsToShow < this.news.length;
        },
        studentsByType() {
            const grouped = { current: {}, alumni: {} };
            const types = ['PhD', 'MSc', 'Postdoc', 'Intern'];
            
            // Initialize groups
            types.forEach(type => {
                grouped.current[type] = [];
                grouped.alumni[type] = [];
            });
            
            // Group current students
            this.students.current.forEach(student => {
                const type = student.type || 'Other';
                if (!grouped.current[type]) grouped.current[type] = [];
                grouped.current[type].push(student);
            });
            
            // Group alumni
            this.students.alumni.forEach(alumnus => {
                const type = alumnus.type || 'Other';
                if (!grouped.alumni[type]) grouped.alumni[type] = [];
                grouped.alumni[type].push(alumnus);
            });
            
            // Sort current students by startYear (descending - most recent first)
            types.forEach(type => {
                if (grouped.current[type]) {
                    grouped.current[type].sort((a, b) => {
                        const yearA = parseInt(a.startYear) || 0;
                        const yearB = parseInt(b.startYear) || 0;
                        return yearB - yearA; // Descending order
                    });
                }
            });
            
            // Sort alumni by graduationYear (descending - most recent first)
            types.forEach(type => {
                if (grouped.alumni[type]) {
                    grouped.alumni[type].sort((a, b) => {
                        const yearA = parseInt(a.graduationYear) || 0;
                        const yearB = parseInt(b.graduationYear) || 0;
                        return yearB - yearA; // Descending order
                    });
                }
            });
            
            return grouped;
        },
        studentCounts() {
            const counts = { current: {}, alumni: {}, total: { current: 0, alumni: 0 } };
            const types = ['PhD', 'MSc', 'Postdoc', 'Intern'];
            
            types.forEach(type => {
                counts.current[type] = this.students.current.filter(s => (s.type || 'Other') === type).length;
                counts.alumni[type] = this.students.alumni.filter(a => (a.type || 'Other') === type).length;
                counts.total.current += counts.current[type];
                counts.total.alumni += counts.alumni[type];
            });
            
            return counts;
        }
    },
    methods: {
        toggleSection(section) {
            this.expandedSections[section] = !this.expandedSections[section];
        },
        showMoreNews() {
            this.newsToShow += NEWS_ITEMS_PER_PAGE;
        },
        toggleStudents() {
            this.showStudents = !this.showStudents;
        },
        setStudentsTab(tab) {
            this.studentsTab = tab;
        },
        hasMoreItems(section) {
            const limit = INITIAL_ITEMS_TO_SHOW[section] || 3;
            switch(section) {
                case 'workshops':
                    return this.events.length > limit;
                case 'talks':
                    return this.talks.length > limit;
                case 'publications':
                    return this.publications.length > limit;
                case 'press':
                    return this.press.length > limit;
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

// Parse BibTeX file directly from citations.bib
function parseBibTeX(bibtexText) {
    const bibs = {};
    let i = 0;
    const len = bibtexText.length;
    
    while (i < len) {
        // Skip whitespace
        while (i < len && /\s/.test(bibtexText[i])) {
            i++;
        }
        
        if (i >= len) break;
        
        // Skip comment lines
        if (bibtexText[i] === '%') {
            while (i < len && bibtexText[i] !== '\n') {
                i++;
            }
            continue;
        }
        
        // Look for @ to start an entry
        if (bibtexText[i] === '@') {
            const entryStart = i;
            i++; // Skip '@'
            
            // Read entry type
            let entryType = '';
            while (i < len && /[a-zA-Z]/.test(bibtexText[i])) {
                entryType += bibtexText[i];
                i++;
            }
            
            // Skip whitespace
            while (i < len && /\s/.test(bibtexText[i])) {
                i++;
            }
            
            // Expect opening brace
            if (i >= len || bibtexText[i] !== '{') {
                continue;
            }
            i++; // Skip '{'
            
            // Read entry ID (until comma or closing brace)
            let entryId = '';
            while (i < len && bibtexText[i] !== ',' && bibtexText[i] !== '}') {
                if (!/\s/.test(bibtexText[i])) {
                    entryId += bibtexText[i];
                }
                i++;
            }
            entryId = entryId.trim();
            
            if (!entryId || i >= len || bibtexText[i] !== ',') {
                continue;
            }
            i++; // Skip ','
            
            // Find the matching closing brace for the entire entry
            let braceDepth = 1;
            let endPos = -1;
            
            while (i < len && braceDepth > 0) {
                if (bibtexText[i] === '{') {
                    braceDepth++;
                } else if (bibtexText[i] === '}') {
                    braceDepth--;
                    if (braceDepth === 0) {
                        endPos = i;
                        break;
                    }
                }
                i++;
            }
            
            if (endPos > 0 && entryId) {
                // Extract the full entry (from @ to closing brace)
                const entryContent = bibtexText.substring(entryStart, endPos + 1);
                bibs[entryId] = entryContent;
            }
            
            if (i < len) i++; // Move past closing brace
        } else {
            i++;
        }
    }
    
    return bibs;
}

// Load BibTeX file directly
$.get('./cv_files/citations.bib', function(bibtexText) {
    myVue.bibs = parseBibTeX(bibtexText);
}, 'text').fail(function() {
    console.warn('Could not load citations.bib, falling back to bibs.json');
    // Fallback to JSON if BibTeX file not found
    $.getJSON('./cv_files/bibs.json', function (json) {
        myVue.bibs = json;
    });
});

$.getJSON('./cv_files/talks.json', function (json) {
    myVue.talks = json.talks;
});

$.getJSON('./cv_files/press.json', function (json) {
    myVue.press = json.press;
});

$.getJSON('./cv_files/students.json', function (json) {
    // Sort current students by startYear (descending - most recent first)
    json.current.sort((a, b) => {
        const yearA = parseInt(a.startYear) || 0;
        const yearB = parseInt(b.startYear) || 0;
        return yearB - yearA; // Descending order
    });
    
    // Sort alumni by graduationYear (descending - most recent first)
    json.alumni.sort((a, b) => {
        const yearA = parseInt(a.graduationYear) || 0;
        const yearB = parseInt(b.graduationYear) || 0;
        return yearB - yearA; // Descending order
    });
    
    myVue.students = json;
});

$.getJSON('./cv_files/courses.json', function (json) {
    myVue.courses = json.courses;
});

$.getJSON('./cv_files/news.json?t=' + Date.now(), function (json) {
    myVue.news = json.news;
}).fail(function (jqxhr, textStatus, err) {
    console.error('Failed to load news.json:', textStatus, err, jqxhr.responseText || '');
    console.warn('Tip: If you opened index.html as a file (file://), use a local server instead, e.g. run: python3 -m http.server 8000');
});

// Sticky Navigation Bar functionality
document.addEventListener('DOMContentLoaded', function() {
    const nav = document.getElementById('sticky-nav');
    let lastScrollTop = 0;
    const scrollThreshold = 200; // Show nav after scrolling 200px
    
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Show nav when scrolling down past threshold
        if (scrollTop > scrollThreshold) {
            nav.classList.add('visible');
        } else {
            nav.classList.remove('visible');
        }
        
        lastScrollTop = scrollTop;
    });
    
    // Smooth scroll for navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                const offsetTop = targetElement.offsetTop - 80; // Account for nav height
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        });
    });
});

