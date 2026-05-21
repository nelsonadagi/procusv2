import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'


const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: () => import('../views/ProductList.vue')
        },
        {
            path: '/products',
            name: 'products',
            component: () => import('../views/ProductList.vue')
        },
        {
            path: '/products/:id',
            name: 'product-detail',
            component: () => import('../views/ProductDetail.vue')
        },
        {
            path: '/login',
            name: 'login',
            component: () => import('../views/Login.vue')
        },
        {
            path: '/register',
            name: 'register',
            component: () => import('../views/Register.vue')
        },
        {
            path: '/vendors/register',
            name: 'vendor-register',
            component: () => import('../views/VendorRegistration.vue'),
            meta: { requiresAuth: true, activationFlow: 'vendor' }
        },
        {
            path: '/contractors/register',
            name: 'contractor-register',
            component: () => import('../views/ContractorRegistration.vue'),
            meta: { requiresAuth: true, activationFlow: 'contractor' }
        },
        {
            path: '/contracts',
            name: 'contracts',
            component: () => import('../views/ContractList.vue')
        },
        {
            path: '/contracts/new',
            name: 'post-contract',
            component: () => import('../views/PostContract.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/contracts/:id',
            name: 'contract-detail',
            component: () => import('../views/ContractDetail.vue')
        },
        {
            path: '/projects',
            name: 'projects-list',
            component: () => import('../views/ProjectList.vue')
        },
        {
            path: '/projects/new',
            name: 'create-project',
            component: () => import('../views/CreateProject.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/projects/:id',
            name: 'project-detail',
            component: () => import('../views/ProjectDetail.vue')
        },
        {
            path: '/tenders',
            name: 'tenders',
            component: () => import('../views/ViewTenders.vue')
        },
        {
            path: '/investor/dashboard',
            name: 'investor-dashboard',
            component: () => import('../views/InvestorDashboard.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/finance/apply',
            name: 'finance-application',
            component: () => import('../views/FinanceApplication.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/government/dashboard',
            name: 'government-dashboard',
            component: () => import('../views/GovernmentDashboard.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/admin/reports',
            name: 'regulatory-reports',
            component: () => import('../views/RegulatoryReports.vue'),
            meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
            path: '/admin',
            name: 'admin-dashboard',
            component: () => import('../views/AdminDashboard.vue'),
            meta: { requiresAuth: true, requiresAdmin: true }
        },
        {
            path: '/vendor/dashboard',
            name: 'vendor-dashboard',
            component: () => import('../views/VendorDashboard.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/contractor/dashboard',
            name: 'contractor-dashboard',
            component: () => import('../views/ContractorDashboard.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/courier/dashboard',
            name: 'courier-dashboard',
            component: () => import('../views/CourierDashboard.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/owner/dashboard',
            name: 'owner-dashboard',
            component: () => import('../views/OwnerDashboard.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/buyer/dashboard',
            name: 'buyer-dashboard',
            component: () => import('../views/BuyerDashboard.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/market/secondary',
            name: 'secondary-market',
            component: () => import('../views/SecondaryMarket.vue')
        },
        {
            path: '/properties',
            name: 'property-list',
            component: () => import('../views/PropertyListing.vue')
        },
        {
            path: '/properties/:id',
            name: 'property-detail',
            component: () => import('../views/PropertyDetail.vue')
        },
        {
            path: '/properties/:id/edit',
            name: 'property-edit',
            component: () => import('../views/PropertyEdit.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/property-manager/dashboard',
            name: 'property-manager-dashboard',
            component: () => import('../views/PropertyManagerDashboard.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/agent/dashboard',
            name: 'agent-dashboard',
            component: () => import('../views/PropertyManagerDashboard.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/surveyor/dashboard',
            name: 'surveyor-dashboard',
            component: () => import('../views/PropertyManagerDashboard.vue'),
            meta: { requiresAuth: true }
        },
        {
            path: '/:pathMatch(.*)*',
            name: 'not-found',
            component: () => import('../views/ProductList.vue')
        },
    ]
})

router.beforeEach((to) => {
    const authStore = useAuthStore();

    if (!authStore.isAuthenticated) {
        if (to.name === 'buyer-dashboard') return true;
        if (to.name === 'login' || to.name === 'register') {
            return true;
        }
        if (to.meta.requiresAuth || to.meta.requiresAdmin) {
            return {
                name: 'login',
                query: { redirect: to.fullPath }
            };
        }
    }

    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        return {
            name: 'login',
            query: { redirect: to.fullPath }
        };
    }

    if (to.meta.requiresAdmin && !authStore.isAdmin) {
        return authStore.isAuthenticated ? { name: 'home' } : { name: 'buyer-dashboard' };
    }

    return true;
});

export default router
