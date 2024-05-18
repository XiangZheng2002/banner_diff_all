<script setup>
import useNewProjStore from "@/stores/NewProjStore.js";
import useUserStore from "@/stores/UserStore.js";

import Dialog from "primevue/dialog";
import MultiSelect from "primevue/multiselect";

import InputNumber from "primevue/inputnumber";
import InputText from "primevue/inputtext";

import {useToast} from "primevue/usetoast";
import Toast from "primevue/toast";
import request from "@/utils/request.js";

const projStore = useNewProjStore();

import {computed, onMounted, ref, watch} from "vue";
import router from "@/router/index.js";

const visible = computed({
    get() {
        return projStore._isDialogOpen;
    },
    set(val) {
        if (val)
            projStore.openDialog();
        else
            projStore.closeDialog();
    }
});

const selectedCate = ref([]);
const selectedStyle = ref([]);
const projHeight = ref(0);
const projWidth = ref(0);
const projTitle = ref("Untitled Project");
const currentStep = ref(false);

import {styles, categories} from "@/stores/StyleOptions.js";

const userid = useUserStore().getUserInfo.userid;

const toast = useToast();

function submitHandler() {
    function toastErr(msg) {
        toast.add(
            {
                severity: "error",
                summary: "创建失败",
                detail: "创建项目失败: " + msg,
                life: 3000
            }
        );
    }

    const body = {
        name: projTitle.value || "未命名项目",
        width: projWidth.value.toString() || "900",
        height: projHeight.value.toString() || "450",
        style: selectedStyle.value,
        type: selectedCate.value
    };

    request.post(
        '/create',
        body,
        {
            params: {
                "user_id": userid.toString()
            }
        }
    ).then((res) => {
        let data = res.data;
        projStore.closeDialog();

        router.replace("/editor/" + data.project_id.toString());
    }).catch((err) => {
        toastErr(err.message);
    });
}

function handleNextstep() {
    if (!selectedCate.value.length || !selectedStyle.value.length) {
        toast.add(
            {
                severity: "warn",
                summary: "配置未完成",
                detail: "请完整填写商品类别和风格.",
                life: 5000
            }
        );

        return;
    }

    currentStep.value = true;
}

// 动态改变颜色
const fillState = computed(() => {
    return {
        first: (selectedStyle.value.length > 0),
        second: (selectedCate.value.length > 0)
    };
});

function updateColor(state) {
    const theLine = document.querySelector("#stepline");
    if (theLine === null)
        return;

    const emptyColor = "#eeaa1e";
    const filledColor = "#ffb899";

    const c = (x) => (x ? filledColor : emptyColor);
    theLine.style.setProperty("--first-color", c(state.first));
    theLine.style.setProperty("--second-color", c(state.second));
}

watch(fillState, (state) => {
    updateColor(state);
});

// 加载时更新变量
watch(visible, (val) => {
    // Only update when dialog opens.
    if (val) {
        if (projStore._selectedCate) {
            selectedCate.value = [projStore._selectedCate];
        } else
            selectedCate.value = [];
        selectedStyle.value = [];
    }

    currentStep.value = false;
});

</script>

