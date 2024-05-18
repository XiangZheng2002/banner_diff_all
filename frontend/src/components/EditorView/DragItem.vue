<script setup>
import MaterialItem from '@/components/EditorView/MaterialItem.vue';
const props = defineProps({
    img_name: {
        type: String,
        required: true,
        default: '图层'
    },
    img: {
        required: true,
        default: {}
    }
})
</script>

<template>
    <div class="flex flex-row w-full h-full items-center gap-2">
        <div class="h-1/2 mr-2 line"></div>
        <div class="h-full aspect-[14/13]">
            <MaterialItem :img="props.img"></MaterialItem>
        </div>
        <div class="text-xs text-[--c-grey]">[{{props.img_name}}]</div>
    </div>
</template>

<style scoped>
.line {
    border: 1.5px solid #FFE18C;
    border-radius: 1.5px;
}
</style>