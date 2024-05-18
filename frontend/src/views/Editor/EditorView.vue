<script setup>
import Button from "primevue/button";
import InputText from "primevue/inputtext";
import InputNumber from "primevue/inputnumber";
import Toast from "primevue/toast";
import { useToast } from "primevue/usetoast";
const toast = useToast();
import FileUpload from "primevue/fileupload";

import draggable from "vuedraggable";
import Drager from "es-drager";
import "es-drager/lib/style.css";
import { cloneDeep } from "lodash";
import { useRoute } from "vue-router";
import { ref, computed, watch, onMounted, onUnmounted } from "vue";

import MaterialContainer from "@/components/EditorView/MaterialContainer.vue";
import DragItem from "@/components/EditorView/DragItem.vue";
import { getDraftInfo, saveDraftInfo, gernerateDraft } from "@/api/banner.js";
import {
    getMaterialList,
    getMaterialById,
    getMaterialTag,
    uploadMaterial,
} from "@/api/material.js";
import useUserStore from "@/stores/UserStore.js";
import { baseURL } from "@/utils/request";
import router from "@/router";
import Title from "@/components/Utilities/Title.vue";

const imgNum = ref(4);
const setImgNum = (newNum) => {
    if (newNum < 1 || newNum > 4) {
        toast.add({
            severity: "warn",
            summary: "Warning",
            detail: "生成海报数量范围为1-4张",
            life: 3000,
        });
        return;
    }
    imgNum.value = newNum;
};

const leftBtn = ref("material");

const basicItem = {
    name: "图层",
    url: "",
    rotatable: true,
    width: 100,
    height: 100,
    top: 0,
    left: 0,
    equalProportion: true,
    border: false,
    w_pos: 0.3,
    w_neg: 1.0,
    t_i: 0.3,
    ref: null,
};
const itemList = ref([]);

const route = useRoute();
const user_id = useUserStore()._userid;
const project_id = route.params.id;
const projectInfo = ref({});

async function modifyOriginList(originList) {
    for (const [index, origin] of Object.entries(originList)) {
        origin.top = origin.pos_y;
        origin.left = origin.pos_x;
        origin.angle = origin.rotate_deg;
        origin.img_url = "";
        delete origin.pos_y;
        delete origin.pos_x;
        delete origin.rotate_deg;
        const {
            data: { image_url },
        } = await getMaterialById({ user_id, img_id: origin.img_id });
        origin.img_url = "/" + image_url;
        const {
            data: { types },
        } = await getMaterialTag(user_id, origin.img_id);
        origin.name = types[0].type;
        origin.t_i = parseFloat(origin.t_i);
        origin.w_pos = parseFloat(origin.w_pos);
        origin.w_neg = parseFloat(origin.w_neg);
        originList[index] = { ...basicItem, ...origin };
        console.log("origin list");
    }
}

const materialTypes = ref({
    主体物: [],
    装饰物: [],
    标语: [],
    LOGO: [],
    背景: [],
});

const getMaterial = async () => {
    Object.keys(materialTypes.value).forEach(async (key) => {
        if (key !== "主体物") {
            const {
                data: { images },
            } = await getMaterialList({
                user_id,
                type: key,
                style: Array.from(projectInfo.value.style),
            });
            for (let img of images) {
                img.img_url = "/" + img.img_url;
            }
            materialTypes.value[key] = cloneDeep(images);
        } else {
            const {
                data: { images },
            } = await getMaterialList({
                user_id,
                type: key,
                style: Array.from(projectInfo.value.style),
                category: Array.from(projectInfo.value.type),
            });
            console.log(images);
            for (let img of images) {
                img.img_url = "/" + img.img_url;
            }
            materialTypes.value[key] = cloneDeep(images);
        }
    });
};

onMounted(async () => {
    // 获取草稿的信息
    const res = await getDraftInfo({ user_id, project_id });
    const data = res.data;
    projectInfo.value = data.project;
    projectInfo.value.scale = 1;
    projectInfo.value.style = new Set(projectInfo.value.style);
    projectInfo.value.type = new Set(projectInfo.value.type);
    itemList.value = data.processed_images;
    modifyOriginList(itemList.value).then(() => {
        record.snapshots.push(cloneDeep(itemList.value));
        record.curIndex++;
        // watch(itemList, debounce(recordPush, 50), {deep: true})
    });

    // 获取素材
    getMaterial();

    // 监听删除素材事件
    window.addEventListener("keyup", handleDeleteMaterial);
});

onUnmounted(() => {
    window.removeEventListener("keyup", handleDeleteMaterial);
});

const canvas_scale = ref(1);
const canvas = ref(); // 画布
const canvas_outerbox = ref(); //画布外边的盒子
// ctrl+滚轮缩放
const handleZoom = (e) => {
    const modifyOuter = (type) => {
        let outerHeight = canvas_outerbox.value.offsetHeight;
        let outerWidth = canvas_outerbox.value.offsetWidth;
        let innerHeight = canvas.value.offsetHeight * canvas_scale.value;
        let innerWidth = canvas.value.offsetWidth * canvas_scale.value;
        console.log(type);
        if (type == "zoomin") {
            canvas_outerbox.value.style.width = `${Math.max(
                innerWidth + 64,
                outerWidth
            )}px`;
            canvas_outerbox.value.style.height = `${Math.max(
                innerHeight + 64,
                outerHeight
            )}px`;
        } else {
            canvas_outerbox.value.style.width = `${Math.min(
                innerWidth,
                outerWidth
            )}px`;
            canvas_outerbox.value.style.height = `${Math.min(
                innerHeight,
                outerHeight
            )}px`;
        }
    };
    if (canvas_scale.value <= 0) return;

    // 判断是不是按下ctrl键
    if (e.ctrlKey) {
        // 取消浏览器默认的放大缩小网页行为
        e.preventDefault();
        // 判断是向上滚动还是向下滚动
        if (e.deltaY < 0) {
            // 放大
            canvas_scale.value += 0.008;
            modifyOuter("zoomin");
        } else {
            // 缩小
            canvas_scale.value -= 0.008;
            modifyOuter("zoomout");
        }
    }
};

// 丢素材到画布上
const handleDrop = (e) => {
    let item = e.dataTransfer.getData("item") || null;
    if (!item) return;
    item = JSON.parse(item);
    console.log("drop a item", item);
    const rectObj = canvas.value.getBoundingClientRect();
    itemList.value.push({
        ...basicItem,
        ...item,
        ...{
            left:
                (e.clientX - rectObj.left) / canvas_scale.value -
                item.width * 0.5,
            top:
                (e.clientY - rectObj.top) / canvas_scale.value -
                item.height * 0.5,
        },
    });
};

const handleDragover = (e) => {
    e.preventDefault();
};

