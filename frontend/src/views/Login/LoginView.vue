<script setup>
import {ref, onMounted} from "vue";
import Title from "@/components/Utilities/Title.vue";
import Parallax from 'parallax-js';

import Button from "primevue/button";

import useUserStore from "@/stores/UserStore.js";
import router from "@/router";

const errMsg = ref("");

const isAdmin = ref(false);

const username = ref("");
const password = ref("");

const userStore = useUserStore();

onMounted(() => {
    let scene = document.getElementById("scene");
    let parallaxInstance = new Parallax(scene);
});

function lgCallback(status, msg) {
    if (status !== 0) {
        errMsg.value = msg;
        return;
    }

    if (status === 0) {
        errMsg.value = "";
        router.replace("/dashboard/recommend");
    }
}

function login() {
    if (!username.value || !password.value) {
        errMsg.value = "用户名或密码不能为空. 请输入相应字段.";
        return;
    }

    userStore.login(username.value, password.value, isAdmin.value, lgCallback);
}
</script>

<template>
    <div class="absolute overflow-hidden w-screen h-screen">
        <div id="scene" class="overflow-visible">
            <img src="/LoginBG.png" data-depth="0.1"
                 class="absolute h-[110vh] object-cover -z-10 opacity-[0.08] overflow-visible"/>
        </div>
    </div>

    <div class="flex flex-1 h-screen w-screen items-center justify-center backdrop-filter backdrop-blur-sm z-10">
        <div
            class="flex flex-row w-[882px] h-[473px] rounded-2xl bg-[#ffffff] shadow-md overflow-hidden items-center justify-center opacity-90">
            <div class="w-1/2 h-[326px]">
                <img src="/LoginIllustration.png" alt="Illustration" class="w-full h-full object-contain"/>
            </div>

            <div class="flex flex-col w-1/2 items-center justify-center">
                <h2 class="text-3xl text-center text-c-title py-6">
                    <span class="font-bold mx-2">登录</span>
                    <span class="text-4xl">
                        <Title class="px-4"/>
                    </span>
                </h2>

                <div class="flex flex-row w-2/3 justify-between gap-4">

                    <button :class="'loginButton w-1/2 rounded-xl ' +
                        (!isAdmin
                            ? 'is-active'
                            : 'is-inactive')
                        " @click="isAdmin = false">
                        普通用户
                    </button>

                    <button :class="'loginButton w-1/2 rounded-xl ' +
                        (isAdmin
                            ? 'is-active'
                            : 'is-inactive')
                        " @click="isAdmin = true">
                        管理员
                    </button>
                </div>

                <div class="flex flex-col w-2/3 justify-between gap-4 my-4">
                    <input type="text" class="cusInput px-5 h-[42px]" placeholder="用户名" v-model="username"/>
                    <input type="password" class="cusInput px-5 h-[42px]" placeholder="密码" v-model="password"/>
                </div>

                <p class="text-sm text-red-600 my-2" v-if="errMsg">
                    {{ errMsg }}
                </p>

                <Button unstyled class="loginButton is-active rounded-full w-2/3 my-2" @click="login">
                    登录
                </Button>

                <div class="my-3">
                    <p class="text-sm text-c-orange">
                        没有账号？ 立即注册
                    </p>
                </div>
            </div>
        </div>
    </div>

</template>

<style scoped>
.loginButton {
    --theme-color: #ffc071;

    padding-left: 14px;
    padding-right: 14px;

    border: 1px solid var(--theme-color);
    height: 42px;

    transition: all 0.2s;
}

.loginButton.is-active {
    background: var(--theme-color);
    color: #ffffff;
}

.loginButton.is-inactive {
    background: #ffffff;
    color: var(--theme-color);
}
</style>
