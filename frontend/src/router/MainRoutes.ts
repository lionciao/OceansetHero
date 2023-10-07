const MainRoutes = {
    path: '/',
    meta: {
        requiresAuth: true
    },
    component: () => import('@/layouts/full/FullLayout.vue'),
    children: [
        {
            name: 'Dashboard',
            path: '/',
            component: () => import('@/views/main/index.vue')
        }
    ]
};

export default MainRoutes;
