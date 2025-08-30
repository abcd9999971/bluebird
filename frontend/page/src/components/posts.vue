<template>
    <ul>
        <li v-for="post in posts" :key="post.created_at ">
            <div class="post">
                <p class="time">{{post.created_at}}</p>
                <p class="detail">{{post.text}}</p>
            </div>
        </li>
    </ul>
</template>

<script setup>
    import posts from '../post.json'
</script>

