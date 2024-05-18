<script setup>
import BaseBanner from "@/components/DesignView/BaseBanner.vue";

const props = defineProps(["src", "id"]);
</script>

<template>
    <div
        class="flex rounded-md bg-c-assets-padding m-2 overflow-hidden shadow-lg p-1 justify-center items-center shadow-md hover:shadow-lg duration-100"
    >
        <div class="flex w-[80%] h-[90%] justify-center items-center">
            <BaseBanner :src="props.src" />
        </div>
    </div>
</template>

<style scoped>
.bg-c-assets-padding {
    height: var(--h, 167px);
    width: var(--w, 250px);
}
</style>
