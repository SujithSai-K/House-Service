<template>
  <div class="container form">
    <form @submit.prevent="register">
      <h2 class="mt-5 mb-3">Register</h2>
      <p>{{ message }}</p>
      <p>{{ error }}</p>
      <div class="row mt-5 mb-3">
        <div class="col">
          <label for="email" class="form-label">Email</label>
          <input type="email" v-model="email" class="form-control" required>
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
          <label for="dob" class="form-label">Date of Birth</label>
          <input type="date" class="form-control" v-model="dob" required>
        </div>
        <div class="col">
          <label for="phone" class="form-label">Phone No</label>
          <input type="phone" class="form-control" v-model="phone" required>
        </div>
      </div>
      <div class="row mb-3">
        <div class="col">
          <label for="address" class="form-label">Address</label>
          <textarea v-model="address" rows="4" class="form-control" style="resize: none;"></textarea>
        </div>
      </div>
      <div>
        <button type="submit" class="btn btn-primary m-2">Submit</button>
        <button type="reset" class="btn btn-danger m-2">Reset</button>
      </div>
        <router-link style="color: black;" to="/tech_register">Register as Technician</router-link>
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
    dob:'',
    phone:'',
    address:'',
    message:'',
    error:''
  }
},
methods:{
async register(){
  await axios.post('http://localhost:5000/user_registration',{
    username: this.username,
    password: this.password,
    email: this.email,
    name: this.name,
    gender: this.gender,
    phone: this.phone,
    dob: this.dob,
    address: this.address
  })
  .then(response => this.message = response.data.message)
  .catch(error => {
        this.error = error;
      });
      if (this.message == 'registration Successful !!!'){
        this.$router.push({name:'login'})
      }
}
}
}
</script>

<style scoped>
  h2{
    color: white;
    font-size: 50px;
  }
</style>