<template>
  <div class="about">
    <div>
      <h1>This is an about page</h1>
    </div>
    <apexchart width="380" type="donut" :options="chartOptions" :series="series"></apexchart>
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
        labels: [],  // Hier sollten die Tag-Namen sein
      },
      series: [],
      tagNames: {}  
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
        const tagID = parseInt(vehicle.TagID);  
        acc[tagID] = (acc[tagID] || 0) + 1;
        return acc;
      }, {});

      console.log('Tag-IDs in updateChartData:', Object.keys(tagCounts));
      console.log('Tag-Names:', this.tagNames);

      this.chartOptions = {
        ...this.chartOptions,  
        labels: Object.keys(tagCounts).map(tagID => this.tagNames[tagID] || `Unbekanntes Tag ${tagID}`),
      };
      this.series = Object.values(tagCounts);

      this.$forceUpdate();
    },
  },
};
</script>

<style>
@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    align-items: center;
  }
}
</style>