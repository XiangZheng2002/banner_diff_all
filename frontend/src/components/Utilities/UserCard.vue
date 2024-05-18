<script setup>
import Menu from "primevue/menu";
import { computed, ref } from "vue";

import useUserStore from "@/stores/UserStore.js";
import router from "@/router";

const profileMenu = ref(null);

const items = [
    {
        label: "退出登录",
        icon: "fas fa-sign-out-alt",
    },
];

const toggle = (event) => {
    profileMenu.value.toggle(event);
};

const props = defineProps(["username", "avatar", "isAdmin"]);

const username = computed(() => props.username || "User");
const avatar = computed(() => "/api/" + encodeURI(props.avatar) || "");
const adminState = computed(() => props.isAdmin || false);
const defaultLetter = computed(() => username.value[0].toUpperCase());

function logoutcb(status, msg) {
    if (status !== 0) {
        console.log(msg);
        return;
    }

    router.replace("/login");
    console.log("Logged out successfully.");
}

function logout() {
    useUserStore().logout(logoutcb);
}
</script>

<template>
    <button
        v-if="!props.avatar"
        class="avatar user-default hover:shadow-lg hover:duration-200 duration-200 shadow-sm"
        @click="toggle"
    >
        {{ defaultLetter }}
    </button>
    <button v-else class="avatar" @click="toggle">
        <img :src="avatar" class="avatar object-cover" />
    </button>

    <Menu
        class="w-[260px]"
        ref="profileMenu"
        id="profile_menu"
        :model="items"
        :popup="true"
    >
        <template
            #start="{
                _username = username,
                _avatar = avatar,
                _defaultLetter = defaultLetter,
                _adminState = adminState,
            }"
        >
            <div class="flex flex-row w-full p-4">
                <div v-if="!avatar" class="avatar user-default" @click="toggle">
                    {{ _defaultLetter }}
                </div>
                <div v-else class="avatar">
                    <img :src="avatar" class="avatar object-cover" />
                </div>

                <div class="flex flex-col px-3 items-start">
                    <h3 class="text-c-title font-bold text-lg">
                        {{ _username }}
                    </h3>
                    <p class="text-sm text-c-text">
                        {{ _adminState ? "管理员" : "普通用户" }}
                    </p>
                </div>
            </div>
            <div class="custom-divider is-horizontal no-margin my-2" />
        </template>

        <template #item="{ item }">
            <div class="p-3" @click="logout">
                <p class="px-3">
                    <span class="mx-1">
                        <i :class="item.icon"></i>
                    </span>
                    {{ item.label }}
                </p>
            </div>
        </template>
    </Menu>
</template>

<style scoped>
.avatar.user-default {
    background: linear-gradient(
        211.18deg,
        #fbd3c6 10.96%,
        #f2f8f2 51.39%,
        #c4fdf5 90.16%
    );
    text-shadow: 1px 2px 3px rgba(0, 0, 0, 0.05);
}
</style>
