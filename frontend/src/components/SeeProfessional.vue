<template>
    <div class="container">
        <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
        </div>
        <div v-if="!error">
            <h2 class="text-start mt-5" style="color: white;">{{service}}</h2>
            <table class="table table-bordered table-striped mt-3">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th scope="col">Name</th>
                        <th scope="col">Gender</th>
                        <th scope="col">Address</th>
                        <th scope="col">Age</th>
                        <th scope="col">Experience</th>
                        <th scope="col"></th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="professional in professionals" :key="professional.id">
                        <td>{{ professional.id }}</td>
                        <td>{{ professional.name }}</td>
                        <td>{{ professional.gender }}</td>
                        <td>{{ professional.address }}</td>
                        <td>{{ professional.age }}</td>
                        <td>{{ professional.experience }}</td>
                        <td><button class="btn btn-primary" @click="bookProfessional(professional.id)">Book</button></td>
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
            professionals: [],
            error: null,
            service: this.$route.query.serviceName,
        }
    },
    computed:{
        ...mapGetters(['token','userId']),
    },
    mounted() {
        const serviceId = this.$route.query.serviceID;
        // const service = this.$route.query.serviceName;
        axios.get(`http://localhost:5000/customer/seeprofessional/${serviceId}/${this.userId}`,{
            headers:{
                Authorization: `Bearer ${this.token}`
            }
            })
            .then(response => {
                this.professionals = response.data.professionals;
            })
            .catch(error => {
                this.error = error;
            })
    },
    methods:{
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
                // console.log(error)
                this.error = error
            }
        }
    }
}
</script>

<style>

</style>