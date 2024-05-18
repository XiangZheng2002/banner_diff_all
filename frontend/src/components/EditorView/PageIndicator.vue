<script setup>
import {computed} from "vue";

const props = defineProps({
    total: Number
});

const current = defineModel();

const range = computed(() => {
    let result = [];
    for (let i = 0; i < props.total; i++) {
        result.push(i === (current.value - 1));
    }

    return result;
});

</script>

<template>
    <div class="indicatorContainer flex flex-row items-center h-[40px] p-[10px]">
        <div v-for="(i, index) in range"
             :class="'circle' + (i ? ' is-active' : '')"
             @click="current = index + 1"/>
    </div>
</template>

<style scoped>
.indicatorContainer {
    --margin: 5px;
}

.indicatorContainer:hover {
    --margin: 7px;
}

.circle {
    --radius: 10px;

    height: var(--radius);
    width: var(--radius);
    margin: var(--margin);
    @apply rounded-full bg-c-selected;

    transition-duration: 200ms;
    cursor: pointer;
}

.circle.is-active {
    @apply bg-c-orange;
}
</style>