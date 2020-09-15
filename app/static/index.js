const vue = new Vue({
    el: '#vue',
    delimiters: ['[[', ']]'],

    data: {
      summary: null,
      cropSummary: {},
      stateData: null,
      activeCrop: null,
      activeState: null,
      activeYear: null,
      activeCounty: null,
      overviewOpen: false,
      cropFilterOpen: false,
      yearFilterOpen: false,
      mobileDropdownOpen: false,
      activeStateOverview: null,
      overviewDropdownOpen: false
    },

    methods: {
      calculateFill(data) {
        let numerator;
        let denominator;
        let timeFrame = this.activeYear ? this.activeYear : 'allTime';

        if (this.activeCrop !== 'COTTON' && this.activeCrop !== 'WHEAT') {
          denominator = 'maxYield';
          numerator = 'averageYield';
        } else {
          denominator = 'maxAcres';
          numerator = 'averageAcres';
        }

        if (data && data[timeFrame] && data[timeFrame][numerator]) {
          let percentage = data[timeFrame][numerator] / this.cropSummary.allStates[denominator];

          // largest max acreage is often far larger, add a bit more color so paths aren't white
          return `rgba(5,25,255,${denominator === 'maxAcres' ? percentage + .1 : percentage})`;
        } else {
          return `#BFBFBF`;
        }
    },

    calculatePercent(record, cropArr, field) {
      let average = cropArr.reduce((total, next) => total + next[field], 0) / cropArr.length;

      if (average) {
        return `${Math.round((record/average) * 100)}%`;
      }
    },

    activateCounty(county) {
      this.activeCounty = county;
      this.overviewDropdownOpen = false;
    },

    activateState(state) {
      axios.get(`/api/state/${state}?formatted=True`)
        .then(res => {
          this.stateData = res.data;
          this.overviewOpen = true;
          this.mobileDropdownOpen = false;
          this.activeStateOverview = state;
        })
        .catch(err => {
          console.log(err);
        });
      },

      deactivateState() {
        this.stateData = null;
        this.activeCounty = null;
        this.overviewOpen = false;
        this.activeStateOverview = null;
      },

      getCrop(crop) {
        this.activeYear = null;
        this.activeCrop = crop;
        this.activeState = null;

        axios.get(`/api/crop/${crop}?formatted=True`)
          .then(res => {
            this.cropSummary = res.data;
          })
          .catch(err => {
            console.log(err);
          });
      },

      getYear(year) {
        this.activeYear = year;
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
        let timePeriod = this.activeYear ? this.activeYear : 'allTime';
        this.activeState = state;

        // credit to Michele Locati for the color mapping function: https://gist.github.com/mlocati/7210513
        if (this.cropSummary && this.cropSummary[state]) {
          this.summary = {};

          // build yield sumary object
          if (this.cropSummary[state][timePeriod]) {
            this.summary.averageYield = this.cropSummary[state][timePeriod].averageYield;
            this.summary.maxYield = this.cropSummary[state][timePeriod].maxYield;
            this.summary.minYield = this.cropSummary[state][timePeriod].minYield;

            // build harvested acres sumary object
            this.summary.averageAcres = this.cropSummary[state][timePeriod].averageAcres;
            this.summary.maxAcres = this.cropSummary[state][timePeriod].maxAcres;
            this.summary.minAcres = this.cropSummary[state][timePeriod].minAcres;
          }
        }
      },

      clearState() {
        this.summary = null;
        this.activeState = null;
      },

      toggleOverviewDropdown() {
        this.overviewDropdownOpen = !this.overviewDropdownOpen;
      },

      toggleMobileDropdown() {
        this.mobileDropdownOpen = !this.mobileDropdownOpen;
      },

      countyHasCrop(county) {
        if (this.stateData[county][this.activeCrop] && this.stateData[county][this.activeCrop].length) {
          return true;
        } else {
          return false;
        }
      }
    }
})
