<script setup>
import {ref} from "vue";
import cusTabs from "@/components/Utilities/CustomMenuTabs.vue"
import Dropdown from "primevue/dropdown";

const items = ref([
    "设计草稿", "生成Banner"
]);

const options = ["编辑时间正序", "编辑时间倒序"];
const sortMethod = ref("");

const currentIndex = ref(0);

</script>

<template>
    <div class="flex flex-col w-full items-between pt-5 px-3">
        <h2 class="text-3xl font-bold">
            回收箱
        </h2>

        <div class="flex flex-row w-full justify-between">
            <cus-tabs :items="items" :active-index="0" @update="(i) => {currentIndex = i}" class="py-5"/>

            <div class="flex items-center">
                <Dropdown :options="options" v-model="sortMethod" placeholder="排序方式"></Dropdown>
            </div>
        </div>
    </div>

</template>

<style scoped>
</style>