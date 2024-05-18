<script setup>
import {ref, computed} from "vue";

const props = defineProps({
    icon: String,
    isLeft: Boolean,
    isRight: Boolean
});
const icon = ref(props.icon);

const computedClass = computed(() => {
    let res = "pageButton text-center p-1 ";
    if (props.isLeft) {
        res += "isLeft";
        return res;
    }
    if (props.isRight) {
        res += "isRight"
        return res;
    }
});
</script>

<template>
    <div :class="computedClass">
        <i :class="icon"/>
    </div>
</template>

<style scoped>
.pageButton {
    --radius: 64px;

    height: var(--radius);
    width: var(--radius);
    border-radius: 999px;

    font-size: calc(0.45 * var(--radius));

    cursor: pointer;

    position: absolute;
    top: calc((100vh - 100px + var(--radius)) / 2);

    @apply bg-c-assets-padding shadow-md;
    @apply flex flex-col justify-center items-center;
    @apply text-c-text;

    transition-duration: 200ms;
}

.pageButton:hover {
    --radius: 70px;
    @apply shadow-lg;
}

.pageButton.isLeft {
    left: 32px;
}

.pageButton.isRight {
    right: 32px;
}
</style>