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
        isAuthenticated: (state) => !!state.token && !!state.user,
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
        },
        hasPermission: (state) => (permission) => {
            if (state.user?.role === 'ADMIN' || state.user?.is_staff) return true;
            const userRole = state.user?.role;
            const userRoles = state.user?.roles || [];
            // Check primary role permissions from backend
            const rolePerms = state.user?.role_permissions || {};
            if (rolePerms[permission]) return true;
            // Fallback to role list check for frontend guards
            const allRoles = [userRole, ...userRoles];
            const rolePermissionMap = {
                'PROPERTY_MANAGER': ['property:view', 'property:list_property', 'property:update_property', 'property:delete_property', 'property:manage_inquiries', 'property:manage_appointments'],
                'REAL_ESTATE_AGENT': ['property:view', 'property:list_property', 'property:update_property', 'property:manage_inquiries', 'property:manage_appointments'],
                'SURVEYOR': ['property:view', 'property:update_property', 'property:verify_property'],
                'PROJECT_OWNER': ['property:view', 'property:list_property', 'property:update_property', 'property:delete_property', 'property:manage_inquiries', 'property:manage_appointments'],
                'GOVERNMENT': ['property:view'],
                'GOVERNMENT_OWNER': ['property:view', 'property:verify_property'],
                'GOVERNMENT_AUDITOR': ['property:view', 'property:verify_property'],
            };
            for (const r of allRoles) {
                const perms = rolePermissionMap[r] || [];
                if (perms.includes(permission)) return true;
            }
            return false;
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
