<script setup>
import { ref, onMounted, computed, watch } from "vue";
import Dropdown from "primevue/dropdown";

import customTabmenu from "@/components/Utilities/CustomMenuTabs.vue";
import DesignCard from "@/components/DesignView/DesignCard.vue";
import BannerCard from "@/components/DesignView/BannerCard.vue";

import useNewProjStore from "@/stores/NewProjStore.js";
import useUserStore from "@/stores/UserStore.js";

const userStore = useUserStore();
const projStore = useNewProjStore();
import request from "@/utils/request.js";

const items = ref(["设计草稿", "生成Banner"]);

const options = ["编辑时间正序", "编辑时间倒序"];
const sortMethod = ref("编辑时间倒序");

const currentTabIndex = ref(0);

const totalPages = ref(1);
const currentPage = ref(1);

const projects = ref([]);
const banners = ref([]);

function getProjects() {
    request
        .get("/projects", {
            params: {
                user_id: userStore.getUserInfo.userid,
            },
        })
        .then((res) => {
            projects.value = res.data.projects;
        });
}

function getBanners() {
    request
        .get("/output", {
            params: {
                user_id: userStore.getUserInfo.userid,
            },
        })
        .then((res) => {
            banners.value = res.data.images;
        });
}

function toggle() {
    projStore.setCate(null);
    projStore.openDialog();
}

onMounted(() => {
    if (!currentTabIndex.value) getProjects();
    else getBanners();
});

watch(currentTabIndex, (val) => {
    if (!val) getProjects();
    else getBanners();
});
</script>

<template>
    <div class="flex flex-col w-full items-between pt-5 px-3">
        <div class="flex flex-row w-full justify-between">
            <h2 class="text-3xl font-bold">我的设计</h2>

            <button
                class="bg-c-orange text-neutral-50 px-8 py-1 rounded-full"
                @click="toggle"
            >
                新建Banner设计
            </button>
        </div>

        <div class="flex flex-row w-full justify-between">
            <custom-tabmenu
                :items="items"
                :active-index="0"
                @update="
                    (i) => {
                        currentTabIndex = i;
                    }
                "
                class="py-5"
            />

            <div class="flex items-center">
                <Dropdown
                    :options="options"
                    v-model="sortMethod"
                    placeholder="排序方式"
                ></Dropdown>
            </div>
        </div>

        <div v-if="currentTabIndex === 0">
            <div class="cardContainer" v-if="projects.length">
                <DesignCard
                    v-for="item in projects"
                    :id="item.id"
                    :title="item.name"
                    :img_url="
                        item.thumbnail_url
                            ? encodeURI(item.thumbnail_url)
                            : '/backend/static/thumbnail/default.png'
                    "
                />
            </div>
            <div
                v-else
                class="flex flex-col w-full justify-center items-center"
            >
                <p class="text-2xl text-c-text text-center p-6">暂无项目</p>
                <button
                    class="bg-c-orange text-neutral-50 px-8 py-2 m-4 rounded-full"
                    @click="toggle"
                >
                    新建一个!
                </button>
            </div>
        </div>

        <div v-if="currentTabIndex === 1">
            <div class="cardContainer" v-if="banners.length">
                <router-link
                    v-for="item in banners"
                    :to="
                        '/result/' +
                        item.project_id +
                        '?redirect=' +
                        encodeURIComponent('/dashboard/design')
                    "
                >
                    <BannerCard
                        :id="item.id"
                        :img_url="item.img_url"
                        :title="item.name"
                    />
                </router-link>
            </div>
            <div v-else class="w-full justify-center items-center">
                <p class="text-2xl text-c-text text-center p-6">
                    暂无已生成Banner
                </p>
            </div>
        </div>
    </div>
</template>

<style scoped>
.cardContainer {
    width: 100%;
    justify-content: center;

    display: grid;
    grid-template-columns: repeat(auto-fill, calc(250px + 2rem));
    grid-auto-rows: minmax(100px, auto);
}
</style>
