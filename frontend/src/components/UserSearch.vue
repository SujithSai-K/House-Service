<template>
    <div class="container-fluid">
      <div v-if="error" class="alert alert-danger" role="alert">
          {{ error }}
      </div>
      <div v-if="!error">
        <form >
        <div class="row justify-content-center mt-3">
          <div class="col-1 mt-2"><label for="search by" class="form-label">Search by</label></div>
          <div class="col-2 me-2">
            <select class="form-select" v-model="searchBy" aria-label="default select example" placeholder="search by">
              <option value="Service">Service ID</option>
              <option value="Technician">Technician ID</option>
              <option value="Service Request">Service Request ID</option>
            </select>
          </div>
          <div class="col-2 ms-2"><input type="text" class="form-control" v-model="query" placeholder="search"></div>
          <div class="col-1"><button type="button" @click="search" class="btn btn-primary">search</button></div>
        </div>
      </form>
        <div v-if="status == 200 && searchBy == 'Technician'" class="mt-2">
          <table class="table table-bordered table-striped mt-3">
                <thead>
                    <tr>
                        <th scope="col">ID</th>
                        <th scope="col">Name</th>
                        <th scope="col">Gender</th>
                        <th scope="col">Address</th>
                        <th>Service</th>
                        <th scope="col">Age</th>
                        <th scope="col">Experience</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="professional in data.technicians" :key="professional.id">
                      <td>{{ professional.id }}</td>
                        <td>{{ professional.name }}</td>
                        <td>{{ professional.gender }}</td>
                        <td>{{ professional.address }}</td>
                        <td>{{ professional.service_name }}</td>
                        <td>{{ professional.age }}</td>
                        <td>{{ professional.experience }}</td>
                        <td><button class="btn btn-primary" @click="bookProfessional(professional.id)">Book</button></td>
                    </tr>
                </tbody>
            </table>
        </div>
        <div v-if="status==200 && searchBy=='Service'" class="mt-3">
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Description</th>
                    <th>Price</th>
                    <th>Time</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="service in data.services" :key="service.id">
                    <td>{{service.id}}</td>
                    <td>{{service.name}}</td>
                    <td>{{service.description}}</td>
                    <td>{{service.price}}</td>
                    <td>{{service.time_required}}</td>
                    <td><router-link :to="{path: '/SeeProfessional',query: { serviceID: service.id, serviceName: service.name}}" class="btn btn-primary mt-2">See Professionals</router-link></td>
                </tr>
            </tbody>
        </table>
      </div>
      <div v-if="status==200 && searchBy=='Service Request'" class="mt-3">
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Service Id</th>
                    <th>Professional Id</th>
                    <th>User Id</th>
                    <th>Requested Date</th>
                    <th>Status</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="request in data.service_requests" :key="request.id">
                    <td>{{ request.id }}</td>
                    <td>{{ request.service_id }}</td>
                    <td>{{ request.technician_id }}</td>
                    <td>{{ request.customer_id }}</td>
                    <td>{{ request.request_date }}</td>
                    <td>{{ request.status }}</td>
                </tr>
            </tbody>
        </table>
      </div>
      </div>
    </div>
  </template>
  
<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
  export default {
  data(){
    return{
        data:'',
        error:'',
        searchBy:'',
        query:'',
        status:''
    }
  },
  computed:{
    ...mapGetters(['token','userId'])
  },
  methods:{
    async search(){
        await axios.post('http://localhost:5000/customer/search',{
          searchBy:this.searchBy,
          query:this.query,
          id:this.userId
        },{
          headers:{
            Authorization:`Bearer ${this.token}`
          }
        })
        .then(response=>{
         // console.log(response)
          this.status = response.status
          this.data = response.data
        })
        .catch(error=>{
          this.error=error
        })
    },
    async bookProfessional(professionalId){
            try{
               // console.log(this.userId)
                const response = await axios.post(`http://localhost:5000/customer/bookProfessional/${professionalId}/${this.userId}`,{
                    headers:{
                        Authorization: `Bearer ${this.token}`
                    }
                })
                if(response.status === 200){
                    this.$router.push('/user_dashboard')
                }
            }
            catch(error){
                this.error = error
            }
        }
  }
  }
</script>
  
  <style>
  
  </style>