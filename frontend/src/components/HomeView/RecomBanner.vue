<script setup>
import useNewProjStore from "@/stores/NewProjStore.js";

const projStore = useNewProjStore();

function toggle() {
    projStore.setCate(null);
    projStore.openDialog();
}
</script>

<template>
    <div
        class="flex flex-shrink-0 rounded-3xl h-[248px] overflow-hidden relative w-full"
    >
        <img
            src="/RecomBanner.png"
            class="w-full h-full object-cover"
        />

        <div
            class="bannerOverlay flex flex-col absolute top-0 left-0 w-full h-full items-center justify-center"
        >
            <h3 class="text-3xl text-center text-[#fff] drop-shadow-md">
                释放创意 无缝融合 不仅仅是拼贴
            </h3>

            <button
                class="bg-c-orange text-[#fff] text-sm rounded-full h-[35px] w-[160px] text-center justify-center my-4 shadow-sm"
                @click="toggle"
            >
                开始Banner设计
            </button>
        </div>
    </div>
</template>

<style scoped>
.bannerOverlay {
    background: rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(2px);
    transition: 0.5s;
}

.bannerOverlay:hover {
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
    transition: 0.5s;
}

</style>

