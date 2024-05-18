<script setup>
import {RouterView} from "vue-router";
import NewProjDialog from "@/components/Utilities/NewProjDialog.vue";
import Sidebar from "primevue/sidebar";

import Banner from "@/components/Banner.vue";
import DashboardMenu from "@/components/DashboardMenu.vue";
import {ref} from "vue";

const sidebarVisible = ref(false);

function openDialog() {
    sidebarVisible.value = true;
}

</script>

<template>
    <main class="flex h-screen w-screen">
        <div class="flex flex-col">
            <div class="flex flex-col fixed w-screen h-[100px] z-[999]" id="BannerContainer">
                <Banner/>
            </div>

            <div class="mt-[100px] w-screen overflow-x-hidden">
                <div class="menuWrapper flex w-[240px] fixed top-[100px]">
                    <DashboardMenu/>
                </div>

                <div class="mainContainer p-3 mr-0 overflow-hidden">
                    <RouterView/>
                </div>
            </div>
        </div>
    </main>

    <NewProjDialog/>

    <button
        class="triggerButton fixed bottom-5 left-5 bg-c-light-orange text-[#fff] text-sm rounded-full h-[50px] w-[50px] text-center justify-center m-4 shadow-md"
        @click="openDialog">
        <i class="fas fa-bars"/>
    </button>

    <Sidebar v-model:visible="sidebarVisible" class="Sidebar"
             :pt="{
                content: {
                    style: 'padding: 0;'
                }
             }">
        <DashboardMenu/>
    </Sidebar>
</template>

<style scoped>
.menuWrapper {
    height: calc(100vh - 100px);
    margin: 0;

    border-right: 1px solid var(--c-divider);
}

.mainContainer {
    margin-left: 250px;
}

.triggerButton {
    display: none;
}

#BannerContainer {
    border-bottom: 1px solid var(--c-divider);
}

@media screen and (max-width: 768px) {
    .menuWrapper {
        display: none;
    }

    .mainContainer {
        margin-left: 0;
        padding: 20px;
    }

    .triggerButton {
        display: block;
    }
}

</style>