<script setup>
import {RouterView} from 'vue-router';
import useUserStore from "@/stores/UserStore.js";
import {onMounted} from "vue";

import Toast from "primevue/toast";
import {useToast} from "primevue/usetoast";
import {setToast} from "@/utils/request.js";

onMounted(() => {
    let state = localStorage.getItem("userStore");
    if (state) {
        let userStore = useUserStore();
        userStore.$patch(JSON.parse(state));
    }

    useUserStore().$subscribe((mutation, state) => {
        localStorage.setItem('userStore', JSON.stringify(state))
    });

    setToast(useToast());
});
</script>

<template>
    <Toast/>
    <RouterView/>
</template>

