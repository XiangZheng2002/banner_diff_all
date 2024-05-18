<script setup>
import BaseBanner from "@/components/DesignView/BaseBanner.vue";

const props = defineProps(["title", "img_url", "id"]);
</script>

<template>
    <!-- router link to /editor/id -->
    <div class="flex flex-col items-start px-2 py-2">
        <router-link :to="'/editor/' + props.id.toString()">
            <div
                class="flex rounded-md bg-c-assets-padding h-[167px] w-[250px] overflow-hidden shadow-md hover:shadow-lg duration-100 p-1"
            >
                <BaseBanner :src="'/api/' + encodeURI(props.img_url)" />
            </div>
            <p class="text-c-black font-bold my-4 px-1">
                {{ props.title || "无标题" }}
            </p>
        </router-link>
    </div>
</template>

<style scoped></style>
