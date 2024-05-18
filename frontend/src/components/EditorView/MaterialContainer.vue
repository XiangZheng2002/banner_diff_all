<script setup>
import { ref } from 'vue'
import Button from 'primevue/button';
import MaterialList from '@/components/EditorView/MaterialList.vue'
import CustomDropdown from '@/components/Utilities/CustomDropdown.vue'

// 选择风格
const props = defineProps({
    selectedStyles: {
        required: true
    },
    selectedTypes: {
        required: true
    },
    materialList: {
        required: true
    }
})
const emit = defineEmits(['selectStyle', 'selectType', 'deleteStyle', 'deleteType'])

const showStyles = ref(false) // 是否显示listbox
const styleList = ref([
    {name: '科技风', id: 0}, 
    {name: '商务风', id: 1}, 
    {name: '炫酷风', id: 2}, 
    {name: '简约风', id: 3}, 
    {name: '清新风', id: 4}, 
    {name: '梦幻风', id: 5}, 
    {name: '中国风', id: 6}, 
    {name: '喜庆风', id: 7}, 
    {name: '可爱风', id: 8},
    {name: '华丽风', id: 9},
    {name: '温馨风', id: 10},
    {name: '动感风', id: 11}])

const handleSelectStyle = (e) => {
    emit('selectStyle', e['name'])
    showStyles.value = false
}

// 选择主体物类型
const showTypes = ref(false) // 是否显示listbox
const typeList = ref([
    {name: '运动类', id: 0}, 
    {name: '美妆类', id: 1}, 
    {name: '节日类', id: 2}, 
    {name: '服装类', id: 3}, 
    {name: '电器类', id: 4}, 
    {name: '钟表类', id: 5}, 
    {name: '文具类', id: 6}, 
    {name: '3C数码', id: 7}])

const handleSelectType = (e) => {
    emit('selectType', e['name'])
    showTypes.value = false
}

const showAll = ref(new Array(5).fill(false))

</script>

