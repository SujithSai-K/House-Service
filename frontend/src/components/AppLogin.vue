<template>
  <div class="container-fluid">
  <div v-if="message" class="alert alert-danger" role="alert">
            {{ message }}
  </div>
  <div class="container-fluid form">
    
    <form @submit.prevent="login">
      <div class="mt-3 mb-3">
        <img src="@/assets/logo1.png" alt="" width="200" height="200"><br>
        <h2>Login</h2>
      </div>
      <div class="mb-3">
        <label for="username" class="form-label">Username</label>
        <input type="test" class="form-control" v-model="username" placeholder="Username" required>
      </div>
      <div class="mb-3" >
        <label for="password" class="form-label">Password</label>
        <input type="password" class="form-control" v-model="password" placeholder="Password" required>
      </div>
      <div class="mb-3">
        <button type="submit" class="btn btn-primary m-1">Login</button>
        <button type="button" @click="reset" class="btn btn-danger m-1">Reset</button>
        <p class="m-1">new user?<router-link to="/user_register">signup</router-link></p>
      </div>
    </form>
  </div>
  </div>
</template>

<script>
import { mapActions, mapState, mapMutations } from 'vuex';

export default {
  name: "AppLogin",
  data() {
    return {
      username: '',
      password: ''
    };
  },
  computed: {
    ...mapState(['message']),
    ...mapState(['role'])
  },
  methods: {
    ...mapActions(['performLogin']),
    ...mapMutations(['setMessage']),
    async login() {
      this.setMessage('');
      await this.performLogin({ username: this.username, password: this.password });
      if (!this.message) {
        if (this.role == 'admin'){
          this.$router.push({ name: 'AdminDashboard' });
        }
        else if(this.role == 'customer'){
          this.$router.push({ name: 'CustDashboard' });
        }
        else if(this.role == 'technician'){
          this.$router.push({ name: 'tech_dashboard' });
        }
      }
    },
    reset() {
      this.username = '';
      this.password = '';
      this.setMessage('');
    }
  }
};

</script>

<style scoped>
  .form{
    display: flex;
    justify-content: center;
    align-items: center;
    background-color: rgba(255, 255, 255, 0.512);
    width: 350px;
    height: 540px;
    margin-top: 100px;
    border-radius: 50px;
  }
</style>