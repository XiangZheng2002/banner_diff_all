<script setup>
import {onMounted} from "vue";

const props = defineProps(["src"]);

onMounted(() => {

});
</script>

<template>
    <img v-if="props.src" class="object-contain max-h-full max-w-full" :src="props.src"/>
    <div v-else class="w-full h-full flex justify-center items-center">
        <div
            class="flex self-center border-dashed border-2 rounded-lg bg-transparent justify-center items-center w-[100px] h-[100px]">
            <p class="text-c-title text-xl">
                暂无预览
            </p>
        </div>
    </div>
</template>

<style scoped>
</style>