// 选择素材的index
const selectedItemIndex = ref(-1);
const selected = ref("hidden");
// 每个素材的参数
const w_pos = computed({
    get: () => {
        if (
            selected.value !== "hidden" &&
            selectedItemIndex.value < itemList.value.length &&
            selectedItemIndex.value >= 0
        ) {
            return itemList.value[selectedItemIndex.value].w_pos;
        } else return 0;
    },
    set: (val) => {
        if (selectedItemIndex.value == -1) {
            toast.add({
                severity: "warn",
                summary: "Warning",
                detail: "未选择素材",
                life: 3000,
            });
            return;
        }
        val = parseFloat(val.toFixed(1));
        if (val >= 1 || val <= 0) {
            toast.add({
                severity: "warn",
                summary: "Warning",
                detail: "正向影响力范围为(0,1)",
                life: 3000,
            });
            return;
        }
        itemList.value[selectedItemIndex.value].w_pos = val;
    },
});
const w_neg = computed({
    get: () => {
        if (
            selected.value !== "hidden" &&
            selectedItemIndex.value < itemList.value.length &&
            selectedItemIndex.value >= 0
        ) {
            return itemList.value[selectedItemIndex.value].w_neg;
        } else return 0;
    },
    set: (val) => {
        if (selectedItemIndex.value == -1) {
            toast.add({
                severity: "warn",
                summary: "Warning",
                detail: "未选择素材",
                life: 3000,
            });
            return;
        }
        val = parseFloat(val.toFixed(1));
        if (val >= 3 || val <= 0) {
            toast.add({
                severity: "warn",
                summary: "Warning",
                detail: "负向影响力范围为(0,3)",
                life: 3000,
            });
            return;
        }
        itemList.value[selectedItemIndex.value].w_neg = val;
    },
});
const t_i = computed({
    get: () => {
        if (
            selected.value != "hidden" &&
            selectedItemIndex.value < itemList.value.length &&
            selectedItemIndex.value >= 0
        ) {
            return itemList.value[selectedItemIndex.value].t_i;
        } else return 0;
    },
    set: (val) => {
        if (selectedItemIndex.value == -1) {
            toast.add({
                severity: "warn",
                summary: "Warning",
                detail: "未选择素材",
                life: 3000,
            });
            return;
        }
        val = parseFloat(val.toFixed(1));
        if (val > 1 || val < 0) {
            toast.add({
                severity: "warn",
                summary: "Warning",
                detail: "影响因子范围为[0,1]",
                life: 3000,
            });
            return;
        }
        itemList.value[selectedItemIndex.value].t_i = val;
    },
});

const saveSuccess = ref("hidden");
// 保存草稿
const handleSave = async () => {
    let form = [];
    const len = itemList.value.length;
    itemList.value.forEach((item, index) => {
        const cur = {};
        cur.original_image_id = item.img_id;
        cur.layer = index;
        cur.pos_x = item.left;
        cur.pos_y = item.top;
        cur.w_pos = item.w_pos;
        cur.w_neg = item.w_neg;
        cur.t_i = item.t_i;
        cur.rotate_deg = item.angle;
        cur.width = item.width;
        cur.height = item.height;
        form.push(cur);
    });
    await saveDraftInfo(user_id, project_id, {
        width: projectInfo.value.width,
        height: projectInfo.value.height,
        style: projectInfo.value.style,
        type: projectInfo.value.type,
        processed_images: form,
    }).then(() => {
        saveSuccess.value = "visible";
        setTimeout(() => {
            saveSuccess.value = "hidden";
        }, 5000);
    });
};
// 生成
const handleGenerate = async () => {
    await handleSave();
    toast.add({
        severity: "success",
        summary:
            "生成已经开始！请耐心等待，生成完成后可在个人主界面的“生成Banner”处查看生成的海报。",
        life: 5000,
    });
    await gernerateDraft(user_id, project_id, imgNum.value).then(
        ({ data: { task_id } }) => {
            router.resolve("/");
        }
    );
};

// 更新itemList的数据
// 画布缩放后drag位置有问题，待修
let drag_evt = {
    left: 0,
    top: 0,
    item_left: 0,
    item_top: 0,
    item: null,
};
const handleMouseDown = (e, item) => {
    // e.preventDefault()
    drag_evt.item_left = item.left;
    drag_evt.item_top = item.top;
    drag_evt.left = e.clientX;
    drag_evt.top = e.clientY;
    drag_evt.item = item;
    window.addEventListener("mousemove", handleMouseMove);
    window.addEventListener("mouseup", handleMouseUp);
};
const handleMouseMove = (e) => {
    e.preventDefault();
    drag_evt.item.left =
        drag_evt.item_left + (e.clientX - drag_evt.left) / canvas_scale.value;
    drag_evt.item.top =
        drag_evt.item_top + (e.clientY - drag_evt.top) / canvas_scale.value;
};
const handleMouseUp = (e) => {
    e.preventDefault();
    drag_evt.item.left =
        drag_evt.item_left + (e.clientX - drag_evt.left) / canvas_scale.value;
    drag_evt.item.top =
        drag_evt.item_top + (e.clientY - drag_evt.top) / canvas_scale.value;
    window.removeEventListener("mousemove", handleMouseMove);
    window.removeEventListener("mouseup", handleMouseUp);
    recordPush();
};
const handleClick = (index) => {
    console.log("click");
    selected.value = "visible";
    selectedItemIndex.value = index;
    let item = itemList.value[index];
    // item.ref.parentNode.classList.add('selected')
    let item_svg = item.ref.parentNode.querySelector(".es-drager-rotate");
    if (item_svg) item_svg.style.display = "block";
    // 取消别的元素的选择样式
    itemList.value.forEach((it, idx) => {
        if (idx !== index) {
            let svg = it.ref.parentNode.querySelector(".es-drager-rotate");
            if (svg) svg.style.display = "none";
            it.selected = false;
            it.ref.parentNode.classList.remove("selected");
        }
    });
};
// 应该是没用的东西，待修
const handleBlur = (e, index = null) => {
    console.log("blur", e);
};
const handleResizeEnd = (e, item) => {
    console.log("resize end", e.width, item.width);
    item.width = e.width;
    item.height = e.height;
    recordPush();
};
const handleRotateEnd = (e, item) => {
    console.log("rotate end", e.angle, item.angle);
    item.angle = e.angle;
    recordPush();
};

const handleDeleteMaterial = (e) => {
    if (e.target.tagName !== "INPUT" && (e.keyCode == 46 || e.keyCode == 8)) {
        itemList.value.forEach((item, index) => {
            if (item.ref.parentNode.classList.contains("selected")) {
                console.log(item.ref.parentNode);
                itemList.value.splice(index, 1);
                selectedItemIndex.value = -1;
                return;
            }
        });
        recordPush();
    }
};

// 撤回重做
// 记录快照
const record = {
    snapshots: [],
    curIndex: 0,
    maxLimit: 20,
    isSnapshot: true,
};

