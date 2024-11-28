<template>
  <div class="container-fluid">
    <div v-if="error" class="alert alert-danger" role="alert">
        {{ error }}
    </div>
    <div v-if="!error">
        <h2 class="mt-5" style="color: white;">Profile</h2>
        <div v-if="userRole ==='customer'">
            <form @submit.prevent="updateCustomer">
                <div class="row mt-2 mb-3">
                    <div class="col">
                    <label for="id" class="form-label">Customer ID</label>
                    <input type="text" v-model="uservalues.id" class="form-control" disabled required>
                    </div>
                    <div class="col">
                    <label for="gender" class="form-label">User ID</label>
                    <input type="text" v-model="uservalues.user_id" disabled required class="form-control">
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" v-model="uservalues.email" class="form-control" required>
                    </div>
                    <div class="col">
                    <label for="name" class="form-label">Username</label>
                    <input type="text" v-model="uservalues.username" class="form-control" disabled required>
                    </div>
                    <div class="col">
                    <label for="gender" class="form-label">Password</label>
                    <input type="password" v-model="uservalues.password" required class="form-control">
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                    <label for="name" class="form-label">Name</label>
                    <input type="text" v-model="uservalues.name" class="form-control" required>
                    </div>
                    <div class="col">
                    <label for="gender" class="form-label">Gender</label>
                    <select v-model="uservalues.gender" class="form-select" required>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                    </select>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                    <label for="dob" class="form-label">Date of Birth</label>
                    <input type="date" class="form-control" v-model="uservalues.dob" required>
                    </div>
                    <div class="col">
                    <label for="phone" class="form-label">Phone No</label>
                    <input type="phone" class="form-control" v-model="uservalues.phone" required>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                    <label for="address" class="form-label">Address</label>
                    <textarea v-model="uservalues.address" rows="4" class="form-control" style="resize: none;"></textarea>
                    </div>
                </div>
                <div>
                    <button type="submit" class="btn btn-primary m-2">Update</button>
                    <button type="button" @click="reset" class="btn btn-danger m-2">Reset</button>
                </div>
            </form>
        </div>
        <div v-if="userRole === 'technician'">
            <form @submit.prevent="updateTech">
                <div class="row mt-3 mb-3">
                    <div class="col">
                    <label for="name" class="form-label">Technician ID</label>
                    <input type="text" v-model="techValues.id" class="form-control" required>
                    </div>
                    <div class="col">
                    <label for="userID" class="form-label">User ID</label>
                    <input type="text" v-model="techValues.user_id" disabled required class="form-control">
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                        <label for="email" class="form-label">Email</label>
                        <input type="email" v-model="techValues.email" class="form-control" required>
                    </div>
                    <div class="col">
                    <label for="name" class="form-label">Username</label>
                    <input type="text" v-model="techValues.username" class="form-control" required>
                    </div>
                    <div class="col">
                    <label for="gender" class="form-label">Password</label>
                    <input type="password" v-model="techValues.password" required class="form-control">
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                    <label for="name" class="form-label">Name</label>
                    <input type="text" v-model="techValues.name" class="form-control" required>
                    </div>
                    <div class="col">
                    <label for="gender" class="form-label">Gender</label>
                    <select v-model="techValues.gender" class="form-select" required>
                        <option value="Male">Male</option>
                        <option value="Female">Female</option>
                    </select>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                    <label for="Age" class="form-label">Age</label>
                    <input type="number" max="60" min="20" class="form-control" v-model="techValues.age" required>
                    </div>
                    <div class="col">
                    <label for="service" class="form-label">Service</label>
                    <select v-model="techValues.service_id" class="form-select" required>
                        <option v-for="service in services" :key="service" :value="service.id" >{{service.name}}</option>
                    </select>
                    </div>
                    <div class="col">
                    <label for="experience" class="form-label">Experience</label>
                    <input type="number" max="20" min="2" class="form-control" v-model="techValues.experience" required>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col">
                    <label for="address" class="form-label">Address</label>
                    <textarea v-model="techValues.address" rows="4" class="form-control" style="resize: none;"></textarea>
                    </div>
                </div>
                <div>
                    <button type="submit" class="btn btn-primary m-2">Submit</button>
                    <button type="button" @click="resetTech" class="btn btn-danger m-2">Reset</button>
                </div>
            </form>
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
            uservalues:{
                id: '',
                user_id: '',
                email: '',
                username: '',
                password: '',
                name: '',
                gender: '',
                dob: '',
                phone: '',
                address: ''
            },
            defaultUserValues:{
                id: '',
                user_id: '',
                email:'',
                username: '',
                password: '',
                name: '',
                gender: '',
                dob: '',
                phone: '',
                address: ''
            },
            techValues:{
                id:'',
                user_id:'',
                email:'',
                username:'',
                password:'',
                name:'',
                gender:'',
                age:'',
                service_id:'',
                experience:'',
                address:''
            },
            deafultTechValues:{
                id:'',
                user_id:'',
                email:'',
                username:'',
                password:'',
                name:'',
                gender:'',
                age:'',
                service_id:'',
                experience:'',
                address:''
            },
            services:[],
            
            error: ''
        }
    },
    computed:{
        ...mapGetters(['token','userRole','userId'])
    },
    mounted(){
        if(this.userRole === 'customer'){
            axios.get(`http://localhost:5000/customer/profile/${this.userId}`,{
                headers:{
                    'Authorization': `Bearer ${this.token}`
                }
            })
            .then((response)=>{
                this.defaultUserValues = response.data.user,
                this.uservalues = { ...this.defaultUserValues }
            })
            .catch((error)=>{
                this.error = error
            })
        }
        else if(this.userRole === 'technician'){
            axios.get(`http://localhost:5000/technician/profile/${this.userId}`,{
                headers:{
                    'Authorization': `Bearer ${this.token}`
                }
            })
            .then((response)=>{
                this.defaultTechValues = response.data.tech,
                this.techValues = { ...this.defaultTechValues },
                this.services = response.data.services
            })
            .catch((error)=>{
                this.error = error
            })
        }
    },
    methods:{
        reset(){
            this.values = { ...this.defaultValues }
        },
        resetTech(){
            this.techValues = { ...this.defaultTechValues }
        },
        async updateCustomer(){
            await axios.post(`http://localhost:5000/customer/update/${this.userId}`,{
                data: this.uservalues
            },{
                headers:{
                    'Authorization': `Bearer ${this.token}`
                }
            })
            .then((response)=>{
                if(response.status === 200){
                    this.$router.push('/user_dashboard')
                    // console.log(response)
                }
            })
            .catch((error)=>{
                this.error = error
            })
        },
        async updateTech(){
            await axios.post(`http://localhost:5000/technician/update/${this.userId}`,{
                data: this.techValues
            },{
                headers:{
                    'Authorization': `Bearer ${this.token}`
                }
            })
            .then((response)=>{
                if(response.status === 200){
                    this.$router.push('/tech_dashboard')
                    // console.log(response)
                }
            })
            .catch((error)=>{
                this.error = error
            })
        }
    }
}
</script>

<style>

</style>