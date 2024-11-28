<template>
    <div>
        {{ message }}
    </div>
</template>

<script>
// import axios from 'axios';
import { mapState, mapActions } from 'vuex';
export default {
    data(){
        return{
            message:''
        }
    },
    computed:{
        ...mapState(['token'])
    },
    methods: {
    ...mapActions(['logout']),
    async login() {
      await this.logout();
      }
    }
  }

</script>

<style>

</style>