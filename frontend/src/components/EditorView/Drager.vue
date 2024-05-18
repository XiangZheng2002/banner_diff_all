<script setup>
import Drager from 'es-drager'
import { ref, onMounted, getCurrentInstance, computed }  from 'vue'

const instance = getCurrentInstance()

const dragerRef = ref()

const dragStyle = computed(() => {
  const { width, height, left, top } = dragData.value
  return {
    width: 0,
    height: 0,
    left: 0,
    top: 0,
    '--es-drager-color': props.color
  }
})

onMounted(() => {
  const entries = Object.entries(dragerRef.value.$.exposed)
  for (const [key, value] of entries) {
    instance.exposed[key] = value
  }
})
</script>

<template>
    <Drager ref="dragerRef" v-bind="$attrs">
      <template v-for="(_value, name) in $slots" #[name]="slotData">
        <slot :name="name" v-bind="slotData || {}" />
      </template>
    </Drager>
</template>