// 比较是否相同
// const same = () => {
//     console.log('same', record.curIndex);
//     if (itemList.value.length != record.snapshots[record.curIndex-1].length) return false
//     for (let i = 0; i < itemList.value.length; ++i) {
//         for (let key in itemList.value[i]) {
//             if (key != 'ref' && itemList.value[i][key] !== record.snapshots[record.curIndex-1][i][key]) {
//                 console.log(key, itemList.value[i][key], record.snapshots[record.curIndex-1][i][key]);
//                 return false
//             }
//         }
//     }
//     return true
// }

const recordPush = () => {
    console.log("recordPush", record.curIndex, record.snapshots.length);
    // 不需要生成快照，退出
    // if (same()) {
    //     return
    // }
    // 超出限制，删掉第一个快照
    if (record.curIndex == record.maxLimit) {
        record.snapshots.shift();
        curIndex--;
    }
    // 撤销后，又进行了操作
    if (record.curIndex != record.snapshots.length) {
        console.log("撤销后，又进行了操作");
        record.snapshots.splice(record.curIndex, record.snapshots.length);
    }
    console.log("push");
    record.snapshots.push(cloneDeep(itemList.value));
    record.curIndex++;
};

const handleUndo = () => {
    if (record.curIndex == 1) return;
    record.isSnapshot = false;
    console.log("Undo", record.curIndex);
    record.curIndex = record.curIndex - 1;
    console.log("Undo", record.curIndex);
    itemList.value = cloneDeep(record.snapshots[record.curIndex - 1]);
};

const handleRedo = () => {
    if (record.curIndex >= record.snapshots.length) return;
    record.isSnapshot = false;
    record.curIndex = record.curIndex + 1;
    itemList.value = cloneDeep(record.snapshots[record.curIndex - 1]);
};

// 重新获取素材
watch(
    () => [projectInfo.value.style, projectInfo.value.type],
    () => {
        getMaterial();
    },
    { deep: true }
);

const uploadImg = ref();
const uploadClick = () => {
    uploadImg.value.click();
};
const selectFile = async (event) => {
    const upload_img_file = event.target.files[0];
    const result = await uploadMaterial(user_id, { images: upload_img_file });
    result.then((res) => {
        console.log(res);
    });
    toast.add({
        severity: "success",
        summary: "Success",
        detail: "素材上传成功",
        life: 3000,
    });
};
</script>

