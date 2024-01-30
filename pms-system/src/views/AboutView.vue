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
        // Lade Tag-Daten
        const tagsResponse = await axios.get('http://127.0.0.1:8000/tags/get_tags/');
        const tags = tagsResponse.data;

        console.log('Tag-Namen vor dem Mapping:', this.tagNames);
        
        // FÃ¼lle Tag-Namen
        this.tagNames = tags.reduce((acc, tag) => {
          acc[tag.TagID] = tag.TagName;
          return acc;
        }, {});

        console.log('Tag-Namen nach dem Mapping:', this.tagNames);

        // Lade Fahrzeug-Daten
        const vehiclesResponse = await axios.get('http://127.0.0.1:8000/vehicles/get_vehicles/');
        const vehicles = vehiclesResponse.data;

        // Aktualisiere Chart-Daten
        this.updateChartData(vehicles);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    updateChartData(vehicles) {
      const tagCounts = vehicles.reduce((acc, vehicle) => {
        acc[vehicle.TagID] = (acc[vehicle.TagID] || 0) + 1;
        return acc;
      }, {});

      console.log('Tag-IDs in updateChartData:', Object.keys(tagCounts));
      console.log('Tag-Namen in updateChartData:', this.chartOptions.labels);

      this.chartOptions.labels = Object.keys(tagCounts).map(TagID => this.tagNames[TagID] || `Unbekanntes Tag ${TagID}`);
      this.series = Object.values(tagCounts);
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