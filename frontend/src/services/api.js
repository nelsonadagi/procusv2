import axios from 'axios';

// Ensure we don't end up with /api/v1 if the env var is changed
const baseURL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
    baseURL: baseURL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor: Attach token if it exists
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('token');
        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }
        const activeCountry = localStorage.getItem('activeCountry');
        if (activeCountry) {
            config.headers['X-Active-Country'] = activeCountry;
        }
        if (config.data instanceof FormData) {
            delete config.headers['Content-Type'];
            delete config.headers['content-type'];
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// Response interceptor: Handle unauthorized/forbidden errors
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response && error.response.status === 401) {
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            const currentPath = `${window.location.pathname}${window.location.search}`;
            if (!currentPath.startsWith('/login') && !currentPath.startsWith('/register')) {
                window.location.href = `/login?redirect=${encodeURIComponent(currentPath)}`;
            }
        }
        return Promise.reject(error);
    }
);

export default api;
