<script setup>
import Dialog from "primevue/dialog";
import useAssetUploadVisible from "@/stores/AssetUploadStore.js";

import { styles, categories } from "@/stores/StyleOptions.js";
import InputText from "primevue/inputtext";
import { ref, computed } from "vue";
import MultiSelect from "primevue/multiselect";
import FileUpload from "primevue/fileupload";
import { useToast } from "primevue/usetoast";
import useUserStore from "@/stores/UserStore.js";
import request from "@/utils/request.js";
import AssetCard from "@/components/AssetsView/AssetCard.vue";

const toast = useToast();
const visibleStore = useAssetUploadVisible();
const visible = computed({
    set: (val) => {
        visibleStore.set(val);
    },
    get: () => {
        return visibleStore.visible;
    },
});

const type = ref("");
const category = ref([]);
const style = ref([]);

async function handleSubmit(e) {
    console.log(e.files);
    let files = e.files;
    let form = new FormData();

    if (files[0]) {
        //form.append("images", files[0]);
        let img = new window.FormData();
        img.append("image", files[0]);
        const res = await fetch("/api/uploadimage", {
            method: "POST",
            body: img,
        })
            .then((response) => response.json())
            .then((json) => {
                console.log(json);
            });
        console.log(res);
    } else {
        toast.add({
            severity: "warn",
            summary: "未选择文件",
            detail: "请选择需要上传的文件",
            life: 5000,
        });

        return;
    }

    if (type.value) form.append("type", type.value);
    if (category.value.length)
        form.append(
            "category",
            JSON.stringify(category.value) //"[" + category.value.toString() + "]"
        );
    if (style.value.length) {
        console.log("HEY" + style.value.toString());
        form.append(
            "styles",
            JSON.stringify(style.value) //"styles", "[" + style.value.toString() + "]"
        );
    }
    console.log("here");
    request
        .post("/upload", form, {
            params: {
                user_id: useUserStore().getUserInfo.userid,
            },
        })
        .then((res) => {
            const data = res;
            if (data.code !== 200) {
                toast.add({
                    severity: "error",
                    summary: "上传失败",
                    detail: data.message,
                    life: 5000,
                });
            } else {
                toast.add({
                    severity: "success",
                    summary: "上传成功",
                    life: 5000,
                });
                visible.value = false;
            }
        });
}
</script>

<template>
    <Dialog
        v-model:visible="visible"
        modal
        :pt="{
            root: 'border-none',
            mask: {
                style: 'backdrop-filter: blur(2px)',
            },
        }"
    >
        <template #container>
            <button
                class="absolute top-[15px] right-[15px] text-xl text-c-text hover:text-c-title px-1 py-1 mx-1"
                @click="visible = false"
            >
                <i class="fa-solid fa-xmark p-0"></i>
            </button>

            <div
                class="flex flex-col items-center px-12 py-5 bg-white rounded-md"
            >
                <h2 class="text-2xl text-c-orange font-bold my-5">上传素材</h2>

                <div class="flex flex-row w-full gap-4">
                    <div
                        class="flex flex-col justify-center items-center h-full"
                    >
                        <FileUpload
                            customUpload
                            @uploader="handleSubmit($event)"
                            mode="advanced"
                            :fileLimit="1"
                            class="flex flex-col justify-center items-center h-full"
                        >
                            <template #empty> </template>
                            <template
                                #header="{
                                    chooseCallback,
                                    clearCallback,
                                    files,
                                    uploadCallback,
                                }"
                            >
                                <button
                                    v-if="files.length === 0"
                                    class="rounded-full text-white text-sm bg-c-orange py-3 px-5"
                                    @click="chooseCallback()"
                                >
                                    选择文件
                                </button>
                                <button
                                    v-else
                                    class="rounded-full text-white text-sm bg-c-orange py-3 px-5"
                                    @click="clearCallback()"
                                >
                                    清除选择
                                </button>

                                <button
                                    v-if="files.length !== 0"
                                    class="rounded-full text-white text-sm bg-c-orange py-3 px-5"
                                    @click="uploadCallback()"
                                >
                                    上传文件
                                </button>
                            </template>
                            <template #content="{ files }">
                                <div
                                    class="flex h-full w-[300px] flex-col items-center justify-center"
                                >
                                    <div v-if="files.length > 0">
                                        <AssetCard
                                            :src="files[0].objectURL"
                                        ></AssetCard>
                                    </div>
                                    <div v-else>在此处拖放上传文件</div>
                                </div>
                            </template>
                        </FileUpload>
                    </div>
                    <div class="flex flex-col w-[250px]">
                        <p class="font-bold text-c-black my-2 px-2">素材类型</p>
                        <InputText v-model="type" class="w-full h-[42px]" />

                        <p class="font-bold text-c-black my-2 px-2">素材风格</p>
                        <div class="w-full">
                            <MultiSelect
                                display="chip"
                                :options="styles"
                                v-model="style"
                                class="w-full"
                                :maxSelectedLabels="4"
                                placeholder="选择素材风格"
                            />
                        </div>

                        <p class="font-bold text-c-black my-2 px-2">
                            素材商品类型
                        </p>
                        <div class="w-full">
                            <MultiSelect
                                display="chip"
                                :options="categories"
                                v-model="category"
                                class="w-full"
                                :maxSelectedLabels="1"
                                placeholder="请选择主题商品类别"
                            />
                        </div>
                    </div>
                </div>
            </div>
        </template>
    </Dialog>
</template>

<style scoped></style>
