<template>
  <div class="container-fluid">
    <div v-if="!error">
        <form class="mt-5" @submit.prevent="updateService">
            <div class="row mb-3">
                <div class="col">
                    <label for="ID" class="form-label">ID</label>
                    <input type="number" v-model="values.id"  disabled class="form-control">
                </div>
                <div class="col">
                    <label for="name" class="form-label">Name</label>
                    <input type="text" v-model="values.name" class="form-control"  required />
                </div>
            </div>
            <div class="row mb-3">
            <label for="Description" class="form-label">Description</label>
            <textarea v-model="values.description" class="form-control" rows="3" style="resize: none;" required></textarea>
            </div>
            <div class="row mb-3">
            <div class="col">
                <label for="time" class="form-label">Time Required</label>
                <div class="input-group">
                <input type="number" v-model="values.time_required" class="form-control" required />
                <span class="input-group-text">hrs</span>
                </div>
            </div>
            <div class="col">
                <label for="price" class="form-label">Price</label>
                <div class="input-group">
                <span class="input-group-text">₹</span>
                <input type="number" v-model="values.price" class="form-control" required />
                </div>
            </div>
            </div>
            <button type="submit" class="btn btn-primary m-3">Submit</button>
            <button type="button" @click="reset" class="btn btn-danger m-3">Reset</button>
        </form>
    </div>
  </div>
</template>

<script>
import { mapGetters } from 'vuex';
import axios from 'axios';
export default {
    data(){
        return{
            message:'',
            error:'',
            serviceId: this.$route.query.serviceID,
            defaultValues:{
                id:'',
                name:'',
                description:'',
                time_required:'',
                price:''
            },
            values:{
                id:'',
                name:'',
                description:'',
                time_required:'',
                price:''
            }
        }
    },
    computed:{
        ...mapGetters(['token'])
    },
    mounted(){
        axios.get(`http://localhost:5000/admin/editServices/${this.serviceId}`,{
            headers:{
                'Authorization': `Bearer ${this.token}`
            }
        })
        .then((response)=>{
            this.defaultValues = response.data.service,
            this.values = { ...this.defaultValues }
        })
        .catch((error)=>{
            this.error = error.response.data
        })
    },
    methods:{
        reset(){
            this.values = { ...this.defaultValues }
        },
        async updateService(){
           const response = await axios.post(`http://localhost:5000/admin/editServices/${this.serviceId}`,
                {
                    name:this.values.name,
                    description:this.values.description,
                    time_required:this.values.time_required,
                    price:this.values.price
                },
                {
                    headers:{
                        'Authorization': `Bearer ${this.token}`
                    }
                }
            );
            if(response.status === 200){
                this.$router.push({name:"AdminDashboard"})
            }
        }
    }
}
</script>

<style>

</style>