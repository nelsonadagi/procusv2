import { createRouter, createWebHistory } from 'vue-router'
import ProductList from '../views/ProductList.vue'

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            name: 'home',
            component: ProductList
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
            path: '/contractors/register',
            name: 'contractor-register',
            component: () => import('../views/ContractorRegistration.vue')
        },
        {
            path: '/contracts',
            name: 'contracts',
            component: () => import('../views/ContractList.vue')
        },
        {
            path: '/contracts/new',
            name: 'post-contract',
            component: () => import('../views/PostContract.vue')
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
            component: () => import('../views/CreateProject.vue')
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
            component: () => import('../views/InvestorDashboard.vue')
        },
        {
            path: '/admin/reports',
            name: 'regulatory-reports',
            component: () => import('../views/RegulatoryReports.vue')
        },
        {
            path: '/admin',
            name: 'admin-dashboard',
            component: () => import('../views/AdminDashboard.vue')
        },
        {
            path: '/vendor/dashboard',
            name: 'vendor-dashboard',
            component: () => import('../views/VendorDashboard.vue')
        },
        {
            path: '/contractor/dashboard',
            name: 'contractor-dashboard',
            component: () => import('../views/ContractorDashboard.vue')
        },
        {
            path: '/owner/dashboard',
            name: 'owner-dashboard',
            component: () => import('../views/OwnerDashboard.vue')
        },
        {
            path: '/buyer/dashboard',
            name: 'buyer-dashboard',
            component: () => import('../views/BuyerDashboard.vue')
        },
        {
            path: '/market/secondary',
            name: 'secondary-market',
            component: () => import('../views/SecondaryMarket.vue')
        },
    ]
})

export default router
