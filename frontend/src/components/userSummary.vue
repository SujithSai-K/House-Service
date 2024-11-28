<template>
    <div class="container-fluid">
      <div v-if="error" class="alert alert-danger" role="alert">
          {{ error }}
      </div>
      <div v-if="!error">
          <div class="row">
              <div class="col">
                  <h2 class="mt-5" style="color: white;">Service Request Summary</h2>
                  <canvas id="requestChart"></canvas>
              </div>
          </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios'
  import { Chart, registerables } from 'chart.js';
  import { mapGetters } from 'vuex';
  Chart.register(...registerables);
  export default {
      data() {
      return {
        error: '',
        requestData: [],
        requestLables: [],
      };
    },
    computed: {
      ...mapGetters(['token','userId'])
    },
    mounted(){
      axios.get(`http://localhost:5000/customer/summary/${this.userId}`,{
          headers: {
            Authorization: `Bearer ${this.token}`
          }
      })
      .then(response => {
          if (response.data.message == "no data found") {
            this.error = response.data.message;
            // this.$router.push('/AdminDashboard');
          }
          this.requestData = response.data.request_data
          this.requestLables = response.data.request_labels
          this.requestChart()
      })
      .catch(error => {
          this.error = error
      })
    },
    methods:{
      requestChart(){
          const ctx = document.getElementById('requestChart').getContext('2d');
          new Chart(ctx, {
          type: 'bar',
          data: {
              labels: this.requestLables,
              datasets: [{
              data: this.requestData,
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
      },
    }
  }
  </script>
  
  <style>
  
  </style>