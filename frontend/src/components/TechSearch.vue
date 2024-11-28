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
              <option value="Service Request">Service Request ID</option>
            </select>
          </div>
          <div class="col-2 ms-2"><input type="text" class="form-control" v-model="query" placeholder="search"></div>
          <div class="col-1"><button type="button" @click="search" class="btn btn-primary">search</button></div>
        </div>
      </form>
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
                    <th>Actions</th>
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
                    <td><button v-if="request.status == 'Requested'" @click="acceptRequest(request.id)" class="btn btn-success me-1">Accept</button><button @click="rejectRequest(request.id)" v-if="request.status == 'Assigned' || request.status == 'Requested'" class="ms-1 btn btn-danger">Reject</button></td>
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
        await axios.post('http://localhost:5000/technician/search',{
          searchBy:this.searchBy,
          query:this.query,
          id:this.userId
        },{
          headers:{
            Authorization:`Bearer ${this.token}`
          }
        })
        .then(response=>{
          //console.log(response)
          this.status = response.status
          this.data = response.data
        })
        .catch(error=>{
          this.error=error
        })
    },
    async acceptRequest(id){
        await axios.post(`http://localhost:5000/technician/acceptRequest/${id}`,{},{
        headers:{
            'Authorization':`Bearer ${this.token}`
        }
    })
        .then(response=>{
            if(response.status == 200){
                window.location.reload()
            }
        })
        .catch(error=>{
            this.error = error
        })
    },
    async rejectRequest(id){
        await axios.post(`http://localhost:5000/technician/rejectRequest/${id}`,{},{
        headers:{
            'Authorization':`Bearer ${this.token}`
        }
    })
        .then(response=>{
            if(response.status == 200){
                window.location.reload()
            }
        })
        .catch(error=>{
            this.error = error
        })
    }
    }
  }
  </script>
  
  <style>
  
  </style>