<template>
    <Toast />
    <main class="flex flex-col h-screen w-screen divide-y">
        <!-- header -->
        <div
            class="flex flex-row grow-0 h-fit px-9 py-4 justify-between align-middle text-center"
        >
            <div class="flex flex-row justify-between flex-1">
                <div class="flex flex-row gap-4">
                    <svg
                        width="48"
                        height="45"
                        viewBox="0 0 48 45"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                        xmlns:xlink="http://www.w3.org/1999/xlink"
                    >
                        <rect
                            width="48"
                            height="45"
                            rx="10"
                            fill="url(#pattern0_359_84)"
                        />
                        <defs>
                            <pattern
                                id="pattern0_359_84"
                                patternContentUnits="objectBoundingBox"
                                width="1"
                                height="1"
                            >
                                <use
                                    xlink:href="#image0_359_84"
                                    transform="matrix(0.000694959 0 0 0.00074129 -0.00315048 0)"
                                />
                            </pattern>
                            <image
                                id="image0_359_84"
                                width="1448"
                                height="1349"
                                xlink:href="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABagAAAVFCAYAAAD9/i4NAAAgAElEQVR4nOzdB5TdZZk/8GdKpmQmM0kmvXdSSZuEYghI70pTpAhWUFBZUFhdV7Et/lkXCBAQAUGqBEQpUqSI9BJpoSSUBAKGQEjPJJnJlP+5F9cVUwmT+d3y+ZwzZxLCOdx8nznM3O997vsWVFd2bgkAAAAAAGhjhQIHAAAAACAJCmoAAAAAABKhoAYAAAAAIBEKagAAAAAAEqGgBgAAAAAgEQpqAAAAAAASoaAGAAAAACARCmoAAAAAABKhoAYAAAAAIBEKagAAAAAAEqGgBgAAAAAgEQpqAAAAAAASoaAGAAAAACARCmoAAAAAABKhoAYAAAAAIBEKagAAAAAAEqGgBgAAAAAgEQpqAAAAAAASoaAGAAAAACARCmoAAAAAABKhoAYAAAAAIBEKagAAAAAAEqGgBgAAAAAgEQpqAAAAAAASoaAGAAAAACARCmoAAAAAABKhoAYAAAAAIBEKagAAAAAAEqGgBgAAAAAgEQpqAAAAAAASoaAGAAAAACARCmoAAAAAABKhoAYAAAAAIBEKagAAAAAAEqGgBgAAAAAgEQpqAAAAAAASoaAGAAAAACARCmoAAAAAABKhoAYAAAAAIBEKagAAAAAAEqGgBgAAAAAgEQpqAAAAAAASoaAGAAAAACARCmoAAAAAABKhoAYAAAAAIBEKagAAAAAAEqGgBgAAAAAgEQpqAAAAAAASoaAGAAAAACARCmoAAAAAABKhoAYAAAAAIBEKagAAAAAAEqGgBgAAAAAgEQpqAAAAAAASoaAGAAAAACARCmoAAAAAABKhoAYAAAAAIBEKagAAAAAAEqGgBgAAAAAgEQpqAAAAAAASoaAGAAAAACARCmoAAAAAABKhoAYAAAAAIBEKagAAAAAAEqGgBgAAAAAgEQpqAAAAACBvFRQUGH6CFNQAAAAAQN5qaWkx/AQpqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiEghoAAAAAgEQoqAEAAAAASISCGgAAAACARCioAQAAAABIhIIaAAAAAIBEKKgBAAAAAEiE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AAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAAAQIVADAAAAABAhUAMAAAAAECFQAwAAAADw86uqfwKfJd3Zc4oULAAAAABJRU5ErkJggg=="
                            />
                        </defs>
                    </svg>
                    <router-link to="/" id="BannerText">
                        <h2 class="text-3xl mx-1">
                            <Title />
                        </h2>
                    </router-link>
                </div>
                <!-- 撤回重做 -->
                <div class="flex flex-row gap-[18px] justify-between">
                    <!-- 撤销 -->
                    <Button @click="handleUndo">
                        <svg
                            class="icon w-6 h-6"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M15.13 19.0601H7.13C6.72 19.0601 6.38 18.7201 6.38 18.3101C6.38 17.9001 6.72 17.5601 7.13 17.5601H15.13C17.47 17.5601 19.38 15.6501 19.38 13.3101C19.38 10.9701 17.47 9.06006 15.13 9.06006H4.13C3.72 9.06006 3.38 8.72006 3.38 8.31006C3.38 7.90006 3.72 7.56006 4.13 7.56006H15.13C18.3 7.56006 20.88 10.1401 20.88 13.3101C20.88 16.4801 18.3 19.0601 15.13 19.0601Z"
                            />
                            <path
                                d="M6.43 11.5599C6.24 11.5599 6.05 11.4899 5.9 11.3399L3.34 8.77988C3.05 8.48988 3.05 8.00988 3.34 7.71988L5.9 5.15988C6.19 4.86988 6.67 4.86988 6.96 5.15988C7.25 5.44988 7.25 5.92988 6.96 6.21988L4.93 8.24988L6.96 10.2799C7.25 10.5699 7.25 11.0499 6.96 11.3399C6.82 11.4899 6.62 11.5599 6.43 11.5599Z"
                            />
                        </svg>
                    </Button>
                    <!-- 重做 -->
                    <Button @click="handleRedo">
                        <svg
                            class="icon w-6 h-6"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M16.87 19.0601H8.87C5.7 19.0601 3.12 16.4801 3.12 13.3101C3.12 10.1401 5.7 7.56006 8.87 7.56006H19.87C20.28 7.56006 20.62 7.90006 20.62 8.31006C20.62 8.72006 20.28 9.06006 19.87 9.06006H8.87C6.53 9.06006 4.62 10.9701 4.62 13.3101C4.62 15.6501 6.53 17.5601 8.87 17.5601H16.87C17.28 17.5601 17.62 17.9001 17.62 18.3101C17.62 18.7201 17.29 19.0601 16.87 19.0601Z"
                            />
                            <path
                                d="M17.57 11.5599C17.38 11.5599 17.19 11.4899 17.04 11.3399C16.75 11.0499 16.75 10.5699 17.04 10.2799L19.07 8.24988L17.04 6.21988C16.75 5.92988 16.75 5.44988 17.04 5.15988C17.33 4.86988 17.81 4.86988 18.1 5.15988L20.66 7.71988C20.95 8.00988 20.95 8.48988 20.66 8.77988L18.1 11.3399C17.95 11.4899 17.76 11.5599 17.57 11.5599Z"
                            />
                        </svg>
                    </Button>
                </div>
            </div>
            <!-- 标题 -->
            <div class="flex flex-row flex-1 justify-center align-center">
                <InputText
                    class="text-[#5f5f5f] text-center"
                    type="text"
                    v-model="projectInfo.name"
                />
            </div>
            <div class="flex flex-row flex-1 justify-between">
                <!-- 保存 -->
                <div class="flex flex-row justify-between">
                    <div
                        class="flex flex-row items-center mr-[1rem]"
                        :style="{ visibility: saveSuccess }"
                    >
                        <svg
                            class="h-[1.128rem] mr-[0.35rem]"
                            viewBox="0 0 20 20"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M7.75002 19H3.25C2.00735 19 0.999992 17.9926 1 16.75L1.00009 3.24999C1.00009 2.00736 2.00745 1 3.25009 1H13.3754C14.618 1 15.6254 2.00736 15.6254 3.25001V9.43752M11.1254 15.8125L13.1879 17.875L18.4379 12.25"
                                stroke="#5F5F5F"
                                stroke-width="1.5"
                                stroke-linecap="round"
                                stroke-linejoin="round"
                            />
                        </svg>
                        <span class="inline-block text-xs text-[#5F5F5F]"
                            >保存成功</span
                        >
                    </div>
                    <Button
                        @click="handleSave"
                        class="py-2 px-[1.6rem] border border-[#eeaa1e] hover:bg-[#eeaa1e] rounded-md text-sm text-[#eeaa1e] hover:text-white font-normal"
                        >保存设计稿</Button
                    >
                </div>
                <!-- 生成 -->
                <div class="flex flex-row">
                    <div
                        class="flex flex-row mr-[0.7rem] gap-[4px] justify-between items-center"
                    >
                        <Button
                            class="w-8 h-8 rounded-md"
                            @click="() => setImgNum(imgNum - 1)"
                        >
                            <svg
                                width="32"
                                height="34"
                                viewBox="0 0 32 34"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <rect
                                    width="32"
                                    height="34"
                                    rx="5"
                                    fill="#F6F4F0"
                                />
                                <path
                                    d="M18.8047 22.416C19.0651 22.1493 19.0651 21.7168 18.8047 21.4501L14.6094 17.1518L18.8047 12.8535C19.0651 12.5867 19.0651 12.1543 18.8047 11.8875C18.5444 11.6208 18.1223 11.6208 17.862 11.8875L13.1953 16.6688C12.9349 16.9355 12.9349 17.368 13.1953 17.6347L17.862 22.416C18.1223 22.6828 18.5444 22.6828 18.8047 22.416Z"
                                    fill="#8B8B8B"
                                />
                            </svg>
                        </Button>
                        <span
                            class="inline-block px-[1.6rem] h-[2.25rem] leading-[2.25rem] bg-[#eeaa1e] rounded-md text-sm text-[#ffffff] font-normal"
                            >{{ imgNum }}张</span
                        >
                        <Button
                            class="w-8 h-8 bg-[#eeaa1e] rounded-md text-sm text-[#ffffff] font-normal"
                            @click="() => setImgNum(imgNum + 1)"
                        >
                            <svg
                                width="32"
                                height="34"
                                viewBox="0 0 32 34"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <rect
                                    x="32"
                                    y="34"
                                    width="32"
                                    height="34"
                                    rx="5"
                                    transform="rotate(-180 32 34)"
                                    fill="#F6F4F0"
                                />
                                <path
                                    d="M13.1953 11.584C12.9349 11.8507 12.9349 12.2832 13.1953 12.5499L17.3906 16.8482L13.1953 21.1465C12.9349 21.4133 12.9349 21.8457 13.1953 22.1125C13.4556 22.3792 13.8777 22.3792 14.138 22.1125L18.8047 17.3312C19.0651 17.0645 19.0651 16.632 18.8047 16.3653L14.138 11.584C13.8777 11.3172 13.4556 11.3172 13.1953 11.584Z"
                                    fill="#8B8B8B"
                                />
                            </svg>
                        </Button>
                    </div>
                    <Button
                        @click="handleGenerate"
                        class="py-2 px-[1.6rem] bg-[#eeaa1e] rounded-md text-sm text-[#ffffff] font-normal"
                    >
                        生成
                    </Button>
                </div>
            </div>
        </div>
        <!-- main -->
        <div class="flex flex-row h-0 items-stretch divide-x grow">
            <!-- 左边按钮 -->
            <div
                class="relative w-[4vw] px-[5px] py-[7px] flex flex-col justify-start gap-[10px] z-[100]"
            >
                <div
                    class="flex flex-col w-full items-center py-[11px] gap-[9px] fill-[#5F5F5F] stroke-white rounded-lg cursor-pointer text-[--c-grey]"
                    :class="{ selectedBtn: leftBtn == 'material' }"
                    @click="
                        () => {
                            leftBtn = 'material';
                        }
                    "
                >
                    <svg
                        class="w-[45%]"
                        viewBox="0 0 25 23"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            fill-rule="evenodd"
                            clip-rule="evenodd"
                            d="M22.0971 6.10695C22.8385 6.56212 23.0034 7.51764 22.6171 8.20962L22.5945 8.25019L22.5688 8.28884C21.9332 9.24789 21.3629 10.2457 20.8576 11.2825C20.8923 11.2902 20.9288 11.2982 20.9674 11.3066C20.9787 11.3091 20.9902 11.3116 21.0019 11.3141C21.2646 11.3711 21.6409 11.4527 22.001 11.6059C22.4505 11.7913 22.75 12.0702 22.9815 12.3239L22.9931 12.3365L23.0042 12.3495C23.7517 13.2171 24.0245 14.6055 23.415 15.7985C22.995 16.9142 21.9938 17.6866 20.9134 17.8483C20.1189 17.9711 19.4872 17.7321 19.0312 17.5078C18.8989 17.4427 18.7384 17.3557 18.6111 17.2868C18.5769 17.2682 18.5451 17.251 18.5168 17.2358C18.2224 18.3375 18.0047 19.4539 17.8636 20.5853C17.8494 21.0882 17.5846 21.4936 17.2552 21.7275C16.9295 21.9588 16.5527 22.0273 16.2218 21.9907C14.5849 21.8429 13.0388 21.2908 11.639 20.637L11.6342 20.6348C10.8391 20.259 10.2432 19.3057 10.5283 18.2356L10.5316 18.2232C10.6622 17.7526 10.9228 17.2595 11.0948 16.9337C11.1363 16.8552 11.1726 16.7865 11.2007 16.7301C11.3992 16.3323 11.4231 16.1723 11.4147 16.0845L11.4131 16.0674L11.4119 16.0502C11.3922 15.7565 11.1614 15.4487 10.9178 15.3517C10.7007 15.2652 10.3155 15.3256 10.0842 15.5537C9.99782 15.6428 9.91153 15.8032 9.80501 16.2152C9.78882 16.2778 9.77073 16.3547 9.7502 16.4419C9.66685 16.7962 9.5433 17.3213 9.34305 17.7579C8.85857 18.8244 7.74174 19.0176 7.00376 18.8265L6.98777 18.8223L6.97189 18.8177C5.48829 18.3873 3.98774 17.7856 2.63801 16.8399C1.9243 16.3771 1.76977 15.4394 2.15041 14.7576L2.17306 14.7171L2.19867 14.6784C2.83892 13.7124 3.41291 12.7071 3.92084 11.6622C3.90073 11.6575 3.8799 11.6527 3.85822 11.6476C3.73578 11.6192 3.58649 11.5845 3.39148 11.5327C2.92557 11.409 2.26604 11.1848 1.73862 10.552L1.72623 10.5371L1.71432 10.5218C1.01398 9.62429 0.784536 8.33622 1.22446 7.20165C1.64782 6.10978 2.66923 5.23675 3.91917 5.13114C4.27928 5.07547 4.68841 5.09031 5.10449 5.24421C5.48157 5.35515 5.81835 5.54247 6.0383 5.6648C6.05051 5.67159 6.06236 5.67818 6.07384 5.68455C6.13154 5.71655 6.18348 5.74511 6.23071 5.77061C6.52599 4.66681 6.74425 3.5483 6.88563 2.4147C6.89988 1.91185 7.16466 1.50645 7.49404 1.27252C7.83016 1.0338 8.22059 0.968468 8.5589 1.0131L8.57493 1.01521C10.1307 1.24302 11.6604 1.6859 13.1102 2.36295L13.115 2.36519C13.9102 2.74101 14.5061 3.69434 14.2209 4.76441L14.2176 4.77683C14.0886 5.24171 13.8429 5.72172 13.6769 6.04608C13.6374 6.12326 13.6025 6.19163 13.5746 6.24888C13.3842 6.64063 13.3495 6.81324 13.3558 6.91978C13.3801 7.26633 13.5994 7.52677 13.8044 7.59861C14.0811 7.69554 14.4065 7.63427 14.6641 7.37024L14.6685 7.36574C14.7662 7.2667 14.858 7.09649 14.9684 6.69551C14.9861 6.63155 15.0062 6.55075 15.0293 6.45821C15.1145 6.11677 15.2395 5.61563 15.4235 5.21157C15.9074 4.14309 17.0253 3.94954 17.7638 4.14078L17.783 4.14576L17.8021 4.15141C19.3565 4.61228 20.7626 5.2646 22.0971 6.10695ZM17.4294 6.56551C17.4047 6.65272 17.3806 6.74897 17.3523 6.86243C17.3182 6.99859 17.2779 7.15955 17.2229 7.35944C17.0883 7.84803 16.8628 8.53445 16.312 9.09431C15.4394 9.98684 14.1902 10.2932 13.0522 9.89448C11.8421 9.4705 11.0977 8.28343 11.0171 7.08529L11.0168 7.0806C10.966 6.27967 11.2649 5.6032 11.4803 5.16014C11.5577 5.00093 11.6246 4.86893 11.6827 4.75461C11.7452 4.63137 11.7973 4.52868 11.8408 4.43457C10.9574 4.04867 10.0362 3.7599 9.09253 3.56471C8.91626 4.69319 8.66992 5.80784 8.35361 6.90833C8.06319 7.96818 7.01322 8.54935 6.03261 8.2954L6.02002 8.29215L6.00751 8.2886C5.5994 8.17293 5.23644 7.97115 4.99977 7.83959C4.98814 7.83312 4.97682 7.82683 4.9658 7.82072C4.68102 7.66274 4.55441 7.59988 4.45361 7.57312L4.38323 7.55444L4.31562 7.52691C4.3151 7.52679 4.3124 7.52614 4.30873 7.52585C4.30125 7.52526 4.28465 7.52504 4.25746 7.52998L4.19217 7.54184L4.12599 7.54601C3.81808 7.56539 3.51923 7.79673 3.40016 8.10382C3.29293 8.38037 3.3438 8.73631 3.52551 8.98236C3.57879 9.04089 3.67278 9.1047 3.97425 9.18472C4.05479 9.2061 4.13976 9.22625 4.24154 9.25012L4.26156 9.25481C4.35404 9.27648 4.46111 9.30158 4.56897 9.32945C4.80021 9.38921 5.08084 9.47283 5.36827 9.61108C6.36153 10.0838 6.69722 11.2843 6.25232 12.251L6.25125 12.2533C5.77043 13.2924 5.23099 14.2966 4.63307 15.2658C5.46015 15.7435 6.37095 16.1085 7.3381 16.4042C7.36702 16.3017 7.39429 16.1872 7.42724 16.0489C7.45803 15.9197 7.49377 15.7696 7.54046 15.5891C7.66736 15.0982 7.88295 14.3907 8.44583 13.8199L8.452 13.8137C9.31477 12.9516 10.6602 12.6513 11.7606 13.0897C12.8309 13.5162 13.6587 14.6198 13.7492 15.8652C13.8227 16.695 13.5074 17.3936 13.2838 17.8417C13.1969 18.0159 13.1231 18.1566 13.0604 18.2763C13.0014 18.3888 12.9522 18.4827 12.9111 18.5682C13.8257 18.9763 14.7396 19.2963 15.6517 19.4675C15.8283 18.328 16.0763 17.2026 16.3956 16.0916C16.6861 15.0318 17.736 14.4507 18.7166 14.7046L18.7475 14.7126L18.778 14.7223C19.0693 14.8154 19.3234 14.9402 19.5254 15.0463C19.6262 15.0993 19.7026 15.141 19.7701 15.1778C19.8632 15.2286 19.9392 15.27 20.0383 15.3188C20.3085 15.4518 20.4375 15.471 20.5679 15.4507L20.5768 15.4493C20.8663 15.4064 21.1454 15.1738 21.2393 14.8947L21.2758 14.7864L21.3312 14.6871C21.3934 14.5757 21.4169 14.4466 21.4001 14.3099C21.3831 14.1727 21.3281 14.0528 21.2626 13.9723C21.2085 13.914 21.1787 13.888 21.1622 13.8751C21.1495 13.8653 21.1428 13.8616 21.1318 13.8572L21.1218 13.8531L21.1119 13.8489C20.9708 13.7883 20.7941 13.7461 20.485 13.6788C20.4737 13.6764 20.4622 13.6739 20.4505 13.6713C20.1855 13.6139 19.8048 13.5313 19.4419 13.3755L19.4228 13.3673L19.404 13.3584C18.4071 12.8873 18.0696 11.6845 18.5152 10.7163L18.5163 10.7139C18.9929 9.68396 19.5271 8.68818 20.1188 7.72683C19.2669 7.25329 18.3803 6.86718 17.4294 6.56551Z"
                            stroke-width="1.2"
                        />
                    </svg>
                    <span class="text-xs">素材</span>
                </div>
                <div
                    class="flex flex-col w-full items-center py-[11px] gap-[9px] fill-[#5F5F5F] stroke-white rounded-lg cursor-pointer text-[--c-grey]"
                    :class="{ selectedBtn: leftBtn == 'upload' }"
                    @click="
                        () => {
                            leftBtn = 'upload';
                        }
                    "
                >
                    <svg
                        class="w-[45%]"
                        viewBox="0 0 23 23"
                        xmlns="http://www.w3.org/2000/svg"
                    >
                        <path
                            fill-rule="evenodd"
                            clip-rule="evenodd"
                            d="M10.45 16.75C10.45 17.3299 10.9201 17.8 11.5 17.8C12.0799 17.8 12.55 17.3299 12.55 16.75V4.58493L16.0075 8.04247C16.4176 8.45252 17.0824 8.45252 17.4925 8.04247C17.9025 7.63242 17.9025 6.96759 17.4925 6.55754L12.2424 1.30754C11.8324 0.897487 11.1676 0.897487 10.7575 1.30754L5.50752 6.55754C5.09747 6.96759 5.09747 7.63241 5.50752 8.04246C5.91757 8.45252 6.5824 8.45252 6.99245 8.04246L10.45 4.58493L10.45 16.75ZM3.1 14.65C3.1 14.0701 2.6299 13.6 2.05 13.6C1.4701 13.6 1 14.0701 1 14.65V18.85C1 20.5897 2.4103 22 4.15 22H18.85C20.5897 22 22 20.5897 22 18.85V14.65C22 14.0701 21.5299 13.6 20.95 13.6C20.3701 13.6 19.9 14.0701 19.9 14.65V18.85C19.9 19.4299 19.4299 19.9 18.85 19.9H4.15C3.5701 19.9 3.1 19.4299 3.1 18.85V14.65Z"
                            stroke-width="0.8"
                            stroke-linecap="round"
                            stroke-linejoin="round"
                        />
                    </svg>
                    <span class="text-xs">上传</span>
                </div>
            </div>
            <!-- 左边素材 -->
            <div class="relative flex flex-col w-[20vw] px-4 pt-7 z-[100]">
                <div
                    :class="{ hidden: leftBtn == 'material' }"
                    class="w-full h-full"
                >
                    <label for="uploadImg">
                        <Button
                            class="flex flex-row gap-1 mx-auto my-0 px-[2.8rem] py-2 border border-[#FFE18C] text-[--c-grey] fill-[--c-grey] stroke-white upload"
                            outlined
                            @click="uploadClick"
                        >
                            <svg
                                width="16"
                                height="16"
                                viewBox="0 0 16 16"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fill-rule="evenodd"
                                    clip-rule="evenodd"
                                    d="M7.29999 11.5C7.29999 11.8866 7.61339 12.2 7.99999 12. 2C8.38659 12.2 8.69999 11.8866 8.69999 11.5L8.69999 3.38995L11.005 5.69498C11.2784 5.96834 11.7216 5.    96834 11.995 5.69498C12.2683 5.42161 12.2683 4.97839 11.995 4.70503L8.49497 1.20503C8.2216 0.931658 7.  77838 0.931658 7.50502 1.20503L4.00502 4.70503C3.73165 4.97839 3.73165 5.42161 4.00501 5.69498C4.27838    5.96834 4.7216 5.96834 4.99496 5.69498L7.29999 3.38995L7.29999 11.5ZM2.4 10.1C2.4 9.7134 2.0866 9.4 1. 7 9.4C1.3134 9.4 1 9.7134 1 10.1V12.9C1 14.0598 1.9402 15 3.1 15H12.9C14.0598 15 15 14.0598 15 12.9V10.  1C15 9.7134 14.6866 9.4 14.3 9.4C13.9134 9.4 13.6 9.7134 13.6 10.1V12.9C13.6 13.2866 13.2866 13.6 12.9    13.6H3.1C2.7134 13.6 2.4 13.2866 2.4 12.9V10.1Z"
                                    stroke-width="0.5"
                                    stroke-linecap="round"
                                    stroke-linejoin="round"
                                />
                            </svg>
                            <span class="text-sm">上传本地素材</span>
                        </Button>
                    </label>
                    <input
                        type="file"
                        id="uploadImg"
                        name="uploadImg"
                        ref="uploadImg"
                        accept=".jpg, .png"
                        class="opacity-0"
                        @change="selectFile"
                    />
                </div>
                <material-container
                    :selectedStyles="projectInfo.style"
                    :selectedTypes="projectInfo.type"
                    :materialList="materialTypes"
                    @selectStyle="
                        (name) => {
                            projectInfo.style.add(name);
                        }
                    "
                    @selectType="
                        (name) => {
                            projectInfo.type.add(name);
                        }
                    "
                    @deleteStyle="
                        (name) => {
                            projectInfo.style.delete(name);
                        }
                    "
                    @deleteType="
                        (name) => {
                            projectInfo.type.delete(name);
                        }
                    "
                    :class="{ hidden: leftBtn == 'upload' }"
                >
                </material-container>
            </div>
            <!-- 中间画布 -->
            <div
                @wheel="(e) => handleZoom(e)"
                class="relative flex flex-col w-[64vw] bg-[#f6f4f0] items-center z-0"
            >
                <!-- 素材编辑栏 -->
                <div
                    :style="{ visibility: selected }"
                    class="relative flex flex-row w-full h-fit px-5 py-4 gap-4 bg-white items-center paramsInput z-[100]"
                >
                    <!-- 正向影响力 -->
                    <div class="flex flex-row items-center">
                        <label for="positive" class="text-xs text-[#313131]"
                            >正向影响力：</label
                        >
                        <InputNumber
                            inputId="positive"
                            :minFractionDigits="1"
                            :maxFractionDigits="1"
                            v-model="w_pos"
                            :min="0.1"
                            :max="0.9"
                        />
                        <div class="flex flex-col">
                            <svg
                                @click="() => (w_pos += 0.1)"
                                class="w-[0.7rem] cursor-pointer arrow"
                                viewBox="0 0 11 11"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fill-rule="evenodd"
                                    clip-rule="evenodd"
                                    d="M2.54049 7.08451C2.3615 6.90552 2.3615 6.61532 2.54049 6.43633L5.06133 3.91549C5.24032 3.7365 5.53052 3.7365 5.70951 3.91549L8.23034 6.43633C8.40933 6.61532 8.40933 6.90552 8.23034 7.08451C8.05135 7.2635 7.76115 7.2635 7.58216 7.08451L5.38542 4.88776L3.18867 7.08451C3.00968 7.2635 2.71948 7.2635 2.54049 7.08451Z"
                                />
                            </svg>
                            <svg
                                @click="() => (w_pos -= 0.1)"
                                class="w-[0.7rem] cursor-pointer arrow"
                                viewBox="0 0 11 11"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fill-rule="evenodd"
                                    clip-rule="evenodd"
                                    d="M8.23035 4.25924C8.40934 4.43823 8.40934 4.72843 8.23035 4.90742L5.70952 7.42826C5.53053 7.60725 5.24033 7.60725 5.06134 7.42826L2.5405 4.90742C2.36151 4.72843 2.36151 4.43823 2.5405 4.25924C2.71949 4.08025 3.00969 4.08025 3.18868 4.25924L5.38543 6.45599L7.58217 4.25924C7.76116 4.08025 8.05136 4.08025 8.23035 4.25924Z"
                                />
                            </svg>
                        </div>
                    </div>
                    <!-- 负向影响力 -->
                    <div class="flex flex-row items-center">
                        <label for="negative" class="text-xs text-[#313131]"
                            >负向影响力：</label
                        >
                        <InputNumber
                            inputId="negative"
                            :minFractionDigits="1"
                            :maxFractionDigits="1"
                            v-model="w_neg"
                            :min="0.1"
                            :max="2.9"
                        />
                        <div class="flex flex-col">
                            <svg
                                @click="() => (w_neg += 0.1)"
                                class="w-[0.7rem] cursor-pointer arrow"
                                viewBox="0 0 11 11"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fill-rule="evenodd"
                                    clip-rule="evenodd"
                                    d="M2.54049 7.08451C2.3615 6.90552 2.3615 6.61532 2.54049 6.43633L5.06133 3.91549C5.24032 3.7365 5.53052 3.7365 5.70951 3.91549L8.23034 6.43633C8.40933 6.61532 8.40933 6.90552 8.23034 7.08451C8.05135 7.2635 7.76115 7.2635 7.58216 7.08451L5.38542 4.88776L3.18867 7.08451C3.00968 7.2635 2.71948 7.2635 2.54049 7.08451Z"
                                />
                            </svg>
                            <svg
                                @click="() => (w_neg -= 0.1)"
                                class="w-[0.7rem] cursor-pointer arrow"
                                viewBox="0 0 11 11"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fill-rule="evenodd"
                                    clip-rule="evenodd"
                                    d="M8.23035 4.25924C8.40934 4.43823 8.40934 4.72843 8.23035 4.90742L5.70952 7.42826C5.53053 7.60725 5.24033 7.60725 5.06134 7.42826L2.5405 4.90742C2.36151 4.72843 2.36151 4.43823 2.5405 4.25924C2.71949 4.08025 3.00969 4.08025 3.18868 4.25924L5.38543 6.45599L7.58217 4.25924C7.76116 4.08025 8.05136 4.08025 8.23035 4.25924Z"
                                />
                            </svg>
                        </div>
                    </div>
                    <!-- 影响因子 -->
                    <div class="flex flex-row items-center mr-2">
                        <label for="influence" class="text-xs text-[#313131]"
                            >影响因子：</label
                        >
                        <InputNumber
                            inputId="influence"
                            :minFractionDigits="1"
                            :maxFractionDigits="1"
                            v-model="t_i"
                            :min="0"
                            :max="1"
                        />
                        <div class="flex flex-col">
                            <svg
                                @click="() => (t_i += 0.1)"
                                class="w-[0.7rem] cursor-pointer arrow"
                                viewBox="0 0 11 11"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fill-rule="evenodd"
                                    clip-rule="evenodd"
                                    d="M2.54049 7.08451C2.3615 6.90552 2.3615 6.61532 2.54049 6.43633L5.06133 3.91549C5.24032 3.7365 5.53052 3.7365 5.70951 3.91549L8.23034 6.43633C8.40933 6.61532 8.40933 6.90552 8.23034 7.08451C8.05135 7.2635 7.76115 7.2635 7.58216 7.08451L5.38542 4.88776L3.18867 7.08451C3.00968 7.2635 2.71948 7.2635 2.54049 7.08451Z"
                                />
                            </svg>
                            <svg
                                @click="() => (t_i -= 0.1)"
                                class="w-[0.7rem] cursor-pointer arrow"
                                viewBox="0 0 11 11"
                                fill="none"
                                xmlns="http://www.w3.org/2000/svg"
                            >
                                <path
                                    fill-rule="evenodd"
                                    clip-rule="evenodd"
                                    d="M8.23035 4.25924C8.40934 4.43823 8.40934 4.72843 8.23035 4.90742L5.70952 7.42826C5.53053 7.60725 5.24033 7.60725 5.06134 7.42826L2.5405 4.90742C2.36151 4.72843 2.36151 4.43823 2.5405 4.25924C2.71949 4.08025 3.00969 4.08025 3.18868 4.25924L5.38543 6.45599L7.58217 4.25924C7.76116 4.08025 8.05136 4.08025 8.23035 4.25924Z"
                                />
                            </svg>
                        </div>
                    </div>
                    <div>
                        <svg
                            class="hint"
                            width="21"
                            height="21"
                            viewBox="0 0 21 21"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                        >
                            <path
                                d="M10.5 8.85C10.928 8.85 11.275 9.19698 11.275 9.625V14.875C11.275 15.303 10.928 15.65 10.5 15.65C10.072 15.65 9.725 15.303 9.725 14.875V9.625C9.725 9.19698 10.072 8.85 10.5 8.85ZM11.275 6.125C11.275 6.55302 10.928 6.9 10.5 6.9C10.072 6.9 9.725 6.55302 9.725 6.125C9.725 5.69698 10.072 5.35 10.5 5.35C10.928 5.35 11.275 5.69698 11.275 6.125ZM19.15 10.5C19.15 15.2773 15.2773 19.15 10.5 19.15C5.72274 19.15 1.85 15.2773 1.85 10.5C1.85 5.72274 5.72274 1.85 10.5 1.85C15.2773 1.85 19.15 5.72274 19.15 10.5ZM10.5 17.6C14.4212 17.6 17.6 14.4212 17.6 10.5C17.6 6.57878 14.4212 3.4 10.5 3.4C6.57878 3.4 3.4 6.57878 3.4 10.5C3.4 14.4212 6.57878 17.6 10.5 17.6Z"
                                fill="#5F5F5F"
                                stroke="white"
                                stroke-width="0.2"
                            />
                        </svg>
                        <div
                            class="absolute hidden flex-auto mt-4 translate-x-[calc(-50%+10.5px)]"
                        >
                            <div
                                class="relative w-5 h-5 rotate-[-45deg] left-1/2 translate-x-[-50%] translate-y-[50%] bg-white shadow-[4px_4px_4px_0_rgba(0,0,0,0.25)] z-0"
                            ></div>
                            <div
                                class="relative w-[28.25rem] h-[12.6rem] bg-white py-5 px-7 text-[0.625rem] rounded-lg shadow-[4px_4px_4px_0_rgba(0,0,0,0.25)] z-1 text-[--c-black]"
                            >
                                <p class="font-semibold">
                                    <span class="text-[#BE8208]"
                                        >正向影响力（w_pos）：</span
                                    >增加该素材在生成过程中对于其所处区域的影响程度
                                </p>
                                <p>
                                    范围：(0,1)
                                    ，默认0.3，建议不进行调整。若想获得更多输出，可尝试微调。
                                </p>
                                <br />
                                <p class="font-semibold">
                                    <span class="text-[#BE8208]"
                                        >负向影响力（w_neg）：</span
                                    >降低该素材在生成过程中对于其所处区域以外的区域的影响程度
                                </p>
                                <p>
                                    范围：(0,3)
                                    ，默认1.0，建议不进行调整，若想获得更多输出，可尝试微调。
                                </p>
                                <br />
                                <p class="font-semibold">
                                    <span class="text-[#BE8208]"
                                        >变化因子（t_i）：</span
                                    >表明该素材的保真度与和谐度
                                </p>
                                <p>
                                    t_i值越小，保真度越高；t_i值越大，和谐度越高。当t_i=0时，该素材不会发生变化（适用于文字、具体产品等），而当t_i=1时，该素材几乎不会保持原有的形态。和谐度可以理解为素材在生成过程中发生变化的程度。范围：[0,1]，默认0.3。
                                </p>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- 画布 -->
                <div class="relative w-full grow z-0 overflow-auto">
                    <div
                        ref="canvas_outerbox"
                        class="flex flex-col min-w-full min-h-full items-center shrink-0 justify-center p-8"
                    >
                        <div
                            ref="canvas"
                            @drop="handleDrop"
                            @dragover="handleDragover"
                            :style="{
                                width: `${projectInfo.width}px`,
                                height: `${projectInfo.height}px`,
                                transform: `scale(${canvas_scale})`,
                            }"
                            class="relative bg-white canvas overflow-hidden shrink-0"
                        >
                            <!-- 拖素材的时候会变形，待修 -->
                            <!-- key为index会出bug，待修，有空查查 -->
                            <div
                                v-for="(item, index) in itemList"
                                :key="item"
                                :style="{
                                    position: `absolute`,
                                    zIndex: `${index}`,
                                    transform: `translate(${item.left}px, ${item.top}px)`,
                                }"
                                @mousedown="(e) => handleMouseDown(e, item)"
                            >
                                <Drager
                                    v-bind="item"
                                    color="#FFB899"
                                    :style="{ position: `static` }"
                                    @blur="(e) => handleBlur(e, index)"
                                    @resize-end="
                                        (e) => handleResizeEnd(e, item)
                                    "
                                    @rotate-end="
                                        (e) => handleRotateEnd(e, item)
                                    "
                                    @click="() => handleClick(index)"
                                >
                                    <img
                                        :ref="
                                            (el) => {
                                                item.ref = el;
                                            }
                                        "
                                        :src="encodeURI(baseURL + item.img_url)"
                                        :key="item"
                                        @load="handleLoaded"
                                        draggable="false"
                                        alt="加载失败"
                                        class="w-full h-full object-contain"
                                    />
                                </Drager>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- 右边图层 -->
            <div
                class="relative flex flex-col w-[12vw] px-2 py-[2px] divide-y z-[100]"
            >
                <div class="w-full py-2.5 px-3.5 font-medium text-base">
                    图层
                </div>
                <!-- 把vh改成rem比较好？待修 -->
                <draggable :list="itemList" chosen-class="bg-gray-100">
                    <template #item="{ element }">
                        <div class="h-[4vh] m-2.5 rounded-md">
                            <drag-item
                                :img_name="element.name"
                                :img="{
                                    img_url: element.img_url,
                                    id: element.img_id,
                                }"
                            ></drag-item>
                        </div>
                    </template>
                </draggable>
            </div>
        </div>
    </main>
