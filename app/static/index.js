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
      outputLoadingError: null,
      segmentUpdateError: null,
      segmentUpdateErrorId: null

    },

    methods: {
      loadSegments() {
        this.segmentsLoading = true;

        axios.get('/api/segments/get/')
          .then(res => {
            res.data.map(s => {
              s.color = Math.floor(100000 + Math.random() * 900000);

              s.urls = s.urls.map(i => {
                i.id = Math.random().toString(36).substring(7);
                return i;
              });

              s.ctas = s.ctas.map(i => {
                i.id = Math.random().toString(36).substring(7);
                return i;
              });

              s.recipeSearches = s.recipeSearches.map(i => {
                i.id = Math.random().toString(36).substring(7);
                return i;
              });

              s.centerSearches = s.centerSearches.map(i => {
                i.id = Math.random().toString(36).substring(7);
                return i;
              });

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

      addView(segment) {
        const id = Math.random().toString(36).substring(7);
        const editing = this.segments.find(s => s.name === segment.name);

        if (!editing.urls) {
          editing.urls = [];
        }

        editing.urls.push({id, link: null, match:null, exact: false, weight: 1, editing: true});
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
        const id = Math.random().toString(36).substring(7);
        const editing = this.segments.find(s => s.name === segment.name);

        if (!editing.recipeSearches) {
          editing.recipeSearches = [];
        }

        editing.recipeSearches.push({id, searchTerm: null, filterGroup: null, editing: true});
      },

      addCenterSearch(segment) {
        const id = Math.random().toString(36).substring(7);
        const editing = this.segments.find(s => s.name === segment.name);

        if (!editing.centerSearches) {
          editing.centerSearches = [];
        }

        editing.centerSearches.push({id, modality: null, zip: null, location: null, editing: true});
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

      deleteViewLogic(item, segment) {
        axios({
          method: 'post',
          url:'/api/logic/delete',
          headers: {
            'Content-Type': 'application/json'
          },
          data: {
            segment,
            eventCategory: 'pageView',
            link: item.match
          }
        })
        .then(res => {
          const editing = this.segments.find(s => s.name === segment);
          editing.urls = editing.urls.filter(v => v.id !== item.id);
        })
      },

      deleteCTALogic(item, segment) {
        axios({
          method: 'post',
          url:'/api/logic/delete',
          headers: {
            'Content-Type': 'application/json'
          },
          data: {
            segment,
            eventCategory: 'cta',
            name: item.name,
            origin: item.origin,
            target: item.target
          }
        })
        .then(res => {
          const editing = this.segments.find(s => s.name === segment);
          editing.ctas = editing.ctas.filter(v => v.id !== item.id);
        })
      },

      deleteRecipeLogic(item, segment) {
        axios({
          method: 'post',
          url:'/api/logic/delete',
          headers: {
            'Content-Type': 'application/json'
          },
          data: {
            segment,
            eventCategory: 'recipeSearch',
            searchTerm: item.searchTerm
          }
        })
        .then(res => {
          const editing = this.segments.find(s => s.name === segment);
          editing.recipeSearches = editing.recipeSearches.filter(v => v.id !== item.id);
        })
      },

      deleteCenterLogic(item, segment) {
        axios({
          method: 'post',
          url:'/api/logic/delete',
          headers: {
            'Content-Type': 'application/json'
          },
          data: {
            segment,
            eventCategory: 'centerSearch',
            modality: item.modality,
            zip: item.zip,
            location: item.location
          }
        })
        .then(res => {
          const editing = this.segments.find(s => s.name === segment);
          editing.centerSearches = editing.centerSearches.filter(v => v.id !== item.id);
        })
      },

      updateViewLogic(e, id, field, segment) {
        const editing = this.segments.find(s => s.name === segment);
        const view = editing.urls.find(v => v.id === id);
        
        view[field] = e.target.value;

        if (field === 'link') {
          view.match = e.target.value;
        }
      },

      updateCTALogic(e, id, field, segment) {
        const editing = this.segments.find(s => s.name === segment);
        const cta = editing.ctas.find(c => c.id === id);
        
        cta[field] = e.target.value;
      },

      updateRecipeLogic(e, id, field, segment) {
        const editing = this.segments.find(s => s.name === segment);
        const search = editing.recipeSearches.find(v => v.id === id);
        
        search[field] = e.target.value;
      },

      updateCenterLogic(e, id, field, segment) {
        const editing = this.segments.find(s => s.name === segment);
        const search = editing.centerSearches.find(v => v.id === id);
        
        search[field] = e.target.value;
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
          cta.editing = false;
        })
      },

      saveViewLogic(e, id, segment) {
        e.preventDefault()

        const editing = this.segments.find(s => s.name === segment);
        const view = editing.urls.find(v => v.id === id);

        axios({
          method: 'post',
          url:'/api/logic/update',
          headers: {
            'Content-Type': 'application/json'
          },
          data: {
            segment,
            eventCategory: 'pageView',
            link: view.link,
            exact: view.exact,
            weight: view.weight
          }
        })
        .then(res => {
          if( res.status === 200) {
            view.editing = false;
          }
        })
        .catch(e => {
          console.log(e);
          this.segmentUpdateErrorId = id;
          this.segmentUpdateError = 'An error occurred loading segments, please contact Mark B. if the issue persists';
        })
      },

      saveRecipeLogic(e, id, segment) {
        e.preventDefault()

        const editing = this.segments.find(s => s.name === segment);
        const search = editing.recipeSearches.find(v => v.id === id);

        axios({
          method: 'post',
          url:'/api/logic/update',
          headers: {
            'Content-Type': 'application/json'
          },
          data: {
            segment,
            eventCategory: 'recipeSearch',
            searchTerm: search.searchTerm,
            filterGroup: search.filterGroup
          }
        })
        .then(res => {
          if( res.status === 200) {
            search.editing = false;
          }
        })
        .catch(e => {
          console.log(e);
          this.segmentUpdateErrorId = id;
          this.segmentUpdateError = 'An error occurred loading segments, please contact Mark B. if the issue persists';
        })
      },

      saveCenterLogic(e, id, segment) {
        e.preventDefault()

        const editing = this.segments.find(s => s.name === segment);
        const search = editing.centerSearches.find(v => v.id === id);

        axios({
          method: 'post',
          url:'/api/logic/update',
          headers: {
            'Content-Type': 'application/json'
          },
          data: {
            segment,
            eventCategory: 'centerSearch',
            modality: search.modality,
            zip: search.zip,
            location: search.location
          }
        })
        .then(res => {
          if( res.status === 200) {
            search.editing = false;
          }
        })
        .catch(e => {
          console.log(e);
          this.segmentUpdateErrorId = id;
          this.segmentUpdateError = 'An error occurred loading segments, please contact Mark B. if the issue persists';
        })
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
