<template>
    <div>
        <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
        </div>
    <div v-if="!error" class="container-fluid mt-5">
    <div>
        <div class="row">
            <div style="text-align: start; color:white;"><h2>Services</h2></div>
            <div style="text-align: end;"><RouterLink to="add_service" style="color: white;"><i class="bi bi-plus"></i>Add Service</RouterLink></div>
        </div>
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Price</th>
                    <th>Time</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="service in message.services" :key="service.id">
                    <td>{{service.id}}</td>
                    <td>{{service.name}}</td>
                    <td>{{service.price}}</td>
                    <td>{{service.time_required}}</td>
                    <td><router-link :to="{path: '/editService',query: { serviceID: service.id }}" class="bi bi-pencil-square"></router-link> | <a class="bi bi-trash" @click.prevent="deleteItem(service.id)"></a></td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="mt-5">
        <div class="row">
            <div style="text-align: start; color:white;"><h2>Professionals</h2></div>
        </div>
        <table class="table table-bordered table-striped mt-4">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Experience</th>
                    <th>Service ID</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="technician in message.technicians" :key="technician">
                    <td>{{ technician.id }}</td>
                    <td>{{ technician.name }}</td>
                    <td>{{ technician.experience }}</td>
                    <td>{{ technician.service_id }}</td>
                    <td>
                        <button v-if="technician.status == 'Available'" @click="suspend(technician.id)" class="btn btn-danger">Suspend</button>
                        <button v-else-if="technician.status == 'Suspended'" @click="activate(technician.id)" class="btn btn-success">Reinstate</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div class="mt-5">
        <div class="row">
            <div style="text-align: start;"><h2>Service Requests</h2></div>
        </div>
        <table class="table table-bordered table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Service</th>
                    <th>Professional Id</th>
                    <th>User Id</th>
                    <th>Requested Date</th>
                    <th>Completed Date</th>
                    <th>Remarks</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="request in message.service_requests" :key="request.id">
                    <td>{{ request.id }}</td>
                    <td>{{ request.service_name }}</td>
                    <td>{{ request.technician_id }}</td>
                    <td>{{ request.customer_id }}</td>
                    <td>{{ request.request_date }}</td>
                    <td>{{ request.completion_date }}</td>
                    <td>{{ request.remarks }}</td>
                    <td>{{ request.status }}</td>
                    <td><button v-if="request.status == 'Assigned'" @click="Close(request.id)" class="btn btn-danger">Close</button></td>
                </tr>
            </tbody>
        </table>
    </div>
  </div>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';
export default {
    data(){
        return{
            message:'',
            error:''
        }
    },
    computed:{
        ...mapState(['token'])
    },
    mounted(){
        // console.log(`Bearer ${this.token}`)
        axios.get('http://localhost:5000/admin/',{
            headers:{
                Authorization: `Bearer ${this.token}`
            }
        })
        .then(response =>this.message = response.data)
    .catch(error => {
        this.error = error;
      });
    //   console.log(this.message)
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
        },
        async Close(id){
            await axios.post(`http://localhost:5000/customer/complete/${id}`,{
                remarks: "Closed by Admin"
            },{
                headers:{
                    Authorization: `Bearer ${this.token}`
                }
            })
            .then(response => {
                if(response.status == 200){
                    window.location.reload();
                }
            })
            .catch(error => {
                this.error = error;
            });
        }
    }
}
</script>

<style scoped>
h2{
    color: white;
}
</style>