</template>

<style scoped>
.icon {
    fill: #313131;
}
.icon:hover {
    fill: #eeaa1e;
}

.arrow {
    fill: #8b8b8b;
}

.arrow:hover {
    fill: #eeaa1e;
}

.paramsInput {
    flex: 0 0 auto;
    border-bottom: 1px solid #d9d9d9;
}

:deep(.p-inputwrapper),
:deep(input.p-inputtext) {
    border: none;
    box-shadow: none;
    text-align: center;
    outline: none;
}

:deep(input.p-inputnumber-input) {
    border: none;
    width: 3rem;
    font-size: 0.75rem;
    color: #5f5f5f;
    border-radius: 0;
    border-bottom: 1px solid #5f5f5f;
}

:deep(.p-button) {
    box-shadow: none;
}

.selectedBtn {
    background-color: #ffedba;
    fill: #be8208;
    stroke: #ffedba;
    color: #be8208;
}

.hint:hover ~ .absolute {
    display: block;
}

.upload:hover {
    background-color: #ffedba;
    border: 1px solid #ffedba;
    color: #be8208;
    fill: #be8208;
    stroke: #ffedba;
}

.canvas {
    transition: all 0.02s linear;
}

:deep(.es-drager-dot) {
    position: absolute;
}
</style>
