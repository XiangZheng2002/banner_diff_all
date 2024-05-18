<script setup>
import {ref} from "vue";

const props = defineProps(["items", "activeIndex"])
const emit = defineEmits(["update"]);
const activeIndex = ref(props.activeIndex);

function changeIndex(i) {
    activeIndex.value = i;
    emit("update", i);
}

</script>

<template>
    <div class="flex flex-row">
        <button
            v-for="(item, i) in props.items"
            @click="changeIndex(i)"
            :class="'tabItem ' + (i === activeIndex ? 'is-selected' : '' )"
        >
            {{ item }}
        </button>
    </div>

</template>

<style scoped>

.tabItem {
    color: var(--c-grey);

    position: relative;
    padding: 10px 20px;
    margin: 0px 20px;
}

.tabItem.is-selected {
    color: var(--c-black);
    font-weight: bold;
}

@keyframes SlideIn {
    0% {
        height: 0;
        opacity: 0;
    }

    100% {
        height: 4px;
        opacity: 1;
    }
}

.tabItem.is-selected::after {
    content: "";

    animation: SlideIn forwards 100ms ease-out;

    position: absolute;
    bottom: -5px;
    left: 0;

    width: 100%;
    height: 4px;

    background-color: #ffe18c;

    border-radius: 20px;
    overflow: hidden;
}

</style>