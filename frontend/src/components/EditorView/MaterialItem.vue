<script setup>
import { ref, computed, nextTick } from "vue";
import { baseURL } from "@/utils/request.js";

const imgRef = ref(); // 图片元素
const props = defineProps({
    img: {
        required: true,
        default: {},
    },
    img_name: {
        required: true,
    },
});

const handleDragStart = (e) => {
    const item = {
        name: props.img_name,
        img_id: props.img.id,
        img_url: props.img.img_url,
        height: imgRef.value.offsetHeight,
        width: imgRef.value.offsetWidth,
    };
    e.dataTransfer.setData("item", JSON.stringify(item));
};

const src = computed(() => {
    return encodeURI(baseURL + props.img.img_url);
});
</script>

<template>
    <div
        class="flex flex-col w-full h-full justify-center items-center bg-[#F6F4F0] rounded-lg"
    >
        <img
            ref="imgRef"
            draggable
            @dragstart="handleDragStart"
            @dragend="handleDragEnd"
            class="w-[80%] h-[80%] object-contain text-xs"
            :src="src"
            alt="加载失败"
        />
    </div>
</template>
