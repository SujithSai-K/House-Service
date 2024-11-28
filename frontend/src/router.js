import { createRouter, createWebHistory } from "vue-router";
import AppLogin from './components/AppLogin.vue'
import user_register from "./components/user_register.vue"; 
import tech_register from "./components/tech_register.vue";
import HomePage from "./components/HomePage.vue";
import AdminDashboard from "./components/AdminDashboard.vue";
import TestPage from "./components/TestPage.vue";
import store from "./store.js";
import Logout_user from "./components/logout_user.vue";
import add_service from "./components/add_service.vue";
import CustDashboard from "./components/CustDashboard.vue";
import SeeProfessional from "./components/SeeProfessional.vue";
import editService from "./components/editService.vue";
import TechDashboard from "./components/TechDashboard.vue";
import adminSearch from "./components/AdminSearch.vue";
import UserSearch from "./components/UserSearch.vue";
import TechSearch from "./components/TechSearch.vue";
import techSummary from "./components/techSummary.vue";
import adminSummary from "./components/adminSummary.vue";
import userSummary from "./components/userSummary.vue";
import profilePage from "./components/profilePage.vue";

const routes = [
    {
        path: '/test',
        name: 'test',
        // meta: { showNavbar: false },
        component: TestPage
    },
    {
        path: '/',
        name: 'HomePage',
        // meta: { showNavbar: false },
        component: HomePage
    },
    {
        path: '/login',
        name: 'login',
        // meta: { showNavbar: "false" },
        component: AppLogin
    },
    {
        path: '/logout',
        name: 'logout_user',
        component: Logout_user
    },
    {
        path: '/user_register',
        name: 'user_register',
        // meta: { showNavbar: false },
        component: user_register
    },
    {
        path: '/tech_register',
        name: 'tech_register',
        // meta: { showNavbar: false },
        component: tech_register
    },
    {
        path:'/AdminDashboard',
        name: 'AdminDashboard',
        // meta: { showNavbar: false },
        component: AdminDashboard,
        meta: { requiresAuth: true, role: 'admin', showNavbar: true }
    },
    {
        path:'/user_dashboard',
        name: 'CustDashboard',
        component: CustDashboard,
        meta: { requiresAuth: true, role: 'customer', showNavbar: true } 
    },
    {
        path:'/tech_dashboard',
        name: 'tech_dashboard',
        component: TechDashboard,
        meta: { requiresAuth: true, role: 'technician', showNavbar: true }
    },
    {
        path:'/add_service',
        name: 'add_service',    
        component: add_service,
        meta: { requiresAuth: true, role: 'admin', showNavbar: true }
    },
    {
        path:'/editservice',
        name: 'editService',
        component: editService,
        meta: { requiresAuth: true, role: 'admin', showNavbar: true }
    },
    {
        path:'/SeeProfessional',
        name: 'SeeProfessional',
        component: SeeProfessional,
        meta: { requiresAuth: true, role: 'customer', showNavbar: true }
    },
    {
        path: '/admin_search',
        name: 'search',
        component: adminSearch,
        meta: { showNavbar: true, requiresAuth: true, role: 'admin' }
    },
    {
        path: '/user_search',
        name: 'user_search',
        component: UserSearch,
        meta: { showNavbar: true, requiresAuth: true, role: 'customer' }
    },
    {
        path: '/tech_search',
        name: 'tech_search',
        component: TechSearch,
        meta: { showNavbar: true, requiresAuth: true, role: 'technician' }
    },
    {
        path: '/tech_summary',
        name: 'tech_summary',
        component: techSummary,
        meta: { showNavbar: true, requiresAuth: true, role: 'technician' }
    },
    {
        path: '/admin_summary',
        name: 'admin_summary',
        component: adminSummary,
        meta: { showNavbar: true, requiresAuth: true, role: 'admin' }
    },
    {
        path: '/user_summary',
        name: 'user_summary',
        component: userSummary,
        meta: { showNavbar: true, requiresAuth: true, role: 'customer' }
    },
    {
        path: '/profile',
        name: 'profile',
        component: profilePage,
        meta: { showNavbar: true, requiresAuth: true}
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    const isAuthenticated = store.getters.isAuthenticated;
    const userRole = store.getters.userRole;
    // console.log(isAuthenticated);
    // console.log(userRole),
    // console.log(to.meta.role);
  
    if (to.matched.some(record => record.meta.requiresAuth)) {
      // Check if the user is logged in
      if (!isAuthenticated) {
        return next({ name: 'login' });
      }
      // Check if the route requires a specific role
      if (to.meta.role && to.meta.role !== userRole) {
        if(confirm("You don't have access to this page")){
            if(userRole == "admin"){
                return next({ name: 'AdminDashboard' });
            }
            else if(userRole == "customer"){
                return next({ name: 'CustDashboard' });
            }
            else if(userRole == "technician"){
                return next({ name: 'tech_dashboard' });
            }
        }  // Redirect to home if the user does not have access
        else{
            if(userRole == "admin"){
                return next({ name: 'AdminDashboard' });
            }
            else if(userRole == "customer"){
                return next({ name: 'CustDashboard' });
            }
            else if(userRole == "technician"){
                return next({ name: 'tech_dashboard' });
            }
        }
      }
    }
    next();
  });

export default router;