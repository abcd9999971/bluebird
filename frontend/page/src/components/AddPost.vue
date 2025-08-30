<template>
    <div class="add-post-bar">
        <input v-model="text" placeholder="What's new?" />
        <button @click="handleAdd">Post</button>
    </div>
</template>

<script setup>

import { ref } from 'vue'

const text = ref('')
const emit = defineEmits(['add'])


function handleAdd() {
    if (text.value.trim() !== '') {
        emit('add', text.value)
        text.value = ''
    }
    else {
        alert('Post cannot be empty!')
}
}

</script>

<style scoped>

</style >
