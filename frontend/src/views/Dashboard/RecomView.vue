<script setup>
import RecomBanner from "@/components/HomeView/RecomBanner.vue";
import CataCard from "@/components/HomeView/CataCard.vue";

const categories = [
    {
        title: "运动类商品",
        desc: "",
        img: "/categories/icon_sport.png"
    },
    {
        title: "美妆类商品",
        desc: "",
        img: "/categories/icon_deco.png"
    },
    {
        title: "节日类商品",
        desc: "",
        img: "/categories/icon_fes.png"
    },
    {
        title: "服装类商品",
        desc: "",
        img: "/categories/icon_cust.png"
    },
    {
        title: "电器类商品",
        desc: "",
        img: "/categories/icon_appl.png"
    },
    {
        title: "钟表类商品",
        desc: "",
        img: "/categories/icon_clock.png"
    },
    {
        title: "文具类商品",
        desc: "",
        img: "/categories/icon_util.png"
    },
    {
        title: "3C数码商品",
        desc: "",
        img: "/categories/icon_elec.png"
    },
];
</script>

<template>

    <div class="flex flex-col items-center justify-center">
        <RecomBanner/>

        <div class="flex flex-row w-full my-8 items-center">
            <h2 class="flex text-xl font-semibold have-bar">选择心仪的设计对象吧</h2>
        </div>

        <div class="cardContainer">
            <CataCard v-for="item in categories"
                      :title="item.title"
                      :desc="'适用于' + item.title + '的海报设计'"
                      :img="item.img"
            />
        </div>
    </div>
</template>

<style scoped>
.cardContainer {
    --card-margin: 20px;

    width: min(100%, 1400px);
    justify-content: center;
    align-items: center;

    display: grid;
    grid-template-columns: repeat(auto-fill, calc(350px + var(--card-margin)));
    grid-auto-rows: minmax(100px, auto);
}
</style>
