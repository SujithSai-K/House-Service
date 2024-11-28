<template>
    <div class="container-fluid">
        <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
        </div>
        <div v-if="!error" class="overflow-x-auto">
            <h2 class="mt-5" style="text-align: start; color:white;">Services</h2>
            <div style="max-height: 300px;" class="overflow-x-auto">
                <div v-for="service in services" :key="service.id" class="card m-2 d-inline-flex" style="width: 16rem; height:12rem;">
                    <div class="card-body">
                        <h5 class="card-title text-start ms-2">{{service.name}}</h5>
                        <p class="card-text text-start ms-2">{{service.description}}</p>
                        <div class="row card-text text-start ms-2"><div class="col">Price:₹{{ service.price }}</div><div class="col">Time: {{ service.time_required }}Hrs</div></div>
                        <router-link :to="{path: '/SeeProfessional',query: { serviceID: service.id, serviceName: service.name}}" class="btn btn-primary mt-2">See Professionals</router-link>
                    </div>
                </div>
            </div>
            <div>
                <h2 class="mt-3" style="text-align: start; color:white;">Service Requests</h2>
                <table class="table table-bordered table-striped">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Service Name</th>
                            <th>Professional Name</th>
                            <th>Request Date</th>
                            <th>Request Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="request in service_requests" :key="request">
                            <td>{{ request.id }}</td>
                            <td>{{ request.service_id }}</td>
                            <td>{{ request.technician_id }}</td>
                            <td>{{ request.request_date }}</td>
                            <td>{{ request.status }}</td>
                            <td>
                                <button v-if="request.status == 'Requested'" @click="cancel(request.id)" class="btn btn-danger">Cancel</button>
                                <button type="button" class="btn btn-success" v-else-if="request.status =='Assigned'" data-bs-toggle="modal" :data-bs-target="'#modal-' + request.id">Completed</button>
                                <p v-else>-</p>
                                <div class="modal fade" :id="'modal-' + request.id" tabindex="-1" aria-labelledby="'modal-label-' + request.id" aria-hidden="true">
                                <div class="modal-dialog modal-dialog-centered">
                                    <div class="modal-content">
                                    <div class="modal-header">
                                        <h1 class="modal-title fs-5" :id="'modal-label-' + request.id">Remarks</h1>
                                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                                    </div>
                                    <div class="modal-body">
                                        <input type="text" v-model="request.remarks" class="form-control">
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                                        <button type="button" @click="complete(request.id,request.remarks)" data-bs-dismiss="modal" class="btn btn-primary">Submit</button>
                                    </div>
                                    </div>
                                </div>
                                </div>
                            </td>
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
    data() {
        return {
            services: [],
            service_requests: [],
            error: null,
            remarks:''
        }
    },
    computed:{
        ...mapGetters(['token', 'userId'])
    },
    mounted() {
        axios.get(`http://localhost:5000/customer/${this.userId}`,{
            headers:{
                Authorization: `Bearer ${this.token}`
            }
            })
            .then(response => {
                this.services = response.data.services;
                this.service_requests = response.data.service_requests;
            })
            .catch(error => {
                this.error = error;
                if (error.response && error.response.status === 404){
                    alert("No services found");
                }
            });
    },
    methods:{
        async complete(id,remarks){
            // console.log(id,remarks);
            await axios.post(`http://localhost:5000/customer/complete/${id}`,{
                remarks: remarks
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
        },
        async cancel(id){
            await axios.post(`http://localhost:5000/customer/cancel/${id}`,{},{
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

<style>

</style>