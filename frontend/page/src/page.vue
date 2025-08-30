<template>
    <div class="title-bar">
        <h1>POST</h1>
    </div>
    <AddPostBar/>
    <TimelineBar/>
</template>

<script setup>

import posts from './components/posts.vue'
import TimelineBar from './components/TimelineBar.vue'
import AddPostBar from './components/AddPost.vue'

</script>

<style>
body {
    background-color: #ffffff;
    margin: 0;
}
.title-bar {
    width: 100vw;
    background-color: rgb(78, 92, 121);
    padding: 20px 0;
    box-sizing: border-box;
    text-align: center;
    margin-bottom: 20px;
    margin-top: 0;
    opacity: 0;
    animation: fadeIn 2s ease forwards;
}
h1 {
    color: #ffffff;
    margin: 0;
    font-size:60px;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

</style>
