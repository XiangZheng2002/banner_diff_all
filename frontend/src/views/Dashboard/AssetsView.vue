<script setup>
import { computed, ref, watch } from "vue";
import cusTabs from "@/components/Utilities/CustomMenuTabs.vue";

import TagList from "@/components/AssetsView/TagList.vue";
import UserAssetCard from "@/components/AssetsView/UserAssetCard.vue";
import AssetUploadDialog from "@/components/AssetsView/AssetUploadDialog.vue";

import useAssetUploadVisible from "@/stores/AssetUploadStore.js";
import useUserStore from "@/stores/UserStore.js";
import request from "@/utils/request.js";

const toggle = useAssetUploadVisible().open;
const userStore = useUserStore();

const items = ref(["素材库", "本地上传图片"]);

const userAssets = ref([]);
const adminAssets = ref([]);

const tagList = ref([]);

async function queryAssetWithTag(tag, use_admin) {
    let params = {
        user_id: userStore._userid,
        use_admin: use_admin,
    };

    if (tag.length > 0) params["type"] = tag;

    const res = await request.get("/get_files", {
        params: params,
    });
    return res.data.images;
}

async function getRecomAssets() {
    let imgList = await queryAssetWithTag([], 1);
    adminAssets.value = [];

    imgList.forEach((e) => {
        adminAssets.value.push({
            id: e.id,
            src: e.img_url,
            name: e.name,
            last_mod: e.last_mod,
            //src: encodeURI(e.img_url),
        });
    });
}

async function getUserAssets() {
    let imgList = await queryAssetWithTag([], 0);
    userAssets.value = [];

    imgList.forEach((e) => {
        userAssets.value.push({
            id: e.id,
            src: e.img_url,
            name: e.name,
            last_mod: e.last_mod,
            //src: encodeURI(e.img_url),
        });
    });
}

const currentTabIndex = ref(0);
getRecomAssets();
watch(currentTabIndex, (val) => {
    if (val === 1) getUserAssets();
    else getRecomAssets();
});
</script>

<template>
    <div class="flex flex-col w-full items-between pt-5 px-3">
        <div class="flex flex-row w-full justify-between">
            <h2 class="text-3xl font-bold">素材管理</h2>

            <button
                class="bg-c-orange text-neutral-50 px-8 py-1 rounded-full"
                @click="toggle"
            >
                上传图片
            </button>
        </div>
    </div>

    <cus-tabs
        :items="items"
        :active-index="0"
        @update="
            (i) => {
                currentTabIndex = i;
            }
        "
        class="py-5"
    />

    <div
        class="flex flex-col w-full items-between pt-5 px-1"
        v-if="currentTabIndex === 0"
    >
        <TagList
            v-for="tag in tagList"
            :tagName="tag.tagName"
            :items="tag.items"
            :key="tag.tagName"
        />
    </div>

    <div class="cardContainer" v-if="currentTabIndex === 1">
        <UserAssetCard
            v-for="c in userAssets"
            :src="'/api/' + encodeURI(c.src)"
            :id="c.id"
            :filename="c.name"
            :lastmod="c.last_mod"
        />
    </div>
    <div class="cardContainer" v-else="currentTabIndex === 0">
        <UserAssetCard
            v-for="c in adminAssets"
            :src="'/api/' + encodeURI(c.src)"
            :id="c.id"
            :filename="c.name"
            :lastmod="c.last_mod"
        />
    </div>

    <AssetUploadDialog />
</template>

<style scoped>
.cardContainer {
    width: 100%;
    justify-content: center;

    display: grid;
    grid-template-columns: repeat(auto-fill, calc(250px + 1.2rem));
    grid-auto-rows: minmax(100px, auto);
}
</style>