<template>
    <div class="flex flex-col h-full pr-2 flex-[1_0_auto] overflow-y-scroll gap-5">
        <!-- 风格选择 -->
        <div class="relative flex flex-row justify-between items-start z-[100]">
            <div class="flex flex-row items-start flex-wrap gap-1 shrink-1">
                <span
                 v-for="item in selectedStyles"
                 class="px-3 py-1.5 bg-[#FFB899] rounded-md text-white text-sm shrink-0"
                 @click="()=>{emit('deleteStyle', item)}">
                    {{ item }}
                </span>
            </div>
            <!-- 按钮会变小，待修 -->
            <Button
             @click="()=>{showStyles = !showStyles}"
             class="px-[3px] py-[6px] hover:bg-[#f6f4f0] shrink-0">
                <svg class="w-[1.125rem]" viewBox="0 0 20 22" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M4 7C5.65685 7 7 5.65685 7 4C7 2.34315 5.65685 1 4 1C2.34315 1 1 2.34315 1 4C1 5.65685 2.34315 7 4 7ZM4 5C4.55228 5 5 4.55228 5 4C5 3.44772 4.55228 3 4 3C3.44772 3 3 3.44772 3 4C3 4.55228 3.44772 5 4 5Z" fill="#313131"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M13.1707 12C13.5825 13.1652 14.6938 14 16 14C17.6569 14 19 12.6569 19 11C19 9.34315 17.6569 8 16 8C14.6938 8 13.5825 8.83481 13.1707 10H2C1.44772 10 1 10.4477 1 11C1 11.5523 1.44772 12 2 12H13.1707ZM16 12C16.5523 12 17 11.5523 17 11C17 10.4477 16.5523 10 16 10C15.4477 10 15 10.4477 15 11C15 11.5523 15.4477 12 16 12Z" fill="#313131"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M9 21C7.69378 21 6.58254 20.1652 6.17071 19H2C1.44772 19 1 18.5523 1 18C1 17.4477 1.44772 17 2 17H6.17071C6.58254 15.8348 7.69378 15 9 15C10.6569 15 12 16.3431 12 18C12 19.6569 10.6569 21 9 21ZM10 18C10 18.5523 9.55228 19 9 19C8.44772 19 8 18.5523 8 18C8 17.4477 8.44772 17 9 17C9.55228 17 10 17.4477 10 18Z" fill="#313131"/>
                    <path d="M9 4C9 3.44772 9.44771 3 10 3L18 3C18.5523 3 19 3.44771 19 4C19 4.55228 18.5523 5 18 5L10 5C9.44772 5 9 4.55228 9 4Z" fill="#313131"/>
                    <path d="M15 17C14.4477 17 14 17.4477 14 18C14 18.5523 14.4477 19 15 19H18C18.5523 19 19 18.5523 19 18C19 17.4477 18.5523 17 18 17H15Z" fill="#313131"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M4 7C5.65685 7 7 5.65685 7 4C7 2.34315 5.65685 1 4 1C2.34315 1 1 2.34315 1 4C1 5.65685 2.34315 7 4 7ZM4 5C4.55228 5 5 4.55228 5 4C5 3.44772 4.55228 3 4 3C3.44772 3 3 3.44772 3 4C3 4.55228 3.44772 5 4 5Z" stroke="white" stroke-linecap="round"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M13.1707 12C13.5825 13.1652 14.6938 14 16 14C17.6569 14 19 12.6569 19 11C19 9.34315 17.6569 8 16 8C14.6938 8 13.5825 8.83481 13.1707 10H2C1.44772 10 1 10.4477 1 11C1 11.5523 1.44772 12 2 12H13.1707ZM16 12C16.5523 12 17 11.5523 17 11C17 10.4477 16.5523 10 16 10C15.4477 10 15 10.4477 15 11C15 11.5523 15.4477 12 16 12Z" stroke="white" stroke-linecap="round"/>
                    <path fill-rule="evenodd" clip-rule="evenodd" d="M9 21C7.69378 21 6.58254 20.1652 6.17071 19H2C1.44772 19 1 18.5523 1 18C1 17.4477 1.44772 17 2 17H6.17071C6.58254 15.8348 7.69378 15 9 15C10.6569 15 12 16.3431 12 18C12 19.6569 10.6569 21 9 21ZM10 18C10 18.5523 9.55228 19 9 19C8.44772 19 8 18.5523 8 18C8 17.4477 8.44772 17 9 17C9.55228 17 10 17.4477 10 18Z" stroke="white" stroke-linecap="round"/>
                    <path d="M9 4C9 3.44772 9.44771 3 10 3L18 3C18.5523 3 19 3.44771 19 4C19 4.55228 18.5523 5 18 5L10 5C9.44772 5 9 4.55228 9 4Z" stroke="white" stroke-linecap="round"/>
                    <path d="M15 17C14.4477 17 14 17.4477 14 18C14 18.5523 14.4477 19 15 19H18C18.5523 19 19 18.5523 19 18C19 17.4477 18.5523 17 18 17H15Z" stroke="white" stroke-linecap="round"/>
                </svg>
            </Button>
            <div
             :style="{display: `${showStyles? 'block': 'none'}`}"
             class="absolute w-full h-[13.5rem] top-full mt-4 z-100">
                <CustomDropdown :customList="styleList" @customSelect="handleSelectStyle"></CustomDropdown>
            </div>
        </div>
        <!-- 主体物 -->
        <div class="relative flex flex-col gap-4 z-[1]">
            <!-- header -->
            <div class="flex flex-row justify-between items-center">
                <span class="font-medium">主体物</span>
                <Button class="text-[#5F5F5F] text-xs font-light" @click="()=>{showAll[0] = !showAll[0]}">{{ showAll[0] ? '收起' : '查看全部' }}</Button>
            </div>
            <div class="relative flex flex-row justify-between items-center z-[100]">
                <div class="flex flex-row items-start flex-wrap gap-1 shrink-1">
                    <span
                     v-for="item in selectedTypes"
                     class="px-3 py-1.5 bg-[#FFB899] rounded-md text-white text-sm shrink-0"
                     @click="()=>{emit('deleteType', item)}">
                        {{ item }}
                    </span>
                </div>
                <Button
                @click="()=>{showTypes = !showTypes}"
                 class="px-[3px] py-[6px] hover:bg-[#f6f4f0] shrink-0">
                    <svg class="w-[1.125rem]" viewBox="0 0 20 22" fill="none" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M4 7C5.65685 7 7 5.65685 7 4C7 2.34315 5.65685 1 4 1C2.34315 1 1 2.34315 1 4C1 5.65685 2.34315 7 4 7ZM4 5C4.55228 5 5 4.55228 5 4C5 3.44772 4.55228 3 4 3C3.44772 3 3 3.44772 3 4C3 4.55228 3.44772 5 4 5Z" fill="#313131"/>
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M13.1707 12C13.5825 13.1652 14.6938 14 16 14C17.6569 14 19 12.6569 19 11C19 9.34315 17.6569 8 16 8C14.6938 8 13.5825 8.83481 13.1707 10H2C1.44772 10 1 10.4477 1 11C1 11.5523 1.44772 12 2 12H13.1707ZM16 12C16.5523 12 17 11.5523 17 11C17 10.4477 16.5523 10 16 10C15.4477 10 15 10.4477 15 11C15 11.5523 15.4477 12 16 12Z" fill="#313131"/>
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M9 21C7.69378 21 6.58254 20.1652 6.17071 19H2C1.44772 19 1 18.5523 1 18C1 17.4477 1.44772 17 2 17H6.17071C6.58254 15.8348 7.69378 15 9 15C10.6569 15 12 16.3431 12 18C12 19.6569 10.6569 21 9 21ZM10 18C10 18.5523 9.55228 19 9 19C8.44772 19 8 18.5523 8 18C8 17.4477 8.44772 17 9 17C9.55228 17 10 17.4477 10 18Z" fill="#313131"/>
                        <path d="M9 4C9 3.44772 9.44771 3 10 3L18 3C18.5523 3 19 3.44771 19 4C19 4.55228 18.5523 5 18 5L10 5C9.44772 5 9 4.55228 9 4Z" fill="#313131"/>
                        <path d="M15 17C14.4477 17 14 17.4477 14 18C14 18.5523 14.4477 19 15 19H18C18.5523 19 19 18.5523 19 18C19 17.4477 18.5523 17 18 17H15Z" fill="#313131"/>
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M4 7C5.65685 7 7 5.65685 7 4C7 2.34315 5.65685 1 4 1C2.34315 1 1 2.34315 1 4C1 5.65685 2.34315 7 4 7ZM4 5C4.55228 5 5 4.55228 5 4C5 3.44772 4.55228 3 4 3C3.44772 3 3 3.44772 3 4C3 4.55228 3.44772 5 4 5Z" stroke="white" stroke-linecap="round"/>
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M13.1707 12C13.5825 13.1652 14.6938 14 16 14C17.6569 14 19 12.6569 19 11C19 9.34315 17.6569 8 16 8C14.6938 8 13.5825 8.83481 13.1707 10H2C1.44772 10 1 10.4477 1 11C1 11.5523 1.44772 12 2 12H13.1707ZM16 12C16.5523 12 17 11.5523 17 11C17 10.4477 16.5523 10 16 10C15.4477 10 15 10.4477 15 11C15 11.5523 15.4477 12 16 12Z" stroke="white" stroke-linecap="round"/>
                        <path fill-rule="evenodd" clip-rule="evenodd" d="M9 21C7.69378 21 6.58254 20.1652 6.17071 19H2C1.44772 19 1 18.5523 1 18C1 17.4477 1.44772 17 2 17H6.17071C6.58254 15.8348 7.69378 15 9 15C10.6569 15 12 16.3431 12 18C12 19.6569 10.6569 21 9 21ZM10 18C10 18.5523 9.55228 19 9 19C8.44772 19 8 18.5523 8 18C8 17.4477 8.44772 17 9 17C9.55228 17 10 17.4477 10 18Z" stroke="white" stroke-linecap="round"/>
                        <path d="M9 4C9 3.44772 9.44771 3 10 3L18 3C18.5523 3 19 3.44771 19 4C19 4.55228 18.5523 5 18 5L10 5C9.44772 5 9 4.55228 9 4Z" stroke="white" stroke-linecap="round"/>
                        <path d="M15 17C14.4477 17 14 17.4477 14 18C14 18.5523 14.4477 19 15 19H18C18.5523 19 19 18.5523 19 18C19 17.4477 18.5523 17 18 17H15Z" stroke="white" stroke-linecap="round"/>
                    </svg>
                </Button>
                <div
                 :style="{display: `${showTypes? 'block': 'none'}`}"
                 class="absolute w-full h-[13.5rem] top-full mt-4 z-100">
                    <CustomDropdown :customList="typeList" @customSelect="handleSelectType"></CustomDropdown>
                </div>
            </div>
            <!-- 素材列表 -->
            <div class="relative flex flex-row pr-4 gap-2.5 z-0">
                <MaterialList img_name="主体物" :MaterialList="props.materialList['主体物']" :showAll="showAll[0]"></MaterialList>
            </div>
        </div>
        <!-- 装饰物 -->
        <div class="relative flex flex-col gap-4 z-0">
            <div class="flex flex-row justify-between items-center">
                <span class="font-medium">装饰物</span>
                <Button class="text-[#5F5F5F] text-xs font-light" @click="()=>{showAll[1] = !showAll[1]}">{{ showAll[1] ? '收起' : '查看全部' }}</Button>
            </div>
            <!-- 素材列表 -->
            <div class="flex flex-row pr-4 gap-2.5">
                <MaterialList img_name="主体物" :MaterialList="props.materialList['装饰物']" :showAll="showAll[1]"></MaterialList>
            </div>
        </div>
        <!-- 标语 -->
        <div class="flex flex-col gap-4">
            <div class="flex flex-row justify-between items-center">
                <span class="font-medium">标语</span>
                <Button class="text-[#5F5F5F] text-xs font-light" @click="()=>{showAll[2] = !showAll[2]}">{{ showAll[2] ? '收起' : '查看全部' }}</Button>
            </div>
            <!-- 素材列表 -->
            <div class="flex flex-row pr-4 gap-2.5">
                <MaterialList img_name="主体物" :MaterialList="props.materialList['标语']" :showAll="showAll[2]"></MaterialList>
            </div>
        </div>
        <!-- LOGO -->
        <div class="flex flex-col gap-4">
            <div class="flex flex-row justify-between items-center">
                <span class="font-medium">LOGO</span>
                <Button class="text-[#5F5F5F] text-xs font-light" @click="()=>{showAll[3] = !showAll[3]}">{{ showAll[3] ? '收起' : '查看全部' }}</Button>
            </div>
            <!-- 素材列表 -->
            <div class="flex flex-row pr-4 gap-2.5">
                <MaterialList img_name="主体物" :MaterialList="props.materialList['LOGO']" :showAll="showAll[3]"></MaterialList>
            </div>
        </div>
        <!-- 背景 -->
        <div class="flex flex-col gap-4">
            <div class="flex flex-row justify-between items-center">
                <span class="font-medium">背景</span>
                <Button class="text-[#5F5F5F] text-xs font-light" @click="()=>{showAll[4] = !showAll[4]}">{{ showAll[4] ? '收起' : '查看全部' }}</Button>
            </div>
            <!-- 素材列表 -->
            <div class="flex flex-row pr-4 gap-2.5">
                <MaterialList img_name="主体物" :MaterialList="props.materialList['背景']" :showAll="showAll[4]"></MaterialList>
            </div>
        </div>
    </div>
</template>

<style scoped>
:deep(.p-button:focus) {
    box-shadow: none;
}
</style>