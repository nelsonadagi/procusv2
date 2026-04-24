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
        isAdmin: (state) => state.user?.role === 'ADMIN' || state.user?.is_staff || false,
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
        },

        setUser(user) {
            this.user = user;
            localStorage.setItem('user', JSON.stringify(user));
        }
    }
});
