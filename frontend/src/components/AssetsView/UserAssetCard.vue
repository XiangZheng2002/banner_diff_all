<script setup>
import AssetCard from "@/components/AssetsView/AssetCard.vue";

const props = defineProps(["src", "id", "filename", "lastmod"]);
</script>

<template>
    <div class="flex flex-col justify-start py-2 mx-3">
        <AssetCard :src="props.src" :id="props.id"/>
        <p class="text-c-black font-bold mt-3 px-2">
            {{ props.filename }}
        </p>
        <p class="text-c-text px-1 text-sm">
            最后修改于 {{ props.lastmod }}
        </p>

    </div>
</template>

<style scoped>

</style>