import {ref, computed} from "vue";
import {defineStore} from "pinia";

const visible = defineStore("asset-upload-visible", () => {
    const visible = ref(false);

    function open() {
        visible.value = true;
    }

    function close() {
        visible.value = false;
    }

    function set(val) {
        visible.value = val;
    }

    return {visible, open, close, set};
});

export default visible;