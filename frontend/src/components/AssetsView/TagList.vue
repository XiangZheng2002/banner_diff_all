<script setup>
import AssetCard from "@/components/AssetsView/AssetCard.vue";

const props = defineProps(["tagName", "items"]);
</script>

<template>
    <div class="flex flex-col justify-between my-4">
        <div class="flex flex-row justify-between items-center px-2 py-2">
            <h2 class="text-xl font-bold">{{ props.tagName }}</h2>
            <button class="text-c-text text-sm font-bold">查看全部</button>
        </div>

        <div class="flex flex-row flex-wrap justify-start items-center my-1">
            <div class="flex my-2 mx-1" v-for="item in props.items">
                <AssetCard :src="item.src" :id="item.id" :key="item.id"/>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>