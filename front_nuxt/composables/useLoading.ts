import { ref } from 'vue'

// 全域 loading 與任務計數 (composable 為 singleton)
const loading = ref(true)
const total = ref(0)
const completed = ref(0)

export function useLoading() {
  const register = (n = 1) => {
    total.value += n
    // if tasks are registered, ensure loader is shown
    if (total.value > 0 && completed.value < total.value) loading.value = true
  }

  const start = () => {
    loading.value = true
  }

  const doneTask = (n = 1) => {
    completed.value += n
    if (total.value > 0 && completed.value >= total.value) {
      loading.value = false
    }
  }

  const reset = () => {
    total.value = 0
    completed.value = 0
    loading.value = false
  }

  return {
    // state
    loading,
    total,
    completed,
    // actions
    register,
    start,
    doneTask,
    reset
  }
}
export const useLoading = () => {
	const isLoading = useState<boolean>('isLoading', () => true)
	return {
		isLoading
	}
}
