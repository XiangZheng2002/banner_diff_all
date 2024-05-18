<script setup>
import { ref, defineEmits, watch } from 'vue'
import Listbox from 'primevue/listbox'

const emit = defineEmits(['customSelect'])
const props = defineProps({
    customList: {
        type: Array,
        required: true
    }
})
const selectedCustomList = ref()
watch(selectedCustomList, (e)=>{
    emit('customSelect', e)
})

</script>

<template>
    <Listbox 
     v-model="selectedCustomList"
     :options="props.customList" 
     optionLabel="name" 
     class="listBox w-full py-2 border border-[#FFB899] rounded-md bg-white/1" 
     listStyle="max-height:250px; padding-left: 1rem; padding-right: 0.5rem;">
        <template #option="item">
            <div class="text-xs">{{ item.option.name }}</div>
        </template>
    </Listbox>
</template>

<style scoped>
:deep(.p-listbox-item) {
    width: 100%;
    padding: 0.5rem 1rem;
    margin: 0.25rem 0;
    border-radius: 0.75rem;
    background-color: white;
    color: #313131;
}

:deep(.p-focus),
:deep(.p-highlight) {
    background-color: #FFB899;
}
</style>