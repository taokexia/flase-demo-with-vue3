<script setup lang="ts">
import { ref } from 'vue';

const isShow = ref(false)
const msg = ref('默认提示内容')
const type = ref('info')

const show = (message: string, showType = 'info', time = 2000) => {
    msg.value = message
    type.value = showType
    isShow.value = true
    setTimeout(() => {
        isShow.value = false
    }, time);
    18
}

const hide = () => {
    isShow.value = false
}

defineExpose({
    show,
    hide
})
</script>

<template>
    <Transition>
        <div v-if="isShow" class="toast toast-top toast-center">
            <div class="alert" :class="{
                'alert-info': type === 'info',
                'alert-error': type === 'error',
                'alert-success': type === 'success'
            }">
                <span>{{ msg }}</span>
            </div>
        </div>
    </Transition>
</template>