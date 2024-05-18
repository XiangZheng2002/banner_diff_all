<script setup>
import Menu from "primevue/menu";

const items = [
    {
        label: "为你推荐",
        icon: "fa-regular fa-face-smile",
        route: "/dashboard/recommend"
    },
    {
        label: "我的设计",
        icon: "fa-regular fa-pen-to-square",
        route: "/dashboard/design"
    },
    {
        label: "素材管理",
        icon: "fa-regular fa-image",
        route: "/dashboard/assets"
    },
]

const footerItems = [
    {
        label: "回收箱",
        icon: "fa-solid fa-trash",
        route: "/dashboard/trash"
    }
]

</script>

<template>

    <div class="flex flex-row h-full px-1 justify-between bg-white">
        <div class="flex flex-col w-full justify-between px-3">
            <Menu :model="items">
                <template #item="{ item }">
                    <router-link :to="item.route">
                        <div v-if=" $route.path !== item.route"
                             class="flex items-center px-5 py-4 my-4 rounded-2xl"
                        >
                            <span :class="item.icon"/>
                            <span class="ml-2 text-color">{{ item.label }}</span>
                        </div>
                        <div v-else
                             class="flex items-center px-5 py-4 my-4 bg-c-selected rounded-2xl"
                        >
                            <span :class="item.icon + ' text-c-selected-text'"/>
                            <span class="ml-2 text-c-selected-text">{{ item.label }}</span>
                        </div>
                    </router-link>
                </template>
            </Menu>

            <div>
                <div class="custom-divider is-horizontal no-margin"/>
                <Menu :model="footerItems" >
                    <template #item="{ item }">
                        <router-link :to="item.route">
                            <div v-if=" $route.path !== item.route"
                                 class="flex items-center px-5 py-4 my-4"
                            >
                                <span :class="item.icon"/>
                                <span class="ml-2 text-color">{{ item.label }}</span>
                            </div>
                            <div v-else
                                 class="flex items-center px-5 py-4 my-4 bg-c-selected rounded-2xl"
                            >
                                <span :class="item.icon + ' text-c-selected-text'"/>
                                <span class="ml-2 text-c-selected-text">{{ item.label }}</span>
                            </div>
                        </router-link>
                    </template>
                </Menu>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>