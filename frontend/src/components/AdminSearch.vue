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
              <option value="customer">Customer ID</option>
            </select>
          </div>
          <div class="col-2 ms-2"><input type="text" class="form-control" v-model="query" placeholder="search"></div>
          <div class="col-1"><button type="button" @click="search" class="btn btn-primary">search</button></div>
        </div>
      </form>
      <div v-if="status==200 && searchBy=='Technician'" class="mt-3">
        <table class="table table-striped table-bordered">
          <thead>
            <tr>  
              <th>ID</th>
              <th>Name</th>
              <th>Service</th>
              <th>Gender</th>
              <th>Age</th>
              <th>Address</th>
              <th>Registration Date</th>
              <th>Experience</th>
              <th>Status</th>
              <th>Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="technician in data.technicians" :key="technician">
              <td>{{ technician.id }}</td>
              <td>{{ technician.name }}</td>
              <td>{{ technician.service_id }}</td>
              <td>{{ technician.gender }}</td>
              <td>{{ technician.age }}</td>
              <td>{{ technician.address }}</td>
              <td>{{ technician.registration_date }}</td>
              <td>{{ technician.experience }}</td>
              <td>{{ technician.status }}</td>
              <td>
                <button v-if="technician.status == 'Available'" @click="suspend(technician.id)" class="btn btn-danger">Suspend</button>
                <button v-else-if="technician.status == 'Suspended'" @click="activate(technician.id)" class="btn btn-success">Reinstate</button>
              </td>
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
                    <td><router-link :to="{path: '/editService',query: { serviceID: service.id }}" class="bi bi-pencil-square"></router-link> | <a class="bi bi-trash" @click.prevent="deleteItem(service.id)"></a></td>
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
      <div v-if="status==200 && searchBy=='customer'" class="mt-3">
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Gender</th>
                    <th>Date of Birth</th>
                    <th>Phone</th>
                    <th>Address</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="customer in data.customers" :key="customer.id">
                    <td>{{ customer.id }}</td>
                    <td>{{ customer.name }}</td>
                    <td>{{ customer.gender }}</td>
                    <td>{{ customer.dob }}</td>
                    <td>{{ customer.phone }}</td>
                    <td>{{ customer.address }}</td>
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
  ...mapGetters(['token'])
},
methods:{
  async deleteItem(id){
    if(confirm("Are you sure you want to delete this item?")){
        await axios.delete(`http://localhost:5000/admin/deleteService/${id}`,{
            headers:{
                 Authorization: `Bearer ${this.token}`
            }
        })
        .then(response =>{
            // console.log(response);
            if (response.status == 200){
                // console.log(response.status)
                window.location.reload();
            }
        })
        .catch(error =>{
            // console.log(error)
            this.error = error;
        })
    }
},
  async search(){
    await axios.post('http://localhost:5000/admin/search',{
      searchBy:this.searchBy,
      query:this.query
    },{
      headers:{
        Authorization: `Bearer ${this.token}`
      }
    })
    .then(response=>{
      // console.log(response.data.services)
      this.data = response.data,
      this.status = response.status
    })
  },
  async suspend(id){
    // console.log(this.token)
            await axios.post(`http://localhost:5000/admin/suspendTechnician/${id}`,{},{
                headers:{
                        Authorization: `Bearer ${this.token}`
                    }
            })
            .then(response =>{
                if(response.status == 200){
                    window.location.reload();
                }
            })
            .catch(error =>{
                // console.log(error)
                this.error = error;
            })
        },
        async activate(id){
            await axios.post(`http://localhost:5000/admin/activateTechnician/${id}`,{},{
                headers:{
                        Authorization: `Bearer ${this.token}`
                    }
            })
            .then(response =>{
                // console.log(response)
                if(response.status == 200){
                    window.location.reload();
                }
            })
            .catch(error =>{
                // console.log(error)
                this.error = error;
            })
        }
}
}
</script>

<style>

</style>