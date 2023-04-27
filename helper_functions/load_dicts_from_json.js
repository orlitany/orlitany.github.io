let myVue = new Vue({
    el: "#vue-app",
    data() {
        return {
            publications: [],
            bibs: [],
            events: [],
            talks: [],
        };
    },
    methods: {
        breakbib2(x) {
            if (x.bibtex in this.bibs) { return this.bibs[x.bibtex]; } else {
                return "Coming soon";
            }
        },
        breakbib(x) {
            bib_split = x.split(",");
            if (bib_split.length == 1) { return bib_split[0]; }
            bib_first = bib_split[0] + ",\n ";
            bib_rest = bib_split.slice(1).join(",").split("},").join("},\n ");
            // breakline for final }
            bib_rest = bib_rest.slice(0, -1) + "\n" + bib_rest.slice(-1);
            return bib_first + bib_rest;
        },
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

