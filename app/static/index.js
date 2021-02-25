const vue = new Vue({
    el: '#vue',
    delimiters: ['~', '~'],

    created() {
      this.loadSegments();

      axios.get('/api/usernames/get/')
      .then(res => {
        this.allUsers = res.data
      })
      .catch(e => {
        console.log(e);
      });
    },

    data: {
      userInteractionData: {},
      activeUserDropdown: null,
      runType: 'all',
      userRunId: null,
      allUsers: null,
      context: 'tester',
      segments: null,
      segmentsLoading: false,
      segmentsLoadingError: null,
      output: null,
      outputLoading: false,
      outputLoadingError: null

    },

    methods: {
      loadSegments() {
        this.segmentsLoading = true;

        axios.get('/api/segments/get/')
          .then(res => {
            res.data.map(s => {
              s.color = Math.floor(100000 + Math.random() * 900000);
              return s;
            });

            this.segments = res.data;
            this.segmentsLoading = false;
          })
          .catch(e => {
            console.log(e);
            this.segmentsLoadingError = 'An error occurred loading segments, please contact Mark B. if the issue persists';
          })
      },

      openSection(e) {
        e.target.classList.toggle('--active');
        e.target.nextElementSibling.classList.toggle('--dropdown-hidden');
      },
      
      openDropdown(e) {
        e.target.classList.toggle('--active');
        e.target.parentElement.nextElementSibling.firstElementChild.classList.toggle('--dropdown-hidden');
      },

      addURL(segment) {
        const editing = this.segments.find(s => s.name === segment.name);

        if (!editing.urls) {
          editing.urls = [];
        }
        
        editing.urls.push({link: null, exact: false, editing: true});
      },

      addCTA(segment) {
        const id = Math.random().toString(36).substring(7);
        const editing = this.segments.find(s => s.name === segment.name);

        if (!editing.ctas) {
          editing.ctas = [];
        }

        editing.ctas.push({id, name: null, origin: null, target: false, editing: true});
      },

      addRecipeSearch(segment) {
        const editing = this.segments.find(s => s.name === segment.name);

        if (!editing.recipeSearches) {
          editing.recipeSearches = [];
        }

        editing.recipeSearches.push({searchTerm: null, recipeCategoryTag: null, predefined: false, editing: true});
      },

      addCenterSearch(segment) {
        const editing = this.segments.find(s => s.name === segment.name);

        if (!editing.centerSearches) {
          editing.centerSearches = [];
        }

        editing.centerSearches.push({zip: null, locationName: null, modality: null, editing: true});
      },

      sendCompileRequest(e) {
        e.preventDefault();

        if (this.runType === 'single') {
          this.deriveSingleSegment();
        } else {
          this.deriveSegments();
        }
      },

      deriveSingleSegment() {
        this.context = 'output';
        this.outputLoading = true;

        axios.get(`/api/user/get/segments/${this.userRunId}`)
          .then(res => {
            this.output = res.data;
            this.outputLoading = false;
          })
          .catch(e => {
            console.log(e);
            this.outputLoadingError = 'An error occurred loading segments, please contact Mark B. if the issue persists';
          })
      },

      deriveSegments() {
        this.context = 'output';
        this.outputLoading = true;

        axios.get('/api/users/get')
          .then(res => {
            this.output = res.data;
            this.outputLoading = false;
          })
          .catch(e => {
            console.log(e);
            this.outputLoadingError = 'An error occurred loading segments, please contact Mark B. if the issue persists';
          })
      },

      getUserEvents(id) {
        if (this.activeUserDropdown === id) {
          this.activeUserDropdown = null;
        } else if (!this.userInteractionData[id]) {
          axios.get(`/api/user/get/events/${id}`)
          .then(res => {
            this.activeUserDropdown = id;
            this.userInteractionData[id] = res.data;
          })
          .catch(e => {
            console.log(e);
            this.outputLoadingError = 'An error occurred loading segments, please contact Mark B. if the issue persists';
          })
        } else {
          this.activeUserDropdown = id;
        }
      },

      saveViewLogic(e, segment) {
        e.preventDefault()
        console.log('saveViewLogic');
      },

      updateCTALogic(e, id, field, segment) {
        const editing = this.segments.find(s => s.name === segment);
        const cta = editing.ctas.find(c => c.id === id);
        
        cta[field] = e.target.value;
      },

      saveCTALogic(e, id, segment) {
        e.preventDefault()

        const editing = this.segments.find(s => s.name === segment);
        const cta = editing.ctas.find(c => c.id === id);

        axios({
          method: 'post',
          url:'/api/logic/update',
          headers: {
            'Content-Type': 'application/json'
          },
          data: {
            segment,
            eventCategory: 'cta',
            name: cta.name,
            origin: cta.origin,
            target: cta.target
          }
        })
        .then(res => {
          console.log(res.data);
        })
      },

      saveRecipeLogic(e, segment) {
        e.preventDefault()
        console.log('saveRecipeLogic');
      },

      saveCenterLogic(e, segment) {
        e.preventDefault()
        console.log('saveCenterLogic');
      },

      getSegmentColor(n) {
        return this.segments.filter(s => s.name === n)[0].color;
      },

      cleanArray(segments) {
        const arrayified = Object.keys(segments).map(k => {return {name: k, count: segments[k]}});

        return arrayified.sort((a, b) => {
          if (a.count > b.count) {
            return -1;
          }
          if (a.count < b.count) {
            return 1;
          }
        });
      },

      getModalityName(modality) {
        const mmap = {
          1: "In-Center Hemodialysis",
          2: "In-Center Nocturnal Dialysis",
          3: "Home Hemodialysis",
          4: "Peritoneal Dialysis",
          5: "Nursing Home Dialysis"
        };

        return mmap[modality];
      }
    }
})
