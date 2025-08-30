<template>
<ul id='timeline'>
    <li v-for="i in index" :key="i" class="post">
    <div class="dot"></div>
    <div class="content">test{{ i }}</div>
</li>
</ul>
</template>

<script setup>
const index = Array.from({ length: 20 }, (_, i) => i + 1)
</script>


<style scoped>

#timeline{
    list-style: none;
    padding: 0;
    margin: 0;
    position: relative;
}

#timeline::before{
    content: '';
    position: absolute;
    width: 2px;
    background-color: #ccc;
    top: 8px;
    left: 50%;
    height: 100%;
    transform: translateX(-50%);
    z-index: 0;
}

#timeline .post{
    position: relative;
    min-height: 60px;
}
#timeline .dot{
    position: absolute;
    top: 0;
    left: 50%;
    width: 12px;
    height: 12px;
    background-color: #000000;
    border-radius: 50%;
    transform: translateX(-50%);
    z-index: 2; /* make sure dot is above the timeline */
}


</style>