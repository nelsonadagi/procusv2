import { defineStore } from 'pinia';
import api from '../services/api';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        user: JSON.parse(localStorage.getItem('user')) || null,
        token: localStorage.getItem('token') || null,
        loading: false,
        error: null,
    }),

    getters: {
        isAuthenticated: (state) => !!state.token,
        userRole: (state) => state.user?.role || 'GUEST',
        hasPermission: (state) => (permission) => {
            if (state.user?.role === 'ADMIN') return true;
            return state.user?.permissions?.includes(permission) || false;
        },
        hasRole: (state) => (role) => {
            if (state.user?.role === 'ADMIN') return true;
            if (state.user?.role === role) return true;
            return state.user?.roles?.includes(role) || false;
        }
    },

    actions: {
        async login(email, password) {
            this.loading = true;
            this.error = null;
            try {
                // Backend returns { token: "...", user: {...} }
                const response = await api.post('/accounts/login/', { email, password });
                const { token, user } = response.data;

                this.token = token;
                this.user = user;

                // Persist
                localStorage.setItem('token', token);
                localStorage.setItem('user', JSON.stringify(user));

                // Add auth header to future requests
                api.defaults.headers.common['Authorization'] = `Token ${token}`;

                return true;
            } catch (err) {
                this.error = err.response?.data?.detail || 'Login failed';
                return false;
            } finally {
                this.loading = false;
            }
        },

        async register(userData) {
            this.loading = true;
            this.error = null;
            try {
                const response = await api.post('/accounts/register/', userData);
                // We can auto-login here if the backend returns token on register
                if (response.data.token) {
                    const { token, user } = response.data;
                    this.token = token;
                    this.user = user;
                    localStorage.setItem('token', token);
                    localStorage.setItem('user', JSON.stringify(user));
                    api.defaults.headers.common['Authorization'] = `Token ${token}`;
                    return true;
                }
                return true;
            } catch (err) {
                this.error = err.response?.data?.detail || Object.values(err.response?.data || {}).flat().join(', ') || 'Registration failed';
                return false;
            } finally {
                this.loading = false;
            }
        },

        logout() {
            this.user = null;
            this.token = null;
            localStorage.removeItem('token');
            localStorage.removeItem('user');
            delete api.defaults.headers.common['Authorization'];
        },

        // Initialize token header on app start
        init() {
            if (this.token) {
                api.defaults.headers.common['Authorization'] = `Token ${this.token}`;
            }
        }
    }
});
