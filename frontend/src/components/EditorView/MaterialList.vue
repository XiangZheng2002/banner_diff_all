<script setup>
import { computed } from "vue";
import MaterialItem from "@/components/EditorView/MaterialItem.vue";

const props = defineProps({
    MaterialList: {
        required: true,
        default: [],
    },
    img_name: {
        required: true,
        default: "图层",
    },
    showAll: {
        required: false,
        default: false,
    },
});

const showMaterials = computed(() => {
    if (props.showAll) return props.MaterialList;
    else return props.MaterialList.slice(0, 3);
});
</script>

<template>
    <div
        class="w-[30%] aspect-[14/13] mt-1"
        v-for="(item, index) of showMaterials"
        :key="index"
    >
        <material-item :img_name="props.img_name" :img="item"></material-item>
    </div>
</template>
