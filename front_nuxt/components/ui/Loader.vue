<template>
	<div class="loader-container">
		<div class="loader">
			<div class="dot"></div>
			<div class="dot"></div>
			<div class="dot"></div>
		</div>
	</div>
</template>

<script setup></script>

<style scope>
@keyframes spin {
	to {
		transform: rotate(360deg);
	}
}

/* Dots Spinner */
.dots-container {
	display: flex;
	gap: 0.5rem;
	align-items: center;
}

.dot {
	width: 0.75rem;
	height: 0.75rem;
	border-radius: 50%;
	animation: bounce 1.4s infinite ease-in-out both;
}

.dot:nth-child(1) {
	animation-delay: -0.32s;
}
.dot:nth-child(2) {
	animation-delay: -0.16s;
}

@keyframes bounce {
	0%,
	80%,
	100% {
		transform: scale(0.5);
		opacity: 0.5;
	}
	40% {
		transform: scale(1);
		opacity: 1;
	}
}
</style>
