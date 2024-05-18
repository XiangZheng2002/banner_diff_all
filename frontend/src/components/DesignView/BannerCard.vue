<script setup>
import BaseBanner from "@/components/DesignView/BaseBanner.vue";

const props = defineProps(["img_url", "title", "id"]);
</script>

<template>
    <div class="flex flex-col items-start mx-7 my-10 max-h-[400px]">
        <div
            class="flex rounded-lg shadow-md hover:shadow-lg duration-100 overflow-hidden justify-center items-center"
        >
            <BaseBanner :src="'/api/' + encodeURI(props.img_url)" />
        </div>
        <p class="text-c-black font-bold my-4 px-1">
            {{ props.title || "未命名Banner" }}
        </p>
    </div>
</template>