<template>
    <Toast/>

    <Dialog v-model:visible="visible" modal
            :pt="{
                root: 'border-none',
                mask: {
                    style: 'backdrop-filter: blur(2px)',
                }
            }">
        <template #container>
            <div class="relative">
                <button class="absolute top-[15px] right-[15px] text-xl text-c-text hover:text-c-title px-1 py-1 mx-1"
                        @click="projStore.closeDialog">
                    <i class="fa-solid fa-xmark p-0"></i>
                </button>
                <div class="mainDialog flex flex-row rounded-xl shadow-md overflow-hidden bg-[#ffffff]">
                    <div class="flex flex-row relative items-center justify-center overflow-hidden flex-shrink-0">
                        <img src="/AssetIllst.png" alt="" class="h-[360px] object-cover"/>
                    </div>

                    <!--step1 container-->
                    <div class="flex flex-col w-[400px] items-center flex-shrink-0 py-6 px-2" v-if="!currentStep">
                        <h2 class="text-2xl text-c-orange font-bold my-5">
                            个性化选择
                        </h2>

                        <div class="relative flex flex-row justify-between w-full px-6 h-[240px]">
                            <div class="flex flex-col w-1/6 items-center justify-center">
                                <div class="stepLine" id="stepline"/>
                            </div>

                            <div class="flex flex-col justify-between py-4 w-5/6">
                                <div class="w-full">
                                    <MultiSelect display="chip" :options="styles" v-model="selectedStyle"
                                                 class="w-full"
                                                 :maxSelectedLabels="4"
                                                 placeholder="请选择Banner风格"/>
                                </div>

                                <div class="w-full">
                                    <MultiSelect display="chip" :options="categories" v-model="selectedCate"
                                                 class="w-full"
                                                 :maxSelectedLabels="4"
                                                 placeholder="请选择主题商品类别"/>
                                </div>
                            </div>
                        </div>

                        <div class="flex flex-row w-full my-8 px-24">
                            <button class="bg-c-orange py-3 rounded-full text-neutral-50 flex-grow"
                                    @click="handleNextstep">
                                下一步
                            </button>
                        </div>
                    </div>

                    <!--step2 container-->
                    <div class="flex flex-col w-[400px] items-center flex-shrink-0 py-6 px-5" v-else>
                        <h2 class="text-xl text-c-orange font-bold my-5">
                            自定义项目
                        </h2>

                        <div class="w-full px-6 py-2">
                            <p class="font-bold text-c-black my-2 px-2">项目标题</p>
                            <InputText v-model="projTitle" class="w-full h-[42px]"/>
                        </div>

                        <div class="w-full px-6 py-1">
                            <p class="font-bold text-c-black my-2 px-2">
                                工程高度
                                <i class="fa-solid fa-arrows-up-down px-2"></i>
                            </p>
                            <InputNumber v-model="projHeight" class="h-[42px] w-full"
                                         :min="0"
                                         show-buttons suffix=" px"/>
                        </div>

                        <div class="w-full px-6 py-1">
                            <p class="font-bold text-c-black my-2 px-2">
                                工程宽度
                                <i class="fa-solid fa-arrows-left-right px-1"></i>
                            </p>
                            <InputNumber v-model="projWidth" class="h-[42px] w-full"
                                         :min="0"
                                         show-buttons suffix=" px"/>
                        </div>

                        <div class="flex flex-row gap-[60px] w-full px-6 py-4 my-2 justify-between">
                            <button class="py-3 rounded-full bg-white text-c-orange
                            border-c-orange border-solid border-2 flex-grow"
                                    @click="currentStep = false">
                                上一步
                            </button>

                            <button class="py-3 rounded-full bg-c-orange text-white font-bold flex-grow"
                                    @click="submitHandler">
                                开始设计
                            </button>
                        </div>

                    </div>
                </div>
            </div>
        </template>
    </Dialog>

</template>

<style scoped>
.mainDialog {
    width: min(950px, 92vw);
    justify-content: end;
}

.stepLine {
    --first-color: #eeaa1e;
    --second-color: #eeaa1e;
    --line-width: 2px;

    height: 100%;
    width: var(--line-width);

    margin: 40px 0;

    position: relative;

    background: linear-gradient(180deg in hsl,
    var(--first-color), var(--first-color) 30%,
    var(--second-color) 70%, var(--second-color));

    transition-duration: 400ms;
}

.stepLine::before, .stepLine::after {
    --line-width: 2px;
    --rad: 20px;

    display: block;
    position: absolute;
    content: "";

    height: var(--rad);
    width: var(--rad);
    border-radius: 100px;
    left: calc((var(--rad) - var(--line-width)) / (-2));

    transition-duration: 200ms;
}

.stepLine::before {
    top: -10px;

    background-color: var(--first-color);
}

.stepLine::after {
    bottom: -10px;

    background-color: var(--second-color);
}

@media screen and (max-width: 768px) {
    img {
        display: none;
    }

    .mainDialog {
        justify-content: center;
    }
}
</style>