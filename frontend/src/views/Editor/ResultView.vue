<script setup>
/**
 * @param id 由url传入, 代表素材的ID. 未来可能需要反查对应项目标题
 * @param redirect 表示来源, 毕竟这个页面可能从多个页面点开. 从url参数传入 ?redirect=/some/link/before
 */

import { ref, onMounted, computed } from "vue";

import Toolbar from "primevue/toolbar";
import Checkbox from "primevue/checkbox";

import Logo from "@/components/Utilities/Logo.vue";
import Title from "@/components/Utilities/Title.vue";

import PageControlFloat from "@/components/EditorView/PageControlFloat.vue";
import PageIndicator from "@/components/EditorView/PageIndicator.vue";
import request from "@/utils/request.js";
import useUserStore from "@/stores/UserStore.js";
import { useRoute } from "vue-router";
import router from "@/router/index.js";

const theCheckbox = ref(false);
const currentPage = ref(1);
const title = ref("");
const totalPage = ref(0);

const route = useRoute();
const props = defineProps({
    id: Number,
});
let redirect = "/dashboard/design";
const valid = ref(false);
const userStore = useUserStore();

function increase() {
    currentPage.value = Math.min(currentPage.value + 1, totalPage.value);
}

function decrease() {
    currentPage.value = Math.max(1, currentPage.value - 1);
}

const tooltipConfig = {
    value: "选择当前Banner是否留用",
    showDelay: 500,
    hideDelay: 300,
};

const bannerList = ref([]);
const renderFlag = ref(false);

const currentSource = computed(() => {
    console.log(bannerList.value[currentPage.value - 1]);
    if (bannerList.value[currentPage.value - 1]) {
        console.log(bannerList.value[currentPage.value - 1].src);
        return "/api/" + bannerList.value[currentPage.value - 1].src;
    } else return null;
});

onMounted(async () => {
    let outputList = [];
    await request
        .get("/output", {
            params: {
                user_id: userStore._userid,
            },
        })
        .then((res) => {
            outputList = res.data.images;
        });

    if (!outputList) {
        console.log("Fetch failed");
        renderFlag.value = false;
        return;
    }

    valid.value = false;
    let currentProject = -1;
    for (let i = 0; i < outputList.length; i++) {
        console.log(route.params.id);
        if (outputList[i].project_id == route.params.id) {
            valid.value = true;
            currentProject = outputList[i].project_id;

            break;
        }
    }

    if (!valid.value) {
        // await router.replace("/dashboard/design");
        return;
    }

    request
        .get("/project", {
            params: {
                user_id: userStore._userid,
                project_id: currentProject,
            },
        })
        .then((res) => {
            title.value = res.data.project.name;
        });

    bannerList.value = [];
    for (let i = 0; i < outputList.length; i++) {
        let banner = outputList[i];
        if (banner.project_id === currentProject) {
            bannerList.value.push({
                id: banner.id,
                src: banner.img_url,
            });
        }

        if (banner.id === route.params.id) currentPage.value = i + 1;
    }

    totalPage.value = bannerList.value.length;

    console.log(bannerList.value);
    console.log(currentPage.value);
    console.log("CUR" + currentSource.value);
    renderFlag.value = true;
});
</script>

<template>
    <!--头部-->
    <div class="resultBanner fixed h-[100px] w-full top-0 left-0 z-[999]">
        <div
            class="absolute top-0 left-0 flex flex-row px-5 items-center justify-center w-full h-full"
        >
            <p class="text-c-black">
                {{ title }}
            </p>
        </div>

        <div
            class="absolute top-0 left-0 flex flex-row px-5 items-center justify-between w-full h-full"
        >
            <div class="flex flex-row items-center justify-self-start">
                <Logo />
                <p class="text-3xl mx-3">
                    <Title />
                </p>
            </div>

            <div class="flex flex-row items-center justify-self-end">
                <button
                    class="resultButton bg-white border-solid border-[1px] border-c-orange text-c-orange mx-6"
                >
                    返回继续修改
                </button>
                <button class="resultButton bg-c-orange text-white">
                    完成
                </button>
            </div>
        </div>
    </div>

    <div class="flex flex-col justify-stretch h-[100vh] pt-[100px]">
        <div class="flex flex-grow justify-center items-center">
            <div
                v-if="renderFlag"
                class="flex flex-col justify-center items-center"
            >
                <img
                    :src="currentSource"
                    id="resultImg"
                    class="shadow-md object-contain w-full h-full"
                />
            </div>
            <div v-else>
                <p class="text-3xl text-c-text">获取失败</p>
            </div>
        </div>

        <div
            class="optionsWrapper flex flex-col items-center justify-start pb-12 flex-grow-0"
        >
            <PageIndicator
                v-model="currentPage"
                :total="totalPage"
                class="mb-4"
            />

            <button class="resultButton bg-c-orange text-white">
                下载选中的Banner
            </button>
        </div>
    </div>

    <!--悬浮物体-->
    <PageControlFloat isLeft icon="fa-solid fa-arrow-left" @click="decrease" />
    <PageControlFloat
        isRight
        icon="fa-solid fa-arrow-right"
        @click="increase"
    />

    <div class="checkboxWrapper absolute right-[45px] top-[150px]">
        <Checkbox
            v-model="theCheckbox"
            :binary="true"
            class="w-[40px] h-[40px]"
            v-tooltip.left="tooltipConfig"
        />
    </div>
</template>

<style scoped>
.resultBanner {
    border-bottom: var(--c-divider) 1px solid;
}

.resultButton {
    @apply px-6 py-2 rounded-full;
}

#resultImg {
    max-height: calc(0.6 * (100vh - 100px));
}
</style>
