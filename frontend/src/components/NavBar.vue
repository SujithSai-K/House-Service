<template>
  <nav v-if="$route.meta.showNavbar" class="navbar navbar-expand-lg" style="background-color: #e3f2fd">
  <div class="container-fluid">
    <a class="navbar-brand" href="#">
      <img src="@/assets/navbarlogo1.png" alt="" width="70" height="52" class="d-inline-block align-text-top">
    </a>
    <router-link to="/" class="navbar-brand">HOUSE CARE</router-link>
    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav">
        <li class="nav-item">
          <router-link v-if="userRole === 'admin'" to="/AdminDashboard" class="nav-link">Home</router-link>
          <router-link v-if="userRole === 'customer'" to="/user_dashboard" class="nav-link">Home</router-link>
          <router-link v-if="userRole === 'technician'" to="/tech_dashboard" class="nav-link">Home</router-link>
        </li>
        <li class="nav-item">
          <router-link v-if="userRole === 'admin'" to="/admin_search" class="nav-link">Search</router-link>
          <router-link v-if="userRole === 'customer'" to="/user_search" class="nav-link">Search</router-link>
          <router-link v-if="userRole === 'technician'" to="/tech_search" class="nav-link">Search</router-link>
        </li>
        <li class="nav-item">
          <router-link v-if="userRole === 'admin'" to="/admin_summary" class="nav-link">Summary</router-link>
          <router-link v-if="userRole === 'customer'" to="/user_summary" class="nav-link">Summary</router-link>
          <router-link v-if="userRole === 'technician'" to="/tech_summary" class="nav-link">Summary</router-link>
        </li>
      </ul>
      <div class="d-flex ms-auto" style="align-items: end;">
        <a @click="performLogout" class="p-2" style="font-size:x-large;"><i class="bi bi-box-arrow-right"></i></a>
        <router-link to="/profile" v-if="userRole != 'admin'" class="p-2" style="font-size:x-large;"><i class="bi bi-person-fill"></i></router-link>
      </div>
    </div>
  </div>
</nav>
</template>

<script>
import { mapActions } from 'vuex';
import { mapGetters } from 'vuex';

export default {
  computed: {
    ...mapGetters(['userRole']),
    showNavbar() {
      return this.$route.meta.showNavbar; // Get the navbar visibility from route metadata
    }
  },
  methods: {
    ...mapActions(['logout']),
    async performLogout() {
      await this.logout(this.$router);
      }
    }
}
</script>

<style>

</style>