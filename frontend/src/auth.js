import axios from 'axios';

// Base URL for the Flask API
const API_URL = 'http://127.0.0.1:5000';

export default {
  login(username, password) {
    return axios.post(`${API_URL}/login`, { username, password });
  },
  getProtectedData(token) {
    return axios.get(`${API_URL}/read-data`, {
      headers: { Authorization: `Bearer ${token}` }
    });
  },
  deleteData(token) {
    return axios.delete(`${API_URL}/delete-data`, {
      headers: { Authorization: `Bearer ${token}` }
    });
  }
};
