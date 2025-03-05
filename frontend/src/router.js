// src/router.js
import Vue from 'vue';
import Router from 'vue-router';
import UserLogin from './components/UserLogin.vue';
import FrpManagement from './components/FrpManager.vue';

Vue.use(Router);

const router = new Router({
    mode: 'history',
    routes: [
        {
            path: '/',
            name: 'Login',
            component: UserLogin
        },
        {
            path: '/frp-management',
            name: 'FrpManagement',
            component: FrpManagement,
            meta: {requiresAuth: true}
        }
    ]
});


router.beforeEach((to, from, next) => {
    const loggedIn = localStorage.getItem('token');

    if (to.matched.some(record => record.meta.requiresAuth) && !loggedIn) {
        next('/');
    } else {
        next();
    }
});

export default router;
