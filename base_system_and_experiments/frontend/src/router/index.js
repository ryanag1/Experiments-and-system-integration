import Vue from 'vue'
import VueRouter from 'vue-router'
Vue.use(VueRouter)

const routes = [
    {
        path: "/",
        redirect: "login",
        meta: { isPublic: true }
    },
    {
        path: "/console",
        //redirect: "condole/dashboard",
        component: () => import("@/views/Console"),
        //name: "Console",
        //props: true
        children: [
          {
            path: "dashboard",
            component: () => import("@/components/pages/Console/Dashboard/index.vue"),
          },
          {
            path: "communication",
            component: () => import("@/components/pages/Console/Communication/index.vue"),
          },
          {
            path: "template",
            component: () => import("@/components/pages/Console/Templates/index.vue"),
          },
          {
            path: "scheme",
            component: () => import("@/components/pages/Console/Scheme/index.vue"),
          },
          {
            path: "calender",
            component: () => import("@/components/pages/Console/Calender/index.vue"),
          },
          {
            path: "presentation",
            component: () => import("@/components/pages/Console/Presentation/index.vue"),
          },
          {
            path: "canvas",
            component: () => import("@/components/pages/Console/Canvas/index.vue"),
          },
          {
            path: "scrape",
            component: () => import("@/components/pages/Console/Scrape/index.vue"),
          },
          {
            path: "unity",
            component: () => import("@/components/pages/Console/Unity/index.vue"),
          }
        ]
    },
    {
        path: "/login",
        //redirect: "condole/dashboard",
        component: () => import("@/views/Login"),
        meta: { isPublic: true }
    },
]

const router = new VueRouter({
    mode: "history",
    base: process.env.BASE_URL,
    //base: "/vue-dev/",
    routes 
})

/**router.beforeEach((to, from, next) => {
    if (to.matched.some(record => !record.meta.isPublic) && !sessionStorage.getItem("Auth")) {
      next({ path: '/', query: { redirect: to.fullPath }});
    } else {
      next();
    }
  });**/

export default router
