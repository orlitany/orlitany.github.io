{/* <script>
    new Vue({
      el: "#read_pub_record",
      data() {              
        return {
          data: data,
          bibs: bibs
        }
      },
      methods: {
        breakbib2(x) {    
          if (x.bibtex in bibs){return bibs[x.bibtex]} else {
            return "Coming soon"
          }
        },
        breakbib(x) {            
          bib_split = x.split(",")
          if (bib_split.length == 1) {return bib_split[0]}
          bib_first = bib_split[0]+",\n "
          bib_rest = bib_split.slice(1).join(",").split("},").join("},\n ")
          // breakline for final }
          bib_rest = bib_rest.slice(0,-1) + "\n" + bib_rest.slice(-1)
          return bib_first + bib_rest
        },
        boldMyName(x) {
          let phrase = "Or Litany"
          let pos = x.search(phrase)
          let length = phrase.length;
          x = x.slice(0,pos) + "<strong>" + x.slice(pos,pos+length) + 
            "</strong>" + x.slice(pos+length)
          return x
        }
      }
    });
  </script>

  <script>
    new Vue({
      el: "#read_workshop_record",
      data() {              
        return {
          events: events,
        }
      },
      methods: {
        concat(x) {          
          let txt
          txt = x.name + ", "+x.venue + " " + x.year            
          if ("upcoming" in x){
            txt = "<mark>[UPCOMING]</mark> " + txt
          }
          return txt
        }
      }
    });
  </script>

<script>
  new Vue({
    el: "#read_talks_record",
    data() {              
      return {
        talks: talks,
      }
    },
    methods: {
      render(x) {          
        let txt
        txt = x.title + ". "
        if ("slides" in x){
            txt += "<a :href=\""+ x.slides + "\">Slides</a>"
          }
        //  + ", "+x.venue + " " + x.year            
        // if ("upcoming" in x){
        //   txt = "<mark>[UPCOMING]</mark> " + txt
        // }
        return txt
      }
    }
  });
</script> */}


new Vue({
      el: "#read_pub_record",
      data() {              
        return {
          data: data,
          bibs: bibs
        }
      },
      methods: {
        breakbib2(x) {    
          if (x.bibtex in bibs){return bibs[x.bibtex]} else {
            return "Coming soon"
          }
        },
        breakbib(x) {            
          bib_split = x.split(",")
          if (bib_split.length == 1) {return bib_split[0]}
          bib_first = bib_split[0]+",\n "
          bib_rest = bib_split.slice(1).join(",").split("},").join("},\n ")
          // breakline for final }
          bib_rest = bib_rest.slice(0,-1) + "\n" + bib_rest.slice(-1)
          return bib_first + bib_rest
        },
        boldMyName(x) {
          let phrase = "Or Litany"
          let pos = x.search(phrase)
          let length = phrase.length;
          x = x.slice(0,pos) + "<strong>" + x.slice(pos,pos+length) + 
            "</strong>" + x.slice(pos+length)
          return x
        }
      }
    });
  

  
    new Vue({
      el: "#read_workshop_record",
      data() {              
        return {
          events: events,
        }
      },
      methods: {
        concat(x) {          
          let txt
          txt = x.name + ", "+x.venue + " " + x.year            
          if ("upcoming" in x){
            txt = "<mark>[UPCOMING]</mark> " + txt
          }
          return txt
        }
      }
    });
  


  new Vue({
    el: "#read_talks_record",
    data() {              
      return {
        talks: talks,
      }
    },
    methods: {
      render(x) {          
        let txt
        txt = x.title + ". "
        if ("slides" in x){
            txt += "<a :href=\""+ x.slides + "\">Slides</a>"
          }
        //  + ", "+x.venue + " " + x.year            
        // if ("upcoming" in x){
        //   txt = "<mark>[UPCOMING]</mark> " + txt
        // }
        return txt
      }
    }
  });
