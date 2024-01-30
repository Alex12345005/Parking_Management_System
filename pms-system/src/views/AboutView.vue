<template>
  <div class="about">
    <div class="fixed-header">
      <h1 class="about-title">Graphs</h1>
    </div>
    <div class="chart-wrapper">
      <div class="chart-container" uk-accordion>
        <li class="uk-open">
          <a class="uk-accordion-title" href="#">Percentage of each Tag</a>
          <div class="uk-accordion-content">
            <apexchart width="380" type="donut" :options="chartOptions" :series="series"></apexchart>
          </div>
        </li>
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
  padding: 1rem;
  background-color: #f5f5f5; /* Hellgrauer Hintergrund */
  margin-top: 2rem; /* Abstand von der Überschrift */
}

.chart-container {
  max-width: 480px; /* Maximalbreite für das Akkordeon */
  margin: 0 auto; /* Zentriere das Akkordeon */
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1); /* Etwas Schatten für Tiefe */
  border-radius: 8px; /* Abgerundete Ecken */
  overflow: hidden; /* Verhindert, dass der Inhalt über die Grenzen hinausragt */
  background: white; /* Weißer Hintergrund für das Akkordeon */
}

.uk-accordion-title {
  font-size: 1.25rem; /* Größere Schriftart für die Titel */
  color: #444; /* Dunkle Schriftfarbe */
}

.uk-accordion-content {
  padding: 1rem; /* Etwas Innenabstand */
}

@media (min-width: 1024px) {
  .about {
    min-height: 100vh;
    display: flex;
    flex-direction: column; /* Stackt Elemente vertikal */
    justify-content: flex-start; /* Inhalte oben beginnen */
    align-items: center; /* Zentriere Inhalte horizontal */
  }

  .chart-wrapper {
    width: 100%; /* Volle Breite innerhalb des .about-Containers */
    max-width: 640px; /* Maximalbreite für die Diagramm-Box */
  }
}
</style>