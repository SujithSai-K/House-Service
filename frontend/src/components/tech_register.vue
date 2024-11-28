<template>
  <div class="container">
    <h2>Register as Technician</h2>
    <p>{{ message }}</p>
    <p>{{ error }}</p>
    <form @submit.prevent="register">
      <div class="row mt-5 mb-3">
        <div class="col">
          <label for="email" class="form-label">Email</label>
          <input type="email" v-model="email" required class="form-control">
        </div>
        <div class="col">
          <label for="name" class="form-label">Username</label>
          <input type="text" v-model="username" class="form-control" required>
        </div>
        <div class="col">
          <label for="gender" class="form-label">Password</label>
          <input type="password" v-model="password" required class="form-control">
        </div>
      </div>
      <div class="row mb-3">
        <div class="col">
          <label for="name" class="form-label">Name</label>
          <input type="text" v-model="name" class="form-control" required>
        </div>
        <div class="col">
          <label for="gender" class="form-label">Gender</label>
          <select v-model="gender" class="form-select" required>
            <option value="Male">Male</option>
            <option value="Female">Female</option>
          </select>
        </div>
      </div>
      <div class="row mb-3">
        <div class="col">
          <label for="Age" class="form-label">Age</label>
          <input type="number" max="60" min="20" class="form-control" v-model="age" required>
        </div>
        <div class="col">
          <label for="service" class="form-label">Service</label>
          <select v-model="service_id" class="form-select" required>
            <option v-for="service in services" :key="service" :value="service.id" >{{service.name}}</option>
          </select>
        </div>
        <div class="col">
          <label for="experience" class="form-label">Experience</label>
          <input type="number" max="20" min="2" class="form-control" v-model="experience" required>
        </div>
      </div>
      <div class="row mb-3">
        <div class="col">
          <label for="address" class="form-label">Address</label>
          <textarea v-model="address" required rows="4" class="form-control" style="resize: none;"></textarea>
        </div>
      </div>
      <div>
        <button type="submit" class="btn btn-primary m-2">Submit</button>
        <button type="reset" class="btn btn-danger m-2">Reset</button>
      </div>
    </form>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data(){
    return{
      email:'',
      username:'',
      password:'',
      name:'',
      gender:'',
      age:'',
      experience:'',
      service_id:'',
      address:'',
      message:'',
      error:'',
      services:[]
    }
  },
  mounted(){
    axios.get('http://localhost:5000/technician_registration')
    .then(response => this.services = response.data)
    .catch(error => this.error = error)
  },
  methods:{
    async register(){
      try {
        const response = await axios.post('http://localhost:5000/technician_registration', {
          email: this.email,
          username: this.username,
          password: this.password,
          name: this.name,
          gender: this.gender,
          age: this.age,
          service_id: this.service_id,
          experience: this.experience,
          address: this.address
        });
        this.message = response.data.message;
        if(response.data.message === "registration Successful !!!") {
          this.$router.push({name:'login'})
        }
        this.error = "";
      } catch (error) {
        if (error.response && error.response.status === 409) {
          this.error = "A user with this username already exists. Please choose another username.";
        } else {
          this.error = "An unexpected error occurred. Please try again.";
        }
        if(this.message == "registration Successful !!!"){
          this.$router.push({name:'login'})
        }
      }
    }
  }
};
</script>

<style>

</style>