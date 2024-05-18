<script setup>
const props = defineProps([
    "title",
    "desc",
    "img"
]);

import useNewProjStore from "@/stores/NewProjStore.js";

const toggle = useNewProjStore().openDialog;
const setCate = useNewProjStore().setCate;

function handleClick() {
    let cat = props.title.slice(0, props.title.length - 2);

    setCate(cat);
    toggle();
}
</script>

<template>
    <div class="CataCard relative overflow-hidden shadow-md hover:shadow-lg">
        <div class="flex flex-row justify-between px-[20px] absolute top-[20px] items-top w-full">
            <h2 class="text-xl font-bold">{{ props.title }}</h2>
            <img :src="props.img" alt="CataCard" class="h-[54px] w-[54px] object-cover"/>
        </div>


        <div class="flex flex-row justify-between px-[20px] absolute bottom-[15px] items-center w-full">
            <p class="text-sm text-stone-500">{{ props.desc }}</p>
            <button class="bg-c-pink text-white px-3 py-2 rounded-full text-xs"
                    @click="handleClick"
            >开始设计
            </button>
        </div>
    </div>
</template>

<style scoped>

</style>