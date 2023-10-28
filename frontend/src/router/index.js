import {createRouter, createWebHistory} from 'vue-router'

import DashBoard from "@/views/main/DashBoard.vue";
import CoursesList from "@/views/main/CourseList.vue";
import DiscussList from "@/views/main/DiscussList.vue";
import Assistant from "@/views/main/Assistant.vue";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {
            path: '/',
            redirect: {path: '/dashboard'}
        },
        {
            path: '/dashboard',
            name: 'Dashboard',
            component: DashBoard,
            meta: {requiresAuth: true}
        },

        {
            path: '/course/:courseId',
            name: 'CourseDetail',
            component: () => import('@/views/main/CourseDetail.vue'),
        },
        {
            path: '/discuss',
            name: 'Discuss',
            component: DiscussList,
            meta: {requiresAuth: true}
        },
        {
            path: '/assistant',
            name: 'Assistant',
            component: Assistant,
        },
        {
            path: '/discuss/:postId',
            name: 'DiscussDetail',
            component: () => import('@/views/main/DiscussDetail.vue'),
        },
        {
            path: '/search',
            name: 'SearchResults',
            component: () => import('@/views/main/SearchResults.vue'),
        },
        {
            path: '/quiz/:quizId',
            name: 'Quiz',
            component: () => import('@/views/main/Quiz.vue'),
        },
        {
            path: '/profile',
            name: 'Profile',
            component: () => import('@/views/main/Profile.vue'),
        },
        {
            path: '/courses',
            name: 'Courses',
            component: CoursesList,
        },
        {
            path: '/login',
            name: 'Login',
            component: () => import('@/views/LoginPage.vue')
        },
        {
            path: '/register',
            name: 'Register',
            component: () => import('@/views/RegisterPage.vue')
        }
    ]
})

// router.beforeEach((to, from, next) => {
//   // Check if the route requires authentication
//   if (to.matched.some((route) => route.meta.requiresAuth)) {
//     // Check if the user is authenticated
//     if (window.$cookies.isKey('auth_token')) {
//       // Check if the user info is already loaded
//       if (store.state.user.user_id === null) {
//         // User info is not loaded
//         fetch(`${import.meta.env.VITE_ROOT_API}/users/me`, {
//           method: 'GET',
//           headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': window.$cookies.get('csrftoken'),
//             Authorization: window.$cookies.get('auth_token')
//           }
//         })
//           .then((response) => {
//             if (!response.ok) {
//               return response.json().then((data) => {
//                 throw new Error(data.message)
//               })
//             }
//             return response.json()
//           })
//           .then((data) => {
//             console.log(data)
//             store.commit('user/setUser', data)
//           })
//           .catch((error) => {
//             console.error(error)
//             window.$cookies.remove('auth_token')
//             next('/login')
//           })
//       }
//       next() // User is authenticated, proceed to the route
//     } else {
//       // User is not authenticated, redirect to the login page
//       next('/login')
//     }
//   } else {
//     // If the route does not require authentication, proceed as usual
//     next()
//   }
// })

export default router
