import Vuex from 'vuex';
import authAPI from './auth';

const storedToken = localStorage.getItem('token');
const storedUserRole = localStorage.getItem('userRole');
const storedId = localStorage.getItem('id'); // Retrieve ID from localStorage

export default new Vuex.Store({
  state: {
    token: storedToken || null,
    role: storedUserRole || null,
    id: storedId || null, // Initialize ID in state
    message: ''
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    setRole(state, role) {
      state.role = role;
      localStorage.setItem('userRole', role);
    },
    setId(state, id) {
      state.id = id; // Update state
      localStorage.setItem('id', id); // Save to localStorage
    },
    setMessage(state, message) {
      state.message = message;
    },
    logout(state) {
      state.token = null;
      state.role = null;
      state.id = null; // Clear ID on logout
      localStorage.removeItem('token');
      localStorage.removeItem('userRole');
      localStorage.removeItem('id'); // Remove ID from localStorage
    }
  },
  actions: {
    async performLogin({ commit }, { username, password }) {
      try {
        const response = await authAPI.login(username, password);
        const { access_token, role, id } = response.data; // Assuming response includes `id`
        commit('setToken', access_token);
        commit('setRole', role);
        commit('setId', id); // Store ID
      } catch (error) {
        commit('setMessage', 'Login failed: ' + error.response.data.message);
      }
    },
    logout({ commit }, router) {
      commit('logout');
      if (router) {
        router.push({ name: 'login' });
      }
    }
  },
  getters: {
    token: state => state.token,
    isAuthenticated: state => !!state.token,
    userRole: state => state.role,
    userId: state => state.id // Add getter for `id`
  }
});
