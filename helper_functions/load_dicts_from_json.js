let events = {};
$.getJSON('./cv_files/workshops.json', function(json) {
    events = json;
});

let data = {};
$.getJSON('./cv_files/publications.json', function(json) {
    data = json;
});

let bibs = {};
$.getJSON('./cv_files/bibs.json', function(json) {
    bibs = json;
});

let talks = {};
$.getJSON('./cv_files/talks.json', function(json) {
    talks = json;
});
