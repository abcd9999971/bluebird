<template>
	<div>
		<!-- loader 只有在 loading 為 true 時顯示 -->
		<UiBaseLoader v-if="loading" />

		<!-- 其餘內容（Nuxt page / layout） -->
		<NuxtPage />
	</div>
</template>

<script setup>
// useLoading 是放在 composables，Nuxt 會自動匯入
const { loading } = useLoading()
</script>