const vue = new Vue({
    el: '#vue',
    delimiters: ['[[', ']]'],

    data: {
      max: null,
      min: null,
      subset: null,
      summary: null,
      cropData: null,
      activeCrop: null,
      activeState: null,
      activeYear: null,
      cropFilterOpen: false,
      yearFilterOpen: false
    },

    methods: {
      calculateFill(id) {
        let data = this.subset ? this.subset : this.cropData;

        // credit to Michele Locati for the color mapping function: https://gist.github.com/mlocati/7210513
        if (data) {
          let stateData = data.filter(item => item.STATE_CODE === id);
          let average = stateData.reduce((total, next) => total + next.TOTAL_YIELD, 0) / stateData.length;

          if (average) {
            let percentage = average / this.max;
            return `rgba(5,25,255,${percentage})`;
          } else {
            return `#BFBFBF`;
          }
        } else {
          return `#BFBFBF`;
        }
      },

      activateState(id) {
        console.log(id);
      },

      getCrop(crop) {
        this.subset = null;
        this.activeYear = null;
        this.activeCrop = crop;
        this.activeState = null;

        axios.get(`/api/crop/${crop}`)
          .then(res => {
            this.cropData = res.data;
            this.max = this.cropData.reduce((max, item) => item.TOTAL_YIELD > max ? item.TOTAL_YIELD : max, this.cropData[0].TOTAL_YIELD);
            this.min = this.cropData.reduce((min, item) => item.TOTAL_YIELD < min ? item.TOTAL_YIELD : min, this.cropData[0].TOTAL_YIELD);
          })
          .catch(err => {
            console.log(err);
          });
      },

      getYear(year) {
        this.activeYear = year;
        this.subset = this.cropData.filter(item => String(item.YEAR) === year);
        this.max = this.cropData.reduce((max, item) => item.TOTAL_YIELD > max ? item.TOTAL_YIELD : max, this.cropData[0].TOTAL_YIELD);
        this.min = this.cropData.reduce((min, item) => item.TOTAL_YIELD < min ? item.TOTAL_YIELD : min, this.cropData[0].TOTAL_YIELD);
      },

      toggleCropFilter() {
        this.cropFilterOpen = !this.cropFilterOpen;

        if (this.cropFilterOpen) {
          this.yearFilterOpen = false;
        }
      },

      toggleYearFilter() {
        this.yearFilterOpen = !this.yearFilterOpen;

        if (this.yearFilterOpen) {
          this.cropFilterOpen = false;
        }
      },

      showStateInfo(state) {
        this.activeState = state;
        let data = this.subset ? this.subset : this.cropData;

        // credit to Michele Locati for the color mapping function: https://gist.github.com/mlocati/7210513
        if (data) {
          let summaryObject = {};
          let stateData = data.filter(item => item.STATE_CODE === state);

          if (stateData) {
            // build yield sumary object
            summaryObject.averageYield = stateData.reduce((total, next) => total + next.TOTAL_YIELD, 0) / stateData.length;
            summaryObject.maxYield = stateData.reduce((max, item) => item.TOTAL_YIELD > max ? item.TOTAL_YIELD : max, stateData[0].TOTAL_YIELD);
            summaryObject.minYield = stateData.reduce((min, item) => item.TOTAL_YIELD < min ? item.TOTAL_YIELD : min, stateData[0].TOTAL_YIELD);

            // build harvested acres sumary object
            summaryObject.averageAcres = stateData.reduce((total, next) => total + next.TOTAL_HARVESTED_ACRES, 0) / stateData.length;
            summaryObject.maxAcres = stateData.reduce((max, item) => item.TOTAL_HARVESTED_ACRES > max ? item.TOTAL_HARVESTED_ACRES : max, stateData[0].TOTAL_HARVESTED_ACRES);
            summaryObject.minAcres = stateData.reduce((min, item) => item.TOTAL_HARVESTED_ACRES < min ? item.TOTAL_HARVESTED_ACRES : min, stateData[0].TOTAL_HARVESTED_ACRES);

            this.summary = summaryObject;
          }
        }
      },

      clearState() {
        this.summary = null;
        this.activeState = null;
      }
    }
})
