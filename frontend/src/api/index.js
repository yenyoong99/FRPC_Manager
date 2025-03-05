// src/api/index.js
import axios from 'axios';

const apiClient = axios.create({
    baseURL: 'http://13.215.38.96:7888',
    headers: {
        'Content-Type': 'application/json'
    }
});

apiClient.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

export default {
    login(credentials) {
        return apiClient.post('/token', credentials);
    },
    createFrp(frp) {
        return apiClient.post('/frp/', frp);
    },
    readFrp(frpId) {
        return apiClient.get(`/frp/${frpId}`);
    },
    updateFrp(frpId, frp) {
        return apiClient.put(`/frp/${frpId}`, frp);
    },
    deleteFrp(frpId) {
        return apiClient.delete(`/frp/${frpId}`);
    },
    listFrps(skip = 0, limit = 10) {
        return apiClient.get('/frps/', { params: { skip, limit } });
    }
};
