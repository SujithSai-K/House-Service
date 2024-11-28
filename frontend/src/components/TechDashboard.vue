<template>
  <div class="container-fluid">
    <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
    </div>
    <div v-if="!error">
        <h2 class="mt-5" style="text-align: start; color:white;">Pending Requests</h2>
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Customer Name</th>
                    <th>Phone No.</th>
                    <th>Address</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="request in requests.pending_requests" :key="request.id">
                    <td>{{ request.id }}</td>
                    <td>{{ request.name }}</td>
                    <td>{{ request.phone }}</td>
                    <td>{{ request.address }}</td>
                    <td>{{ request.status }}</td>
                    <td><button v-if="request.status == 'Requested'" @click="acceptRequest(request.id)" class="btn btn-success me-1">Accept</button><button @click="rejectRequest(request.id)" class="ms-1 btn btn-danger">Reject</button></td>
                </tr>
            </tbody>
        </table>
        <h2 class="mt-5" style="text-align: start; color:white;">Completed Requests</h2>
        <table class="table table-striped table-bordered">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Customer Name</th>
                    <th>Phone No.</th>
                    <th>Address</th>
                    <th>Status</th>
                    <th>Remarks</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="request in requests.completed_requests" :key="request.id">
                    <td>{{ request.id }}</td>
                    <td>{{ request.name }}</td>
                    <td>{{ request.phone }}</td>
                    <td>{{ request.address }}</td>
                    <td>{{ request.status }}</td>
                    <td>{{ request.remarks }}</td>
                </tr>
            </tbody>
        </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapGetters } from 'vuex';
export default {
data(){
    return{
        message:'',
        error:'',
        requests:[]
    }
},
computed:{
    ...mapGetters(['token','userId'])
},
mounted(){
    axios.get(`http://localhost:5000/technician/${this.userId}`,{
        headers:{
            'Authorization':`Bearer ${this.token}`
        }
    })
    .then(response=>{
        this.requests=response.data
        // console.log(this.requests)
    })
    .catch(error=>{
        this.error = error
    })
},
methods:{
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