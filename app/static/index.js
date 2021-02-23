const vue = new Vue({
    el: '#vue',
    delimiters: ['[[', ']]'],

    created() {
      this.loadSegments();
    },

    data: {
      context: 'tester',
      segments: null,
      segmentsLoading: false,
      segmentsLoadingError: null
    },

    methods: {
      loadSegments() {
        this.segmentsLoading = true;

        axios.get('/api/segments/get/')
          .then(res => {
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
        const editing = this.segments.find(s => s.name === segment.name);

        if (!editing.ctas) {
          editing.ctas = [];
        }

        editing.ctas.push({name: null, origin: null, target: false, editing: true});
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
      }
    }
})
