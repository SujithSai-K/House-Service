<template>
    <div class="container">
      <form class="mt-5" @submit.prevent="post">
        <div class="row mb-3">
          <label for="name" class="form-label">Name</label>
          <input type="text" v-model="name" class="form-control" required />
        </div>
        <div class="row mb-3">
          <label for="Description" class="form-label">Description</label>
          <textarea v-model="description" class="form-control" rows="3" style="resize: none;" required></textarea>
        </div>
        <div class="row mb-3">
          <div class="col">
            <label for="time" class="form-label">Time Required</label>
            <div class="input-group">
              <input type="number" v-model="time" class="form-control" required />
              <span class="input-group-text">hrs</span>
            </div>
          </div>
          <div class="col">
            <label for="price" class="form-label">Price</label>
            <div class="input-group">
              <span class="input-group-text">₹</span>
              <input type="number" v-model="price" class="form-control" required />
            </div>
          </div>
        </div>
        <button type="submit" class="btn btn-primary m-3">Submit</button>
        <button type="reset" class="btn btn-danger m-3">Reset</button>
      </form>
      <p v-if="message">{{ message }}</p> <!-- Display the response message -->
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import { mapState } from 'vuex';
  
  export default {
    data() {
      return {
        name: '',
        description: '',
        price: '',
        time: '',
        message: '',
      };
    },
    computed: {
      ...mapState(['token']),
    },
    methods: {
      async post() {
        try {
          const response = await axios.post(
            'http://localhost:5000/admin/newService',
            {
              name: this.name,
              description: this.description,
              price: this.price,
              time: this.time,
            },
            {
              headers: {
                Authorization: `Bearer ${this.token}`,
              },
            }
          );
  
          this.message = response.data.message; 
          this.$router.push({name:"AdminDashboard"})
        } catch (error) {
          console.log("Error:", error.response ? error.response.data : error.message); // Log any errors
        }
      },
    },
  };
  </script>
  
  <style>
  .form-label {
    display: flex;
    text-align: left;
    align-items: start;
    color: white;
    font-size: large;
  }
  </style>
  