import { createRouter, createWebHistory } from "vue-router";

const HomeView = () => import("@/views/Dashboard/HomeView.vue");
const LoginView = () => import("@/views/Login/LoginView.vue");
const EditorView = () => import("@/views/Editor/EditorView.vue");

const Recommend = () => import("@/views/Dashboard/RecomView.vue");
const AssetsView = () => import("@/views/Dashboard/AssetsView.vue");
const DesignView = () => import("@/views/Dashboard/DesignView.vue");
const TrashView = () => import("@/views/Dashboard/TrashView.vue");
const ResultView = () => import("@/views/Editor/ResultView.vue");

import useUserStore from "@/stores/UserStore";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),

    routes: [
        {
            path: "/",
            redirect: "/dashboard/recommend", // to be mod
        },
        {
            path: "/login",
            name: "login",
            component: LoginView,
        },
        {
            path: "/dashboard",
            name: "home",
            component: HomeView,
            children: [
                {
                    path: "",
                    name: "default",
                    redirect: "/dashboard/recommend",
                },
                {
                    path: "recommend",
                    name: "recommend",
                    component: Recommend,
                },
                {
                    path: "assets",
                    name: "assets",
                    component: AssetsView,
                },
                {
                    path: "design",
                    name: "design",
                    component: DesignView,
                },
                {
                    path: "trash",
                    name: "trash",
                    component: TrashView,
                },
            ],
        },
        {
            path: "/editor/:id",
            component: EditorView,
        },
        {
            path: "/result/:id",
            component: ResultView,
        },
    ],
});

router.beforeEach((to, from, next) => {
    const userStore = useUserStore();

    function isAuthed() {
        return userStore.isAuthed;
    }

    if (isAuthed()) {
        next();
    } else {
        if (to.name === "login") {
            next();
        } else {
            next({ name: "login" });
        }
    }
});

export default router;
