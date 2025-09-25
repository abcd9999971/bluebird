<template>
	<div class="loader fixed inset-0 z-50 flex items-center justify-center bg-white bg-opacity-75">
		<div class="loader-content">
			<!-- Spinner -->
			<img src="../../public/logos/emblem.png" alt="Loading..." class="loader-logo h-20 w-20" />
			<div class="dots-container mx-auto w-fit mt-2">
				<div class="dot bg-blue-500 dark:bg-blue-400"></div>
				<div class="dot bg-blue-500 dark:bg-blue-400"></div>
				<div class="dot bg-blue-500 dark:bg-blue-400"></div>
			</div>
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
