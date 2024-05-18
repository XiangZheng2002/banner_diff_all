import {defineStore} from "pinia";
import {ref} from "vue";

const useNewProjStore = defineStore("newProj", () => {
    const _isDialogOpen = ref(false);
    const _selectedCate = ref(null);

    function openDialog() {
        _isDialogOpen.value = true;
    }

    function closeDialog() {
        _isDialogOpen.value = false;
    }

    function setCate(i) {
        _selectedCate.value = i;
    }

    return {
        _isDialogOpen,
        _selectedCate,

        openDialog,
        closeDialog,
        setCate
    };
});

export default useNewProjStore;