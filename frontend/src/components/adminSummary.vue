<template>
  <div class="container-fluid">
    <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
    </div>
    <div v-if="!error">
        <div class="row">
            <div class="col">
                <h2 class="mt-5" style="color: white;">Service Bookings (Last 30 Days)</h2>
                <canvas id="serviceChart"></canvas>
            </div>
            <div class="col">
                <h2 class="mt-5" style="color: white;">Service Request Summary</h2>
                <canvas id="technicianChart"></canvas>
            </div>
        </div>
        <!-- <div class="row">
            <div class="col">
                <h2 class="mt-5" style="color: white;">Number of Customers (Last 30 Days)</h2>
                <canvas id="cuatomersChart"></canvas>
            </div>
        </div> -->
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  data() {
    return {
      error: '',
      serviceData: [],
      serviceLables: [],
      technicianData: [],
      technicianLables: []
    };
  },
  computed: {
    ...mapGetters(['token'])
  },
  mounted() {
    this.fetchSummaryData();
  },
  methods: {
    fetchSummaryData() {
      axios
        .get('http://localhost:5000/admin/summary', {
          headers: {
            Authorization: `Bearer ${this.token}`
          }
        })
        .then(response => {
          if (response.data.message == "no data found") {
            this.error = response.data.message;
            // this.$router.push('/AdminDashboard');
          }
          this.serviceData = response.data.service_data;
          this.serviceLables = response.data.service_lables;
          this.technicianData = response.data.tech_data;
          this.technicianLables = response.data.tech_lables;
          this.pieChart();
          this.barChart();
        })
        .catch(error => {
          this.error = error;
        });
    },
    pieChart() {
        const ctx = document.getElementById('serviceChart').getContext('2d');
        new Chart(ctx, {
        type: 'pie',
        data: {
            labels: this.serviceLables,
            datasets: [{
            data: this.serviceData,
            //   backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            }],
        },
        options: {
            responsive: true,
            plugins: {
            legend: {
                display: true,
                position: 'top',
                labels: {
                font: {
                    size: 20,
                },
                color: '#000',
                },
            },
            },
        },
    });
    },
    barChart(){
        const ctx = document.getElementById('technicianChart').getContext('2d');
        new Chart(ctx, {
        type: 'bar',
        data: {
            labels: this.technicianLables,
            datasets: [{
            data: this.technicianData,
            borderWidth:1,
              backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56'],
            }],
        },
        options: {
            responsive: true,
            plugins: {
            legend: {
                display: false,
                position: 'top',
                labels: {
                font: {
                    size: 20,
                },
                color: '#000',
                },
            },
            },
        },
    });
    }
  }
};
</script>

<style>
canvas{
    width: 500px;
    min-height: 400px;
    max-height: 400PX;
    margin: 0 auto;
    background-color: #fff;
}
</style>