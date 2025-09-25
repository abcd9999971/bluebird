export const useLoading = () => {
	const isLoading = useState<boolean>('isLoading', () => true)
	return {
		isLoading
	}
}
