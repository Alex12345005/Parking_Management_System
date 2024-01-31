<template>
  <div class="about">
      <div class="fixed-header">
        <h1 class="about-title uk-heading-divider uk-postition-top">Graphs</h1>
      </div>
      <div class="uk-column-1-2">
          <div class="chart-wrapper">
            <div class="chart-container">
              <apexchart width="500" type="donut" :options="chartOptions" :series="series"></apexchart>
            </div>
            <div class="chart-container">
              <apexchart type="line" :options="lineChartOptions" :series="lineSeries"></apexchart>
            </div>
          </div>
          <div class="chart-wrapper">
            <div class="chart-container">
              <apexchart type="bar" :options="barChartOptions" :series="barSeries"></apexchart>
            </div>
            <div class="chart-container">
              <apexchart type="area" :options="areaChartOptions" :series="areaSeries"></apexchart>
            </div>
        </div>
      </div>
  </div>
</template>

<script>
import VueApexCharts from 'vue3-apexcharts';
import axios from 'axios';

export default {
  name: 'AboutPage',
  components: {
    apexchart: VueApexCharts,
  },
  data() {
    return {
      chartOptions: {
        labels: []
      },
      series: [],
      tagNames: {},
      lineChartOptions: {
        xaxis: {
          categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']
        }
      },
      lineSeries: [{
        name: 'Series 1',
        data: [31, 40, 28, 51, 42, 109]
      }],
      barChartOptions: {
        xaxis: {
          categories: ['2015', '2016', '2017', '2018', '2019']
        }
      },
      barSeries: [{
        name: 'Series 1',
        data: [300, 400, 300, 500, 400]
      }],
      areaChartOptions: {
        xaxis: {
          categories: ['A', 'B', 'C', 'D', 'E']
        }
      },
      areaSeries: [{
        name: 'Series 1',
        data: [10, 15, 9, 20, 16]
      }]
    };
  },
  mounted() {
    this.getData();
  },
  methods: {
    async getData() {
      try {
        const tagsResponse = await axios.get('http://127.0.0.1:8000/tags/get_tags/');
        const tags = tagsResponse.data;
        this.tagNames = tags.reduce((acc, tag) => {
          acc[tag.TagID] = tag.TagName;
          return acc;
        }, {});
        const vehiclesResponse = await axios.get('http://127.0.0.1:8000/vehicles/get_vehicles/');
        const vehicles = vehiclesResponse.data;
        this.updateChartData(vehicles);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    updateChartData(vehicles) {
      const tagCounts = vehicles.reduce((acc, vehicle) => {
        acc[parseInt(vehicle.TagID)] = (acc[parseInt(vehicle.TagID)] || 0) + 1;
        return acc;
      }, {});
      this.chartOptions = {
        ...this.chartOptions,  
        labels: Object.keys(tagCounts).map(tagID => this.tagNames[tagID] || `Unbekanntes Tag ${tagID}`),
      };
      this.series = Object.values(tagCounts);
    },
  },
};
</script>

<style>
.about {
  padding-top: 2rem;
  text-align: center;
}

.fixed-header {
  position: sticky;
  top: 0;
  background: white;
  padding: 1rem 0;
  z-index: 10;
}

.about-title {
  margin-bottom: 2rem;
  color: #333;
  font-size: 2.5rem;
}

.chart-wrapper {
  display: flex;
  flex-wrap: wrap;
  justify-content: start;
  gap: 2rem;
  padding: 4rem;
  background-color: #f5f5f5;
}

.chart-container {
  flex: 1 0 50%; /* Ermöglicht zwei Diagramme pro Reihe */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
  background: white;
  padding: 1rem;
  margin-bottom: 2rem;
}

@media (max-width: 1024px) {
  .chart-container {
    flex: 1 0 100%; /* Auf kleineren Bildschirmen wird jedes Diagramm auf 100% der Breite skaliert */
    max-width: 100%;
  }
}

.uk-accordion-title {
  font-size: 1.25rem;
  color: #444;
}

.uk-accordion-content {
  padding: 1rem;
}
</style>