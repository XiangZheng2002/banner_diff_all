<script setup>
import Toolbar from "primevue/toolbar";

import logo from "@/components/Utilities/Logo.vue"
import Title from "@/components/Utilities/Title.vue"
import UserCard from "@/components/Utilities/UserCard.vue"

import userStore from "@/stores/UserStore.js";
const user = userStore().getUserInfo;
const isAdmin = userStore().isAdmin;

</script>

<template>
    <Toolbar class="bg-[#ffffff] shadow-lg z-50 h-full">
        <template #start>
            <router-link to="/">
                <logo class="mx-4"/>
            </router-link>

            <router-link to="/" id="BannerText">
                <h2 class="text-3xl mx-1">
                    <Title/>
                </h2>
            </router-link>
        </template>

        <template #center>
            <router-link to="/" id="BannerTextCenter">
                <h2 class="text-2xl mx-4">
                    <Title/>
                </h2>
            </router-link>
        </template>

        <template #end>
            <UserCard
                :username="user.username"
                :avatar="user.avatar"
                :is-admin="isAdmin"
            />
        </template>
    </Toolbar>
</template>

<style scoped>

.logo {
    width: var(--radius);
    height: var(--radius);

    background: #66ccff;
    border-radius: 1000px;
}

#BannerTextCenter {
    display: none;
}

@media screen and (max-width: 768px) {
    #BannerText {
        display: none;
    }

    #BannerTextCenter {
        display: block;
    }
}

</style>

